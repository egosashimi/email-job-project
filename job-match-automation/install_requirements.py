import sys
import subprocess

def install_requirements():
    """Install required packages."""
    requirements = [
        "python-dotenv",
        "cryptography",
        "imaplib2",
        "pytest",
        "pytest-asyncio",
        "coverage"
    ]
    
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}")

if __name__ == "__main__":
    install_requirements()