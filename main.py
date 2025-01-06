from api_business_logic import Manager
import os
import emoji
from colorama import Fore, Style, init
import questionary

init(autoreset=True)

def clean_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def update_payload(manager):
    issue_key = questionary.text("Please Enter the issue key to update:").ask()
    if not manager.validate_issue(issue_key):
        print("Please try again with different key")
        return update_payload(manager)
    summary = questionary.text("New summary (leave blank if unchanged):").ask().strip()
    description = questionary.text("New description (leave blank if unchanged):").ask().strip()

    payload = {}
    if summary:
        payload["summary"] = summary
    if description:
        payload["description"] = description

    return payload, issue_key


def main():
    clean_screen()
    print("👋 Welcome to the Jira CLI Application!")
    
    while True:
        try:
            base_url = questionary.text("Enter Jira base URL (e.g., https://your-domain.atlassian.net): ").ask()
            user_name = questionary.text("Enter your Jira username (email): ").ask()
            api_token = questionary.text("Enter your Jira API token: ").ask()
            manager = Manager(base_url, user_name, api_token)
            if manager:
                break
        except Exception as e:
            print("Could not connect to Jira, please try again")
            
    while True:

        try:
            action = questionary.select(
                emoji.emojize(":rocket: Jira CLI Application - Choose an action:"),
                choices=[
                    "Get an Issue 📁",
                    "Create an Issue 📝",
                    "Update an Issue 🏷️",
                    "Delete an Issue ❌",
                    "Exit 🚪"
                ]
            ).ask()

            if action == "Get an Issue 📁":
                clean_screen()
                issue_key = questionary.text("Enter the issue key (e.g., PROJ-123):").ask().strip()
                manager.get_issue(issue_key)

            elif action == "Create an Issue 📝":
                clean_screen()
                project_key = questionary.text("Enter the project key (e.g., PROJ):").ask().strip()
                summary = questionary.text("Enter the issue summary:").ask().strip()
                description = questionary.text("Enter the issue description:").ask().strip()
                manager.create_issue(project_key, summary, description)

            elif action == "Update an Issue 🏷️":
                payload, issue_key = update_payload(manager)
                if payload:
                    manager.update_issue(payload, issue_key)
                else:
                    print(Fore.YELLOW + "No updates provided. Returning to menu..." + Style.RESET_ALL)
            elif action == "Delete an Issue ❌":
                issue_key = questionary.text("Please Enter the issue key to delete:").ask()
                manager.delete_issue(issue_key)

            elif action == "Exit 🚪":
                print(Fore.MAGENTA + "Thanks for trying out the JIRA Client CLI! 🚀\nGoodbye! 👋" + Style.RESET_ALL)
                break
        except Exception as e:
            print(Fore.RED + "Oops something went wrong, please try again" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
