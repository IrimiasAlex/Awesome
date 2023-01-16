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

class BaanBw(BaanDesktop):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.baan_elements = self.actions.read_configuration("data/baan_desktop_config/baan_bw_elements.json")

    def open_file_run_program(self) -> None:
        try:
            self.windows.clear_anchor()
            ##get windows main screen becs
            self.user_main_screen = self.wait_until_element_window_exist("type:Window","User",control_main_screen=True)
            sleep(std_1s_wait)
            #get file -> run program
            self.windows.click(self.baan_elements["bw_button_file_locator"])
            sleep(std_3s_wait)
            run_program_button_search=self.windows.get_elements(self.baan_elements["bw_button_run_program_locator"],search_depth=20)
            run_program_button = self.return_item_by_name(run_program_button_search,"Run")
            self.windows.click(run_program_button)
            self.windows.screenshot(self.user_main_screen, "baan_open_file_run_program.png")
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
        
    def unblock_sales_orders_yes_no(self,window_title: str) -> None:
        try:
            self.windows.clear_anchor()
            #wait until new screen exist
            unblock_sales_orders_yes_no_locator = self.wait_until_window_exists(window_title,15)
            #control new window
            self.unblock_sales_orders_yes_no_screen=self.windows.control_window(unblock_sales_orders_yes_no_locator)
            #get button
            buttons_list = self.windows.get_elements("type:Button and class:TsPushButtonWinClass",search_depth=20)
            button_no_locator=self.return_item_by_name(buttons_list,"Yes")
            #####focus on input field
            offsetx = button_no_locator.xcenter 
            offsety = button_no_locator.ycenter
            self.desktop.click(f"coordinates:{offsetx},{offsety}") 
            #self.windows.click(button_no_locator)
            self.windows.screenshot(self.unblock_sales_orders_yes_no_screen, "baan_unblock_sales_orders_yes_no.png")
        except Exception as ex:
            raise ex
        
    def unblock_sales_orders(self,window_title: str,order_number: str, customer_number: str) -> None:
        try:
            self.windows.clear_anchor()
            #wait until new screen exist
            unblock_sales_orders_locator = self.wait_until_window_exists(window_title,15)
            #control new window
            self.unblock_sales_orders_screen=self.windows.control_window(unblock_sales_orders_locator)
            #get button ok
            buttons_list = self.windows.get_elements("type:Button and class:TsPushButtonWinClass",search_depth=20)
            button_ok_locator=self.return_item_by_name(buttons_list,"OK")
            if not bool(button_ok_locator):
                raise Exception("Sales order field cannot be found")
            #get input sales order
            sales_order_input_list = self.windows.get_elements("type:Edit and class:TsTextWinClass",search_depth=20)
            sales_order_input = self.return_item_by_index(sales_order_input_list,0)
            self.write_and_read_information(sales_order_input,order_number,interval=0.7,wait_time=0.5)
            #####click ok
            button_ok_offsetx = button_ok_locator.xcenter 
            button_ok_offsety = button_ok_locator.ycenter
            self.desktop.click(f"coordinates:{button_ok_offsetx},{button_ok_offsety}") 
            #check data and select yes or no
            sleep(std_3s_wait)
            order_input_list = self.windows.get_elements("type:Edit and class:TsTextWinClass",search_depth=20)
            #locate list yes and no
            order_yes_no_button_list = self.windows.get_elements("type:Button and class:TsArrowButtonWinClass",search_depth=20)
            first_yes_no_drop_down_button =  self.return_item_smaller_x_y_location(order_yes_no_button_list)
            #get order number field
            order_number_input_item = self.return_item_by_value(order_input_list,order_number)
            #customer_number_input_item = self.return_item_by_value(order_input_list,customer_number)
            #get field
            input_yes_no_locator = self.return_item_by_x_location_range(order_input_list,int(order_number_input_item.ycenter),(int(first_yes_no_drop_down_button.xcenter)-45),(int(first_yes_no_drop_down_button.xcenter)+5))
            #click input yes and no
            input_yes_no_input_offsetx = input_yes_no_locator.xcenter 
            input_yes_no_input_offsety = input_yes_no_locator.ycenter
            self.desktop.click(f"coordinates:{input_yes_no_input_offsetx},{input_yes_no_input_offsety}") 
            self.write_and_read_information(input_yes_no_locator,"No",interval=0.7,wait_time=0.5)
            self.windows.screenshot(self.unblock_sales_orders_screen, "customer "+customer_number+" order "+order_number+".png")
            self.windows.send_keys(self.unblock_sales_orders_screen,"{Ctrl}s",wait_time=1.5)
            self.windows.screenshot(self.unblock_sales_orders_screen, "baan_unblock_sales_orders.png")
            self.windows.send_keys(self.unblock_sales_orders_screen,"{Ctrl}s",wait_time=1.5)
            self.windows.send_keys(self.unblock_sales_orders_screen,"{Ctrl}f",wait_time=1.5)
        except Exception as ex:
            raise ex
        
    def select_device(self,window_title: str) -> None:
        try:
            self.windows.clear_anchor()
            #wait until new screen exist
            select_device_screen=self.wait_until_element_window_exist("type:Window",window_title,return_element=True)
            sleep(std_3s_wait)
            #device input
            input_device_list=self.windows.get_elements(self.baan_elements["bw_input_device"],search_depth=20)
            input_device = self.return_item_by_index(input_device_list,10)
            #####focus on input field
            offsetx = input_device.xcenter 
            offsety = input_device.ycenter
            self.desktop.click(f"coordinates:{offsetx},{offsety}") 
            sleep(std_3s_wait)
            #write device
            self.write_and_read_information(input_device,"b2Excel",interval=0.7,wait_time=0.5)
            self.windows.send_keys(input_device,"{TAB}",interval=0.7,wait_time=0.5)
            #click continue
            #buttons_list = self.windows.get_elements("type:Button",search_depth=20)
            #button_continue_locator=self.return_item_by_name(buttons_list,"Continue")
            self.windows.click('type:Button and name:Continue and depth:20')
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
    
    def return_item_by_x_location_range(self, elements_list: list, y_location: int, x_start_location: int, x_end_location: int) -> None:
        try:
            counter_windows=0
            if not len(elements_list)>0:
                raise Exception("windows- return_item_by_x_location_range item list cannot be empty")
            for item in elements_list:
                if int(item.ycenter) == y_location and (x_start_location <= int(item.xcenter) and x_end_location >= int(item.xcenter)):
                    counter_windows=counter_windows+1
                    return item
            if counter_windows==0:
                raise Exception("windows- return_item_by_x_location_range cannot find the criteria")
        except Exception as ex:
            raise ex
        
    def return_item_smaller_x_y_location(self, elements_list: list) -> None:
        try:
            counter_windows=0
            if not len(elements_list)>0:
                raise Exception("windows- return_item_smaller_x_y_location item list cannot be empty")
            smaller_item = elements_list[0]
            for item in elements_list:
                counter_windows=counter_windows+1
                if int(item.xcenter) <= int(smaller_item.xcenter) and int(item.ycenter) <= int(smaller_item.ycenter):
                    smaller_item = item
            if counter_windows==0:
                raise Exception("windows- return_item_smaller_x_y_location cannot find the criteria")
            return smaller_item
        except Exception as ex:
            raise ex
        
    def return_item_by_value(self, elements_list: list, value: str) -> None:
        try:
            counter_windows=0
            for item in elements_list:
                counter_windows=counter_windows+1
                current_text=self.windows.get_value(item)
                if value.strip().lower() == current_text.strip().lower():
                    return item
            if counter_windows==0:
                raise Exception("windows- return_item_by_value cannot find the criteria")
        except Exception as ex:
            raise ex
        
    def return_item_by_index(self, elements_list: list, element_index: int) -> None:
        try:
            if len(elements_list)>=element_index:
                return elements_list[element_index]
            else:
                raise Exception("windows- return_item_by_index The requested element index does not exist")
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
                raise Exception("windows - write_and_read_information The text cannot be written correctly")
        except Exception as ex:
            raise ex
    
