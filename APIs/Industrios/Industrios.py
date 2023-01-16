from datetime import timedelta
from importlib import resources
from multiprocessing.connection import wait
from time import sleep

from requests import session
from . import IndustriosDesktop
from Emerson.variables import std_15s_wait
from Emerson.variables import std_5s_wait
from Emerson.variables import std_1s_wait
from Emerson.variables import std_60s_wait

class Industrios(IndustriosDesktop):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.industrios_elements = self.actions.read_configuration("data/industrios_desktop_config/industrios_elements.json")

    def attach_screen(self, window_locator, window_title) -> None:
        try:
            self.windows.clear_anchor()
            #wait until new screen exist
            industrios_screen = self.wait_until_element_window_exist(window_locator, window_title, control_main_screen=True)
        except Exception as ex:
            raise ex
        
    def wait_until_element_window_exist(self,locator:str,key_name: str, time_out=10, control_main_screen=False, return_element=False, root_element=None) -> None:
        try:
            retries=0
            counter_windows=0
            while retries< time_out:
                if root_element == None:
                    elements_list = self.windows.get_elements(locator)
                else:
                    elements_list = self.windows.get_elements(locator, root_element=root_element)
                for item in elements_list:
                    if key_name in item.name:
                        counter_windows=counter_windows+1
                        if control_main_screen:
                            user_main_screen = self.windows.control_window(item)
                            return user_main_screen
                        elif return_element:
                            return item
                retries=retries+1
                sleep(std_1s_wait)
            if counter_windows==0:
                raise Exception("windows- wait_until_element_window_exist cannot find the criteria")
        except Exception as ex:
            raise ex
    
