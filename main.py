from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import os

SCOPES = ['https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('authclients.json', scopes = SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

def create_drive_folder(obsidian, parent_folder_id=None):
    file_metadata = {
        'name': obsidian,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id] if parent_folder_id else []
    }
    
    folder = drive_service.files().create(body=file_metadata, fields = 'id').execute()
    return folder.get('id')

def upload_file(file_path, drive_folder_id):
    file_name = os.path.basename(file_path)
    file_metadata = {'name': file_name, 'parents': [drive_folder_id]}
    media = MediaFileUpload(file_path, resumable=True)
    uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"uploaded: {file_name}")
    return uploaded_file.get('id')

def upload_folder(local_folder, drive_folder_id):
    for item in os.listdir(local_folder):
        item_path = os.path.join(local_folder, item)
        
        if os.path.isdir(item_path):
            new_drive_folder_id = create_drive_folder(item, drive_folder_id)
            print(f"created folder: {item} in google drive")
            upload_folder(item_path, new_drive_folder_id)
        else:
            upload_file(item_path, drive_folder_id)
            
local_folder = "/home/notme6000/Documents/Obsidian Vault"
drive_folder_id = '1w5_iE0uQGddQvEQ4pYc7PrNvCu4NnZHC'

upload_folder(local_folder, drive_folder_id)
print("folder uploaded complete")