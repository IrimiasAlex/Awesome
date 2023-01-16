import os

from Emerson.GeneralActions import GeneralActions
from .Sharepoint import Sharepoint
from .Utilities import Utilities
from RPA.HTTP import HTTP

class SharepointActions(Sharepoint):
    def __init__(self, *args, **kwargs):
        Sharepoint.__init__(self, *args, **kwargs)
        self.http = HTTP()
        
    def core_ms_graph_upload_file_to_sharepoint_library(self, sharepoint_url: str, sub_folder_path: str, full_file_path: str, file_name_with_ext: str):
        upload_status = False
        try:
            #Inputs
            sharepoint_url = sharepoint_url.strip()
            sub_folder_path = sub_folder_path.strip()
            full_file_path = full_file_path.strip()
            #MsGraph
            sharepoint_path_dict = Utilities.get_sharepoint_path_by_url(sharepoint_url)
            sharepoint_path = sharepoint_path_dict.get("sharepoint_path")
            sharepoint_site_id = self.get_sharepoint_site_id(sharepoint_path)
            sharepoint_site_drives = self.get_sharepoint_site_drives(sharepoint_site_id)
            sharepoint_drive_id = Utilities.get_sharepoint_drive_id_by_url(sharepoint_url, sharepoint_site_drives)

            sharepoint_file_location = Utilities.build_sharepoint_sub_folder_path_and_file(sub_folder_path, file_name_with_ext)
            sharepoint_file_status = self.verify_file_exist_sharepoint_drive(sharepoint_site_id, sharepoint_drive_id, sharepoint_file_location)
            #File exist already?
            os.path.getsize(full_file_path)
            if sharepoint_file_status["status_code"] == 200 and os.path.getsize(full_file_path)< 3145728:
                #overwrite if exist <4mb
                self.update_file_content_sharepoint_drive(sharepoint_site_id, sharepoint_drive_id, sharepoint_file_status["id"], full_file_path)
            elif sharepoint_file_status["status_code"] == 200 and os.path.getsize(full_file_path)> 3145728:
                self.create_large_file_content_sharepoint_drive(sharepoint_site_id, sharepoint_drive_id, sharepoint_file_status["id"], full_file_path, file_name_with_ext)
            elif sharepoint_file_status["status_code"] != 200 and os.path.getsize(full_file_path)< 3145728:
                #create if new <4mb
                self.create_small_file_content_sharepoint_drive(sharepoint_site_id, sharepoint_drive_id, sharepoint_file_location, full_file_path)
            else:
                seedid = self.create_seed_file_content_sharepoint_drive(sharepoint_site_id, sharepoint_drive_id, sharepoint_file_location, full_file_path)
                self.create_large_file_content_sharepoint_drive(sharepoint_site_id, sharepoint_drive_id, seedid, full_file_path, file_name_with_ext)
            upload_status = True
        except Exception as ex:
            raise ex
        return upload_status
    
    def create_item_in_list(self, sharepoint_url: str, 
                            list_name: str, 
                            items: dict):
            upload_status = False
            try:
                #Inputs
                sharepoint_url = sharepoint_url.strip()
                #MsGraph
                sharepoint_path_dict = Utilities.get_sharepoint_path_by_url(sharepoint_url)
                sharepoint_path = sharepoint_path_dict.get("sharepoint_path")
                sharepoint_site_id = self.get_sharepoint_site_id(sharepoint_path)
                sharepoint_lists = self.get_sharepoint_lists(sharepoint_site_id)
                sharepoint_list_id = Utilities.get_list_id_from_lists(sharepoint_lists, list_name)
                #File exist already?
                json_data = self.create_item_in_sharepoint_list(sharepoint_site_id, sharepoint_list_id, items)
            except Exception as ex:
                raise ex
            return json_data
        
    def core_ms_graph_get_file_name(self, sharepoint_url: str, sub_folder_path: str,):
        excel_tables_data = {}
        try:
            #Validations
            if(sharepoint_url is not None and sharepoint_url != "" and sub_folder_path is not None  and sub_folder_path != "" ):
                sharepoint_url = sharepoint_url.strip()
                sub_folder_path = sub_folder_path.strip()
                #MsGraph
                sharepoint_path_dict = Utilities.get_sharepoint_path_by_url(sharepoint_url)
                sharepoint_path = sharepoint_path_dict.get("sharepoint_path")
                sharepoint_site_id = self.get_sharepoint_site_id(sharepoint_path)
                sharepoint_site_drives = self.get_sharepoint_site_drives(sharepoint_site_id)
                sharepoint_drive_id = Utilities.get_sharepoint_drive_id_by_url(sharepoint_url, sharepoint_site_drives)
                sub_folder_path = Utilities.fix_sharepoint_sub_folder_path(sub_folder_path)
                sharepoint_files_from_drive = self.get_sharepoint_files_from_drive(sharepoint_site_id, sharepoint_drive_id, sub_folder_path)
                #sharepoint_file_id = Utilities.get_file_id_from_drive_list_by_file_name(sharepoint_files_from_drive, file_name_with_ext)
                file_name = Utilities.get_name_from_folder(sharepoint_files_from_drive)
            else:
                raise Exception("The Sharepoint url, subfolder path, file name with extension and the table names list given cannot be empty")
        except Exception as ex:
            raise ex
        return file_name
    
    def update_item_in_list(self, sharepoint_url: str, 
                            list_name: str, 
                            items: dict,
                            item_id: str):
            upload_status = False
            try:
                #Inputs
                sharepoint_url = sharepoint_url.strip()
                item_id = item_id.strip()
                #MsGraph
                sharepoint_path_dict = Utilities.get_sharepoint_path_by_url(sharepoint_url)
                sharepoint_path = sharepoint_path_dict.get("sharepoint_path")
                sharepoint_site_id = self.get_sharepoint_site_id(sharepoint_path)
                sharepoint_lists = self.get_sharepoint_lists(sharepoint_site_id)
                sharepoint_list_id = Utilities.get_list_id_from_lists(sharepoint_lists, list_name)
                #File exist already?
                json_data = self.update_item_in_sharepoint_list(sharepoint_site_id, sharepoint_list_id, items, item_id)
            except Exception as ex:
                raise ex
            return json_data
        
    def core_ms_graph_download_file(self, 
                                    sharepoint_url: str,
                                    sub_folder_path: str,
                                    file_name_with_ext: str,
                                    destination_local_folder_path: str) -> None:
        try:
            #Validations
            if(sharepoint_url is not None and sharepoint_url != "" and file_name_with_ext is not None and file_name_with_ext != ""):
                sharepoint_url = sharepoint_url.strip()
                file_name_with_ext = file_name_with_ext.strip()
                destination_local_folder_path = destination_local_folder_path.strip()
                #MsGraph
                sharepoint_path_dict = Utilities.get_sharepoint_path_by_url(sharepoint_url)
                sharepoint_path = sharepoint_path_dict.get("sharepoint_path")
                sharepoint_site_id = self.get_sharepoint_site_id(sharepoint_path)
                sharepoint_site_drives = self.get_sharepoint_site_drives(sharepoint_site_id)
                sharepoint_drive_id = Utilities.get_sharepoint_drive_id_by_url(sharepoint_url, 
                                                                               sharepoint_site_drives)
                sub_folder_path = Utilities.fix_sharepoint_sub_folder_path(sub_folder_path)
                sharepoint_files_from_drive = self.get_sharepoint_files_from_drive(sharepoint_site_id, 
                                                                                   sharepoint_drive_id, 
                                                                                   sub_folder_path)
                try:
                    file_data = GeneralActions.filter_dictionary_list_equal_to_no_case_sensitive(sharepoint_files_from_drive,
                                                                                                 "name",
                                                                                                 file_name_with_ext)
                    url_to_download = file_data[0].get("@microsoft.graph.downloadUrl")
                except Exception as exception:
                    raise Exception(f"Could not find the file: '{file_name_with_ext}' in the given Sharepoint")
                local_file_path = f"{destination_local_folder_path}//{file_name_with_ext}"
                donwload_result = self.http.download(url=url_to_download,
                                                     target_file=local_file_path, 
                                                     overwrite=True)
                if "200" not in str(donwload_result).strip().lower():
                    raise Exception(f"The file: '{file_name_with_ext}' cannot be downloaded in this path: '{destination_local_folder_path}'")
            else:
                raise Exception("The Sharepoint url, subfolder path, file name with extension and the table names list given cannot be empty, update row works one by one")
        except Exception as ex:
            raise ex
    
    def get_data_from_sharepoint_list(self, 
                                      sharepoint_url: str, 
                                      list_name: str, 
                                      first_filter=None, 
                                      first_value=None, 
                                      second_filter=None, 
                                      second_value=None):
            try:
                #Inputs
                sharepoint_url = sharepoint_url.strip()
                list_name = list_name.strip()
                #MsGraph
                sharepoint_path_dict = Utilities.get_sharepoint_path_by_url(sharepoint_url)
                sharepoint_path = sharepoint_path_dict.get("sharepoint_path")
                sharepoint_site_id = self.get_sharepoint_site_id(sharepoint_path)
                sharepoint_lists = self.get_sharepoint_lists(sharepoint_site_id)
                sharepoint_list_id = Utilities.get_list_id_from_lists(sharepoint_lists, list_name)
                #File exist already?
                json_data = self.get_data_from_sharepoint_list_item(sharepoint_site_id, sharepoint_list_id)
                json_data = Utilities.select_column_list_of_dict(json_data, 'fields')
                json_data = Utilities.get_values_from_dict(json_data, 'fields')
                if bool(first_value)>0 or bool(first_filter)>0:
                    json_data = GeneralActions.filter_dictionary_list_equal_to_no_case_sensitive(json_data, 
                                                                                                 first_filter, 
                                                                                                 first_value, 
                                                                                                 second_filter,
                                                                                                 second_value)
            except Exception as ex:
                raise ex
            return json_data
        
    def move_file_from_sharepoint_folder_to_new_sharepoint_folder(self, sharepoint_url: str, sub_folder_path: str, 
                                                                 file_name_with_ext: str, main_folder_name: str, new_sub_folder_name: str):
        try:
            #Validations
            if(sharepoint_url is not None and sharepoint_url != "" and sub_folder_path is not None  and sub_folder_path != "" and  file_name_with_ext is not None  and file_name_with_ext != ""
               and  main_folder_name is not None  and main_folder_name != "" and  new_sub_folder_name is not None  and new_sub_folder_name != ""):
                sharepoint_url = sharepoint_url.strip()
                sub_folder_path = sub_folder_path.strip()
                file_name_with_ext = file_name_with_ext.strip()
                #MsGraph
                sharepoint_path_dict = Utilities.get_sharepoint_path_by_url(sharepoint_url)
                sharepoint_path = sharepoint_path_dict.get("sharepoint_path")
                sharepoint_site_id = self.get_sharepoint_site_id(sharepoint_path)
                sharepoint_site_drives = self.get_sharepoint_site_drives(sharepoint_site_id)
                sharepoint_drive_id = Utilities.get_sharepoint_drive_id_by_url(sharepoint_url, sharepoint_site_drives)
                sub_folder_path = Utilities.fix_sharepoint_sub_folder_path(sub_folder_path)
                sharepoint_files_from_drive = self.get_sharepoint_files_from_drive(sharepoint_site_id, sharepoint_drive_id, sub_folder_path)
                file_id = Utilities.get_file_id_from_drive_list_by_file_name(sharepoint_files_from_drive, file_name_with_ext)
                
                #Get ID New Folder
                main_folder_name = Utilities.fix_sharepoint_sub_folder_path(main_folder_name)
                list_folder = self.get_sharepoint_files_from_drive(sharepoint_site_id, sharepoint_drive_id, main_folder_name)
                folder_id = Utilities.get_file_id_from_drive_list_by_file_name(list_folder, new_sub_folder_name)
                
                new_data_json = {
                    "parentReference": {
                        "id" : folder_id 
                    },
                    "name": file_name_with_ext,
                    "@microsoft.graph.conflictBehavior": "replace"
                }
                
                self.move_file_from_sharepoint_folder(sharepoint_site_id, sharepoint_drive_id, file_id, new_data_json)
            else:
                raise Exception("The Sharepoint url, subfolder path, file name with extension list given cannot be empty")
        except Exception as ex:
            raise ex
        
    def get_data_from_sharepoint_list_item_not_equal(self, 
                                                     sharepoint_url: str, 
                                                     list_name: str, 
                                                     first_filter=None, 
                                                     first_value=None, 
                                                     second_filter=None, 
                                                     second_value=None):
            try:
                #Inputs
                sharepoint_url = sharepoint_url.strip()
                list_name = list_name.strip()
                #MsGraph
                sharepoint_path_dict = Utilities.get_sharepoint_path_by_url(sharepoint_url)
                sharepoint_path = sharepoint_path_dict.get("sharepoint_path")
                sharepoint_site_id = self.get_sharepoint_site_id(sharepoint_path)
                sharepoint_lists = self.get_sharepoint_lists(sharepoint_site_id)
                sharepoint_list_id = Utilities.get_list_id_from_lists(sharepoint_lists, list_name)
                #File exist already?
                json_data = self.get_data_from_sharepoint_list_item(sharepoint_site_id, sharepoint_list_id)
                json_data = Utilities.select_column_list_of_dict(json_data, 'fields')
                json_data = Utilities.get_values_from_dict(json_data, 'fields')
                if bool(first_value) > 0 or bool(first_filter) > 0:
                    json_data = GeneralActions.filter_dictionary_list_no_case_sensitive(json_data, 
                                                                                        first_filter, 
                                                                                        first_value, 
                                                                                        second_filter,
                                                                                        second_value)
            except Exception as ex:
                raise ex
            return json_data

    def core_ms_graph_get_user_information_list(self, 
                                                sharepoint_url: str, 
                                                list_name: str) -> list:
        user_information_list = []
        try:
            #Inputs
            if bool(sharepoint_url) and bool(list_name):
                sharepoint_url = sharepoint_url.strip()
                list_name = list_name.strip()
                #MsGraph
                sharepoint_path_dict = Utilities.get_sharepoint_path_by_url(sharepoint_url)
                sharepoint_path = sharepoint_path_dict.get("sharepoint_path")
                sharepoint_site_id = self.get_sharepoint_site_id(sharepoint_path)
                sharepoint_list_id = self.get_sharepoint_list_by_display_name(sharepoint_site_id,
                                                                              list_name)[0]["id"]
                user_information_list = self.get_sharepoint_users_list(sharepoint_site_id,
                                                                    sharepoint_list_id)
            else:
                raise Exception("The values for the fields 'Sharepoint URL' and List 'Name' given cannot be empty")
        except Exception as ex:
            raise ex
        return user_information_list
    
    def core_ms_graph_get_data_from_sharepoint_library(self,
                                                       sharepoint_url: str,
                                                       sub_folder_path: str) -> tuple:
        try:
            #Validations
            if(sharepoint_url is not None and sharepoint_url != "" and sub_folder_path is not None and sub_folder_path != ""):
                sharepoint_url = sharepoint_url.strip()
                sub_folder_path = sub_folder_path.strip()
                #MsGraph
                sharepoint_path_dict = Utilities.get_sharepoint_path_by_url(sharepoint_url)
                sharepoint_path = sharepoint_path_dict.get("sharepoint_path")
                sharepoint_site_id = self.get_sharepoint_site_id(sharepoint_path)
                sharepoint_site_drives = self.get_sharepoint_site_drives(sharepoint_site_id)
                sharepoint_drive_id = Utilities.get_sharepoint_drive_id_by_url(sharepoint_url, 
                                                                               sharepoint_site_drives)
                sub_folder_path = Utilities.fix_sharepoint_sub_folder_path(sub_folder_path)
                json_data = self.get_data_from_sharepoint_library(sharepoint_site_id, 
                                                                  sharepoint_drive_id,
                                                                  sub_folder_path)
                json_data_list_items = Utilities.select_column_list_of_dict(json_data, 'listItem')
                json_data_list_items = Utilities.get_values_from_dict(json_data_list_items, 'listItem')
                json_data_fields = Utilities.select_column_list_of_dict(json_data_list_items, 'fields')
        except Exception as ex:
            raise ex
        return json_data, json_data_fields

    def core_ms_graph_update_sharepoint_document_library_item(self, 
                                                              sharepoint_url: str,
                                                              items: dict,
                                                              item_id: str) -> dict:
        try:
            #Inputs
            sharepoint_url = sharepoint_url.strip()
            item_id = item_id.strip()
            #MsGraph
            sharepoint_path_dict = Utilities.get_sharepoint_path_by_url(sharepoint_url)
            sharepoint_path = sharepoint_path_dict.get("sharepoint_path")
            sharepoint_site_id = self.get_sharepoint_site_id(sharepoint_path)
            sharepoint_site_drives = self.get_sharepoint_site_drives(sharepoint_site_id)
            sharepoint_drive_id = Utilities.get_sharepoint_drive_id_by_url(sharepoint_url, sharepoint_site_drives)
            json_data = self.update_sharepoint_library_data(sharepoint_site_id, sharepoint_drive_id, item_id, items)
        except Exception as ex:
            raise ex
        return json_data

    def core_ms_graph_get_sharepoint_file_id(self, 
                                             sharepoint_url: str, 
                                             sub_folder_path: str, 
                                             file_name_with_ext: str) -> str:
        try:
            #Validations
            if(sharepoint_url is not None and sharepoint_url != "" and sub_folder_path is not None  and sub_folder_path != "" and file_name_with_ext is not None and file_name_with_ext != ""):
                sharepoint_url = sharepoint_url.strip()
                sub_folder_path = sub_folder_path.strip()
                file_name_with_ext = file_name_with_ext.strip()
                #MsGraph
                sharepoint_path_dict = Utilities.get_sharepoint_path_by_url(sharepoint_url)
                sharepointPath = sharepoint_path_dict.get("sharepointPath")
                if bool(sharepointPath) == False:
                    sharepointPath = sharepoint_path_dict.get("sharepoint_path")
                sharepoint_site_id = self.get_sharepoint_site_id(sharepointPath)
                sharepoint_site_drives = self.get_sharepoint_site_drives(sharepoint_site_id)
                sharepoint_drive_id = Utilities.get_sharepoint_drive_id_by_url(sharepoint_url, sharepoint_site_drives)
                sub_folder_path = Utilities.fix_sharepoint_sub_folder_path(sub_folder_path)
                sharepoint_files_from_drive = self.get_sharepoint_files_from_drive(sharepoint_site_id, sharepoint_drive_id, sub_folder_path)
                sharepoint_file_id = Utilities.get_file_id_from_drive_list_by_file_name(sharepoint_files_from_drive, file_name_with_ext)
            else:
                raise Exception("The Sharepoint url, subfolder path, file name with extension given cannot be empty")
        except Exception as ex:
            raise ex
        return sharepoint_file_id