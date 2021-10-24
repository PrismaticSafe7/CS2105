import sys
import socket

key_dict = {}
counter_dict = {}

class WebServer:
    def __init__(self,port):
        self.port = port

    def ServerSocket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("", self.port))
        self.socket.listen(1)

        while True:
            try:
                connection, address = self.socket.accept()
                self.Client_Handler(connection)
            except KeyboardInterrupt:
                break

        self.end()

    def end(self):
        self.socket.socket.shutdown(socket.SHUT_RDWR)
        self.socket.socket.close()
        exit(0)

    def Client_Handler(self, connection):
        packet = b""
        noMoreRequest = False
        endOfRequest = False
        while not endOfRequest:
            input = connection.recv(1024)
            if not input:
                noMoreRequest = True
            else:
                packet += input

            while True:
                packet, request = self.Request(packet)

                if request is None:
                    break

                else:
                    response = self.Response(request, key_dict, counter_dict)
                    connection.sendall(response)

            if noMoreRequest and not packet:
                endOfRequest = True

    def Request(self, packet):
        request = {}

        headerlength = packet.find(b"  ")

        if headerlength == -1:
            return packet,None

        header = packet[:headerlength].decode().split()
        data = packet[headerlength+2:]

        request["method"] = header[0].upper()
        request["path"] = header[1].split("/")[1]
        request["key"] = header[1].split("/")[2]

        for i in range(2, len(header)):
            header[i] = header[i].lower()

        if "content-length" in header:

            for j in range(2, len(header) - 1):
                if header[j] == "content-length":
                    if header[j+1].isdigit():
                        content_length = int(header[j+1])
                        break

            content_length = int(content_length)

            if len(data) < content_length:
                return packet, None

            else:
                content = data[:content_length]
                packet = data[content_length:]
                request["content"] = content

        else:
            packet = data

        return packet, request

    def Response(self, reply, key_dict, counter_dict):
        method = reply["method"]
        path = reply["path"]
        key = reply["key"]
        statuses = {200: b"200 OK ",
                  404: b"404 NotFound  ",
                  405: b"405 MethodNotAllowed  "
                  }

        if method == "GET":
            if path == "key":
                if key not in key_dict:
                    return statuses[404]
                contentLength = key_dict[key][0]
                content = key_dict[key][1]
                status = 200

            elif path == "counter":
                if key not in counter_dict:
                    content = b"0"
                    contentLength = 1
                    status = 200
                else:
                    content = str(counter_dict[key]).encode()
                    contentLength = 1
                    status = 200
            else:
                return statuses[404]

            response = statuses[status] + b"content-length " + str(contentLength).encode() + b"  " + content


        elif method == "POST":
            if path == "key":
                data = reply["content"]
                if key in key_dict and key_dict[key] is None:
                    return statuses[405]

                if data != None:
                    dataLength = len(data)
                    content = data
                    key_dict[key] = [dataLength,content]
                    return statuses[200] + b" "
                else:
                    key_dict[key] = [0,None]

            elif path == "counter":
                if key in counter_dict:
                    counter_dict[key] += 1
                    return statuses[200] + b" "
                else:
                    counter_dict[key] = 1
                    return statuses[200] + b" "

            else:
                return statuses[404]


        elif method == "DELETE":

            if path == "key":
                if key not in key_dict:
                    return statuses[404]

                else:
                    content = key_dict[key][1]
                    status = 200
                    contentLength = key_dict[key][0]
                    del key_dict[key]
                    response = statuses[status] + b"content-length " + str(contentLength).encode() + b"  " + content

        else:
            return statuses[404]

        return response


if __name__ == "__main__":
    portNumber = int(sys.argv[1])
    server = WebServer(portNumber)
    server.ServerSocket()



