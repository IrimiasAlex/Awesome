from datetime import timedelta
from importlib import resources
from multiprocessing.connection import wait
from time import sleep
from xml.sax.xmlreader import Locator
from Browser import ElementState, SelectAttribute
from Emerson.variables import std_15s_wait
from Emerson.variables import std_5s_wait
from Emerson.variables import std_1s_wait
from Emerson.variables import std_60s_wait
from . import CDBWeb
from RPA.Desktop import Desktop

class CDB(CDBWeb):
    def __init__(self, *args, **kwargs):
        CDBWeb.__init__(self, *args, **kwargs)
        self.cdb_elements = self.actions.read_configuration("data/cdb_web_config/cdb_elements.json")
        self.desktop = Desktop()
        
    def login_into_cdb_edge(self, cdb_responsibility_link: str, user_name: str, password: str) -> None:
        try:
            cdb_responsibility_link = cdb_responsibility_link.strip()
            user_name = user_name.strip()
            password = password.strip()
            #
            self.desktop.wait_for_element(locator="alias:cdb_launch_locator")
            self.desktop.click(locator="alias:cdb_launch_locator")
            self.desktop.wait_for_element(locator="alias:cdb_username_locator")
            self.desktop.type_text_into(locator="alias:cdb_username_locator",text=user_name)
            self.desktop.type_text_into(locator="alias:cdb_password_locator",text=password)
            self.desktop.wait_for_element(locator="alias:cdb_logon_locator")
            self.desktop.click(locator="alias:cdb_logon_locator")
            
            sleep(std_5s_wait)
            
            sleep(std_1s_wait)
        except Exception as ex:
            raise ex