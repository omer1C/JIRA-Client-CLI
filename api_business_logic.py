from api_client import APIClient
from colorama import Fore, Style
from tabulate import tabulate

class Manager:
        
    def __init__(self, base_url, user_name, api_token):
        self.client = APIClient(base_url, user_name, api_token)
        try:
            user_info = self.client.test_connection()
            print(f"Connected as {user_info['displayName']}")
        except Exception as e:
            print(Fore.RED + f"Failed to connect: {e}" + Style.RESET_ALL)
            raise(e)
            
        
    def get_issue(self, issue_key):
        try:
            issue_data = self.client.get_issue(issue_key)
            self.print_issue(issue_data)

        except Exception as e:
            print(Fore.RED + f"Error retrieving issue: {e}" + Style.RESET_ALL)

    def create_issue(self, project_key, summary, description):
            try:
                payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": "Task"}
            }
        }
                issue = self.client.create_issue(project_key, payload)
                self.get_issue(issue['key'])
            except Exception as e:
                print(Fore.RED + f"Error creating issue: {e}" + Style.RESET_ALL)

    def update_issue(self, payload, issue_key):
        try:
            payload = {"fields": payload}
            response = self.client.update_issue(issue_key, payload)
            self.get_issue(issue_key)
            
        except Exception as e:
            return {"error": str(e), "response": response.text if response else None}
        
    def validate_issue(self, issue_key):
        try:
            self.client.get_issue(issue_key)
            return True
        except Exception as e:
            return False

    def print_issue(self, issue_data):
        fields = issue_data['fields']
        created = fields.get('created', 'N/A')
        description = fields.get('description', 'No description available')
        status = fields.get('status', {}).get('name', 'Unknown')
        summary = fields.get('summary', 'No summary available')
        creator = fields.get('creator', {}).get('displayName', 'Unknown')

        table = [
            ["Summary", summary],
            ["Description", description],
            ["Status", status],
            ["Created", created],
            ["Creator", creator]
        ]

        print(Fore.GREEN + "\nIssue Details:" + Style.RESET_ALL)
        print(tabulate(table, headers=["Field", "Value"], tablefmt="pretty"))

    def delete_issue(self, issue_key):
        if self.validate_issue(issue_key):
            response = self.client.delete_issue(issue_key)
            if response.status_code == 204:
                print(Fore.GREEN + f"Issue {issue_key} deleted successfully!" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"Failed to delete issue {issue_key}. Status Code: {response.status_code}" + Style.RESET_ALL)
                print(Fore.RED + f"Response: {response.text}" + Style.RESET_ALL)                   
        else:
            print("Invalid issue key, please try again.")
    
    def add_comment(self, issue_key, comment):
        if self.validate_issue(issue_key):
            try:
                response = self.client.add_comment(issue_key, comment)
                print(Fore.GREEN + "Comment added successfully!" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Failed to add comment: {e}" + Style.RESET_ALL)


    def update_status(self, issue_key, status_name):
        if self.validate_issue(issue_key):
            try:
                transitions = self.client.get_transitions(issue_key)
                transition_id = None
        
                for transition in transitions['transitions']:
                    if transition['to']['name'].lower() == status_name.lower():
                        transition_id = transition['id']
                        break
                
                if not transition_id:
                    print(Fore.RED + f"No transition found for status '{status_name}'." + Style.RESET_ALL)
                    return
                response = self.client.transition_issue(issue_key, transition_id)
                if response:
                    print(Fore.GREEN + f"Issue {issue_key} successfully transitioned to '{status_name}'." + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Failed to change status: {e}" + Style.RESET_ALL)

        else:
            print("Invalid issue key, please try again.")