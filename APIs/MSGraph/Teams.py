import requests, json, re

from . import MSGraph, MSGraphError
from Emerson.variables import LOGGER

class Teams(MSGraph):
    def __init__(self, *args, **kwargs):
        self.domain = kwargs.pop("domain", "emerson")
        MSGraph.__init__(self, *args, **kwargs)

    def create_one_to_one_chat(self, 
                               email_first_id: str, 
                               email_second_id: str) -> str:
        try:
            #inputs
            email_first_id = email_first_id.strip()
            email_second_id = email_second_id.strip()
            #Validate
            if not (bool(email_first_id) or bool(email_second_id)):
                raise Exception('CreateOnetoOneChat: Action allows just two email users')
            #request
            request_url = self.graph_api_endpoint.format('/v1.0/chats')
            email_data = {
                "chatType": "oneOnOne",
                "members": [
                    {
                        "@odata.type": "#microsoft.graph.aadUserConversationMember",
                        "roles": [
                            "owner"
                        ],
                        "user@odata.bind": "https://graph.microsoft.com/v1.0/users('"+email_first_id+"')"
                    },
                    {
                        "@odata.type": "#microsoft.graph.aadUserConversationMember",
                        "roles": [
                            "owner"
                        ],
                        "user@odata.bind": "https://graph.microsoft.com/v1.0/users('"+email_second_id+"')"
                    }
                ]
            }
            json_email_data=json.dumps(email_data)
            response = requests.post(url = request_url, headers = self.headers, data=json_email_data)
            json_data = json.loads(response.content)
            return str(json_data['id'])
        except Exception as ex:
            raise ex

    def get_email_user_id(self, 
                          user_email:str) -> str:
        try:
            user_email = user_email.strip()
            #
            request_url = self.graph_api_endpoint.format("/v1.0/users?$filter=mail eq '" + user_email + "'")
            response = requests.get(url = request_url, headers = self.headers)
            json_data = json.loads(response.content)
            return str(json_data['value'][0]['id'])
        except Exception as ex:
            raise ex
    
    def post_chat_message(self, 
                          chat_id: str, 
                          chat_message: str) -> str:
        try:
            request_url = self.graph_api_endpoint.format('/v1.0/me/chats/' + chat_id + '/messages')
            email_data = {
                "body": {
                    "contentType": "html",
                    "content": chat_message
                }
            }
            json_email_data=json.dumps(email_data)
            response = requests.post(url = request_url, headers = self.headers, data=json_email_data)
            json_data = json.loads(response.content)
            if not response.status_code == 201 or response.status_code == 202 or response.status_code == 200:
                raise Exception("postChatMessage: chat message cannot be posted " + response.status_code)
            return str(json_data['id'])
        except Exception as ex:
            raise ex
    
    def create_group_chat(self, 
                          email_contacts_ids: str) -> str:
        try:
            #inputs
            email_contacts_ids = email_contacts_ids.strip()
            #Validate
            if not (bool(email_contacts_ids)):
                raise Exception('CreateOnetoOneChat: Action allows just two email users')
            #request
            request_url = self.graph_api_endpoint.format('/v1.0/chats')
            email_data = {
                "chatType": "group",
                "topic": "Group chat",
                "members": []
            }
            list_emails_ids = re.split(';', email_contacts_ids)
            if not len(list_emails_ids)>2:
                raise Exception("createGroupChat: To create a group chat at least 3 emails are required")
            email_data["members"] = [{"@odata.type": "#microsoft.graph.aadUserConversationMember","roles": ["owner"],"user@odata.bind": "https://graph.microsoft.com/v1.0/users('" + add + "')"} for add in list_emails_ids]
            json_email_data=json.dumps(email_data)
            response = requests.post(url = request_url, headers = self.headers, data=json_email_data)
            json_data = json.loads(response.content)
            return str(json_data['id'])
        except Exception as ex:
            raise ex

    def get_joined_teams(self) -> list:
        try:
            #
            request_url = self.graph_api_endpoint.format("/v1.0/me/joinedTeams?$select=id,displayName")
            response = requests.get(url = request_url, headers = self.headers)
            json_data = json.loads(response.content)
            return json_data['value']
        except Exception as ex:
            raise ex
        
    def get_team_channels(self,
                          team_id: str) -> list:
        try:
            team_id = team_id.strip()
            #
            request_url = self.graph_api_endpoint.format("/v1.0/teams/" + team_id + "/channels?$select=id,displayName")
            response = requests.get(url = request_url, headers = self.headers)
            json_data = json.loads(response.content)
            return json_data['value']
        except Exception as ex:
            raise ex

    def post_channel_message(self, 
                             team_id: str, 
                             team_channel_id: str, 
                             chat_message: str) -> str: 
        try:
            request_url = self.graph_api_endpoint.format('/v1.0/teams/' + team_id + '/channels/' + team_channel_id + '/messages')
            email_data = {
                "body": {
                    "contentType": "html",
                    "content": chat_message
                }
            }
            json_email_data=json.dumps(email_data)
            response = requests.post(url = request_url, headers = self.headers, data=json_email_data)
            json_data = json.loads(response.content)
            if not response.status_code == 201 or response.status_code == 202 or response.status_code == 200:
                raise Exception("postChatMessage: chat message cannot be posted "+response.status_code)
            return str(json_data['id'])
        except Exception as ex:
            raise ex