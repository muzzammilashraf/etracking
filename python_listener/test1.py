from websocket import create_connection
import mysql.connector
import json
from Parser import Parser

acceptable_devices = []

if __name__ == "__main__":
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT imei FROM device_details")
    myresult = mycursor.fetchall()
    for row in myresult:
        acceptable_devices.append(row['imei'])
    ws = create_connection("ws://localhost:5001")
    register = {
        'type': 'parser',
        'id': '0001'
    }
    wqe = {
        'opcode': 'register',
        'data': json.dumps(register),
    }
    ws.send(json.dumps(wqe))
    imei = '350424066309087'
    if(imei not in acceptable_devices):
        exit()
    new_str = "00000000000000db0804000000f9cebbc97000000000000000000000000000000000000903f0000100b30006423024180000cd98b7ce283b4300000900570000000001827291fb900027ef25420ed0fee6001e0060060000000903f0000100b3000642301b180000cd98b7ce283b4300000900570000000001827292e5f00027ef25420ed0fee6000d0060060000000903f0000100b30006423020180000cd98b7ce283b4300000900570000000001827293d4380027ef25420ed0fee6000d0060070000000903f0000100b3000642301e180000cd98b7ce283b4300000900570000040000f6f1"
    parser = Parser(imei, new_str)
    # parser.insert_records(mydb)
    avl_data = []
    for x in range(parser.num_data_1):
        tmp_avl_data = {
            'dev_id': parser.dev_id,
            'timestamp': parser.avl_data.gpsrecords[x].timestamp,
            'priority': parser.avl_data.gpsrecords[x].priority,
            'lng': parser.avl_data.gpsrecords[x].lng,
            'lat': parser.avl_data.gpsrecords[x].lat,
            'alt': parser.avl_data.gpsrecords[x].alt,
            'angle': parser.avl_data.gpsrecords[x].alt,
            'speed': parser.avl_data.gpsrecords[x].speed
        }
        avl_data.append(json.dumps(tmp_avl_data))
    wqe = {
        'opcode': 'avl_data',
        'data_count': parser.num_data_1,
        'data': avl_data
    }
    ws.send(json.dumps(wqe))   