import logging
from RPA.Robocorp.WorkItems import State, WorkItems

class WorkItemsActions(WorkItems):
    def __init__(self, *args, **kwargs):
        WorkItems.__init__(self, *args, **kwargs)
        self.logger = logging.getLogger(__file__)
        
    def load_work_items(self, item_list: list):
        try:
            self.get_input_work_item()
            for item in item_list:
                self.create_output_work_item()
                self.set_work_item_payload(item)
                self.save_work_item()
        except Exception as ex:
            raise ex
    
    def release_queue_work_item(self, work_item_status: tuple):
        current_work_item_status = State.FAILED
        try:
            temp_work_item_status = work_item_status[0].strip().lower()
            if temp_work_item_status == "pass":
                current_work_item_status = State.DONE
            self.get_input_work_item()
            self.release_input_work_item(current_work_item_status)
        except Exception as ex:
            raise ex