import base64
import json
import os
import re
import requests
import time

from . import MSGraph, MSGraphError
from Emerson.variables import LOGGER

class Sharepoint(MSGraph):
    def __init__(self, *args, **kwargs):
        self.domain = kwargs.pop("domain", "emerson")
        MSGraph.__init__(self, *args, **kwargs)

    def get_sharepoint_site_id(self, site_direction: str = None):
        try:
            site_direction = f":{site_direction.strip()}" if site_direction else ""
            request_url = self.graph_api_endpoint.format(
                f"/v1.0/sites/{self.domain}.sharepoint.com"
                + site_direction
                + "?select=id,webUrl"
            )
            response = requests.get(url=request_url, headers=self.headers)
            response.raise_for_status()
            json_data = response.json()
            return str(json_data["id"])
        except Exception as ex:
            raise ex
        
    def get_sharepoint_site_drives(self, site_id: str):
        try:
            site_id = site_id.strip()
            request_url = self.graph_api_endpoint.format('/v1.0/sites/' + site_id + '/drives?select=id,webUrl,name,driveType')
            response = requests.get(url = request_url, headers = self.headers)
            response.raise_for_status()
            json_data = json.loads(response.content)
            return json_data['value']
        except Exception as ex:
            raise ex
    
    def get_sharepoint_files_from_drive(self, site_id: str, site_drive_id: str, site_folder_level: str):
        try:
            site_id = site_id.strip()
            site_drive_id = site_drive_id.strip()
            site_folder_level = site_folder_level.strip()
            request_url = self.graph_api_endpoint.format('/v1.0/sites/' + site_id +'/drives/' + site_drive_id + '/' +site_folder_level + '?$top=10000&select=id,name,size,@microsoft.graph.downloadUrl')
            response = requests.get(url = request_url, headers = self.headers)
            response.raise_for_status()
            json_data = json.loads(response.content)
            return json_data['value']
        except Exception as ex:
            raise ex
        
    def verify_file_exist_sharepoint_drive(self, site_id: str, site_drive_id: str, site_file_location: str):
        result_dict = {}
        try:
            site_id = site_id.strip()
            site_drive_id = site_drive_id.strip()
            site_file_location = site_file_location.strip()
            request_url = self.graph_api_endpoint.format('/v1.0/sites/' + site_id +'/drives/' + site_drive_id + '/' +site_file_location + '?$top=10000&select=id,name')
            response = requests.get(url = request_url, headers = self.headers)
            json_data = json.loads(response.content)
            #dict Result
            result_dict["status_code"] = response.status_code
            if response.status_code == 404 or response.status_code == 400:
                result_dict["id"] = None
                result_dict["name"] = None
            else:
                response.raise_for_status()
                result_dict["id"] = json_data["id"]
                result_dict["name"] = json_data["name"]
            return result_dict
        except Exception as ex:
            if response.status_code == 404 or response.status_code == 400:
                json_data = json.loads(response.content)
                result_dict["status_code"] = response.status_code
                result_dict["id"] = None
                result_dict["name"] = None
                return result_dict
            raise ex
    
    def update_file_content_sharepoint_drive(self, site_id: str, site_drive_id: str, site_file_id: str,  full_file_path: str):
        try:
            site_id = site_id.strip()
            site_drive_id = site_drive_id.strip()
            site_file_id = site_file_id.strip()
            full_file_path = full_file_path.strip()
            request_url = self.graph_api_endpoint.format('/v1.0/sites/' + site_id +'/drives/' + site_drive_id + '/items/'+site_file_id+'/content')
            response = requests.put(url = request_url, headers = self.headers,data = open(full_file_path, 'rb').read())
            response.raise_for_status()
            json_data = json.loads(response.content)
            return response.status_code
        except Exception as ex:
            raise ex
        
    def create_small_file_content_sharepoint_drive(self, site_id: str, site_drive_id: str, site_file_path: str, full_file_path: str):
        try:
            site_id = site_id.strip()
            site_drive_id = site_drive_id.strip()
            site_file_path = site_file_path.strip()
            full_file_path = full_file_path.strip()
            request_url = self.graph_api_endpoint.format('/v1.0/sites/' + site_id +'/drives/' + site_drive_id + '/'+site_file_path+':/content')
            response = requests.put(url = request_url, headers = self.headers,data = open(full_file_path, 'rb').read())
            response.raise_for_status()
            json_data = json.loads(response.content)
            return response.status_code
        except Exception as ex:
            raise ex
    
    def create_seed_file_content_sharepoint_drive(self, site_id: str, site_drive_id: str, site_file_path: str, full_file_path: str):
        try:
            site_id = site_id.strip()
            site_drive_id = site_drive_id.strip()
            site_file_path = site_file_path.strip()
            full_file_path = full_file_path.strip()
            request_url = self.graph_api_endpoint.format('/v1.0/sites/' + site_id +'/drives/' + site_drive_id + '/'+site_file_path+':/content')
            response = requests.put(url = request_url, headers = self.headers,data = "Hello")
            response.raise_for_status()
            json_data = json.loads(response.content)
            return json_data["id"]
        except Exception as ex:
            raise ex
        
    def create_large_file_content_sharepoint_drive(self, site_id: str, site_drive_id: str, site_file_id: str, full_file_path: str, file_name: str):
        try:
            site_id = site_id.strip()
            site_drive_id = site_drive_id.strip()
            site_file_id = site_file_id.strip()
            full_file_path = full_file_path.strip()
            #createUploadSession
            request_url_UploadSession = self.graph_api_endpoint.format('/v1.0/sites/' + site_id +'/drives/' + site_drive_id + '/items/'+site_file_id+'/createUploadSession')
            self.headers["Content-Type"]="application/json"
            response_upload_session = requests.post(url = request_url_UploadSession, headers = self.headers, json={  '@microsoft.graph.conflictBehavior': 'replace',
                                                                                        'description': 'A large file',
                                                                                        'fileSystemInfo': {'@odata.type': 'microsoft.graph.fileSystemInfo'},
                                                                                        'name': file_name})
            response_upload_session.raise_for_status()
            upload_session = response_upload_session.json()
            upload_session_url = upload_session['uploadUrl']
            #FileSize
            st = os.stat(full_file_path)
            size = st.st_size
            # 10mb
            #CHUNK_SIZE = 10485760
            # 3mb
            CHUNK_SIZE = 3145728
            chunks = int(size / CHUNK_SIZE) + 1 if size % CHUNK_SIZE > 0 else 0
            with open(full_file_path, 'rb') as fd:
                start = 0
                for chunk_num in range(chunks):
                    chunk = fd.read(CHUNK_SIZE)
                    bytes_read = len(chunk)
                    upload_range = f'bytes {start}-{start + bytes_read - 1}/{size}'
                    print(f'chunk: {chunk_num} bytes read: {bytes_read} upload range: {upload_range}')
                    result = requests.put(
                        upload_session_url,
                        headers={
                            'Content-Length': str(bytes_read),
                            'Content-Range': upload_range
                        },
                        data=chunk
                    )
                    result.raise_for_status()
                    start += bytes_read
            if size > start:
                return False
            else:
                return True
        except Exception as ex:
            raise ex
    
    def create_item_in_sharepoint_list(self, 
                                       site_id: str, 
                                       list_id: str, 
                                       item: dict):
        try:
            site_id = site_id.strip()
            list_id = list_id.strip()
            new_item = json.dumps(item)
            request_url = self.graph_api_endpoint.format('/v1.0/sites/' + site_id +'/lists/' + list_id + '/items')
            response = requests.post(url = request_url, headers = self.headers, data=new_item)
            response.raise_for_status()
            json_data = json.loads(response.content)
            return json_data
        except Exception as ex:
            raise ex
        
    def get_sharepoint_lists(self, 
                             site_id: str):
        try:
            site_id = site_id.strip()
            request_url = self.graph_api_endpoint.format('/v1.0/sites/' + site_id + '/lists?$select=name,displayName,id')
            response = requests.get(url = request_url, headers = self.headers)
            response.raise_for_status()
            json_data = json.loads(response.content)
            return json_data['value']
        except Exception as ex:
            raise ex
        
    def update_item_in_sharepoint_list(self, 
                                       site_id: str, 
                                       list_id: str, 
                                       item: dict,
                                       item_id: str):
        try:
            site_id = site_id.strip()
            list_id = list_id.strip()
            item_id = item_id.strip()
            new_item = json.dumps(item)
            request_url = self.graph_api_endpoint.format('/v1.0/sites/' + site_id +'/lists/' + list_id + '/items/' + item_id + "/fields")
            response = requests.patch(url = request_url, headers = self.headers, data=new_item)
            response.raise_for_status()
            json_data = json.loads(response.content)
            return json_data
        except Exception as ex:
            raise ex
           
    def download_sharepoint_file(self,
                                 site_id: str, 
                                 site_drive_id: str, 
                                 site_file_id: str):
        try:
            site_id = site_id.strip()
            site_drive_id = site_drive_id.strip()
            site_file_id = site_file_id.strip()
            request_url = self.graph_api_endpoint.format('/v1.0/sites/' + site_id +'/drives/' + site_drive_id + '/root:/'+ site_file_id)
            response = requests.get(url = request_url, headers = self.headers)
            response.raise_for_status()
            json_data = json.loads(response.content)
        except Exception as ex:
            raise ex
        return json_data['@microsoft.graph.downloadUrl']
    
    def get_data_from_sharepoint_list_item(self, 
                                           site_id: str, 
                                           list_id: str):
        try:
            site_id = site_id.strip()
            list_id = list_id.strip()
            request_url = self.graph_api_endpoint.format('/v1.0/sites/' + site_id + '/lists/' + list_id + '/items?expand=fields&$top=10000')
            response = requests.get(url = request_url, headers = self.headers)
            response.raise_for_status()
            json_data = json.loads(response.content)
        except Exception as ex:
            raise ex
        return json_data['value']
    
    def move_file_from_sharepoint_folder(self, 
                                         site_id: str, 
                                         drive_id: str,
                                         item_id: str,
                                         file: dict):
        try:
            site_id = site_id.strip()
            drive_id = drive_id.strip()
            item_id = item_id.strip()
            new_item = json.dumps(file)
            request_url = self.graph_api_endpoint.format('/v1.0/sites/' + site_id + '/drives/' + drive_id + '/items/' + item_id)
            response = requests.patch(url = request_url, headers = self.headers, data=new_item)
            response.raise_for_status()
            json_data = json.loads(response.content)
        except Exception as ex:
            raise ex
        
    def get_sharepoint_list_by_display_name(self, 
                                            site_id: str,
                                            list_display_name: str) -> list:
        try:
            site_id = site_id.strip()
            list_display_name = list_display_name.strip()
            request_url = self.graph_api_endpoint.format(f"/v1.0/sites/{site_id}/lists?$filter=DisplayName eq '{list_display_name}'")
            response = requests.get(url = request_url, headers = self.headers)
            response.raise_for_status()
            json_data = json.loads(response.content)
            return json_data['value']
        except Exception as ex:
            raise ex
        
    def get_sharepoint_users_list(self, 
                                  site_id: str,
                                  users_list_id: str) -> list:
        users_list = []
        try:
            site_id = site_id.strip()
            users_list_id = users_list_id.strip()
            request_url = self.graph_api_endpoint.format(f"/v1.0/sites/{site_id}/lists/{users_list_id}/items?$expand=fields&$top=300")
            next_link_key = "@odata.nextLink"
            while True:
                response = requests.get(url = request_url, headers = self.headers)
                response.raise_for_status()
                json_data = json.loads(response.content)
                users_list.extend(json_data['value'])
                if(next_link_key not in json_data):
                    break
                request_url = json_data[next_link_key]
        except Exception as ex:
            raise ex
        return users_list
    
    def get_data_from_sharepoint_library(self, 
                                         site_id: str, 
                                         site_drive_id: str,    
                                         site_folder_level: str) -> dict:
    
        try:
            site_id = site_id.strip()
            site_drive_id = site_drive_id.strip()
            site_folder_level = site_folder_level.strip()
            request_url = self.graph_api_endpoint.format('/v1.0/sites/' + site_id +'/drives/' + site_drive_id + '/' +site_folder_level + '?$top=10000&$expand=listItem')
            #/v1.0/sites/[Site_ID]/drives/[Drive_ID]/[Site_Folder_Level]?$top=10000&$expand=listItem
            response = requests.get(url = request_url, headers = self.headers)
            response.raise_for_status()
            json_data = json.loads(response.content)
            return json_data['value']
        except Exception as ex:
            raise ex

    def update_sharepoint_library_data(self, 
                                       site_id: str, 
                                       drive_id: str,
                                       item_id: str,
                                       item: dict) -> dict:
        try:
            site_id = site_id.strip()
            drive_id = drive_id.strip()
            item_id = item_id.strip()
            new_item = json.dumps(item)
            request_url = self.graph_api_endpoint.format('/v1.0/sites/' + site_id + '/drives/' + drive_id + '/items/' + item_id + '/listItem')
            #/v1.0/sites/[Site_ID]/drives/[Drive_ID]/items/[Item_ID]/listItem
            response = requests.patch(url = request_url, headers = self.headers, data=new_item)
            response.raise_for_status()
            json_data = json.loads(response.content)
            return json_data
        except Exception as ex:
            raise ex