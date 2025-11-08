import json
import os
import sys
import requests

JIRA_URL = os.getenv("JIRA_URL")
JIRA_USER = os.getenv("JIRA_USER")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")

def create_jira_issue(summary, description):
    url = f"{JIRA_URL}/rest/api/2/issue"
    headers = {"Content-Type": "application/json"}
    payload = {
        "fields": {
            "project": {"key": "DP"},  # Replace with your Jira project key
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Bug"},
            "priority": "Medium"
        }
    }
    response = requests.post(url, headers=headers, auth=(JIRA_USER, JIRA_TOKEN), json=payload)
    if response.status_code == 201:
        print(f"✅ Created Jira issue: {summary}")
    else:
        print(f"❌ Failed to create issue: {response.status_code} {response.text}")

def parse_semgrep(file_path):
    if not os.path.exists(file_path):
        print(f"No results file found at {file_path}. Skipping Jira ticket creation.")
        return

    with open(file_path) as f:
        data = json.load(f)

    results = data.get("results", [])
    if not results:
        print("No vulnerabilities found by Semgrep.")
        return

    for result in results:
        summary = f"[Semgrep] {result['check_id']}"
        description = (
            f"File: {result['path']}\n"
            f"Line: {result['start']['line']}\n"
            f"Message: {result['extra']['message']}"
        )
        severity = result['extra'].get('severity', 'Medium')
        create_jira_issue(summary, description, severity)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_jira_tickets.py <semgrep-results.json>")
        sys.exit(1)

    semgrep_file = sys.argv[1]
    parse_semgrep(semgrep_file)