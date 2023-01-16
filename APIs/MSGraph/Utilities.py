import re

class Utilities():
    
    @staticmethod
    def get_sharepoint_path_by_url(sharepoint_url: str):
        result = None
        try:
            sharepoint_url = sharepoint_url.strip()
            sharepoint_domain_regex = r"^((http|https|ftp):\/\/)?([^:\/\n]+)"
            sharepoint_path_regex = r"^(.+?)[a-zA-Z0-9](\/Lists\/|\/Shared%|\/Forms\/)"
            sharepoint_forms_regex = r"\/([^\/]+)\/?$"
            sharepoint_path_position = 7
            if(sharepoint_url is not None):
                sharepoint_domain = re.match(sharepoint_domain_regex, sharepoint_url).group(0)
                sharepoint_url = sharepoint_url.replace(sharepoint_domain, "")
                if(sharepoint_url.lower().__contains__("/shared%")):
                    sharepoint_path_position = 8
                sharepoint_path = re.match(sharepoint_path_regex, sharepoint_url).group(0)
                sharepoint_path = sharepoint_path[:-sharepoint_path_position]
                if(sharepoint_url.lower().__contains__("/forms/") and sharepoint_path_position != 8):
                    sharepoint_path_last_word = re.search(sharepoint_forms_regex, sharepoint_path, re.MULTILINE).group(0)
                    sharepoint_path = sharepoint_path.replace(sharepoint_path_last_word, "").strip()
                result = {
                    "sharepoint_domain" : sharepoint_domain,
                    "sharepoint_path" : sharepoint_path,
                    "sharepoint_full_path" : sharepoint_domain + sharepoint_path
                }
            else:
                raise Exception("The Sharepoint URL given cannot be empty")
        except Exception as ex:
            raise ex
        return result
    
    @staticmethod
    def get_sharepoint_drive_id_by_url(sharepoint_url: str, sharepoint_drives_list: list):
        sharepoint_drive_id = ""
        try:
            sharepoint_url = sharepoint_url.strip()
            sharepoint_drive_name_regex = r"^(.+?)(\/Forms\/)"
            sharepoint_drive_name_position = 7
            if(sharepoint_url is not None and len(sharepoint_drives_list) > 0):
                sharepoint_drive_name = re.match(sharepoint_drive_name_regex, sharepoint_url).group(0)
                sharepoint_drive_name_fixed = sharepoint_drive_name[:-sharepoint_drive_name_position]
                sharepoint_drive = filter(lambda sharepoint_drive: sharepoint_drive.get("webUrl").strip().lower() ==  sharepoint_drive_name_fixed.strip().lower(), sharepoint_drives_list)
                sharepoint_drive_id = list(sharepoint_drive)[0].get("id").strip()
            else:
                raise Exception("The Sharepoint URL and Sharepoint drives list given cannot be empty")
        except Exception as ex:
            raise ex
        return sharepoint_drive_id
    
    @staticmethod
    def fix_sharepoint_sub_folder_path(sharepoint_sub_folder_path: str):
        sharepoint_sub_folder_path_fixed = ""
        try:
            sharepoint_sub_folder_path = sharepoint_sub_folder_path.strip()
            if(sharepoint_sub_folder_path is None or sharepoint_sub_folder_path.strip() == ""):
                sharepoint_sub_folder_path_fixed = r"root/children"
            else:
                sharepoint_sub_folder_path_fixed = r"root:/" + sharepoint_sub_folder_path + ":/Children"
        except Exception as ex:
            raise ex
        return sharepoint_sub_folder_path_fixed
    
    @staticmethod
    def build_sharepoint_sub_folder_path_and_file(sharepoint_sub_folder_path: str, file_name_with_ext: str):
        sharepoint_sub_folder_path_fixed = ""
        try:
            sharepoint_sub_folder_path = sharepoint_sub_folder_path.strip()
            if(sharepoint_sub_folder_path is None or sharepoint_sub_folder_path.strip() == ""):
                sharepoint_sub_folder_path_fixed = r"root:/"+file_name_with_ext
            else:
                sharepoint_sub_folder_path_fixed = r"root:/" + sharepoint_sub_folder_path + "/"+file_name_with_ext
        except Exception as ex:
            raise ex
        return sharepoint_sub_folder_path_fixed
    
    @staticmethod
    def get_file_id_from_drive_list_by_file_name(sharepoint_files_from_drive: list, file_name_with_ext: str):
        drive_file_id = ""
        try:
            file_name_with_ext = file_name_with_ext.strip()
            if(file_name_with_ext is not None or len(sharepoint_files_from_drive) > 0):
                drive_file = filter(lambda file: file.get("name").strip().lower() ==  file_name_with_ext.strip().lower(), sharepoint_files_from_drive)
                drive_file_id = list(drive_file)[0].get("id").strip()
            else:
                raise Exception("The Sharepoint files list name and Sharepoint file name given cannot be empty")
        except Exception as ex:
            raise ex
        return drive_file_id
    
    @staticmethod
    def format_data_list_of_lists_to_dictionary_list(values_list: list, key_list: list = None):
        key_list_counter = 0
        values_list_counter = 0
        values_first_list_counter = 0
        dictionary_list = None
        try:
            values_list_counter = 0 if values_list is None else len(values_list)
            key_list_counter = 0 if key_list is None else len(key_list)
            if(values_list_counter > 0): 
                if(key_list_counter > 0):
                    values_first_list_counter = len(values_list[0])
                    if(key_list_counter != values_first_list_counter):
                        raise Exception("The lisf of keys for the dictionary needs to have the same amount of items that all the lists given in the list of lists")
                else:
                    key_list = values_list[0]
                    del values_list[0]
                dictionary_list = [dict(zip(key_list, item)) for item in values_list]
            else:
                raise Exception("The list of values given cannot be empty")
        except Exception as ex:
            raise ex
        return dictionary_list
    
    @staticmethod  
    def format_data_dictionary_list_to_list(values_list: list):
        my_list = []
        list_counter = 0
        try:
            list_counter = 0 if values_list is None else len(values_list)
            if(list_counter > 0): 
                my_list = [[key for key in values_list[0].keys()], *[list(idx.values()) for idx in values_list ]]
                del my_list[0]
            else:
                raise Exception("format_data_dictionary_list_to_list: The list of values given cannot be empty")
        except Exception as ex:
            raise ex
        return my_list
    
    @staticmethod
    def create_index_list_of_dict(values_list: list):
        my_list = []
        list_counter = 0
        try:
            list_counter = 0 if values_list is None else len(values_list)
            if(list_counter > 0): 
                my_list = [dict(item, **{'Index':index_counter}) for index_counter,item in enumerate(values_list)]
                #[dict(item, elem='value') for item in my_list]
            else:
                raise Exception("create_index_list_of_dict: The list of values given cannot be empty")
        except Exception as ex:
            raise ex
        return my_list
    
    @staticmethod
    def remove_column_list_of_dict(values_list: list, key_to_remove: str):
        my_list = []
        list_counter = 0
        try:
            list_counter = 0 if values_list is None else len(values_list)
            if(list_counter > 0): 
                my_list = [{key: value for key, value in item.items() if key != key_to_remove} for item in values_list]
            else:
                raise Exception("remove_column_list_of_dict: The list of values given cannot be empty")
        except Exception as ex:
            raise ex
        return my_list
    
    @staticmethod
    def format_data_dictionary_to_list_property(values_list: list, column_name: str):
        my_list = []
        list_counter = 0
        try:
            list_counter = 0 if values_list is None else len(values_list)
            if(list_counter > 0):
                my_list = [idx[column_name] for idx in values_list]
            else:
                raise Exception("format_data_dictionary_to_list_property: The list of values given cannot be empty")
        except Exception as ex:
            raise ex
        return my_list
    
    @staticmethod
    def get_enviroment_variables_dict(values_list: list, enviroment_name: str):
        environment_dict = {}
        try:
            counter = 0
            temp = ""
            if bool(values_list) and bool(enviroment_name):
                for list_item in values_list:
                    for actual_value in list_item.values():
                        if counter == 0:
                            temp = str(actual_value)
                            counter=+1
                        else:
                            environment_dict[temp] = actual_value  
                            counter = 0
                            temp = ""
        except Exception as ex:
            raise ex
        return environment_dict
    
    @staticmethod
    def get_list_id_from_lists(sharepoint_lists: list, 
                               sharepoint_list_name: str):
        sharepoint_list_id = ""
        try:
            sharepoint_list_name = sharepoint_list_name.strip()
            if(sharepoint_list_name is not None or len(sharepoint_list_name) > 0):
                list_lists = filter(lambda sharepoint_list: sharepoint_list.get("name").strip().lower() ==  sharepoint_list_name.strip().lower(), sharepoint_lists)
                sharepoint_list_id = list(list_lists)[0].get("id").strip()
            else:
                raise Exception("The Sharepoint files list name and Sharepoint file name given cannot be empty")
        except Exception as ex:
            raise ex
        return sharepoint_list_id
    
    @staticmethod
    def get_name_from_folder(sharepoint_lists: list):
        sharepoint_list_id = ""
        try:
            sharepoint_list_id = list(sharepoint_lists)[0].get("name").strip()
        except Exception as ex:
            raise ex
        return sharepoint_list_id
    
    @staticmethod
    def get_property_from_folder(sharepoint_lists: list,
                                 property_name: str):
        property_value = ""
        try:
            property_name = property_name.strip()
            property_value = list(sharepoint_lists)[0].get(property_name).strip()
        except Exception as ex:
            raise ex
        return property_value
    
    @staticmethod
    def select_column_list_of_dict(values_list: list, 
                                   key_to_select: str):
        my_list = []
        try:
            if(bool(values_list)>0): 
                my_list = [{key: value for key, value in item.items() if key == key_to_select} for item in values_list]
            else:
                raise Exception("select_column_list_of_dict: The list of values given cannot be empty")
        except Exception as ex:
            raise ex
        return my_list
    
    @staticmethod
    def get_values_from_dict(values_list: list, 
                             enviroment_name: str):
        environment_list = []
        try:
            counter = 0
            temp = ""
            if bool(values_list) and bool(enviroment_name):
                for list_item in values_list:
                    for actual_value in list_item.values():
                        environment_list.append(actual_value)
        except Exception as ex:
            raise ex
        return environment_list
    
    @staticmethod
    def get_email_folder_id(email_folder_list: list,
                            email_folder_name: str):
        email_folder_id = ""
        try:
            if(bool(email_folder_list)>0 and len(email_folder_name)>0):
                drive_file = filter(lambda file: file.get("displayName").strip().lower() ==  email_folder_name.strip().lower(), email_folder_list)
                email_folder_id = list(drive_file)[0].get("id").strip()
            else:
                raise Exception("getEmailFolderId: Error getting the email id")
        except Exception as ex:
            raise ex
        return email_folder_id
    
    @staticmethod
    def filter_result_by_column(param_value: str, 
                                column_value: str, 
                                list_data: list, 
                                result_column: str):
        result = None
        param_value = param_value.strip()
        column_value = column_value.strip()
        try:
            if(bool(param_value) and bool(column_value) and bool(list_data)):
                result = list(filter(lambda file: file.get(column_value).strip().lower() ==  param_value.strip().lower(), list_data))
                if(bool(result_column)):
                    result = result[0].get(result_column)
            else:
                raise Exception("filterResultByColumn: Missing information")
        except Exception as ex:
            raise ex
        return result