import re

from .Teams import Teams
from .Utilities import Utilities

class TeamsActions(Teams):
    def __init__(self, *args, **kwargs):
        Teams.__init__(self, *args, **kwargs)
    
    def core_ms_graph_send_chat_one_to_one_message(self,
                                                   chat_message: str, 
                                                   chat_contacts: str) -> bool:
        try:
            #Inputs
            chat_message = chat_message.strip()
            chat_contacts = chat_contacts.strip()
            #Attachments
            if bool(chat_message) or bool(chat_contacts):
                #Get Ids
                list_contacts = re.split(';', chat_contacts)
                if not len(list_contacts)==2:
                    raise Exception('coreMSGraphSendChatMessage: two contacts are necesary to send the teams message')
                first_user_id = self.get_email_user_id(list_contacts[0])
                second_user_id = self.get_email_user_id(list_contacts[1])
                chat_id = self.create_one_to_one_chat(first_user_id,
                                                      second_user_id)
                result = self.post_chat_message(chat_id, 
                                                chat_message)
            else:
                raise Exception('coreMSGraphSendChatMessage: inputs cannot be empty values')
            if not bool(result):
                raise Exception('coreMSGraphSendChatMessage: teams message cannot be posted')
        except Exception as ex:
            raise ex
        return True
    
    def core_ms_graph_send_chat_group_message(self,
                                              chat_message: str, 
                                              chat_contacts: str) -> bool:
        try:
            list_user_ids=""
            #Inputs
            chat_message = chat_message.strip()
            chat_contacts = chat_contacts.strip()
            #Attachments
            if bool(chat_message) or bool(chat_contacts):
                #Get Ids
                list_contacts = re.split(';', chat_contacts)
                if not len(list_contacts)>2:
                    raise Exception('coreMSGraphSendChatMessage: 3 contacts are necesary to send the teams message')
                counter_items = 0
                for item in list_contacts:
                    temp_user_id = str(self.get_email_user_id(item))
                    if counter_items == len(list_contacts)-1:
                        list_user_ids = list_user_ids + temp_user_id
                    elif len(list_user_ids)>0:
                        list_user_ids = list_user_ids + temp_user_id + ";"
                    elif len(temp_user_id)==0:
                        list_user_ids = list_user_ids
                    else:
                        list_user_ids = temp_user_id + ";"
                    counter_items += 1
                chat_id = self.create_group_chat(list_user_ids)
                result = self.post_chat_message(chat_id,
                                                chat_message)
            else:
                raise Exception('coreMSGraphSendChatMessage: missing informamation message or contacts')
            if not bool(result):
                raise Exception('coreMSGraphSendChatMessage: teams message cannot be posted')
        except Exception as ex:
            raise ex
        return True
    
    def core_ms_graph_send_message_to_teams_channel(self,
                                                    chat_message: str, 
                                                    team_name: str, 
                                                    team_channel_name: str) -> bool:
        try:
            #Inputs
            chat_message = chat_message.strip()
            team_name = team_name.strip()
            team_channel_name = team_channel_name.strip()
            #Attachments
            if bool(chat_message) and bool(team_name) and bool(team_channel_name):
                #Get Ids
                temp_teams_joined = self.get_joined_teams()
                team_id = Utilities.filter_result_by_column(team_name,
                                                           "displayName",
                                                           temp_teams_joined,
                                                           "id")
                temp_teams_channels = self.get_team_channels(team_id)
                team_channel_id = Utilities.filter_result_by_column(team_channel_name,
                                                                  "displayName",
                                                                  temp_teams_channels,
                                                                  "id")
                result = self.post_channel_message(team_id,
                                                   team_channel_id, 
                                                   chat_message)
            else:
                raise Exception('coreMSGraphSendMessageToTeamsChannel: missing informamation message or contacts')
            if not bool(result):
                raise Exception('coreMSGraphSendMessageToTeamsChannel: teams message cannot be posted')
        except Exception as ex:
            raise ex
        return True