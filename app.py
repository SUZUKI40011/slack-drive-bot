from flask import Flask, request, jsonify
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

# ==== Google Drive API 設定 ====
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'path/to/your/service-account.json'  # 適宜置き換え
PARENT_FOLDER_ID = '1ATD4rxXNynNqC8HXp3IKkBqKxoW_jGXN'  # あなたの親フォルダID

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)


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


@app.route('/slack/command', methods=['POST'])
def slack_command():
    text = request.form.get('text') or ''
    company_name = text.strip()

    if not company_name:
        return jsonify(response_type='ephemeral', text='会社名を入力してください。')

    results = search_drive(company_name)

    if not results:
        return jsonify(response_type='in_channel', text=f"Drive上に「{company_name}」の「キックオフ資料」は見つかりませんでした。")

    msg = f"「{company_name}」のキックオフ資料はこちらです:\n" + "\n".join(results)
    return jsonify(response_type='in_channel', text=msg)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
