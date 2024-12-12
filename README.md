# Verdict Tool

## Overview

The Verdict Tool is a command-line utility that reads a .txt or .csv file containing a list of domains and retrieves verdicts (e.g., allow, block, none) for each domain using an API.

## Requirements

• Python 3.8 or higher
• Installed dependencies from requirements.txt

## Installation

1. Create a virtual environment and activate it:

   ```bash
   python -m venv .venv
   source .venv/bin/activate # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Add your API key to a .env file in the project directory:

   ```bash
   APIKEY=your-api-key
   CLIENTID=your-client-id
   ```

## Usage

1. Run the tool:

   ```bash
   python main.py
   ```

2. Enter the file path to your .txt or .csv containing domains when prompted:

   ```bash
   Enter the file path to your txt or csv: ~/Downloads/domains.txt
   ```

3. View the progress and results in the terminal. The verdicts will be saved to a CSV report in your Downloads folder:

   ```bash
   CSV created successfully: ~/Downloads/verdict_report.csv
   ```

## Example Input

A .txt or .csv file with one domain per line:

```bash
example.com
google.com
yahoo.com
```

## Example Output

The generated CSV report will include:

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
```
