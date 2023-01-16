import datetime, json, os, psutil
from pathlib import Path
from time import sleep

from Emerson.variables import std_5s_wait
from RPA.FileSystem import FileSystem

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
"""libraries_path = str(Path(ROOT_DIR).parent.absolute())
tool_box_dll = libraries_path + r'\dll\MARSToolBox.dll'
clr.AddReference(tool_box_dll)
from MARSToolBox import GeneralActions"""


class GeneralActions:
    """def get_handle_by_process_name_and_window_title(, process_name: str, window_title: str):
    handle = 0
    try:
        general_actions = GeneralActions()
        handle = general_actions.GetHandleByWindowTitle(process_name, window_title)
    except Exception as ex:
        raise ex
    return handle"""

    @staticmethod
    def text_contains_ignore_case(full_string: str, sub_string: str):
        result = False
        try:
            if sub_string.strip().lower() in full_string.strip().lower():
                result = True
        except Exception as ex:
            raise ex
        return result

    @staticmethod
    def get_month_name(month_number: int):
        result = ""
        try:
            month_number_converted = int(month_number)
            date = datetime.datetime(2021, month_number_converted, 1)
            result = str(date.strftime("%b").upper())
        except Exception as ex:
            raise ex
        return result

    @staticmethod
    def get_month_last_two_digits(month_number: int):
        result = ""
        try:
            month_number_converted = int(month_number)
            date = datetime.datetime(2021, month_number_converted, 1)
            result = str(date.strftime("%m").upper())
        except Exception as ex:
            raise ex
        return result

    @staticmethod
    def get_year_last_two_digits(year_number: int):
        result = ""
        try:
            year_number_converted = int(year_number)
            date = datetime.datetime(year_number_converted, 1, 1)
            result = str(date.strftime("%y").upper())
        except Exception as ex:
            raise ex
        return result

    @staticmethod
    def format_date(date, date_format: str):
        date_format = date_format.strip()
        formatted_date = ""
        try:
            formatted_date = date.strftime(date_format)
        except Exception as ex:
            raise ex
        return formatted_date

    @staticmethod
    def filter_dictionary_list_no_case_sensitive(
        dictionary_list: list,
        key_name: str,
        key_value_to_exclude: str,
        second_key_name=None,
        second_key_value_to_exclude=None,
    ):
        dictionary_list_filtered = None
        try:
            key_name = key_name.strip()
            key_value_to_exclude = key_value_to_exclude.strip()
            counter_second_key = 0 if second_key_name is None else len(second_key_name)
            counter_second_value = (
                0
                if second_key_value_to_exclude is None
                else len(second_key_value_to_exclude)
            )
            if (
                dictionary_list is not None
                or len(dictionary_list) > 0
                or key_name is not None
                or len(key_name) > 0
                or key_value_to_exclude is not None
                or len(key_value_to_exclude) > 0
            ):
                if counter_second_key > 0 and counter_second_value > 0:
                    dictionary_list_filtered = list(
                        filter(
                            lambda item: item.get(key_name).strip().lower()
                            != key_value_to_exclude.strip().lower()
                            and item.get(second_key_name).strip().lower()
                            != second_key_value_to_exclude.strip().lower(),
                            dictionary_list,
                        )
                    )
                else:
                    dictionary_list_filtered = list(
                        filter(
                            lambda item: item.get(key_name).strip().lower()
                            != key_value_to_exclude.strip().lower(),
                            dictionary_list,
                        )
                    )
            else:
                raise Exception(
                    "The dictionary list, key name and key value given cannot be empty"
                )
        except Exception as ex:
            raise ex
        return dictionary_list_filtered

    @staticmethod
    def filter_dictionary_list_equal_to_no_case_sensitive(
        dictionary_list: list,
        key_name: str,
        key_value_to_exclude: str,
        second_key_name=None,
        second_key_value_to_exclude=None,
    ):
        dictionary_list_filtered = None
        try:
            key_name = key_name.strip()
            key_value_to_exclude = key_value_to_exclude.strip()
            counter_second_key = 0 if second_key_name is None else len(second_key_name)
            counter_second_value = (
                0
                if second_key_value_to_exclude is None
                else len(second_key_value_to_exclude)
            )
            if (
                dictionary_list is not None
                or len(dictionary_list) > 0
                or key_name is not None
                or len(key_name) > 0
                or key_value_to_exclude is not None
                or len(key_value_to_exclude) > 0
            ):
                if counter_second_key > 0 and counter_second_value > 0:
                    dictionary_list_filtered = list(
                        filter(
                            lambda item: item.get(key_name).strip().lower()
                            == key_value_to_exclude.strip().lower()
                            and item.get(second_key_name).strip().lower()
                            == second_key_value_to_exclude.strip().lower(),
                            dictionary_list,
                        )
                    )
                else:
                    dictionary_list_filtered = list(
                        filter(
                            lambda item: item.get(key_name).strip().lower()
                            == key_value_to_exclude.strip().lower(),
                            dictionary_list,
                        )
                    )
            else:
                raise Exception(
                    "The dictionary list, key name and key value given cannot be empty"
                )
        except Exception as ex:
            raise ex
        return dictionary_list_filtered

    @staticmethod
    def update_dictionary_key_value(
        dictionary: dict, key_name: str, key_value_to_update: str
    ):
        try:
            key_name = key_name.strip()
            key_value_to_update = key_value_to_update.strip()
            if (
                dictionary is not None
                or key_name is not None
                or len(key_name) > 0
                or key_value_to_update is not None
                or len(key_value_to_update) > 0
            ):
                dictionary[key_name] = key_value_to_update
            else:
                raise Exception(
                    "The dictionary, key name and key value given cannot be empty"
                )
        except Exception as ex:
            raise ex
        return dictionary

    @staticmethod
    def split_string_to_list(string: str, separator: str):
        result = []
        try:
            string = string.strip()
            separator = separator.strip()
            counter_string = 0 if string is None else len(string)
            counter_separator = 0 if separator is None else len(separator)
            if counter_string > 0 and counter_separator > 0:
                result = string.split(separator)
            else:
                raise Exception("The string and separator values given cannot be empty")
        except Exception as ex:
            raise ex
        return result

    @staticmethod
    def read_json_file(file_path_with_ext: str):
        data = None
        try:
            file_path = file_path_with_ext.strip()
            if bool(file_path_with_ext):
                with open(file_path, encoding="utf-8") as json_file:
                    data = json.load(json_file)
            else:
                raise Exception(
                    "The file path with extension value given cannot be empty"
                )
        except Exception as ex:
            raise ex
        return data

    @staticmethod
    def get_root_directory():
        robot_root = os.getenv("ROBOT_ROOT", None)
        emerson_root = os.getenv("EMERSON_ROOT", "modules")
        return Path(robot_root) / emerson_root if robot_root else Path(".")

    @staticmethod
    def read_configuration(filename):
        config_file_path = str((GeneralActions.get_root_directory() / filename).resolve())
        return GeneralActions.read_json_file(
            config_file_path
        )

    @staticmethod
    def kill_process(process_name: str):
        try:
            process_name = process_name.strip()
            user_name = os.getenv("USERNAME", "").strip()
            if user_name != "":
                os.system('TASKKILL /F /FI "USERNAME eq ' + user_name + '" /IM ' + process_name + ' /T')
            else:
                os.system('TASKKILL /F /IM ' + process_name + ' /T')
            sleep(std_5s_wait)
        except Exception as ex:
            raise ex

    @staticmethod
    def remove_files_from_directory(directory_path: str) -> None:
        # TODO. Remove RPA.FileSystem and use OperatingSystem.Remove Files
        try:
            directory_path = directory_path.strip()
            file_system = FileSystem()
            files_to_remove = file_system.list_files_in_directory(directory_path)
            files_to_remove = [file.path for file in files_to_remove]
            file_system.remove_files(*files_to_remove)
        except Exception as ex:
            raise ex
        
    @staticmethod 
    def retry_function_until_succeeds(retry_number: int, 
                                      wait_time: float, 
                                      c_function, 
                                      *current_args) -> any:
        try:
            output = None
            result = ""
            counter = 0
            for counter in range(retry_number):
                try:
                    output = c_function(*current_args)
                    break
                except Exception as e:
                    result = str(e)
                    pass
                sleep(wait_time)
            if len(result) > 0:
                raise Exception(f"Error executing '{str(c_function.__name__)}' after {retry_number} retries. Last error was: {result}")
        except Exception as ex:
            raise ex
        return output
        
    @staticmethod
    def retry_function_and_ignore_error(retry_number: int, 
                                        wait_time: float, 
                                        c_function, 
                                        *current_args) -> any:
        try:
            output = None
            counter = 0
            for counter in range(retry_number):
                try:
                    output = c_function(*current_args)
                    break
                except Exception as e:
                    output = str(e)
                    pass
                sleep(wait_time)
            return output
        except Exception:
            raise Exception(f"Error executing '{str(c_function.__name__)}' after {retry_number} retries. Last error was: {output}")
    
    @staticmethod
    def wait_for_process_to_exists(process_name: str,
                                   time_out = 60):
        try:
            counter_process = 0
            counter_loop = 0
            while counter_loop < time_out:
                for proc in psutil.process_iter():
                    if proc.name().lower() == process_name.lower():
                        counter_process = counter_process + 1
                        break
                if(counter_process != 0):
                    break
                else:
                    sleep(1)
                    counter_loop = counter_loop+1
            if(counter_process == 0):
                raise Exception(f"Timeout process '{process_name}' is not running")
        except Exception as ex:
            raise ex