# Verdict Tool

## Overview

The **Verdict Tool** is a command-line utility that reads a .txt or .csv file containing a list of domains and retrieves verdicts (e.g., **allow**, **block**, **none**) for each domain using an API. The results are saved to a CSV report in your **Downloads** folder.

## Requirements

• **Python:** 3.11 or higher
• **Dependencies:** installed via the script

## Installation

The tool comes with an **install script** to make setup simple and streamlined.

### Run the Install Script

1. **Make the script executable:**

   ```bash
   chmod +x install.sh
   ```

2. **Run the script:**

   ```bash
   ./install.sh
   ```

3. **Follow the prompts:**

   - Enter your **API key** and **Client ID** when prompted.
   - The script will:
     - Creates an .env file with your API credentials
     - Set up a virtual environment named `verdict-toolEnvironment`
     - Install all required dependencies from `requirements.txt`

## Usage

After installation, follow these steps to run the tool:

1. **Activate the virtual environment:**

   ```bash
   source verdict-toolEnvironment/bin/activate
   ```

2. **Run the tool:**

   ```bash
   python verdict-tool.py
   ```

3. **Enter the file** path to your `.txt` or `.csv` file when prompted:

   ```bash
   Enter the file path to your txt or csv: ~/Downloads/domains.txt
   ```

4. **View Progress:**

   - The tool will process each domain and display the progress in the terminal
   - A CSV report will be generated in your **Downloads** folder.

5. **Deactivate the virtual environment** (optional):

   ```bash
   deactivate
   ```

## Example Input

A .txt or .csv file with one domain per line:

```bash
example.com
google.com
yahoo.com
```

## Example Output

The generated **CSV report** will include:

| Domain      | Verdict |
| ----------- | ------- |
| example.com | allow   |
| google.com  | block   |
| yahoo.com   | none    |

Summary

At the end of processing, a summary will display the count of domains in each category:

```bash
Summary:
Allow: 39 domains
Block: 6 domains
None: 1 domains

CSV created successfully: ~/Downloads/verdict_report.csv
```

## Troubleshooting

- **Error:** `install.sh: Permission Denied`

Solution: Ensure the script is executable

```bash
chmod +x install.sh
```

- **Error:** `Python` command not found

Solution: Verify Python 3 is installed

```bash
python3 --version
```
