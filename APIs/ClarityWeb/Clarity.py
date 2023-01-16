from datetime import timedelta
from importlib import resources
from multiprocessing.connection import wait
from time import sleep
from Browser import ElementState, SelectAttribute
from . import ClarityWeb
from Emerson.variables import std_15s_wait
from Emerson.variables import std_5s_wait
from Emerson.variables import std_3s_wait
from Emerson.variables import std_1s_wait
from Emerson.variables import std_60s_wait

class Clarity(ClarityWeb):
    def __init__(self, *args, **kwargs):
        ClarityWeb.__init__(self, *args, **kwargs)
        self.clarity_elements = self.actions.read_configuration("data/clarity_web_config/clarity_elements.json")

    def login_into_clarity_chrome(self, clarity_responsibility_link: str, clairty_logout_link: str, user_name: str, password: str) -> None:
        try:
            clairty_logout_link = clairty_logout_link.strip()
            clarity_responsibility_link = clarity_responsibility_link.strip()
            user_name = user_name.strip()
            password = password.strip()
            self.go_to(clairty_logout_link)
            self.delete_all_cookies()
            self.go_to(clarity_responsibility_link)
            self.delete_all_cookies()
            self.wait_for_elements_state(self.clarity_elements["user_name_input_locator"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["user_name_input_locator"],
                                        state=ElementState.focused,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["user_name_input_locator"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            sleep(std_3s_wait)
            self.type_text(self.clarity_elements["user_name_input_locator"], txt=user_name,clear=True)
            self.type_text(self.clarity_elements["password_input_locator"], txt=password,clear=True)
            self.click(self.clarity_elements["login_button_locator"],delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_1s_wait)
        except Exception as ex:
            raise ex
    
    def logout_clarity(self) -> None:
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
    
    def return_to_home_page(self) -> None:
        try:
            self.wait_for_elements_state(self.clarity_elements["home_icon_button_locator"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["home_icon_button_locator"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.click(self.clarity_elements["home_icon_button_locator"],delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_1s_wait)
        except Exception as ex:
            raise ex
        
    def open_projects_chrome(self) -> None:
        try:
            self.wait_for_elements_state(self.clarity_elements["home_button_locator"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["home_button_locator"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.click(self.clarity_elements["home_button_locator"],delay=timedelta(seconds=std_1s_wait))
            self.wait_for_elements_state(self.clarity_elements["projects_button_locator"],
                                    state=ElementState.stable,
                                    timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["projects_button_locator"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.click(self.clarity_elements["projects_button_locator"],delay=timedelta(seconds=std_1s_wait))
            
            self.wait_for_all_promises()
            sleep(std_1s_wait)
        except Exception as ex:
            raise ex
        
    def search_projects_chrome(self, clarity_project_name:str, clarity_project_id: str) -> None:
        try:
            locator_project_id = str(self.clarity_elements["id_button_locator"]).replace("{id}", clarity_project_id)
            clarity_project_name = clarity_project_name.strip()
            clarity_project_id = clarity_project_id.strip()
            self.wait_for_elements_state(self.clarity_elements["project_name_input_locator"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["project_name_input_locator"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.type_text(self.clarity_elements["project_name_input_locator"], txt=clarity_project_name,clear=True)
            self.type_text(self.clarity_elements["project_id_input_locator"], txt=clarity_project_id,clear=True)
            self.click(self.clarity_elements["filter_button_locator"],delay=timedelta(seconds=std_1s_wait))
            sleep(std_1s_wait)
            self.wait_for_elements_state(locator_project_id,
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(locator_project_id,
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.click(locator_project_id,delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_1s_wait)
        except Exception as ex:
            raise ex
        
    def main_properties_select_tasks(self) -> None:
        try:
            self.wait_for_elements_state(self.clarity_elements["tab_menu_tasks"],
                                        state=ElementState.stable,
                                        timeout=std_15s_wait,
            )
            self.wait_for_elements_state(self.clarity_elements["tab_menu_tasks"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.click(self.clarity_elements["tab_menu_tasks"],delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_3s_wait)
            self.wait_for_elements_state(self.clarity_elements["button_expand_filter_task"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["button_expand_filter_task"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.click(self.clarity_elements["button_expand_filter_task"],delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_1s_wait)
            self.wait_for_elements_state(self.clarity_elements["filter_button_locator"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["filter_button_locator"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
        except Exception as ex:
            raise ex
        
    def main_properties_select_team(self) -> None:
        try:
            self.wait_for_elements_state(self.clarity_elements["tab_menu_team"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["tab_menu_team"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.click(self.clarity_elements["tab_menu_team"],delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_3s_wait)
            self.wait_for_elements_state(self.clarity_elements["button_expand_filter_team"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["button_expand_filter_team"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.click(self.clarity_elements["button_expand_filter_team"],delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_1s_wait)
            self.wait_for_elements_state(self.clarity_elements["filter_button_locator"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["filter_button_locator"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
        except Exception as ex:
            raise ex
        
    def search_by_tasks_name(self, task_name: str) -> list:
        try:
            resources_assigned_list = []
            temp_locator = str(self.clarity_elements["id_button_locator"]).replace("{id}", task_name)
            self.wait_for_elements_state(self.clarity_elements["task_name_input_locator"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["task_name_input_locator"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.type_text(self.clarity_elements["task_name_input_locator"], txt=task_name,clear=True)
            self.wait_for_elements_state(self.clarity_elements["filter_button_locator"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["filter_button_locator"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            sleep(std_1s_wait)
            self.click(self.clarity_elements["filter_button_locator"],delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_3s_wait)
            try:
                self.wait_for_elements_state(temp_locator,
                                            state=ElementState.visible,
                                            timeout=std_15s_wait
                )
                self.wait_for_elements_state(temp_locator,
                                            state=ElementState.stable,
                                            timeout=std_15s_wait
                )
                self.wait_for_elements_state(temp_locator,
                                            state=ElementState.attached,
                                            timeout=std_15s_wait
                )
            except Exception:
                raise Exception("The task "+task_name+" is a new task")

            self.click(selector=temp_locator,delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_1s_wait)
            #get task status
            self.wait_for_elements_state(self.clarity_elements["task_status_locator"],
                                            state=ElementState.visible,
                                            timeout=std_15s_wait
                                        )
            task_status = self.get_selected_options(self.clarity_elements["task_status_locator"])
            if str(task_status).lower().strip() == "completed":
                raise Exception("Current task status completed")
            #get resources data
            resources = True
            resource_counter = 0
            while resources:
                item_text=""
                resource_counter=resource_counter+1
                resource_assigned_locator = str(self.clarity_elements["resource_assigned_name"]).replace("{counter}", str(resource_counter))
                try:
                    item_text = self.get_text(resource_assigned_locator)
                except Exception:
                    resources = False
                    pass
                if bool(item_text):
                    resources_assigned_list.append(item_text)
            return resources_assigned_list
        except Exception as ex:
            raise ex
        
    def clean_resource_etc_value(self, member_name: str) -> None:
        try:
            counter = 1
            temp_resource_name_locator = str(self.clarity_elements["resource_name_locator"]).replace("{resource_name}", member_name)
            temp_table_row_input_etc_value = str(self.clarity_elements["table_row_input_etc_value"]).replace("{counter}", str(counter))
            self.wait_for_elements_state(temp_resource_name_locator,
                                        state=ElementState.visible,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(temp_resource_name_locator,
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(temp_resource_name_locator,
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.click(temp_resource_name_locator,delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_1s_wait)
            while counter != 0:
                try:
                    self.wait_for_elements_state(temp_table_row_input_etc_value,
                                        state=ElementState.visible,
                                        timeout=std_15s_wait,
                    )
                    self.wait_for_elements_state(temp_table_row_input_etc_value,
                                                state=ElementState.stable,
                                                timeout=self.library_timeout,
                    )
                    self.wait_for_elements_state(temp_table_row_input_etc_value,
                                                state=ElementState.attached,
                                                timeout=self.library_timeout,
                    )
                    input_current_value = self.get_text(temp_table_row_input_etc_value)
                    if bool(str(input_current_value).strip()):
                        self.type_text(temp_table_row_input_etc_value,"0",timedelta(seconds=std_1s_wait),True)
                    sleep(std_1s_wait)
                    counter = counter+1
                    temp_table_row_input_etc_value = str(self.clarity_elements["table_row_input_etc_value"]).replace("{counter}", str(counter))
                except:
                    counter = 0
                    pass
            self.click(self.clarity_elements["button_save_and_return_etc"],delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_1s_wait)
        except Exception as ex:
            raise ex
        
    def complete_task(self) -> None:
        try:
            self.wait_for_elements_state(self.clarity_elements["task_status_locator"],
                                            state=ElementState.visible,
                                            timeout=self.library_timeout
                                        )
            task_status = self.get_selected_options(self.clarity_elements["task_status_locator"])
            if str(task_status).lower().strip() != "completed":
                self.select_options_by(self.clarity_elements["task_status_locator"],SelectAttribute["value"],"2")
            self.wait_for_elements_state(self.clarity_elements["input_porcent_complete"],
                                            state=ElementState.visible,
                                            timeout=self.library_timeout
                                        )
            self.wait_for_elements_state(self.clarity_elements["input_porcent_complete"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["input_porcent_complete"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.type_text(self.clarity_elements["input_porcent_complete"],"100",timedelta(seconds=std_1s_wait),True)
            self.wait_for_elements_state(self.clarity_elements["check_box_open_for_entry_time"],
                                            state=ElementState.visible,
                                            timeout=self.library_timeout
                                        )
            self.wait_for_elements_state(self.clarity_elements["check_box_open_for_entry_time"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["check_box_open_for_entry_time"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.uncheck_checkbox(self.clarity_elements["check_box_open_for_entry_time"])
            self.wait_for_all_promises()
            sleep(std_1s_wait)
            self.wait_for_elements_state(self.clarity_elements["button_save_and_return_etc"],
                                            state=ElementState.visible,
                                            timeout=self.library_timeout
                                        )
            self.wait_for_all_promises()
            sleep(std_1s_wait)
        except Exception as ex:
            raise ex
    
    def save_and_return_from_task(self) -> None:
        try:
            self.wait_for_elements_state(self.clarity_elements["button_save_and_return_etc"],
                                        state=ElementState.visible,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["button_save_and_return_etc"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["button_save_and_return_etc"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.click(self.clarity_elements["button_save_and_return_etc"],delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_3s_wait)
            self.wait_for_elements_state(self.clarity_elements["button_new_task"],
                                        state=ElementState.visible,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["button_new_task"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["button_new_task"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
        except Exception as ex:
            raise ex
    
    def search_team_member_by_name(self, member_name: str) -> None:
        try:
            
            temp_locator = str(self.clarity_elements["id_button_locator"]).replace("{id}", member_name)
            self.wait_for_elements_state(self.clarity_elements["team_resource_name_input_locator"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["team_resource_name_input_locator"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.type_text(self.clarity_elements["team_resource_name_input_locator"], txt=member_name,clear=True)
            self.wait_for_elements_state(self.clarity_elements["filter_button_locator"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["filter_button_locator"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.click(self.clarity_elements["filter_button_locator"],delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_1s_wait)
            try:
                self.wait_for_elements_state(temp_locator,
                                            state=ElementState.stable,
                                            timeout=std_15s_wait,
                )
                self.wait_for_elements_state(temp_locator,
                                            state=ElementState.attached,
                                            timeout=self.library_timeout,
                )
                self.wait_for_all_promises()
                sleep(std_1s_wait)
            except Exception as e:
                raise Exception(str("Team member does not exist: "+str(member_name)))
        except Exception as ex:
            raise ex
        
    def create_new_task(self, task_name: str, task_id: str, start_date: str, end_date: str) -> None:
        try:
            counter_id= 0
            task_created=True
            self.wait_for_elements_state(self.clarity_elements["task_name_input_locator"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout
            )
            self.wait_for_elements_state(self.clarity_elements["task_name_input_locator"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout
            )
            self.wait_for_elements_state(self.clarity_elements["button_new_task"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout
            )
            self.wait_for_elements_state(self.clarity_elements["button_new_task"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout
            )
            self.click(self.clarity_elements["button_new_task"],delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_1s_wait)
            self.wait_for_elements_state(self.clarity_elements["task_name_input_locator_2"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout
            )
            self.wait_for_elements_state(self.clarity_elements["task_name_input_locator_2"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout
            )
            self.type_text(self.clarity_elements["task_name_input_locator_2"], txt=task_name,clear=True)
            self.type_text(self.clarity_elements["task_id_input_locator_2"], txt=str(task_id+"-"+str(counter_id)),clear=True)
            self.type_text(self.clarity_elements["start_date_input_locator"], txt=start_date,clear=True)
            self.type_text(self.clarity_elements["finish_date_input_locator"], txt=end_date,clear=True)
            self.wait_for_elements_state(self.clarity_elements["button_save_and_return_locator"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["button_save_and_return_locator"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.click(self.clarity_elements["button_save_and_return_locator"],delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_1s_wait)
            while task_created:
                try:
                    counter_id = counter_id+1
                    element_states = self.get_element_states(self.clarity_elements["span_error_locator"])
                    if 'visible' in element_states:
                        self.type_text(self.clarity_elements["task_id_input_locator_2"], txt=str(task_id+"-"+str(counter_id)),clear=True)
                        self.wait_for_elements_state(self.clarity_elements["button_save_and_return_locator"],
                                                    state=ElementState.stable,
                                                    timeout=self.library_timeout
                        )
                        self.wait_for_elements_state(self.clarity_elements["button_save_and_return_locator"],
                                                    state=ElementState.attached,
                                                    timeout=self.library_timeout
                        )
                        self.click(self.clarity_elements["button_save_and_return_locator"],delay=timedelta(seconds=std_1s_wait))
                        self.wait_for_all_promises()
                        sleep(std_1s_wait)
                        element_states = self.get_element_states(self.clarity_elements["span_error_locator"])
                        if 'detached' in element_states:
                            task_created = False
                    else:
                        task_created = False
                except Exception:
                    pass
        except Exception as ex:
            raise ex
        
    def assign_new_resource(self, resource_name: str) -> None:
        try:
            temp_checkbox_locator = str(self.clarity_elements["check_box_resource_name"]).replace("{name}", resource_name)
            self.wait_for_elements_state(self.clarity_elements["button_assign_new_locator"],
                                        state=ElementState.visible,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["button_assign_new_locator"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["button_assign_new_locator"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.click(self.clarity_elements["button_assign_new_locator"],delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_3s_wait)
            self.wait_for_elements_state(self.clarity_elements["button_expand_filter_resources"],
                                        state=ElementState.visible,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["button_expand_filter_resources"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["button_expand_filter_resources"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.click(self.clarity_elements["button_expand_filter_resources"],delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_3s_wait)
            self.wait_for_elements_state(self.clarity_elements["resource_name_input"],
                                        state=ElementState.visible,
                                        timeout=self.library_timeout,
            )
            self.type_text(self.clarity_elements["resource_name_input"], txt=resource_name,clear=True)
            self.wait_for_elements_state(self.clarity_elements["filter_resources_locator"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["filter_resources_locator"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.click(self.clarity_elements["filter_resources_locator"],delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_1s_wait)
            self.wait_for_elements_state(temp_checkbox_locator,
                                        state=ElementState.visible,
                                        timeout=std_15s_wait,
            )
            self.wait_for_elements_state(temp_checkbox_locator,
                                        state=ElementState.stable,
                                        timeout=std_15s_wait,
            )
            self.wait_for_elements_state(temp_checkbox_locator,
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.click(temp_checkbox_locator,delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_1s_wait)
            self.wait_for_elements_state(self.clarity_elements["button_assign_name_locator"],
                                        state=ElementState.stable,
                                        timeout=self.library_timeout,
            )
            self.wait_for_elements_state(self.clarity_elements["button_assign_name_locator"],
                                        state=ElementState.attached,
                                        timeout=self.library_timeout,
            )
            self.click(self.clarity_elements["button_assign_name_locator"],delay=timedelta(seconds=std_1s_wait))
            self.wait_for_all_promises()
            sleep(std_1s_wait)
        except Exception as ex:
            raise Exception(str("Resource not available "+ resource_name+" exception: ") + str(ex))