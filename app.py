def search_drive(company_name):
    folder_results = drive_service.files().list(
        q=f"'{PARENT_FOLDER_ID}' in parents and mimeType='application/vnd.google-apps.folder' and name contains '{company_name}'",
        fields="files(id, name)").execute()
    folders = folder_results.get('files', [])

    if not folders:
        return []

    folder_id = folders[0]['id']

    sheet_results = drive_service.files().list(
        q=f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.spreadsheet' and name contains 'キックオフ資料'",
        fields="files(id, name)").execute()

    sheets = sheet_results.get('files', [])
    return [f"https://docs.google.com/spreadsheets/d/{f['id']}" for f in sheets]
