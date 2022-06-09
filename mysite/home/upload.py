from __future__ import print_function
import os
import io
import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file, client, tools
import sys
sys.argv=['']
del sys

# 權限必須
SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']


def delete_drive_service_file(service, file_id):
    service.files().delete(fileId=file_id).execute()

# 將本地端的檔案傳到雲端上
def update_file(service, update_drive_service_name, local_file_path, update_drive_service_folder_id):

    print("正在上傳檔案...")
    if update_drive_service_folder_id is None:
        file_metadata = {'name': update_drive_service_name}
    else:
        print("雲端資料夾id: %s" % update_drive_service_folder_id)
        file_metadata = {'name': update_drive_service_name,
                         'parents': update_drive_service_folder_id}

    media = MediaFileUpload(local_file_path, )
    file_metadata_size = media.size()
    start = time.time()
    file_id = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    end = time.time()

    print("上傳檔案成功！")
    print('雲端檔案名稱為: ' + str(file_metadata['name']))
    print('雲端檔案ID為: ' + str(file_id['id']))
    print('檔案大小為: ' + str(file_metadata_size) + ' byte')
    print("上傳時間為: " + str(end-start))

    return file_metadata['name'], file_id['id']


def search_folder(service, update_drive_folder_name=None):
    """
    如果雲端資料夾名稱相同，則只會選擇一個資料夾上傳，請勿取名相同名稱
    :param service: 認證用
    :param update_drive_folder_name: 取得指定資料夾的id，沒有的話回傳None，給錯也會回傳None
    """

    get_folder_id_list = []
    print(len(get_folder_id_list))
    if update_drive_folder_name is not None:
        response = service.files().list(fields="nextPageToken, files(id, name)", spaces='drive',
                                       q = "name = '" + update_drive_folder_name + "' and mimeType = 'application/vnd.google-apps.folder' and trashed = false").execute()

        for file in response.get('files', []):
            # Process change
            print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
            get_folder_id_list.append(file.get('id'))

        if len(get_folder_id_list) == 0:
            print("你給的資料夾名稱沒有在你的雲端上！，因此檔案會上傳至雲端根目錄")
            return None
        else:
            return get_folder_id_list

    return None


def search_file(service, update_drive_service_name, is_delete_search_file=False):
    # Call the Drive v3 API
    results = service.files().list(fields="nextPageToken, files(id, name)", spaces='drive',
                                   q="name = '" + update_drive_service_name + "' and trashed = false",
                                   ).execute()

    items = results.get('files', [])

    if not items:
        print('沒有發現你要找尋的 ' + update_drive_service_name + ' 檔案')
    else:
        print('搜尋的檔案: ')

        for item in items:
            times = 1
            print(u'{0} ({1})'.format(item['name'], item['id']))
            if is_delete_search_file is True:
                print("刪除檔案為:" + u'{0} ({1})'.format(item['name'], item['id']))
                delete_drive_service_file(service, file_id=item['id'])
            if times == len(items):
                return item['id']
            else:
                times += 1


def trashed_file(service, is_delete_trashed_file=False):
    results = service.files().list(fields="nextPageToken, files(id, name)", spaces='drive', q="trashed = true",
                                   ).execute()
    items = results.get('files', [])

    if not items:
        print('垃圾桶無任何資料.')
    else:
        print('垃圾桶檔案: ')

        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
            if is_delete_trashed_file is True:
                print("刪除檔案為:" + u'{0} ({1})'.format(item['name'], item['id']))
                delete_drive_service_file(service, file_id=item['id'])


def main(is_update_file_function=False, update_drive_service_folder_name=None, update_drive_service_name=None, update_file_path=None):
    print("is_update_file_function: %s" % is_update_file_function)
    print("update_drive_service_folder_name: %s" % update_drive_service_folder_name)
    store = file.Storage('token.json')
    creds = None

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    service = build('drive', 'v3', http=creds.authorize(Http()))
    print('*' * 10)

    if is_update_file_function is True:
        print(update_file_path + update_drive_service_name)
        print("=====執行上傳檔案=====")
        get_folder_id = search_folder(service = service, update_drive_folder_name = update_drive_service_folder_name)

        search_file(service=service, update_drive_service_name=update_drive_service_name,
                    is_delete_search_file=True)

        update_file(service=service, update_drive_service_name=update_drive_service_name,
                    local_file_path='C:/Users/HomeOffice_16/Desktop/testdjango/mysite/media' + '/' + update_drive_service_name, update_drive_service_folder_id=get_folder_id)
        


if __name__ == '__main__':
    main(is_update_file_function=bool(True), update_drive_service_folder_name='TestAPI', update_drive_service_name="test8.docx", update_file_path=r"C:\Users\HomeOffice_16\Desktop\testdjango\mysite\media")
   