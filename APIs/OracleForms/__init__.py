from Emerson.GeneralActions import GeneralActions
from Emerson.variables import std_1s_wait, std_60s_wait
from time import sleep
from RPA.JavaAccessBridge import JavaAccessBridge
from RPA.Desktop import Desktop
from pynput_robocorp.keyboard import Controller as KeyboardController
from pynput_robocorp.keyboard import Key

class OracleForms:
    def __init__(self, *args, **kwargs):
        self.library_timeout = kwargs.pop("timeout", std_60s_wait)
        self.config_file_path = None
        self.oracle_forms_elements = None
        self.actions = GeneralActions()
        self.desktop = Desktop()
        self.keyboard = KeyboardController()

    def attach_oracle_forms(self, window_title: str, foreground: bool = False):
        try:
            # Inputs
            window_title = window_title.strip()
            self.java = JavaAccessBridge(ignore_callbacks=True)
            self.java.select_window(
                title=window_title, bring_foreground=foreground, timeout=self.library_timeout
            )
        except Exception as ex:
            raise ex

    def close_oracle_forms(self):
        try:
            if not self.java:
                raise ValueError("Oracle Forms has not been attached with 'Attach Oracle Forms' keyword")
            self.java.close_java_window()
        except Exception as ex:
            raise ex

    def move_oracle_forms_to_front(self, window_title: str):
        try:
            #Inputs
            window_title = window_title.strip()
            self.java.select_window(title=window_title, bring_foreground=True, timeout=self.library_timeout)
        except Exception as ex:
            raise ex

    def refresh_application_elements_tree(self):
        try:
            self.java.application_refresh()
        except Exception as ex:
            raise ex

    def wait_until_element_exists(self, element_locator: str, timeout: int):
        # TODO. timeout is actually retry count, NOT a timeout!
        element_found = False
        try:
            # Inputs
            element_locator = element_locator.strip()
            for item in range(timeout):
                elements_list = self.java.get_elements(element_locator, strict=True)
                if len(elements_list) > 0:
                    element_found = True
                    break
                self.java.application_refresh()
                #sleep(std_1s_wait)  # Unnecessary sleep because application_refresh
                # will cause delay
        except Exception as ex:
            raise ex
        return element_found

    def get_element_by_attribute(
        self,
        element_locator: str,
        element_attribute: str,
        element_attribute_value: str,
        timeout: int,
    ):
        element = None
        try:
            # Inputs
            element_locator = element_locator.strip()
            element_attribute = element_attribute.strip()
            element_attribute_value = element_attribute_value.strip()
            for item in range(timeout):
                self.java.application_refresh()
                elements_list = self.java.get_elements(element_locator, strict=True)
                for current_element in elements_list:
                    try:
                        attribute_value = current_element.context_info.__getattribute__(
                            element_attribute
                        )
                        if (
                            element_attribute_value.strip().lower()
                            in attribute_value.strip().lower()
                        ):
                            element = current_element
                            break
                    except:
                        raise Exception(
                            "The current element doesn't have the attributte given: '"
                            + element_attribute
                            + "'"
                        )
                if element is not None:
                    break
                sleep(std_1s_wait)
        except Exception as ex:
            raise ex
        return element

    def read_element_value(self, element_locator: str):
        element_value = ""
        try:
            # Inputs
            element_locator = element_locator.strip()
            self.java.application_refresh()
            element_value = self.java.get_element_text(element_locator).strip()
        except Exception as ex:
            raise ex
        return element_value

    def write_in_element(self, element_locator, value: str, verify: bool = False):
        try:
            # Inputs
            if isinstance(element_locator, str):
                element_locator = element_locator.strip()
            value = value.strip()
            self.java.type_text(element_locator, value, clear=True)
            if verify:
                self.java.application_refresh()
                current_text = self.java.get_element_text(element_locator).strip().lower()
                if current_text != value.lower():
                    raise Exception(
                        "Error in writing on the element: "
                        + str(element_locator).strip()
                        + ". The written text: "
                        + current_text
                        + "is not equal to the given one: "
                        + value
                    )
        except Exception as ex:
            raise ex

    def click_java_element(self, element_locator: str):
        try:
            # Inputs
            if isinstance(element_locator, str):
                element_locator = element_locator.strip()
            self.java.click_element(element_locator, timeout=self.library_timeout)
        except Exception as ex:
            raise ex

    def select_drop_down_option(self, element_locator: str, element_index: int = 0):
        try:
            # Inputs
            element_locator = element_locator.strip()
            self.java.toggle_drop_down(element_locator, element_index)
        except Exception as ex:
            raise ex

    def send_keys(self, *keys_to_send):
        try:
            self.java.press_keys(*keys_to_send)
        except Exception as ex:
            raise ex

    def read_table(self, columns_list: list, return_java_elements:bool = False):
        columns_data = []
        payload = {}
        max_rows = 8
        try:
            for current_column in columns_list:
                current_column_values = current_column.values()
                for index, value in enumerate(current_column_values):
                    if index == 0:
                        payload[value] = ""
            self.java.application_refresh()
            for index, current_column in enumerate(columns_list):
                column_key_name = list(current_column.keys())[0]
                locator_key_name = list(current_column.keys())[
                    len(current_column.keys()) - 1
                ]
                elements_list = self.java.get_elements(current_column[locator_key_name], java_elements=return_java_elements, strict=True)
                elements_list = elements_list[:max_rows] if len(elements_list)>max_rows else elements_list
                for index_element, current_element in enumerate(elements_list):
                    temp_row_data = payload.copy()
                    if "role:check box" in current_column[locator_key_name]:
                        element_value = bool(current_element.checked)
                    else:
                        element_value = self.java.get_element_text(current_element).strip()
                    element_properties = None
                    try:
                        element_properties = current_element
                    except:
                        pass
                    temp_row_data[current_column[column_key_name]] = element_value
                    temp_row_data[
                        current_column[column_key_name] + "Element"
                    ] = element_properties
                    if index == 0:
                        columns_data.append(temp_row_data)
                    else:
                        columns_data[index_element][
                            current_column[column_key_name]
                        ] = element_value
                        columns_data[index_element][
                            current_column[column_key_name] + "Element"
                        ] = element_properties
        except Exception as ex:
            raise ex
        return columns_data

    def read_table_with_scroll_down(
        self, columns_list: list, key_column_name: str, *scroll_down_key_combinations
    ):
        columns_data = []
        try:
            key_column_name = key_column_name.strip()
            columns_data = self.read_table(columns_list)
            if not any(key_column_name in column_name for column_name in columns_data):
                raise Exception(
                    "Cannot find the key column name: '"
                    + key_column_name
                    + "' in the columns list given"
                )
            while True:
                counter_columns_data = 0 if columns_data is None else len(columns_data)
                last_key_value_columns_data = columns_data[counter_columns_data - 1][
                    key_column_name
                ]
                last_element_columns_data = columns_data[counter_columns_data - 1][
                    key_column_name + "Element"
                ]
                self.java.click_element(last_element_columns_data)
                self.java.press_keys(*scroll_down_key_combinations)
                self.java.application_refresh()
                temp_columns_data = self.read_table(columns_list)
                counter_temp_columns_data = (
                    0 if columns_data is None else len(temp_columns_data)
                )
                last_key_value_temp_columns_data = temp_columns_data[
                    counter_temp_columns_data - 1
                ][key_column_name]
                if last_key_value_temp_columns_data == last_key_value_columns_data:
                    break
                columns_data.append(temp_columns_data[counter_temp_columns_data - 1])
        except Exception as ex:
            raise ex
        return columns_data

    def get_all_elements(self, locator:str, strict:bool=True):
        return self.java.get_elements(locator, java_elements=True, strict=strict)

    def click_coordinates(self, element, shift_click: bool = False):
        if shift_click:
            with self.keyboard.pressed(Key.shift):
                self.java.click_coordinates(element.center_x, element.center_y)
        else:
            self.java.click_coordinates(element.center_x, element.center_y)

    def type_text(self, text, enter=True):
        #self.java.type_text(locator, text, clear=False)
        self.desktop.type_text(text, enter=enter)

    def click_java_element_without_action(self, element_locator: str):
        try:
            # Inputs
            if isinstance(element_locator, str):
                element_locator = element_locator.strip()
            self.java.click_element(element_locator, timeout=self.library_timeout, action=False)
        except Exception as ex:
            raise ex

    def press_java_keys(self, *keys):
        self.java.press_keys(*keys)

    def take_desktop_screenshot(self, filepath:str = None):
        """Take desktop screenshot

        :param filepath: optional filepath for screenshot (without .png)
        :return: filepath to the screenshot file
        """
        return self.desktop.take_screenshot(path=filepath)

    def is_desktop_locator_visible(self, locator:str, timeout:int = 5):
        try:
            self.desktop.wait_for_element(f"{locator}", timeout)
            return True
        except Exception as ex:
            pass
        return False

    def click_desktop_locator(self, locator:str, timeout:int = 5):
        # TODO. Create Desktop package which contains desktop keywords
        try:
            self.desktop.wait_for_element(f"{locator}", timeout)
            self.desktop.click(f"{locator}")
            return True
        except Exception as ex:
            pass
        return False