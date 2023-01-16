from datetime import timedelta
from importlib import resources
from multiprocessing.connection import wait
from time import sleep
from . import BaanDesktop
from Emerson.variables import std_15s_wait
from Emerson.variables import std_5s_wait
from Emerson.variables import std_3s_wait
from Emerson.variables import std_1s_wait
from Emerson.variables import std_60s_wait

class BaanBecs(BaanDesktop):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.baan_elements = self.actions.read_configuration("data/baan_desktop_config/baan_becs_elements.json")

    def open_baan_environment_by_file_name(self, window_title:str) -> None:
        try:
            self.windows.clear_anchor()
            becs_windows_result = self.windows.get_elements("type:Window")
            counter_windows=0
            for item in becs_windows_result:
                if window_title in item.name and bool(item.name):
                    counter_windows=counter_windows+1
                    windows_main_element = self.windows.control_window(item)
                    break
            if counter_windows==0:
                raise Exception("windows- Becs main screen cannot be found")
            sleep(std_1s_wait)
            #click windows mode
            open_baan_filename=self.windows.get_elements(self.baan_elements["becs_env_name_locator"],search_depth=20)
            self.windows.double_click(self.baan_elements["becs_env_name_locator"])
            self.windows.screenshot(windows_main_element, "start_up_baan.png")
        except Exception as ex:
            raise ex