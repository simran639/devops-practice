import json
import os
import sys
import requests
# from bs4 import BeautifulSoup

file_path = "./results/semgrep-results.json"

JIRA_URL = os.getenv("JIRA_URL")
JIRA_USER = os.getenv("JIRA_USER")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")

def create_jira_issue(summary, description, severity="Medium"):
    url = f"{JIRA_URL}/rest/api/2/issue"
    headers = {"Content-Type": "application/json"}
    payload = {
        "fields": {
            "project": {"key": "DP"},  # Replace with your Jira project key
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Bug"},
            "priority": {"name": severity}
        }
    }
    response = requests.post(url, headers=headers, auth=(JIRA_USER, JIRA_TOKEN), json=payload)
    if response.status_code == 201:
        print(f"Created Jira issue: {summary}")
    else:
        print(f"Failed to create issue: {response.text}")

def parse_semgrep(file_path):
    with open(file_path) as f:
        data = json.load(f)
        if not data.get("results"):
            print("No vulnerabilities found by Semgrep.")
            sys.exit(0)  # gracefully exit instead of error

    for result in data.get("results", []):
        summary = f"[Semgrep] {result['check_id']}"
        description = f"File: {result['path']}\nLine: {result['start']['line']}\nMessage: {result['extra']['message']}"
        severity = result['extra'].get('severity', 'Medium')
        create_jira_issue(summary, description, severity)
 
# def parse_zap(file_path):
#     with open(file_path) as f:
#         soup = BeautifulSoup(f, "html.parser")
#     alerts = soup.find_all("tr", class_="risk-High")  # Example: parse high-risk rows
#     for alert in alerts:
#         summary = f"[ZAP] {alert.find('td').text.strip()}"
#         description = alert.text.strip()
#         create_jira_issue(summary, description, "High")

if __name__ == "__main__":
    semgrep_file = sys.argv[1]
    # zap_file = sys.argv[2]
    parse_semgrep(semgrep_file)
    # parse_zap(zap_file)