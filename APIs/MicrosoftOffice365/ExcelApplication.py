from time import sleep
from . import MicrosoftOffice365
from Emerson.variables import std_3s_wait, std_20s_wait, search_depth

class ExcelApplication(MicrosoftOffice365):
    
    def __init__(self, 
                 *args, 
                 **kwargs):
        super().__init__(*args, 
                         **kwargs)
        self.excel_application_elements = self.actions.read_configuration("data/microsoft_office_365_config/microsoft_excel_elements.json")
        
    def attach_excel_application(self) -> None:
        """
        Connect the library to Excel Application
        """
        try:
            self.windows.clear_anchor()
            sleep(std_3s_wait)
            excel_main_screen_locator = self.wait_until_window_exists(self.excel_application_elements.get("excel_application_title"),
                                                                      std_20s_wait)
            sleep(std_3s_wait)
            self.excel_main_screen = self.windows.control_window(excel_main_screen_locator)
            sleep(std_3s_wait)
        except Exception as ex:
            raise ex
        
    def check_element_exists(self, 
                             element_name: str,
                             search_depth_value: int = None, 
                             timeout: float = None) -> bool:
        """
        Checks if an element exists based on the given element name
        @param element_name: The name of the element to verify
        @param search_depth_value: How deep the element search will traverse
        @param timeout: Float value in seconds, see keyword
        """
        element_exists = False
        try:
            element_name = element_name.strip().lower()
            excel_application_elements = self.excel_application_elements
            if element_name not in excel_application_elements:
                raise Exception(
                    "The element with the name: "
                    + element_name
                    + " doesn't exists in Excel application"
                )
            element_locator = excel_application_elements.get(element_name)
            element_exists = super().check_element_exists(element_locator, search_depth_value, timeout)
        except Exception as ex:
            raise ex
        return element_exists
        
        
    def click_element(self,
                      element_name: str) -> None:
        """
        Clicks an element in Excel application by it's name
        @param element_name: Must be one of this possible values:
        "excel_tab_oracle",
        "excel_tab_oracle_button_upload",
        "excel_tab_oracle_button_login",
        "excel_tab_oracle_button_select",
        "excel_tab_oracle_button_journals_upload"
        """
        try:
            element_name = element_name.strip().lower()
            excel_application_elements = self.excel_application_elements
            if element_name not in excel_application_elements:
                raise Exception(
                    "The element with the name: "
                    + element_name
                    + " doesn't exists in Excel application"
                )
            element_locator = excel_application_elements.get(element_name)
            element = self.windows.get_element(locator=element_locator,
                                               search_depth=search_depth)
            self.excel_main_screen = self.windows.foreground_window(locator=self.excel_main_screen)
            self.windows.click(locator=element)
        except Exception as ex:
            raise ex
        
    def write_in_element(self,
                         element_name: str,
                         element_value: str,
                         delete_previous_content: bool = False) -> None:
        """
        Writes a text in an element inside Excel application by it's name
        @param element_name: Must be one of this possible values:
        "excel_tab_oracle_input_user_name",
        "excel_tab_oracle_input_user_password"
        @param element_value: The text to write in the element
        @param delete_previous_content: Must be 'True' or 'False', if you want to delete the content of the element before write
        """
        try:
            element_name = element_name.strip().lower()
            element_value = element_value.strip().lower()
            excel_application_elements = self.excel_application_elements
            if element_name not in excel_application_elements:
                raise Exception(
                    "The element with the name: "
                    + element_name
                    + " doesn't exists in Excel application"
                )
            element_locator = excel_application_elements.get(element_name)
            element = self.windows.get_element(locator=element_locator,
                                               search_depth=search_depth)
            self.excel_main_screen = self.windows.foreground_window(locator=self.excel_main_screen)
            if delete_previous_content:
                clear_keys = excel_application_elements.get("clear_field_keys")
                self.windows.send_keys(locator=element,
                                       keys=clear_keys)
            self.windows.send_keys(locator=element,
                                   keys=element_value)
        except Exception as ex:
            raise ex