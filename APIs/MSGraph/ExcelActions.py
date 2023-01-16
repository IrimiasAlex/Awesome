from .Excel import Excel
from .Utilities import Utilities

class ExcelActions(Excel):
    def __init__(self, *args, **kwargs):
        Excel.__init__(self, *args, **kwargs)

    def core_ms_graph_get_excel_file_as_json(self, sharepoint_url: str, sub_folder_path: str, file_name_with_ext: str, table_names: list):
        excel_tables_data = {}
        try:
            tables_names_list_counter = 0 if table_names is None else len(table_names)
            #Validations
            if(sharepoint_url is not None and sharepoint_url != "" and sub_folder_path is not None  and sub_folder_path != "" and file_name_with_ext is not None and file_name_with_ext != "" and 
               tables_names_list_counter > 0):
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
                sharepoint_file_id = Utilities.get_file_id_from_drive_list_by_file_name(sharepoint_files_from_drive, file_name_with_ext)
                for table in table_names:
                    current_table = table.strip()
                    excel_table_data = self.get_table_data_from_file(sharepoint_site_id, sharepoint_drive_id, sharepoint_file_id, current_table)
                    excel_table_data = Utilities.format_data_list_of_lists_to_dictionary_list(excel_table_data)
                    excel_table_data = Utilities.create_index_list_of_dict(excel_table_data)
                    excel_tables_data[current_table] = excel_table_data
            else:
                raise Exception("The Sharepoint url, subfolder path, file name with extension and the table names list given cannot be empty")
        except Exception as ex:
            raise ex
        return excel_tables_data
    
    def core_ms_graph_write_excel_table_with_json(self, sharepoint_url: str, sub_folder_path: str, file_name_with_ext: str, table_name: str, excel_json_data: dict):
        try:
            #Validations
            if(sharepoint_url is not None and sharepoint_url != "" and sub_folder_path is not None  and sub_folder_path != "" and file_name_with_ext is not None and file_name_with_ext != "" and 
               table_name is not None  and table_name != "" and bool(excel_json_data) and excel_json_data):
                sharepoint_url = sharepoint_url.strip()
                sub_folder_path = sub_folder_path.strip()
                file_name_with_ext = file_name_with_ext.strip()
                table_name = table_name.strip()
                #MsGraph
                sharepoint_path_dict = Utilities.get_sharepoint_path_by_url(sharepoint_url)
                sharepoint_path = sharepoint_path_dict.get("sharepoint_path")
                sharepoint_site_id = self.get_sharepoint_site_id(sharepoint_path)
                sharepoint_site_drives = self.get_sharepoint_site_drives(sharepoint_site_id)
                sharepoint_drive_id = Utilities.get_sharepoint_drive_id_by_url(sharepoint_url, sharepoint_site_drives)
                sub_folder_path = Utilities.fix_sharepoint_sub_folder_path(sub_folder_path)
                sharepoint_files_from_drive = self.get_sharepoint_files_from_drive(sharepoint_site_id, sharepoint_drive_id, sub_folder_path)
                sharepoint_file_id = Utilities.get_file_id_from_drive_list_by_file_name(sharepoint_files_from_drive, file_name_with_ext)
                #Format Data
                excel_json_data = Utilities.remove_column_list_of_dict(excel_json_data,'Index')
                table_data = Utilities.format_data_dictionary_list_to_list(excel_json_data)
                dic_table_data={'values': table_data}
                self.post_table_data_from_json(sharepoint_site_id, sharepoint_drive_id, sharepoint_file_id,table_name,dic_table_data)
            else:
                raise Exception("The Sharepoint url, subfolder path, file name with extension and the table names list given cannot be empty")
        except Exception as ex:
            raise ex
    
    def core_ms_graph_get_excel_tables(self, sharepoint_url: str, sub_folder_path: str, file_name_with_ext: str):
        excel_table_names = []
        try:
            #Validations
            if(sharepoint_url is not None and sharepoint_url != "" and sub_folder_path is not None  and sub_folder_path != "" and file_name_with_ext is not None and file_name_with_ext != ""):
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
                sharepoint_file_id = Utilities.get_file_id_from_drive_list_by_file_name(sharepoint_files_from_drive, file_name_with_ext)
                #Get Tables
                dict_excel_table_names = self.get_table_names_from_file(sharepoint_site_id, sharepoint_drive_id, sharepoint_file_id)
                excel_table_names = Utilities.format_data_dictionary_to_list_property(dict_excel_table_names, "name")
            else:
                raise Exception("The Sharepoint url, subfolder path, file name with extension and the table names list given cannot be empty")
        except Exception as ex:
            raise ex
        return excel_table_names
    
    def core_ms_graph_update_row(self, sharepoint_url: str, sub_folder_path: str, file_name_with_ext: str, table_name: str, table_row_data: list):
        try:
            table_row_list_counter = 0 if table_row_data is None else len(table_row_data)
            #Validations
            if(sharepoint_url is not None and sharepoint_url != "" and sub_folder_path is not None  and sub_folder_path != "" and file_name_with_ext is not None and file_name_with_ext != "" and table_row_list_counter>0 and table_row_list_counter<2):
                sharepoint_url = sharepoint_url.strip()
                sub_folder_path = sub_folder_path.strip()
                file_name_with_ext = file_name_with_ext.strip()
                table_name = table_name.strip()
                #MsGraph
                sharepoint_path_dict = Utilities.get_sharepoint_path_by_url(sharepoint_url)
                sharepointPath = sharepoint_path_dict.get("sharepoint_path")
                sharepoint_site_id = self.get_sharepoint_site_id(sharepointPath)
                sharepoint_site_drives = self.get_sharepoint_site_drives(sharepoint_site_id)
                sharepoint_drive_id = Utilities.get_sharepoint_drive_id_by_url(sharepoint_url, sharepoint_site_drives)
                sub_folder_path = Utilities.fix_sharepoint_sub_folder_path(sub_folder_path)
                sharepoint_files_from_drive = self.get_sharepoint_files_from_drive(sharepoint_site_id, sharepoint_drive_id, sub_folder_path)
                sharepoint_file_id = Utilities.get_file_id_from_drive_list_by_file_name(sharepoint_files_from_drive, file_name_with_ext)
                #Update Row
                table_row_index = int(table_row_data[0]['Index'])
                table_row_data = Utilities.remove_column_list_of_dict(table_row_data,'Index')
                list_value_row = Utilities.format_data_dictionary_list_to_list(table_row_data)
                table_data={'values': list_value_row}
                self.patch_table_row_from_json(sharepoint_site_id, sharepoint_drive_id, sharepoint_file_id,table_name,table_data,str(table_row_index))
            else:
                raise Exception("The Sharepoint url, subfolder path, file name with extension and the table names list given cannot be empty, update row works one by one")
        except Exception as ex:
            raise ex
        
    def get_enviroment_data(self, enviroment_sp_url: str, enviroment_sp_subfolder: str, enviroment_sp_file: str, enviroment_sp_table: str, enviroment_name: str):
        list_result = {}
        try:
            enviroment_sp_table = [enviroment_sp_table.strip()]
            list_enviroment_table = self.core_ms_graph_get_excel_file_as_json(enviroment_sp_url,enviroment_sp_subfolder,enviroment_sp_file,enviroment_sp_table)
            if enviroment_name.strip().lower() == 'dev':
                list_enviroment_table = list_enviroment_table[str(enviroment_sp_table[0])]
                list_enviroment_table = Utilities.remove_column_list_of_dict(list_enviroment_table,'Index')
                list_enviroment_table = Utilities.remove_column_list_of_dict(list_enviroment_table,'UAT')
                list_enviroment_table = Utilities.remove_column_list_of_dict(list_enviroment_table,'PROD')
                list_result = Utilities.get_enviroment_variables_dict(list_enviroment_table,str(enviroment_sp_table[0]))
            elif enviroment_name.strip().lower() == 'uat':
                list_enviroment_table = list_enviroment_table[str(enviroment_sp_table[0])]
                list_enviroment_table = Utilities.remove_column_list_of_dict(list_enviroment_table,'Index')
                list_enviroment_table = Utilities.remove_column_list_of_dict(list_enviroment_table,'DEV')
                list_enviroment_table = Utilities.remove_column_list_of_dict(list_enviroment_table,'PROD')
                list_result = Utilities.get_enviroment_variables_dict(list_enviroment_table,str(enviroment_sp_table[0]))
            elif enviroment_name.strip().lower() == 'prod':
                list_enviroment_table = list_enviroment_table[str(enviroment_sp_table[0])]
                list_enviroment_table = Utilities.remove_column_list_of_dict(list_enviroment_table,'Index')
                list_enviroment_table = Utilities.remove_column_list_of_dict(list_enviroment_table,'DEV')
                list_enviroment_table = Utilities.remove_column_list_of_dict(list_enviroment_table,'UAT')
                list_result = Utilities.get_enviroment_variables_dict(list_enviroment_table,str(enviroment_sp_table[0]))
            else:
                raise Exception("Enviroment Constant cannot be blank")     
        except Exception as ex:
            raise ex
        return list_result
    
    def core_ms_graph_refresh_all_excel_file(self, sharepoint_url: str, sub_folder_path: str, file_name_with_ext: str, worksheet_name: str):
        try:
            #Validations
            if(sharepoint_url is not None and sharepoint_url != "" and sub_folder_path is not None  and sub_folder_path != "" and file_name_with_ext is not None and file_name_with_ext != "" and worksheet_name != "" and worksheet_name is not None):
                sharepoint_url = sharepoint_url.strip()
                sub_folder_path = sub_folder_path.strip()
                file_name_with_ext = file_name_with_ext.strip()
                worksheet_name = worksheet_name.strip()
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
                #Refresh File                
                self.refresh_all_excel_file(sharepoint_site_id, sharepoint_drive_id, sharepoint_file_id, worksheet_name)
            else:
                raise Exception("The Sharepoint url, subfolder path, file name with extension and the table names list given cannot be empty, update row works one by one")
        except Exception as ex:
            raise ex
        
    def core_ms_graph_remove_excel_file(self, sharepoint_url: str, sub_folder_path: str, file_name_with_ext: str):
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
                #Remove File                
                self.remove_excel_file(sharepoint_site_id, sharepoint_drive_id, sharepoint_file_id)
            else:
                raise Exception("The Sharepoint url, subfolder path, file name with extension and the table names list given cannot be empty, update row works one by one")
        except Exception as ex:
            raise ex