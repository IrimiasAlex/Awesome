import json
import requests

from .Sharepoint import Sharepoint


class Excel(Sharepoint):
    def __init__(self, *args, **kwargs):
        Sharepoint.__init__(self, *args, **kwargs)

    def get_table_data_from_file(
        self,
        site_id: str,
        site_drive_id: str,
        site_drive_item_id: str,
        workbook_table_name: str,
    ):
        try:
            site_id = site_id.strip()
            site_drive_id = site_drive_id.strip()
            site_drive_item_id = site_drive_item_id.strip()
            workbook_table_name = workbook_table_name.strip()
            request_url = self.graph_api_endpoint.format(
                "/v1.0/sites/"
                + site_id
                + "/drives/"
                + site_drive_id
                + "/items/"
                + site_drive_item_id
                + "/workbook/tables/"
                + workbook_table_name
                + "/range?$select=text"
            )
            response = requests.get(url=request_url, headers=self.headers)
            response.raise_for_status()
            jsonData = json.loads(response.content)
            return jsonData["text"]
        except Exception as ex:
            raise ex

    def get_table_names_from_file(
        self, site_id: str, site_drive_id: str, site_drive_item_id: str
    ):
        try:
            site_id = site_id.strip()
            site_drive_id = site_drive_id.strip()
            site_drive_item_id = site_drive_item_id.strip()
            request_url = self.graph_api_endpoint.format(
                "/v1.0/sites/"
                + site_id
                + "/drives/"
                + site_drive_id
                + "/items/"
                + site_drive_item_id
                + "/workbook/tables"
            )
            response = requests.get(url=request_url, headers=self.headers)
            response.raise_for_status()
            jsonData = json.loads(response.content)
            return jsonData["value"]
        except Exception as ex:
            raise ex

    def post_table_data_from_json(
        self,
        site_id: str,
        site_drive_id: str,
        site_drive_item_id: str,
        workbook_table_name: str,
        table_data: dict,
    ):
        try:
            site_id = site_id.strip()
            site_drive_id = site_drive_id.strip()
            site_drive_item_id = site_drive_item_id.strip()
            workbook_table_name = workbook_table_name.strip()
            request_url = self.graph_api_endpoint.format(
                "/v1.0/sites/"
                + site_id
                + "/drives/"
                + site_drive_id
                + "/items/"
                + site_drive_item_id
                + "/workbook/tables/"
                + workbook_table_name
                + "/rows"
            )
            jsonTableData = json.dumps(table_data)
            response = requests.post(
                url=request_url, headers=self.headers, data=jsonTableData
            )
            response.raise_for_status()
        except Exception as ex:
            raise ex

    def patch_table_row_from_json(
        self,
        site_id: str,
        site_drive_id: str,
        site_drive_item_id: str,
        workbook_table_name: str,
        rowData: dict,
        rowIndex: str,
    ):
        try:
            site_id = site_id.strip()
            site_drive_id = site_drive_id.strip()
            site_drive_item_id = site_drive_item_id.strip()
            workbook_table_name = workbook_table_name.strip()
            request_url = self.graph_api_endpoint.format(
                "/v1.0/sites/"
                + site_id
                + "/drives/"
                + site_drive_id
                + "/items/"
                + site_drive_item_id
                + "/workbook/tables/"
                + workbook_table_name
                + "/rows/$/ItemAt(index="
                + rowIndex
                + ")"
            )
            jsonRowData = json.dumps(rowData)
            response = requests.patch(
                url=request_url, headers=self.headers, data=jsonRowData
            )
            response.raise_for_status()
        except Exception as ex:
            raise ex
    
    def refresh_all_excel_file(self, site_id: str, site_drive_id: str, site_drive_item_id: str, worksheet_id: str):
        try:
            site_id = site_id.strip()
            site_drive_id = site_drive_id.strip()
            site_drive_item_id = site_drive_item_id.strip()
            worksheet_id = worksheet_id.strip()
            request_url = self.graph_api_endpoint.format('/v1.0/sites/' + site_id + '/drives/' + site_drive_id + '/items/' + site_drive_item_id + '/workbook/worksheets/'+worksheet_id+'/pivotTables/refreshAll')
            response = requests.post(url = request_url, headers = self.headers)
            if(response.status_code != 204):
                json_data = json.loads(response.content)
                raise Exception("Error on refresh all the excel file")
        except Exception as ex:
            raise ex
        
    def remove_excel_file(self, site_id: str, site_drive_id: str, site_drive_item_id: str):
        try:
            site_id = site_id.strip()
            site_drive_id = site_drive_id.strip()
            site_drive_item_id = site_drive_item_id.strip()
            request_url = self.graph_api_endpoint.format('/v1.0/sites/' + site_id + '/drives/' + site_drive_id + '/items/' + site_drive_item_id)
            response = requests.delete(url = request_url, headers = self.headers)
            if(response.status_code != 204):
                json_data = json.loads(response.content)
                raise Exception("Error on delete the excel file")
        except Exception as ex:
            raise ex