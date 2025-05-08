"""
Core functionality for detecting drift in Terraform-managed infrastructure.
"""

import json
import os
import subprocess
import sys
from typing import Dict, List, Optional, Tuple, Any
import concurrent.futures
import re
from colorama import Fore, Style, init

# Initialize colorama for cross-platform color support
init(autoreset=True)

class TerraformDriftDetector:
    def __init__(self, terraform_dir: str, show_details: bool = False, max_workers: int = 5):
        self.terraform_dir = terraform_dir
        self.show_details = show_details
        self.max_workers = max_workers
    
    def run_terraform_command(self, command: List[str], cwd: str = None) -> Tuple[int, str, str]:
        """Run a terraform command and return exit code, stdout and stderr"""
        working_dir = cwd or self.terraform_dir
        
        try:
            result = subprocess.run(
                command,
                cwd=working_dir,
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return 1, "", str(e)
    
    def check_terraform_installed(self) -> bool:
        """Check if terraform is installed and accessible"""
        try:
            subprocess.run(["terraform", "--version"], 
                           capture_output=True, 
                           check=True)
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def check_terraform_initialized(self, dir_path: str) -> bool:
        """Check if terraform is initialized in the given directory"""
        return os.path.isdir(os.path.join(dir_path, ".terraform"))
    
    def initialize_terraform(self, dir_path: str) -> bool:
        """Initialize terraform in the given directory"""
        print(f"{Fore.YELLOW}Initializing Terraform in {dir_path}...")
        code, stdout, stderr = self.run_terraform_command(["terraform", "init"], cwd=dir_path)
        if code != 0:
            print(f"{Fore.RED}Failed to initialize Terraform: {stderr}")
            return False
        return True
    
    def get_terraform_directories(self) -> List[str]:
        """Find all directories containing .tf files"""
        tf_dirs = []
        
        # First check if the main directory contains .tf files
        if any(f.endswith('.tf') for f in os.listdir(self.terraform_dir)):
            tf_dirs.append(self.terraform_dir)
        
        # Then look for modules or subdirectories with .tf files
        for root, dirs, files in os.walk(self.terraform_dir):
            if root != self.terraform_dir and any(f.endswith('.tf') for f in files):
                tf_dirs.append(root)
        
        return tf_dirs
    
    def check_drift_in_directory(self, dir_path: str) -> Dict:
        """Check drift in a specific directory using terraform plan"""
        if not self.check_terraform_initialized(dir_path):
            if not self.initialize_terraform(dir_path):
                return {
                    "directory": dir_path,
                    "error": "Failed to initialize Terraform",
                    "has_drift": False,
                    "details": None
                }
        
        # Run terraform plan with JSON output
        code, stdout, stderr = self.run_terraform_command(
            ["terraform", "plan", "-detailed-exitcode", "-out=tfplan", "-input=false"],
            cwd=dir_path
        )
        
        # Terraform plan detailed exit codes:
        # 0 = No changes
        # 1 = Error
        # 2 = Changes present (drift detected)
        
        if code == 1:
            return {
                "directory": dir_path,
                "error": stderr,
                "has_drift": False,
                "details": None
            }
        
        has_drift = (code == 2)
        
        details = None
        if has_drift and self.show_details:
            # Get the plan details in JSON format if drift is detected and details are requested
            show_code, show_stdout, show_stderr = self.run_terraform_command(
                ["terraform", "show", "-json", "tfplan"],
                cwd=dir_path
            )
            
            if show_code == 0:
                try:
                    plan_json = json.loads(show_stdout)
                    details = self.parse_plan_details(plan_json)
                except json.JSONDecodeError:
                    details = {"error": "Failed to parse terraform show output"}
            else:
                details = {"error": show_stderr}
        
        # Clean up the plan file
        if os.path.exists(os.path.join(dir_path, "tfplan")):
            os.remove(os.path.join(dir_path, "tfplan"))
        
        return {
            "directory": dir_path,
            "error": None,
            "has_drift": has_drift,
            "details": details
        }
    
    def parse_plan_details(self, plan_json: Dict) -> Dict:
        """Parse terraform plan JSON to extract drift details"""
        details = {
            "resources_to_add": [],
            "resources_to_change": [],
            "resources_to_destroy": []
        }
        
        if "resource_changes" not in plan_json:
            return details
        
        for resource in plan_json["resource_changes"]:
            actions = resource.get("change", {}).get("actions", [])
            address = resource.get("address", "unknown")
            
            if "create" in actions:
                details["resources_to_add"].append(address)
            elif "update" in actions:
                details["resources_to_change"].append(address)
            elif "delete" in actions:
                details["resources_to_destroy"].append(address)
        
        return details
    
    def run(self) -> Dict:
        """Run drift detection on all terraform directories"""
        if not self.check_terraform_installed():
            print(f"{Fore.RED}Error: Terraform is not installed or not in PATH")
            sys.exit(1)
        
        tf_dirs = self.get_terraform_directories()
        if not tf_dirs:
            print(f"{Fore.YELLOW}No Terraform files found in {self.terraform_dir}")
            sys.exit(0)
        
        results = []
        drift_found = False
        
        print(f"{Fore.BLUE}Scanning {len(tf_dirs)} directories for Terraform drift...")
        
        # Use ThreadPoolExecutor for parallel processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_dir = {executor.submit(self.check_drift_in_directory, dir_path): dir_path for dir_path in tf_dirs}
            
            for future in concurrent.futures.as_completed(future_to_dir):
                dir_path = future_to_dir[future]
                try:
                    result = future.result()
                    if result["has_drift"]:
                        drift_found = True
                    results.append(result)
                    self._print_result(result)
                except Exception as exc:
                    print(f"{Fore.RED}Error checking {dir_path}: {exc}")
                    results.append({
                        "directory": dir_path,
                        "error": str(exc),
                        "has_drift": False,
                        "details": None
                    })
        
        return {
            "drift_found": drift_found,
            "results": results
        }
    
    def _print_result(self, result: Dict) -> None:
        """Print a nicely formatted result"""
        dir_path = result["directory"]
        rel_path = os.path.relpath(dir_path, self.terraform_dir)
        
        if result["error"]:
            print(f"{Fore.RED}[ERROR] {rel_path}: {result['error']}")
            return
        
        if result["has_drift"]:
            print(f"{Fore.RED}[DRIFT] {rel_path}")
            
            if self.show_details and result["details"]:
                details = result["details"]
                if details["resources_to_add"]:
                    print(f"  {Fore.GREEN}Resources to add ({len(details['resources_to_add'])}):")
                    for res in details["resources_to_add"]:
                        print(f"    + {res}")
                
                if details["resources_to_change"]:
                    print(f"  {Fore.YELLOW}Resources to change ({len(details['resources_to_change'])}):")
                    for res in details["resources_to_change"]:
                        print(f"    ~ {res}")
                
                if details["resources_to_destroy"]:
                    print(f"  {Fore.RED}Resources to destroy ({len(details['resources_to_destroy'])}):")
                    for res in details["resources_to_destroy"]:
                        print(f"    - {res}")
        else:
            print(f"{Fore.GREEN}[OK] {rel_path}")