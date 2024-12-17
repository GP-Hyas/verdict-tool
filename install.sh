#!/bin/bash

# Color variables
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
CYAN="\033[0;36m"
WHITE="\033[0;37m"
RESET="\033[0m"

# Set virtual environment directory name
set_venv_dir() {
    # Default to "venv" if not set externally
    VENV_DIR="${VENV_DIR:-verdict-toolENV}"
}

# Function to display the HYAS logo
display_welcome() {
    echo -e "${RED}"
    cat << "EOF"

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


EOF
echo -e "${RESET}"
}

# Function to determine the correct Python command
get_python_command() {
    case "$OSTYPE" in
        msys*|cygwin*)
            if command -v python &>/dev/null; then
                PYTHON_CMD="python"
            else
                echo -e "${RED}Error: Python is not installed or not in PATH.${RESET}"
                exit 1
            fi
            ;;
        linux*|darwin*)
            if command -v python3 &>/dev/null; then
                PYTHON_CMD="python3"
            elif command -v python &>/dev/null; then
                PYTHON_CMD="python"
            else
                echo -e "${RED}Error: Python is not installed or not in PATH.${RESET}"
                exit 1
            fi
            ;;
            *)
                echo -e "${RED}Unsupported OS: $OSTYPE.${RESET}"
                exit 1
                ;;
    esac

    # Check Python version (must be 3.8 or newer)
    PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    REQUIRED_VERSION=3.11

    if [[ $(echo -e "$PYTHON_VERSION\n$REQUIRED_VERSION" | sort -V | head -n1) != "$REQUIRED_VERSION" ]]; then
        echo -e "${RED}Error: Python 3.11 or newer is required. Found Python $PYTHON_VERSION.${RESET}"
        exit 1
    fi

    export PYTHON_CMD
    export PYTHON_VERSION

    echo -e "${CYAN}Using Python version: $PYTHON_VERSION${RESET}"
}

# Function to validate UUIDv4
is_valid_uuid() {
    local uuid="$1"
    [[ $uuid =~ ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$ ]]
}

# Function to read user input and create the .env file
create_env_file() {
    echo -e "${YELLOW}\nLet's set up your API credentials.${RESET}"
    while true; do
        read -rp "Enter your API Key: " APIKEY
        if [[ "$APIKEY" == "q" || "$APIKEY" == "quit" ]]; then
            echo -e "${CYAN}Exiting setup. Goodbye!${RESET}"
            exit 0
        fi
        if is_valid_uuid "$APIKEY"; then
            break
        else
            echo -e "${RED}Invalid API key. Please enter a valid key or 'quit' to exit.${RESET}"
        fi
    done

    while true; do
        read -rp "Enter your Client ID: " CLIENTID
        if [[ "$CLIENTID" == "q" || "$CLIENTID" == "quit" ]]; then
            echo -e "${CYAN}Exiting setup. Goodbye!${RESET}"
            exit 0
        fi
        if is_valid_uuid "$CLIENTID"; then
            break
        else
            echo -e "${RED}Invalid Client ID. Please enter a valid ID or 'quit' to exit.${RESET}"
        fi
    done

    echo "Creating .env file with your credentials..."
    cat > .env << EOF
APIKEY=$APIKEY
CLIENTID=$CLIENTID
EOF
    echo -e "${GREEN}.env file created successfully!${RESET}"
}

# Function to create and activate a virtual environment
setup_virtual_environment() {
    set_venv_dir

    echo -e "${YELLOW}\nSetting up the Python virtual environment...${RESET}"
    echo -e "${CYAN}Using Python version: $PYTHON_VERSION${RESET}"

    if ! $PYTHON_CMD -c "import venv" &>/dev/null; then
        echo -e "${RED}Error: The 'venv' module is not available in Python. Ensure Python 3.8+ is installed properly.${RESET}"
        exit 1
    fi

    $PYTHON_CMD -m venv "${VENV_DIR}"
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to create virtual environment.${RESET}"
        exit 1
    fi

    # Activate virtual environment (different for Windows Git Bash)
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        source "${VENV_DIR}/Scripts/activate"
    else
        source "${VENV_DIR}/bin/activate"
    fi

    echo -e "${GREEN}Virtual environment '${VENV_DIR}' created and activated!${RESET}"
}

# Function to install dependencies
install_dependencies() {
    echo -e "${YELLOW}\nInstalling dependencies from requirements.txt...${RESET}"
    if [ ! -f "requirements.txt" ]; then
        echo -e "${RED}Error: requirements.txt file not found. Exiting...${RESET}"
        deactivate
        exit 1
    fi

    if [ ! -s "requirements.txt" ]; then
        echo -e "${RED}Error: requirements.txt is empty. Exiting...${RESET}"
        deactivate
        exit 1
    fi

    if ! command -v pip &>/dev/null; then
        echo -e "${YELLOW}pip not found. Attempting to install pip...${RESET}"
        $PYTHON_CMD -m ensurepip --upgrade
        if [ $? -ne 0 ]; then
            echo -e "${RED}Error: Failed to install pip in the virtual environment.${RESET}"
            deactivate
            exit 1
        fi
    fi

    pip install --upgrade pip
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to install dependencies.${RESET}"
        deactivate
        exit 1
    fi

    echo -e "${GREEN}Dependencies installed successfully!${RESET}"
    deactivate
    echo -e "${CYAN}Virtual environment '${VENV_DIR}' has been deactivated.${RESET}"
}

# Main function
main() {
    clear
    # Display welcome message with ASCII art
    display_welcome

    echo -e "${WHITE}Starting the installation process...${RESET}"
    # Get Python command and version
    get_python_command
    
    # Gather user credentials and create a .env file
    create_env_file

    # Set up and activate the virtual environment
    setup_virtual_environment

    # Install required dependencies from requirements.txt
    install_dependencies

    echo -e "${GREEN}\nInstallation complete! 🎉${RESET}"
    echo -e "${WHITE}To activate the virtual environment, run:${RESET}"
    echo "  source ${VENV_DIR}/bin/activate # For Linux/macOS"
    echo "  .\\${VENV_DIR}\\Scripts\\activate # For Windows"
    echo -e "${WHITE}To run the tool:${RESET}"
    echo "  python verdict-tool.py"
    echo -e "${WHITE}To deactivate the environment:${RESET}"
    echo "  deactivate"
}

# Run the main function
main
