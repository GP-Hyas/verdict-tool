#!/bin/bash

# Function to display the HYAS logo as ASCII art
display_welcome() {
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
}

# Function to read user input and create the .env file
create_env_file() {
    echo -e "\nLet's set up your API credentials."
    read -rp "Enter your API Key: " APIKEY
    if [ -z "$APIKEY" ]; then
        echo "Error: API Key cannot be empty. Exiting..."
        exit 1
    fi

    read -rp "Enter your Client ID: " CLIENTID
    if [ -z "$CLIENTID" ]; then
        echo "Error: Client ID cannot be empty. Exiting..."
        exit 1
    fi

    echo "Creating .env file with your credentials..."
    cat > .env << EOF
APIKEY=$APIKEY
CLIENTID=$CLIENTID
EOF
    echo ".env file created successfully!"
}

# Function to create and activate a virtual environment
setup_virtual_environment() {
    echo -e "\nSetting up the Python virtual environment..."
    python3 -m venv verdict-toolEnvironment
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment. Make sure Python 3 is installed."
        exit 1
    fi

    source verdict-toolEnvironment/bin/activate
    echo "Virtual environment activated!"
}

# Function to install dependencies
install_dependencies() {
    echo -e "\nInstalling dependencies from requirements.txt..."
    if [ ! -f "requirements.txt" ]; then
        echo "Error: requirements.txt file not found. Exiting..."
        deactivate
        exit 1
    fi

    pip install --upgrade pip
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies."
        deactivate
        exit 1
    fi

    echo "Dependencies installed successfully!"
    deactivate
    echo "Virtual environment deactivated."
}

# Main function
main() {
    clear
    display_welcome

    echo "Starting the installation process..."
    create_env_file
    setup_virtual_environment
    install_dependencies

    echo -e "\nInstallation complete! 🎉"
    echo "To activate the virtual environment, run:"
    echo "  source verdict-toolEnvironment/bin/activate"
    echo "To run the tool:"
    echo "  python verdict-tool.py"
    echo "To deactivate the environment:"
    echo "  deactivate"
}

# Run the main function
main