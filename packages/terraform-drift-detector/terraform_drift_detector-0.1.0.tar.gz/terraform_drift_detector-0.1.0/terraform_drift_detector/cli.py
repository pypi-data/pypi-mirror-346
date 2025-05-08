"""
Command-line interface for the Terraform Drift Detector.
"""

import argparse
import json
import os
import sys
from colorama import Fore, init

from terraform_drift_detector.detector import TerraformDriftDetector

def main():
    parser = argparse.ArgumentParser(description="Detect drift in Terraform-managed infrastructure")
    parser.add_argument(
        "-d", "--directory", 
        default=".", 
        help="Directory containing Terraform files (default: current directory)"
    )
    parser.add_argument(
        "--details", 
        action="store_true", 
        help="Show detailed information about detected drift"
    )
    parser.add_argument(
        "-w", "--workers", 
        type=int, 
        default=5, 
        help="Maximum number of parallel workers (default: 5)"
    )
    parser.add_argument(
        "-o", "--output", 
        help="Save results to a JSON file"
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show the version and exit"
    )
    
    args = parser.parse_args()
    
    # Initialize colorama
    init(autoreset=True)
    
    # Handle version display
    if args.version:
        from terraform_drift_detector import __version__
        print(f"Terraform Drift Detector v{__version__}")
        sys.exit(0)
    
    detector = TerraformDriftDetector(
        terraform_dir=args.directory,
        show_details=args.details,
        max_workers=args.workers
    )
    
    print(f"{Fore.BLUE}Terraform Drift Detector")
    print(f"{Fore.BLUE}{'=' * 25}")
    print(f"Scanning directory: {os.path.abspath(args.directory)}\n")
    
    results = detector.run()
    
    # Summary
    total_dirs = len(results["results"])
    dirs_with_drift = sum(1 for r in results["results"] if r["has_drift"])
    dirs_with_errors = sum(1 for r in results["results"] if r["error"])
    
    print(f"\n{Fore.BLUE}{'=' * 25}")
    print(f"{Fore.BLUE}Scan Summary:")
    print(f"Total directories scanned: {total_dirs}")
    
    if dirs_with_drift > 0:
        print(f"{Fore.RED}Directories with drift: {dirs_with_drift}")
    else:
        print(f"{Fore.GREEN}Directories with drift: {dirs_with_drift}")
    
    if dirs_with_errors > 0:
        print(f"{Fore.RED}Directories with errors: {dirs_with_errors}")
    
    if results["drift_found"]:
        print(f"\n{Fore.RED}DRIFT DETECTED in your infrastructure!")
        exit_code = 2
    else:
        print(f"\n{Fore.GREEN}No drift detected. Your infrastructure matches your Terraform files.")
        exit_code = 0
        
    # Save results to file if requested
    if args.output:
        try:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nResults saved to {args.output}")
        except Exception as e:
            print(f"{Fore.RED}Error saving results: {e}")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()