from dataclasses import replace
from datetime import timedelta
from importlib import resources
from multiprocessing.connection import wait
from time import sleep
from Browser import ElementState, SelectAttribute
from . import ETQWeb
from Emerson.variables import std_15s_wait
from Emerson.variables import std_5s_wait
from Emerson.variables import std_1s_wait
from Emerson.variables import std_60s_wait
from RPA.Desktop import Desktop

class Etq(ETQWeb):
    def __init__(self, *args, **kwargs):
        ETQWeb.__init__(self, *args, **kwargs)
        self.etq_elements = self.actions.read_configuration("data/etq_web_config/etq_elements.json")
        self.desktop = Desktop()
        

    def login_into_etq_chrome(self, etq_responsibility_link: str, user_name: str, password: str):
        try:
            etq_responsibility_link = etq_responsibility_link.strip()
            user_name = user_name.strip()
            password = password.strip()
            self.delete_all_cookies()
            self.go_to(etq_responsibility_link)
            self.delete_all_cookies()
            self.wait_for_elements_state(self.etq_elements["user_name_input_locator"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.etq_elements["user_name_input_locator"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.etq_elements["user_name_input_locator"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            sleep(std_5s_wait)
            self.type_text(self.etq_elements["user_name_input_locator"], txt=user_name,clear=True)
            self.type_text(self.etq_elements["password_input_locator"], txt=password,clear=True)
            self.click(self.etq_elements["login_button_locator"],delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_1s_wait)
        except Exception as ex:
            raise ex
    
    def logout_clarity(self):
        try:
            self.wait_for_elements_state(self.clarity_elements["logout_button_locator"],
                                        state=ElementState.stable,
                                        timeout=std_5s_wait,
            )
            self.wait_for_elements_state(self.clarity_elements["logout_button_locator"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.click(self.clarity_elements["logout_button_locator"],delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_1s_wait)
        except Exception as ex:
            raise ex
             
    def close_tab(self):
        try:
            self.wait_for_elements_state(self.etq_elements["close_customer_issue_button"],
                                        state=ElementState.visible,
                                        timeout=self.library_timeout,
            )
            self.click(self.etq_elements["close_customer_issue_button"],delay=timedelta(seconds=std_1s_wait))
            self.click(self.etq_elements["close_customer_issue_button"],delay=timedelta(seconds=std_1s_wait))
            self.click(self.etq_elements["close_tab_button"],delay=timedelta(seconds=std_1s_wait))
            self.click(self.etq_elements["close_tab_button"],delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_1s_wait)
        except Exception as ex:
            raise ex
        
    def go_to_application(self, application_locator: str):
        try:
            self.wait_for_elements_state(self.etq_elements[application_locator],
                                            state=ElementState.visible,
                                            timeout=self.library_timeout,
                )
            self.click(self.etq_elements[application_locator],delay=timedelta(seconds=std_1s_wait))
        except Exception as ex:
            raise ex
    
    def press_button(self, locator_name: str):
        try:
            self.wait_for_elements_state(self.etq_elements[locator_name],
                                            state=ElementState.visible,
                                            timeout=self.library_timeout,
                )
            self.click(self.etq_elements[locator_name],delay=timedelta(seconds=std_1s_wait))
        except Exception as ex:
            raise ex
        
    def read_field(self, locator_name: str):
        try:
            self.wait_for_elements_state(self.etq_elements[locator_name],
                                            state=ElementState.visible,
                                            timeout=self.library_timeout,
                )
            text = self.get_text(self.etq_elements[locator_name])
            return text
        except Exception as ex:
            raise ex
        
    def write_field(self, locator_name: str, txt_to_write: str):
        try:
            self.wait_for_elements_state(self.etq_elements[locator_name],
                                            state=ElementState.visible,
                                            timeout=self.library_timeout,
                )
            self.type_text(self.etq_elements[locator_name], txt=txt_to_write, clear=True)
        except Exception as ex:
            raise ex

    def wait_for_element_visible(self, locator_name: str, wait_timeout: int):
        try:
            self.wait_for_elements_state(self.etq_elements[locator_name],
                                            state=ElementState.visible,
                                            timeout=wait_timeout,
                )
        except Exception as ex:
            raise ex
        
    def read_field_custom_timeout(self, locator_name: str, custom_timeout: int):
        try:
            self.wait_for_elements_state(self.etq_elements[locator_name],
                                            state=ElementState.visible,
                                            timeout=custom_timeout,
                )
            text = self.get_text(self.etq_elements[locator_name])
            return text
        except Exception as ex:
            raise ex
        
    def fill_calendar(self, locator_name: str, day: str, month: int, year: str):
        try:
            self.wait_for_elements_state(self.etq_elements[locator_name],
                                            state=ElementState.visible,
                                            timeout=10,
                )
            self.click(self.etq_elements[locator_name],delay=timedelta(seconds=std_1s_wait))
            self.select_options_by(self.etq_elements["month_calendar"], SelectAttribute.index, month-1)
            self.select_options_by(self.etq_elements["year_calendar"], SelectAttribute.label, year)
            a = self.get_elements(self.etq_elements["day_calendar"])
            for i in a:
                if self.get_text(i) == day:
                    self.click(i,delay=timedelta(seconds=std_1s_wait))
                    return True
            return False    
        except Exception as ex:
            raise ex
        
    def select_dropdown(self,locator_name1: str, locator_name2: str, subject: str, field = 0, second_time = False):
        try:
            self.wait_for_elements_state(self.etq_elements[locator_name1],
                                            state=ElementState.visible,
                                            timeout=10,
                )
            if second_time:
                self.click(self.etq_elements[locator_name1],delay=timedelta(seconds=std_1s_wait))
            self.click(self.etq_elements[locator_name1],delay=timedelta(seconds=std_1s_wait))
            self.type_text(self.etq_elements[locator_name2],  subject)
            sleep(1)
            if field == 0: 
                list_elem = self.get_elements(self.etq_elements["subject_input_search_locator"])
                for x in list_elem:
                    option = self.get_text(x)
                    option = option.replace("\xa0", "")
                    if option == subject:
                        self.click(x,delay=timedelta(seconds=std_1s_wait))
                        return True
            elif field == 1:
                list_elem = self.get_elements(self.etq_elements["responsible_location_search_locator"])
                for x in list_elem:
                    option = self.get_text(x)
                    option = option.replace("\xa0", "")
                    if subject in option:
                        self.click(x,delay=timedelta(seconds=std_1s_wait))
                        return True
            elif field == 2:
                list_elem = self.get_elements(self.etq_elements["return_type_input_search_locator"])
                for x in list_elem:
                    option = self.get_text(x)
                    option = option.replace("\xa0", "")
                    if subject in option:
                        self.click(x,delay=timedelta(seconds=std_1s_wait))
                        return True  
            else:
                return False    
        except Exception as ex:
            raise ex
    
    def search_screen(self, locator_name, customer_look_up: str, locator_id):
        try:
            self.wait_for_elements_state(self.etq_elements[locator_name],
                                            state=ElementState.visible,
                                            timeout=10,
                )
            self.click(self.etq_elements[locator_name],delay=timedelta(seconds=std_1s_wait))
            sleep(3)
            list_elem = self.get_elements(self.etq_elements["search_input"])
            self.type_text(list_elem[0], customer_look_up)
            sleep(6)
            list_elem2 = self.get_elements(self.etq_elements[locator_id])
            for x in range(len(customer_look_up)):
                if customer_look_up[0] == '0':
                    customer_look_up = customer_look_up.replace(customer_look_up[0],"",1)
                elif customer_look_up[0] != '0':
                    break
            option: str
            count = 0
            for a in list_elem2:
                option = self.get_text(a)
                for y in range(len(option)):
                    if option[0] == '0':
                        option = option.replace(option[0],"",1)
                    elif option[0] != '0':
                        break
                if option == customer_look_up:
                    sleep(4)
                    self.click(a,delay=timedelta(seconds=std_1s_wait))
                    sleep(3)
                    self.click(self.etq_elements["search_ok_button"],delay=timedelta(seconds=std_1s_wait))
                    break
                else:
                    if len(list_elem2) == count:
                        raise "Customer look up account number was not found."
                    else:
                        count = count + 1
                        continue
        except Exception as ex:
            raise ex
    
    def check_search_results(self, expected_result: str):
        try:
            list_elem = self.get_elements(self.etq_elements["customer_lookup_value"])
            for i in list_elem:
                value = self.get_text(i)
                if expected_result in value:
                    return expected_result
            return ""
                
        except Exception as ex:
            raise ex