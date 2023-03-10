from google.oauth2 import service_account
from googleapiclient.discovery import build

def create_calendar(group_name, timezone):
    # Автентифікація за допомогою сервісного облікового запису
    credentials = service_account.Credentials.from_service_account_file('path/to/credentials.json')
    service = build('calendar', 'v3', credentials=credentials)

    # Створення календаря
    calendar = {
        'summary': group_name,
        'timeZone': timezone
    }
    created_calendar = service.calendars().insert(body=calendar).execute()

    # Повернення ідентифікатора календаря
    return created_calendar['id']
