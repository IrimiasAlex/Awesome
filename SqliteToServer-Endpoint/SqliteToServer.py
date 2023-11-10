import sqlite3
import requests
import json
from datetime import datetime

def execute_sql_query(query):
    conn = sqlite3.connect(r'C:\\path\\to\\the\\sqlite\\file.sqlite3')
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    results = cursor.fetchall()
    conn.close()
    return [dict(zip(columns, row)) for row in results]

def send_data_to_endpoint(json_data, endpoint_url):
    try:
        response = requests.post(endpoint_url, json=json_data, verify='C:\\Your\\Certificate.crt')
    except requests.exceptions.RequestException as e:
        response = None
    return response

def save_results_to_file(file_path, success, response_status_code, json_data_length):
    with open(file_path, 'a') as file:
        if success:
            file.write(f"File SqliteToServer.py transmitted {json_data_length} JSON files on {datetime.now().strftime('%Y-%m-%d')}\n")
        else:
            file.write(f"File SqliteToServer.py on {datetime.now().strftime('%Y-%m-%d')} failed to transmit JSON files, error: {response_status_code}\n")

def main():
    json_count = 0
    transformed_results = []
    for item in transformed_results:
        json_data += json.dumps(item, indent=2) + ",\n"
        json_count += 1
    queries = [
        """
        SELECT datetime(Readings.createdAt, 'localtime') AS ServerDate,
               Readings.id AS Id,
               Devices.host AS Host,
               Devices.port AS Port,
               Readings.convertedVolumeBaseConditions AS VolumeBaseCond,
               Readings.volumeMeasurementConditions AS VolumeMeasurementCond,
               Readings.temperature AS Temperature,
               Readings.relativePressure AS Pressure,
               datetime(Readings.dateTime, 'localtime') AS StationDate,
               Readings.batteryLevel AS BatteryLife,
               Readings.serialNumber AS SerialNo,
               Readings.volumeWithErrors as Vbt
        FROM Readings
        INNER JOIN Devices ON Readings.deviceId = Devices.id
        WHERE datetime(Readings.createdAt, 'localtime') > datetime('now','start of day', '+06 hours')
          AND datetime(Readings.createdAt, 'localtime') < datetime('now','start of day', '+10 hours')
          AND Readings.serialNumber LIKE '500%';
        """
    ]
    file_path = r'C:\\Path\\to\\the\\text\\file\\Results.txt'
    json_data = []

    for query in queries:
        result = execute_sql_query(query)
        transformed_results = [
            {
                "MsgId": row["Id"],
                "Did": row["SerialNo"],
                "Dip": row["Host"],
                "MeasTS": row["ServerDate"],
                "TransTS": row["StationDate"],
                "UCV": row["VolumeMeasurementCond"],
                "CV": row["VolumeBaseCond"],
                "ACV": row["Vbt"],
                "P": row["Pressure"],
                "T": row["Temperature"],
                "BL": row["BatteryLife"]
            }
            for row in result
        ]
        json_data.extend(transformed_results)

    endpoint_url = "https://EndpointHere"
    response = send_data_to_endpoint(json_data, endpoint_url)

    if response and response.status_code == 200:
        save_results_to_file(file_path, True, response.status_code, len(json_data))
    else:
        if response:
            error_message = f"File SqliteToServer.py on {datetime.now().strftime('%Y-%m-%d')} failed to transmit JSON files, error: {response.status_code}\n"
        else:
            error_message = f"File SqliteToServer.py on {datetime.now().strftime('%Y-%m-%d')} failed to transmit JSON files, error: No response\n"

        try:
            with open(file_path, 'a') as file:
                file.write(error_message)
        except Exception as e:
            print(f"An error occurred while writing to the file: {e}")

if __name__ == "__main__":
    main()
