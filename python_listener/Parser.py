from AvlData import AvlData

class Parser:
    
    def insert_records(self, mydb):
        mycursor = mydb.cursor()
        sql = "INSERT INTO records VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = []
        for x in range(self.num_data_1):
            tuple_val = (None, self.dev_id, self.avl_data.gpsrecords[x].timestamp, self.avl_data.gpsrecords[x].lng, self.avl_data.gpsrecords[x].lat, self.avl_data.gpsrecords[x].alt, self.avl_data.gpsrecords[x].angle, self.avl_data.gpsrecords[x].speed)
            val.append(tuple_val)
        mycursor.executemany(sql, val)
        mydb.commit()

    def reply_to_device(self, sock):
        reply = self.num_data_1.to_bytes(1, "big")
        sock.send(reply)

    def __init__(self, imei, server_data):
        self.dev_id = imei
        self.preamble = int(server_data[:8], 16)
        self.data_field_length = int(server_data[8:16], 16)
        x_length = self.data_field_length - 3
        self.codec_id = int(server_data[16:18], 16)
        self.num_data_1 = int(server_data[18:20], 16)
        self.avl_data = AvlData(self.num_data_1, server_data[20:(x_length*2)+20])
        self.num_data_2 = int(server_data[(x_length*2)+20:(x_length*2)+22], 16)
        self.crc_16 = int(server_data[(x_length*2)+22:(x_length*2)+30], 16)