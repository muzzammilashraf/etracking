class NRecord:

    def __init__(self, id, value) -> None:
        self.id = int(id, 16)
        self.value = int(value, 16)
        
class N1Records:

    def parse(self, data):
        self.records = [0] * self.num_data
        bytes_covered = 0
        for x in range(0, self.num_data):
            self.records[x] = NRecord(data[bytes_covered:bytes_covered+2], data[bytes_covered+2:bytes_covered+4])
            bytes_covered = bytes_covered + 4

    def __init__(self, num_data) -> None:
        self.num_data = num_data
        pass

class N2Records:

    def parse(self, data):
        self.records = [0] * self.num_data
        bytes_covered = 0
        for x in range(0, self.num_data):
            self.records[x] = NRecord(data[bytes_covered:bytes_covered+2], data[bytes_covered+2:bytes_covered+6])
            bytes_covered = bytes_covered + 6

    def __init__(self, num_data) -> None:
        self.num_data = num_data
        pass

class N4Records:

    def parse(self, data):
        self.records = [0] * self.num_data
        bytes_covered = 0
        for x in range(0, self.num_data):
            self.records[x] = NRecord(data[bytes_covered:bytes_covered+2], data[bytes_covered+2:bytes_covered+10])
            bytes_covered = bytes_covered + 10

    def __init__(self, num_data) -> None:
        self.num_data = num_data
        pass

class N8Records:

    def parse(self, data):
        self.records = [0] * self.num_data
        bytes_covered = 0
        for x in range(0, self.num_data):
            self.records[x] = NRecord(data[bytes_covered:bytes_covered+2], data[bytes_covered+2:bytes_covered+18])
            bytes_covered = bytes_covered + 18

    def __init__(self, num_data) -> None:
        self.num_data = num_data
        pass

class AvlDataRecords:

    def __init__(self, data):
        self.timestamp = int(data[:16], 16)
        self.priority = int(data[16:18], 16)
        self.lng = int(data[18:26], 16)
        self.lat = int(data[26:34], 16)
        self.alt = int(data[34:38], 16)
        self.angle = int(data[38:42], 16)
        self.sat = int(data[42:44], 16)
        self.speed = int(data[44:48], 16)
        self.event_id = int(data[48:50], 16)

class AvlData:

    def __init__(self, num_data, data):
        bytes_coverd = 0
        self.num_data = num_data
        self.gpsrecords = [''] * num_data
        self.n1records = [''] * num_data
        self.n2records = [''] * num_data
        self.n4records = [''] * num_data
        self.n8records = [''] * num_data
        for x in range(0, num_data):
            self.gpsrecords[x] = AvlDataRecords(data[bytes_coverd:bytes_coverd+50])
            bytes_coverd = bytes_coverd+52
            self.n1records[x] = N1Records(int(data[bytes_coverd:bytes_coverd+2], 16))
            bytes_coverd = bytes_coverd+2
            self.n1records[x].parse(data[bytes_coverd:bytes_coverd+(self.n1records[x].num_data*4)])
            bytes_coverd = bytes_coverd+(self.n1records[x].num_data*4)
            self.n2records[x] = N2Records(int(data[bytes_coverd:bytes_coverd+2], 16))
            bytes_coverd = bytes_coverd+2
            self.n2records[x].parse(data[bytes_coverd:bytes_coverd+(self.n2records[x].num_data*6)])
            bytes_coverd = bytes_coverd+(self.n2records[x].num_data*6)
            self.n4records[x] = N4Records(int(data[bytes_coverd:bytes_coverd+2], 16))
            bytes_coverd = bytes_coverd+2
            self.n4records[x].parse(data[bytes_coverd:bytes_coverd+(self.n4records[x].num_data*10)])
            bytes_coverd = bytes_coverd+(self.n4records[x].num_data*10)
            self.n8records[x] = N8Records(int(data[bytes_coverd:bytes_coverd+2], 16))
            bytes_coverd = bytes_coverd+2
            self.n8records[x].parse(data[bytes_coverd:bytes_coverd+(self.n8records[x].num_data*18)])
            bytes_coverd = bytes_coverd+(self.n8records[x].num_data*18)
            