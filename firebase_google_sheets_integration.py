import firebase_admin
from firebase_admin import credentials, firestore
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def initialize_firebase():
    """Initializes Firebase connection."""
    try:
        cred = credentials.Certificate(
            "path/to/your/firebase_credentials.json")  # Replace with your Firebase credentials file
        firebase_admin.initialize_app(cred, {'databaseURL': 'YOUR_DATABASE_URL'})  # Replace with your database URL
        print("Firebase initialized successfully.")
        return firestore.client()
    except FileNotFoundError:
        print("Error: Firebase credentials file not found. Please check the file path.")
        return None
    except firebase_admin.exceptions.FirebaseError as e:
        print(f"Error initializing Firebase: {e}")
        return None


db = initialize_firebase()


def initialize_google_sheets():
    """Initializes Google Sheets connection."""
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']  # If modifying these scopes, delete the file token.json.
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            'path/to/your/google_sheets_credentials.json',
            scope)  # Replace with your Google Sheets credentials file
        client = gspread.authorize(creds)
        print("Google Sheets initialized successfully.")
        # Replace with your spreadsheet name or ID
        spreadsheet_name = "Your Spreadsheet Name"  # or spreadsheet_id
        return client.open(spreadsheet_name).sheet1
    except FileNotFoundError:
        print("Error: Google Sheets credentials file not found. Please check the file path.")
        return None
    except gspread.exceptions.APIError as e:
        print(f"Error initializing Google Sheets: {e}")
        return None


sheet = initialize_google_sheets()


def add_data_to_firebase(data):
    """Adds data to Firebase."""
    doc_ref = db.collection("your_collection").document()  # Replace "your_collection"
    doc_ref.set(data)
    print(f"Data added to Firebase: {data}")


def add_data_to_google_sheets(data):
    """Adds data to Google Sheets."""
    sheet.append_row(list(data.values()))  # Convert dictionary values to a list
    print(f"Data added to Google Sheets: {data}")


# Example usage (replace with your actual data)
data = {"name": "John Doe", "age": 30, "city": "New York"}

add_data_to_firebase(data)
add_data_to_google_sheets(data)