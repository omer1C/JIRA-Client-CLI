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

    def create_issue(self, payload):
        url = f"{self.base_url}/{ISSUE_URL}"
        response = requests.post(url, json=payload, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def update_issue(self, issue_key, payload):
        url = f"{self.base_url}/{ISSUE_URL}/{issue_key}"
        response = requests.put(url, json=payload, auth=self.auth, headers=self.headers)
        if response.status_code == 204:
           print("Issue updated successfully!")
        else:
            print(f"Failed to update issue. Status code: {response.status_code}")
            raise(Exception("Invalid request"))

    def delete_issue(self, issue_key):
        url = f"{self.base_url}/{ISSUE_URL}/{issue_key}"
        response = requests.delete(url, headers=self.headers, auth=self.auth)
        return response

    def add_comment(self, issue_key, comment):
        url = f"{self.base_url}/{ISSUE_URL}/{issue_key}/comment"
        payload = {"body": comment}
        response = requests.post(url, json=payload, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_transitions(self, issue_key):
        url = f"{self.base_url}/{ISSUE_URL}/{issue_key}/transitions"
        response = requests.get(url, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def transition_issue(self, issue_key, transition_id):
        url = f"{self.base_url}/{ISSUE_URL}/{issue_key}/transitions"
        payload = {"transition": {"id": transition_id}}
        response = requests.post(url, json=payload, auth=self.auth, headers=self.headers)
        if response.status_code == 204:
            return True
        else:
            return False