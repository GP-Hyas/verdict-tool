#!/bin/bash

# Color variables
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
CYAN="\033[0;36m"
WHITE="\033[0;37m"
RESET="\033[0m"

# Function to display the HYAS logo as ASCII art
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
    # Detect the OS type
    case "$OSTYPE" in
        msys*|cygwin*)
            # For Windows (Git Bash or Cygwin)
            if command -v python &> /dev/null; then
                if python --version 2>&1 | grep -q "Python 3"; then
                    echo "python"
                else
                    echo -e "${RED}Error: Python 3 is required but not found.${RESET}"
                    exit 1
                fi
            else
                echo -e "${RED}Error: Python is not installed or not in PATH.${RESET}"
                exit 1
            fi
            ;;
        linux*|darwin*)
            # For Linux or macOS
            if command -v python3 &> /dev/null; then
                echo "python3"
            elif command -v python &> /dev/null; then
                if python --version 2>&1 | grep -q "Python 3"; then
                    echo "python"
                else
                    echo -e "${RED}Error: Python 3 is required but not found.${RESET}"
                    exit 1
                fi
            else
                echo -e "${RED}Error: Python is not installed or not in PATH.${RESET}"
                exit 1
            fi
            ;;
        *)
            echo -e "${RED}Unsupported OS: $OSTYPE${RESET}"
            exit 1
            ;;
    esac
}

# Function to read user input and create the .env file
create_env_file() {
    echo -e "${YELLOW}\nLet's set up your API credentials.${RESET}"
    read -rp "Enter your API Key: " APIKEY
    if [ -z "$APIKEY" ]; then
        echo -e "${RED}Error: API Key cannot be empty. Exiting...${RESET}"
        exit 1
    fi

    read -rp "Enter your Client ID: " CLIENTID
    if [ -z "$CLIENTID" ]; then
        echo -e "${RED}Error: Client ID cannot be empty. Exiting...${RESET}"
        exit 1
    fi

    echo "Creating .env file with your credentials..."
    cat > .env << EOF
APIKEY=$APIKEY
CLIENTID=$CLIENTID
EOF
    echo -e "${GREEN}.env file created successfully!${RESET}"
}

# Function to create and activate a virtual environment
setup_virtual_environment() {
    echo -e "${YELLOW}\nSetting up the Python virtual environment...${RESET}"

    PYTHON_CMD=$(get_python_command)
    $PYTHON_CMD -m venv verdict-toolEnvironment

    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to create virtual environment. Make sure Python 3 is installed.${RESET}"
        exit 1
    fi

    # Activate virtual environment (different for Windows Git Bash)
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source verdict-toolEnvironment/Scripts/activate
    else
        source verdict-toolEnvironment/bin/activate
    fi

    echo -e "${GREEN}Virtual environment activated!${RESET}"
}

# Function to install dependencies
install_dependencies() {
    echo -e "${YELLOW}\nInstalling dependencies from requirements.txt...${RESET}"
    if [ ! -f "requirements.txt" ]; then
        echo -e "${RED}Error: requirements.txt file not found. Exiting...${RESET}"
        deactivate
        exit 1
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
    echo -e "${CYAN}Virtual environment deactivated.${RESET}"
}

# Main function
main() {
    clear
    display_welcome

    echo -e "${WHITE}Starting the installation process...${RESET}"
    create_env_file
    setup_virtual_environment
    install_dependencies

    echo -e "${GREEN}\nInstallation complete! 🎉${RESET}"
    echo -e "${WHITE}To activate the virtual environment, run:${RESET}"
    echo "  source verdict-toolEnvironment/bin/activate"
    echo -e "${WHITE}To run the tool:${RESET}"
    echo "  python verdict-tool.py"
    echo -e "${WHITE}To deactivate the environment:${RESET}"
    echo "  deactivate"
}

# Run the main function
main