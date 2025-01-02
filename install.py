import sys
import uuid
import shutil
import platform
import subprocess
from pathlib import Path
from typing import Optional

# Color constants for terminal
RED: str = "\033[0;31m"
GREEN: str = "\033[0;32m"
YELLOW: str = "\033[0;33m"
CYAN: str = "\033[0;36m"
WHITE: str = "\033[0;37m"
RESET: str = "\033[0m"

# Default virtual environment directory
VENV_DIR: Path = Path.home() / ".venv"

def display_welcome() -> None:
    """Display the welcome message with ASCII art."""
    print(f"{RED}")
    print(
        """
                                                           .=-                 
                *****************.                       .=*#-                 
                ***-:::::::::-***.                     .=****-                 
                **+           +**.                   .=*#++**-                 
                ***           +**.                 .=*#+: -**-                 
                ***           +**.               :=*#+:   =**-                 
                ***           +**              :+*#+:     =**-                 
                ***           +**:......     :+*#+:       =**-                 
                ***           ********+:   :+#*+:         =**-                 
                ***           ::::::::   :+#*+:           =**-                 
                ***                    :+#*=:             =**-                 
                ***                  :+#*=.               =**-                 
                ***                :+#*=.                 =**-                 
                ***              -+#*=.                   =**-                 
                ***            -+#*=.   .......           =**-                 
                ***          -+#*=.  .=********.          =**-                 
                ***        -*#*=.    .::::::+**.          =**-                 
                ***      -*#*=.             +**.          =**-                 
                ***    -*#*=.               +**.          =**-                 
                **+  -*#*-.                 +**.          =**-                 
                ***=*#*-.                   +**.          -**-                 
                ***#*-                      +**-::::::::::=**-                 
                ***-                        +***************#-                 
               .*-                          .................                  
                                                                               
                                                                               
                                                                              
  ..         ...       ..         ...         ....             ..:::::::..     
  *#-        =#+       -**-      -#+:        =#+**:           +*++++++++*#+    
  +*:        -*+         =#+.  .+#-         -#= .**:         :**.        ::    
  **+========+*+          :**:-#+.         -#+   :**.        .*#+========:.    
  **=--------+*+            =**-          -#+   . -**.         .:--------*#:   
  **:        -#+            :**          -#+  :+++++**.      .=-         *#-   
  **:        -#+            :**.        -*+.        -**.     .+*+++++++++*+.   
  ..          ..             ..         ..           ..         .........  


                Welcome to the HYAS Verdict Tool Installer!
        """
    )
    print(RESET)

def get_python_command() -> str:
    """Determine the correct Python command."""
    python_cmd: Optional[str] = None
    os_type: str = platform.system().lower()

    if "windows" in os_type:
        python_cmd = "python" if shutil.which("python") else None
    else:
        python_cmd = "python3" if shutil.which("python3") else "python"

    if not python_cmd or not shutil.which(python_cmd):
        print(f"{RED}Error: Python is not installed or not in PATH.{RESET}")
        sys.exit(1)

    # Check Python version
    try:
        result = subprocess.run(
            [python_cmd, "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"],
            capture_output=True,
            text=True,
            check=True,
        )
        python_version: str = result.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"{RED}Error: Unable to determine Python version.{RESET}")
        sys.exit(1)

    if float(python_version) < 3.11:
        print(f"{RED}Error: Python 3.11 or newer is required. Found Python {python_version}.{RESET}")
        sys.exit(1)
    
    print(f"{CYAN}Using Python version: {python_version}{RESET}")
    return python_cmd

def is_valid_uuid(value: str) -> bool:
    """Validate if the input string is a UUID."""
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False

def create_env_file() -> None:
    """Prompt user for API credentials and create .env file."""
    print(f"{YELLOW}\nLet's set up your API credentials.{RESET}")

    while True:
        api_key: str = input("Enter your API key: ").strip()
        if api_key.lower() in {"q", "quit"}:
            print(f"{CYAN}Exiting setup. Goodbye!{RESET}")
            sys.exit(0)
        if is_valid_uuid(api_key):
            break
        else:
            print(f"{RED}Invalid API key. Please enter a valid key or 'quit' to exit.{RESET}")

    while True:
        client_id: str = input("Enter your Client ID: ").strip()
        if client_id.lower() in ("q", "quit"):
            print(f"{CYAN}Exiting setup. Goodbye!{RESET}")
            sys.exit(0)
        if is_valid_uuid(client_id):
            break
        else:
            print(f"{RED}Invalid Client ID. Please enter a valid ID or 'quit' to exit.{RESET}")

    env_file: Path = Path(".env")
    env_file.write_text(f"APIKEY={api_key}\nCLIENT_ID={client_id}\n")
    print(f"{GREEN}.env file created successfully!{RESET}")

def setup_virtual_environment(python_cmd: str) -> None:
    """Set up and activate a virtual environment."""
    print(f"{YELLOW}\nSetting up the Python virtual environment...{RESET}")

    if not shutil.which(python_cmd):
        print(f"{RED}Error: Python executable not found.{RESET}")
        sys.exit(1)

    subprocess.run([python_cmd, "-m", "venv", str(VENV_DIR)], check=True)

    # Activate the virtual environment
    activate_script: Path = (
        VENV_DIR / "Scripts" / "activate.bat"
        if platform.system().lower() == "windows"
        else VENV_DIR / "bin" / "activate"
    )

    if not activate_script.exists():
        print(f"{RED}Error: Unable to find activation script for the virtual environment.{RESET}")
        sys.exit(1)

    print(f"{GREEN}Virtual environment '{VENV_DIR}' created successfully!{RESET}")
    print(f"{CYAN}To activate, run: source {activate_script}{RESET}")

def install_dependencies() -> None:
    """Install dependencies from requirements.txt."""
    req_file: Path = Path("requirements.txt")
    if not req_file.exists() or req_file.stat().st_size == 0:
        print(f"{RED}Error: requirements.txt file not found.{RESET}")
        sys.exit(1)

    subprocess.run(["pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run(["pip", "install", "-r", str(req_file)], check=True)
    print(f"{GREEN}Dependencies installed successfully!{RESET}")

def main() -> None:
    """Main function to coordinate the installation process."""
    display_welcome()
    python_cmd: str = get_python_command()
    create_env_file()
    setup_virtual_environment(python_cmd)
    install_dependencies()

if __name__ == "__main__":
    main()