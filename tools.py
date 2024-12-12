import requests
from typing import List, Dict, Union

# Define the base URL for the API
BASE_URL = "http://localhost:8080"

def get_remember() -> List[Dict[str, Union[str, int, None]]]:
    """
    Get all reminders from the API.

    Returns
    -------
    List[Dict[str, Union[str, int, None]]]
        A list of reminders in JSON format.

    Raises
    ------
    HTTPError
        If the request to the API fails.
    """
    response = requests.get(f"{BASE_URL}/GetRemember")
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def create_remember(what: str, priority: str, notes: str) -> Dict[str, Union[str, int, None]]:
    """
    Create a new reminder.

    Parameters
    ----------
    what : str
        The description of the reminder.
    priority : str
        The priority level of the reminder.
    notes : str
        Additional notes for the reminder.

    Returns
    -------
    Dict[str, Union[str, int, None]]
        The created reminder in JSON format.

    Raises
    ------
    HTTPError
        If the request to the API fails.
    """
    payload = {
        "What": what,
        "Priority": priority,
        "Notes": notes
    }
    response = requests.post(f"{BASE_URL}/CreateRemember", json=payload)
    if response.status_code == 201:
        created_reminder = response.json()
        print("Created Reminder:", created_reminder)
        return created_reminder
    else:
        response.raise_for_status()

def update_remember(id: int, what: str, priority: str, notes: str) -> str:
    """
    Update an existing reminder.

    Parameters
    ----------
    id : int
        The unique identifier of the reminder to be updated.
    what : str
        The description of the reminder.
    priority : str
        The priority level of the reminder.
    notes : str
        Additional notes for the reminder.

    Returns
    -------
    str
        A success message.

    Raises
    ------
    HTTPError
        If the request to the API fails.
    """
    payload = {
        "Id": id,
        "What": what,
        "Priority": priority,
        "Notes": notes
    }
    response = requests.put(f"{BASE_URL}/UpdateRemember", json=payload)
    if response.status_code == 204:
        return "Reminder updated successfully"
    else:
        response.raise_for_status()

def delete_remember(id: int) -> str:
    """
    Delete a reminder by ID.

    Parameters
    ----------
    id : int
        The unique identifier of the reminder to be deleted.

    Returns
    -------
    str
        A success message or an error message if the reminder is not found.

    Raises
    ------
    HTTPError
        If the request to the API fails.
    """
    response = requests.delete(f"{BASE_URL}/DeleteRemember/{id}")
    if response.status_code == 204:
        return "Reminder deleted successfully"
    elif response.status_code == 404:
        return "Reminder not found"
    else:
        response.raise_for_status()

# Example usage
if __name__ == "__main__":
    # Create a new reminder
    created_reminder = create_remember(
        what="Submit project report",
        priority="High",
        notes="Include Q4 financials"
    )
    print("Created Reminder:", created_reminder)

    # Get all reminders
    reminders = get_remember()
    print("All Reminders:", reminders)

    # Update an existing reminder
    if 'id' in created_reminder:
        update_response = update_remember(
            id=created_reminder['id'],
            what="Submit project report with updates",
            priority="High",
            notes="Include Q4 financials and updates"
        )
        print("Update Response:", update_response)
    else:
        print("Created reminder does not contain 'Id' field.")

    # Delete a reminder by ID
    if 'id' in created_reminder:
        delete_response = delete_remember(created_reminder['id'])
        print("Delete Response:", delete_response)
    else:
        print("Created reminder does not contain 'Id' field.")
