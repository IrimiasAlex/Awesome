import base64
import json
import os
import re
import requests

from . import MSGraph, MSGraphError
from Emerson.variables import LOGGER


class Email(MSGraph):
    """docstring for MsGraphEmail."""

    def __init__(self, *args, **kwargs):
        MSGraph.__init__(self, *args, **kwargs)

    def create_draft_email(
        self,
        email_subject: str,
        email_body: str,
        email_to: str,
        email_cc = "",
        email_bcc = "",
    ):
        if not self.token:
            raise MSGraphError("Authentication token does not exist")
        try:
            # inputs
            email_subject = email_subject.strip()
            email_body = email_body.strip()
            email_to = email_to.strip()
            # Validate
            if not bool(email_subject):
                email_subject = "None"
            if not bool(email_body):
                email_body = "None"
            if not bool(email_to):
                raise Exception("The field To Recipient cannot be blank")
            # request
            request_url = self.graph_api_endpoint.format("/v1.0/me/messages")
            email_data = {
                "subject": email_subject,
                "body": {"contentType": "HTML", "content": email_body},
                "toRecipients": [],
            }
            list_to = re.split(";", email_to)
            email_data["toRecipients"] = [
                {"emailAddress": {"address": add}} for add in list_to
            ]
            if bool(email_cc):
                email_cc = email_cc.strip()
                list_cc = re.split(";", email_cc)
                email_data["ccRecipients"] = [
                    {"emailAddress": {"address": add}} for add in list_cc
                ]
            if bool(email_bcc):
                email_bcc = email_bcc.strip()
                list_bcc = re.split(";", email_bcc)
                email_data["bccRecipients"] = [
                    {"emailAddress": {"address": add}} for add in list_bcc
                ]
            json_email_data = json.dumps(email_data)
            response = requests.post(
                url=request_url, headers=self.headers, data=json_email_data
            )
            response.raise_for_status()
            json_data = response.json()
            return str(json_data["id"])
        except Exception as ex:
            raise ex

    def add_file_content_email_message(
        self, 
        email_message_id: str, 
        full_file_path: str, 
        file_name: str
    ):
        try:
            email_message_id = email_message_id.strip()
            full_file_path = full_file_path.strip()
            file_name = file_name.strip()

            # FileSize
            st = os.stat(full_file_path)
            size = st.st_size
            # createUploadSession
            if size >= 2150830:
                request_url_UploadSession = self.graph_api_endpoint.format(
                    "/v1.0/me/messages/"
                    + email_message_id
                    + "/attachments/createUploadSession"
                )
                self.headers["Content-Type"] = "application/json"
                response_upload_session = requests.post(
                    url=request_url_UploadSession,
                    headers=self.headers,
                    json={
                        "AttachmentItem": {
                            "attachmentType": "file",
                            "name": file_name,
                            "size": size,
                        }
                    },
                )
                upload_session = response_upload_session.json()
                upload_session_url = upload_session["uploadUrl"]
                # FileSize
                # st = os.stat(full_file_path)
                # size = st.st_size
                # 10mb
                # CHUNK_SIZE = 10485760
                # 3mb
                CHUNK_SIZE = 3145728
                chunks = int(size / CHUNK_SIZE) + 1 if size % CHUNK_SIZE > 0 else 0
                with open(full_file_path, "rb") as fd:
                    start = 0
                    for chunk_num in range(chunks):
                        chunk = fd.read(CHUNK_SIZE)
                        bytes_read = len(chunk)
                        upload_range = f"bytes {start}-{start + bytes_read - 1}/{size}"
                        print(
                            f"chunk: {chunk_num} bytes read: {bytes_read} upload range: {upload_range}"
                        )
                        result = requests.put(
                            upload_session_url,
                            headers={
                                "Content-Length": str(bytes_read),
                                "Content-Range": upload_range,
                            },
                            data=chunk,
                        )
                        result.raise_for_status()
                        start += bytes_read
                if size > start:
                    return False
                else:
                    return True
            else:
                # Read File
                with open(full_file_path, "rb") as fi:
                    encoded = base64.encodebytes(fi.read()).decode("utf-8")
                    # fi_bytes_read = fi.read()

                email_data = {
                    "@odata.type": "#microsoft.graph.fileAttachment",
                    "name": file_name,
                    "contentBytes": str(encoded),
                }
                json_email_data = json.dumps(email_data)
                # Upload
                request_url = self.graph_api_endpoint.format(
                    "/v1.0/me/messages/" + email_message_id + "/attachments"
                )
                self.headers["Content-Type"] = "application/json"
                response = requests.post(
                    url=request_url, headers=self.headers, data=json_email_data
                )
                response.raise_for_status()
                return True
        except Exception as ex:
            raise ex

    def send_email_message_from_draft(self, 
                                      email_message_id: str):
        try:
            email_message_id = email_message_id.strip()

            request_url = self.graph_api_endpoint.format(
                "/v1.0/me/messages/" + email_message_id + "/send"
            )
            response = requests.post(url=request_url, headers=self.headers)
            response.raise_for_status()
            return response.status_code
        except Exception as ex:
            raise ex

    def list_email_folders(self):
        try:
            request_url = self.graph_api_endpoint.format(
                "/v1.0/me/mailFolders?$top=1000&$select=id,displayName"
            )
            response = requests.get(url=request_url, headers=self.headers)
            json_data = response.json()
            response.raise_for_status()
            return json_data["value"]
        except Exception as ex:
            raise ex

    def list_folder_messages(self, email_folder_id: str, email_filter=""):
        email_folder_id = email_folder_id.strip()
        email_filter = email_filter.strip()
        try:
            request_url = self.graph_api_endpoint.format(
                "/v1.0/me/mailFolders/" + email_folder_id + "/messages" + email_filter
            )
            response = requests.get(url=request_url, headers=self.headers)
            response.raise_for_status()
            json_data = json.loads(response.content)
            return json_data["value"]
        except Exception as ex:
            raise ex
        
    def get_mime_email_by_id(self, 
                             email_id:str):
        email_id = email_id.strip()
        try:
            request_url = self.graph_api_endpoint.format('/v1.0/me/messages/' + email_id + '/$value')
            response = requests.get(url = request_url, headers = self.headers)
            if(response.status_code==200 or response.status_code==201 or response.status_code==202):
                return response.content
            else:
                raise Exception('GetMimeEmailbyId: Error getting the content response '+str(response.status_code))
        except Exception as ex:
            raise ex

    def get_email_with_attachments(self, 
                                   folder_name: str):
        try:
            # MsGraph
            content_type = "application/json"
            email_filter = "?$select=id,receivedDateTime,sentDateTime,hasAttachments,subject,conversationId,isRead"
            # Attachments
            email_folders = self.list_email_folders()
            folders_list = filter(
                lambda item: item.get("displayName").strip().lower()
                == folder_name.strip().lower(),
                email_folders,
            )
            email_folder_id = str(list(folders_list)[0].get("id").strip())
            emails_list = self.list_folder_messages(email_folder_id, email_filter)
        except Exception as ex:
            raise ex
        return True
