import re, os, time

from Emerson.MSGraph.Utilities import Utilities

from .Email import Email

class EmailActions(Email):
    def __init__(self, *args, **kwargs):
        Email.__init__(self, *args, **kwargs)
        
    def core_ms_graph_send_email(self, 
                                 email_subject: str, 
                                 email_body: str, 
                                 email_to: str, 
                                 email_cc = "", 
                                 email_bcc = "", 
                                 email_attachments = ""):
        try:
            #Inputs
            email_subject = email_subject.strip()
            email_body = email_body.strip()
            email_to = email_to.strip()
            #Attachments
            if bool(email_attachments):
                email_attachments = email_attachments.strip()
                #Draft
                email_id = self.create_draft_email(email_subject, email_body, email_to, email_cc, email_bcc)
                listAttachments = re.split(';', email_attachments)
                for attachment in listAttachments:
                    time.sleep(2)
                    fileName = os.path.basename(attachment)
                    self.add_file_content_email_message(email_id, attachment, fileName)
                result_sent = self.send_email_message_from_draft(email_id)
            else:
                email_id = self.create_draft_email(email_subject, email_body, email_to, email_cc, email_bcc)
                result_sent = self.send_email_message_from_draft(email_id)
            if result_sent != 202:
                raise Exception('Email cannot be sent, please check the draft folder')
        except Exception as ex:
            raise ex
        return True
    
    def core_ms_graph_get_email_with_attachments(self, folder_name: str):
        try:
            #MsGraph
            email_filter = '?$select=id,receivedDateTime,sentDateTime,hasAttachments,subject,conversationId,isRead'
            #Attachments
            email_folders = self.list_email_folders()
            folders_list = filter(lambda item: item.get("displayName").strip().lower() ==  folder_name.strip().lower(), email_folders)
            email_folder_id = str(list(folders_list)[0].get("id").strip())
            self.list_folder_messages(email_folder_id, email_filter)
        except Exception as ex:
            raise ex
        return True
    
    def core_ms_graph_download_email(self,
                                     email_subject: str, 
                                     email_folder:str,
                                     email_location:str,
                                     email_filter=None):
        try:
            #Inputs
            email_subject = email_subject.strip()
            email_folder = email_folder.strip()
            email_location = email_location.strip()
            #Attachments
            email_folder_list = self.list_email_folders()
            if bool(email_folder_list)>0:
                email_folder_id = Utilities.get_email_folder_id(email_folder_list,
                                                                email_folder)
                if(bool(email_subject)>0):
                    email_result_list = self.list_folder_messages(email_folder_id, 
                                                                "?$filter=contains(subject, '" + email_subject + "')")
                    if(bool(email_result_list) > 0):
                        counter_email = 0
                        for item in email_result_list:
                            email_mime_content = self.get_mime_email_by_id(str(item['id']))
                            if counter_email == 0:
                                f = open(email_location, "wb")
                                f.write(email_mime_content)
                                f.close()
                                counter_email+=1
                            else:
                                split_path = os.path.splitext(email_location)
                                new_file_name=str(split_path[0])+str(counter_email)+str(split_path[1])
                                f = open(new_file_name, "wb")
                                f.write(email_mime_content)
                                f.close()
                                counter_email+=1
                    else:
                        raise Exception('CoreMSGraphDownloadEmail: The filter for downloading emails did not find any results.')
                else:
                    raise Exception('CoreMSGraphDownloadEmail: Email folder id cannot be found')
            else:
                raise Exception('CoreMSGraphDownloadEmail: Missing email folders, please check the account')
        except Exception as ex:
            raise ex
        return True