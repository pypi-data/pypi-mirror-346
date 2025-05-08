from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="terraform-drift-detector",
    version="0.1.0",
    author="Rohan Rustagi",
    description="A CLI tool to detect drift in Terraform-managed infrastructure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/terraform-drift-detector",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.6",
    install_requires=[
        "colorama>=0.4.4",
    ],
    entry_points={
        "console_scripts": [
            "tfdd=terraform_drift_detector.cli:main",
        ],
    },
    license="MIT",
)
