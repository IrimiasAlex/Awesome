from time import sleep
from RPA.Windows import Windows
from Emerson.GeneralActions import GeneralActions
from Emerson.variables import std_2s_wait, std_15s_wait, search_depth

class MicrosoftOffice365():
    def __init__(self, 
                 *args, 
                 **kwargs):
        self.windows = Windows()
        self.windows.set_wait_time(std_2s_wait)
        self.windows.set_global_timeout(std_15s_wait)
        self.actions = GeneralActions()

    def wait_until_window_exists(self, 
                                 window_title: str, 
                                 time_out: int = 10) -> str:
        """
        Method that waits for an specific window
        @param window_title: Can be part of the title
        @param time_out: Default 10 seconds
        """
        try:
            retries = 0
            window_exist = False
            while retries < time_out:
                windows_list = self.windows.list_windows()
                for window in windows_list:
                    if window_title in window.get("title") and bool(window.get("title")) and not ".py" in window.get("title"):
                        window_exist = True
                        return f'name:"{window.get("object").Name}" and class:{window.get("object").ClassName}'
                if window_exist:
                    break
                sleep(1)
                retries = retries + 1
            if not window_exist:
                raise Exception(f"Wait until window exists time out, {window_title} does not exist")
        except Exception as ex:
            raise ex
        
    def check_element_exists(self,
                             element_locator: str,
                             search_depth_value: int = None,
                             timeout: float = None) -> bool:
        """
        Checks if an element exists based on the given locator
        @param element_locator: The locator of the element to verify
        @param search_depth_value: How deep the element search will traverse
        @param timeout: Float value in seconds, see keyword
        """
        element_exists = False
        previous_timeout = None
        try:
            element_locator = element_locator.strip()
            if search_depth_value is None:
                search_depth_value = search_depth
            if timeout is not None:
                previous_timeout = self.windows.set_global_timeout(timeout)
            element = self.windows.get_element(locator=element_locator,
                                               search_depth=search_depth_value)
            if element is not None:
                element_exists = True
        except Exception:
            pass
        try:
            if previous_timeout is not None:
                self.windows.set_global_timeout(previous_timeout)
        except Exception as ex:
            raise ex
        return element_exists