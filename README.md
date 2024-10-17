# JSQL - SQL-Injection Automation Tool

## Description
This Python-based SQL Injection Automation Tool is designed to help security researchers and penetration testers automate the process of testing web applications for SQL injection vulnerabilities. The tool sends various SQL payloads to specified endpoints and checks for successful injections based on the application's responses.

## Features
- **Automatic Parameter Detection**: Automatically detects input parameters from forms on the target web application.
- **Custom Payloads**: Load custom SQL injection payloads from a user-specified word list.
- **Logging**: Logs details of each request sent, including URL, method, and request body.
  
## Requirements
- Python 3.x
- Required Python libraries:
  - `requests`
  - `beautifulsoup4`
  - `colorama`

You can install the required libraries using pip:
```bash
pip install requests beautifulsoup4 colorama
```

Usage
1-Clone this repository to your local machine:
```bash
git clone https://github.com/John-A0/JSQL.git
cd JSQL
```
2-Run the script:
```bash
python JSQL.py
```

## Important Notes
- **Customization:** You may want to customize the parameter extraction logic based on the target application’s specific forms and structure.
- **Authorization:** Ensure that you have permission to test the target web application. Unauthorized testing is illegal and unethical.
- **Use Cases:** This tool is primarily intended for educational purposes, security research, and authorized penetration testing.

## Contributing
**If you would like to contribute to this project, feel free to fork the repository and submit a pull request. Suggestions and improvements are welcome!**



