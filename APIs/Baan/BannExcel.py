from datetime import timedelta
from importlib import resources
from multiprocessing.connection import wait
from time import sleep

from requests import session
from . import BaanDesktop
from Emerson.variables import std_15s_wait
from Emerson.variables import std_5s_wait
from Emerson.variables import std_3s_wait
from Emerson.variables import std_1s_wait
from Emerson.variables import std_60s_wait

class BannExcel(BaanDesktop):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.baan_elements = self.actions.read_configuration("data/baan_desktop_config/baan_excel_elements.json")

    def save_excel_as_file(self) -> None:
        try:
            self.windows.clear_anchor()
            #get excel main screen
            sleep(std_3s_wait)
            excel_main_screen_locator = self.wait_until_window_exists("Excel",20)
            sleep(std_3s_wait)
            self.excel_main_screen=self.windows.control_window(excel_main_screen_locator)
            sleep(std_3s_wait)
            if "b2win" in excel_main_screen_locator:
                self.windows.send_keys(self.excel_main_screen,"{CTRL}s",wait_time=1.5)
            elif "Excel" in excel_main_screen_locator:
                try:
                    self.windows.click('type:Button and name:"Read Only" and depth:20')
                except Exception as e:
                    pass
            else:
                raise Exception("Excel b2win cannot be found")
                
            #try:
            #    button_internal_list=self.windows.get_elements('type:SplitButton and class:Button',search_depth=20)
            #    button_internal = self.return_item_by_index(button_internal_list,0)
            #    self.windows.click(button_internal)
            #    sleep(std_3s_wait)
            #    button_no_label_list=self.windows.get_elements('class:MenuItem and name:"No Label" and depth:20',search_depth=20)
            #    self.windows.click('class:MenuItem and name:"No Label" and depth:20')
            #    sleep(std_3s_wait)
            #    self.windows.click('class:Button and type:Button and name:OK and depth:20')
            #except Exception as e:
            #    pass
            #sleep(std_3s_wait)
            #self.windows.send_keys(self.excel_main_screen,"{CTRL}s",wait_time=1.5)
            self.windows.screenshot(self.excel_main_screen, "baan_open_file_run_program.png")
        except Exception as ex:
            raise ex
    
    def open_program_by_code(self, program_code:str) -> None:
        try:
            self.windows.clear_anchor()
            #check run program screen exist
            run_program_screen=self.wait_until_element_window_exist("type:Window","Run",return_element=True)
            input_program=self.windows.get_elements(self.baan_elements["bw_input_session_program"],search_depth=20)
            self.write_and_read_information(input_program[0],program_code,interval=0.7,wait_time=0.5)
            self.windows.send_keys(input_program[0],"{ENTER}",wait_time=1.5)
            self.windows.screenshot(run_program_screen, "baan_open_program_by_code.png")
        except Exception as ex:
            raise ex
        
    def continue_blocked_sales_orders(self,window_title: str) -> None:
        try:
            self.windows.clear_anchor()
            #wait until new screen exist
            blocked_sales_screen_locator = self.wait_until_window_exists(window_title,15)
            #control new window
            self.blocked_sales_screen=self.windows.control_window(blocked_sales_screen_locator)
            #get button
            buttons_list = self.windows.get_elements("type:Button and class:TsPushButtonWinClass",search_depth=20)
            button_continue_locator=self.return_item_by_name(buttons_list,"Continue")
            self.windows.click(button_continue_locator)
            self.windows.screenshot(self.blocked_sales_screen, "baan_continue_blocked_sales_orders.png")
        except Exception as ex:
            raise ex
        
    def select_device(self,window_title: str) -> None:
        try:
            self.windows.clear_anchor()
            #wait until new screen exist
            select_device_screen=self.wait_until_element_window_exist("type:Window",window_title,return_element=True)
            #device input
            input_device_list=self.windows.get_elements(self.baan_elements["bw_input_device"],search_depth=20)
            input_device = self.return_item_by_index(input_device_list,10)
            
                #####focus on field
                
            sleep(std_3s_wait)
                #self.windows.set_value(input_device,"b2Excel")
                #self.windows.click("class:TsTextWinClass and type:Edit and handle:"+str(input_device.item.NativeWindowHandle)+" and offset:1,1")
                #self.windows.click(input_device)
            #write device
            self.write_and_read_information(input_device,"b2Excel",interval=0.7,wait_time=0.5)
            self.windows.send_keys(input_device,"{TAB}",interval=0.7,wait_time=0.5)
            
                #####click continue
                
                #buttons_list = self.windows.get_elements("type:Button and class:TsPushButtonWinClass",search_depth=20)
                #button_continue_locator=self.return_item_by_name(buttons_list,"Continue")
                #self.windows.click(button_continue_locator)
                #self.windows.click('type:Button and offset:1,1 and class:TsPushButtonWinClass and index:0')
            sleep(std_3s_wait)
            self.windows.screenshot(select_device_screen, "baan_select_device_orders.png")
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
        
    def return_item_by_name(self, elements_list: list, key_name: str) -> None:
        try:
            counter_windows=0
            for item in elements_list:
                if key_name in item.name:
                    counter_windows=counter_windows+1
                    return item
            if counter_windows==0:
                raise Exception("windows- return_item_by_name cannot find the criteria")
        except Exception as ex:
            raise ex
        
    def return_item_by_index(self, elements_list: list, element_index: int) -> None:
        try:
            if len(elements_list)>=element_index:
                return elements_list[element_index]
            else:
                raise Exception("The requested element index does not exist")
        except Exception as ex:
            raise ex
        
    def write_and_read_information(self, element_or_locator, text:str, interval=0.7, wait_time=0.5) -> None:
        try:
            counter_windows=0
            element_status=False
            while counter_windows<3:
                self.windows.send_keys(element_or_locator,text,interval=interval,wait_time=wait_time)
                current_text=self.windows.get_value(element_or_locator)
                if text.lower().strip()==current_text.lower().strip():
                    element_status=True
                    break
                else:
                    current_text=self.windows.set_value(element_or_locator,"")
                    sleep(std_1s_wait)
                    counter_windows=counter_windows+1
            if not element_status:
                raise Exception("The text cannot be written correctly")
        except Exception as ex:
            raise ex
    
