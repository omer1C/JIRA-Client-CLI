import requests

ISSUE_URL = "rest/api/2/issue"

class APIClient:
    def __init__(self, base_url, user_name, api_token):
        self.base_url = base_url
        self.auth = (user_name, api_token)
        self.headers = {"Content-Type": "application/json"}
    
    def test_connection(self):
        url = f"{self.base_url}/rest/api/2/myself"
        response = requests.get(url, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_issue(self, issue_key):
        url = f"{self.base_url}/{ISSUE_URL}/{issue_key}"
        response = requests.get(url, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_issue(self, project_key, summary, description):
        url = f"{self.base_url}/{ISSUE_URL}"
        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": "Task"}
            }
        }
        response = requests.post(url, json=payload, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def update_issue(self, issue_key, payload):
        url = f"{self.base_url}/{ISSUE_URL}/{issue_key}"
        response = requests.put(url, json={"fields": payload}, auth=self.auth, headers=self.headers)
        if response.status_code == 204:
           print("Issue updated successfully!")
        else:
            print(f"Failed to update issue. Status code: {response.status_code}")
            raise(Exception("Invalid request"))

    def delete_issue(self, issue_key):
        url = f"{self.base_url}/{ISSUE_URL}/{issue_key}"
        response = requests.delete(url, headers=self.headers, auth=self.auth)
        return response
  
        
