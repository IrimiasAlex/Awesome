from time import sleep
from Emerson.GeneralActions import GeneralActions
from Emerson.variables import std_60s_wait, root_directory
from RPA.Windows import Windows
from RPA.Desktop import Desktop
from robot.libraries.BuiltIn import BuiltIn

class IndustriosDesktop():
    def __init__(self, *args, **kwargs):
        self.windows = Windows()
        self.desktop = Desktop()
        self.actions = GeneralActions()
        self.industrios_elements = None
        self.builtin = BuiltIn()
        

    def open_industrios_application(self,file_name: str, window_title: str, time_out:int):
        """
        filename = entire address,
        window_title = can be part of the title
        """
        try:
            self.builtin.log_to_console("kw: Before Window Run - BEGIN")
            self.windows.windows_run(file_name)
            self.builtin.log_to_console("kw: After Window Run - BEGIN")
            #windows_desktop_root_list = self.windows.get_elements("desktop:desktop")
            #self.windows_desktop_root = windows_desktop_root_list[0]
            #self.wait_until_window_exists(window_title, time_out)
            #self.builtin.log_to_console("kw: After Wait - BEGIN")
        except Exception as ex:
            raise ex

    def wait_until_window_exists(self, window_title: str, time_out = 10):
        """
        window_title = can be part of the title,
        time_out = default 10 seconds
        """
        try:
            retries=0
            window_exist=False
            while retries< time_out:
                windows_list = self.windows.list_windows()
                for window in windows_list:
                    if window_title in window['title'] and bool(window['title']) and not ".py" in window['title']:
                        window_exist=True
                        return 'name:"'+window['object'].Name+'" and class:'+window['object'].ClassName
                if window_exist:
                    break
                sleep(1)
                retries=retries+1
            if not window_exist:
                raise Exception("wait until window exists time out, "+window_title+" does not exist")
        except Exception as ex:
            raise ex
    
    def close_industrios(self):
        try:
            self.windows.close_all_applications()
        except Exception as ex:
            raise ex
    
    