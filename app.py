def search_drive(company_name):
    folder_results = drive_service.files().list(
        q=f"'{PARENT_FOLDER_ID}' in parents and mimeType='application/vnd.google-apps.folder' and name contains '{company_name}'",
        fields="files(id, name)").execute()
    folders = folder_results.get('files', [])

    if not folders:
        return []

    folder_id = folders[0]['id']

    sheet_results = drive_service.files().list(
        q=f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.spreadsheet' and name contains 'キックオフ'",
        fields="files(id, name)").execute()

    sheets = sheet_results.get('files', [])
    return [f"https://docs.google.com/spreadsheets/d/{f['id']}" for f in sheets]

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

