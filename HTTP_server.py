import socket
import sys
import os.path

# request format
MIN_FIRST_LINE_LENGTH = 13
FIRST_LINE_START = "GET "
FIRTS_LINE_END = " HTTP/1.1"
SPACES_IN_FIRST_LINE = 2
LINE_END = "\r\n"
REQUEST_END = "\r\n\r\n"
FILE_NAME_INDEX = 4
SPACE = " "
DOT = "."
CONNECTION = "Connection: "

# connection statuses
CLOSE = "close"
KEEP_ALIVE = "keep-alive"

# files
FILES_DIR = "files/"
REDIRECT_REQUEST = "/redirect"
JPG_EXTENSION = ".jpg"
ICO_EXTENSION = ".ico"
INDEX_FILE_REQUEST = "/"
INDEX_FILE_NAME = "index.html"

# messages
OUTPUT_MESSAGE = "HTTP/1.1 200 OK\nConnection: "
CONTENT_LENGTH = "Content-Length: "
MISSING_FILE_MESSAGE = "HTTP/1.1 404 Not Found\nConnection: close\n\n"
REDIRECT_MESSAGE = "HTTP/1.1 301 Moved Permanently\nConnection: close\nLocation: /result.html\n\n"

# this function returns True if the given request (string) is in the correct format, False else
def is_in_format(request):
    if len(request) < MIN_FIRST_LINE_LENGTH or request[:FILE_NAME_INDEX] != FIRST_LINE_START:
        return False
    first_space_index = request.find(SPACE)
    second_space_index = request[first_space_index + 1:].find(SPACE) + first_space_index + 1
    line_end_index = request.find(LINE_END)
    if second_space_index == -1 or line_end_index - second_space_index != len(FIRTS_LINE_END) or request[second_space_index:line_end_index] != FIRTS_LINE_END or request.find(CONNECTION) == -1:
        return False
    return True

def main(argv):
    server = socket.socket(socket.SOCK_DGRAM)
    server.bind(('', int(argv[1])))
    server.listen(10)
    while True:
        client_socket, client_address = server.accept()
        client_socket.settimeout(1)
        connection = KEEP_ALIVE
        while connection == KEEP_ALIVE:
            request = ""
            client_timed_out = False
            received_empty_request = False
            while request.find(REQUEST_END) == -1 and not client_timed_out and not received_empty_request:
                try:
                    data = client_socket.recv(1)
                    if len(data) == 0:
                        received_empty_request = True
                    request += data.decode('utf-8')
                except socket.timeout:
                    client_timed_out = True
            if client_timed_out or received_empty_request:
                connection = CLOSE
                client_socket.close()
                continue
            print(request)
            if not is_in_format(request):
                connection = CLOSE
                client_socket.close()
                continue
            # the index for the requested connection status
            connection_index = request.find(CONNECTION) + len(CONNECTION)
            connection_end_index = request[connection_index:].find(LINE_END) + connection_index
            connection = request[connection_index:connection_end_index]
            if connection != KEEP_ALIVE and connection != CLOSE:
                connection = CLOSE
                client_socket.close()
                continue
            file_end_index = request[FILE_NAME_INDEX:].find(SPACE) + FILE_NAME_INDEX
            file_name = request[FILE_NAME_INDEX: file_end_index]
            if file_name == REDIRECT_REQUEST:
                client_socket.send(REDIRECT_MESSAGE.encode('utf-8'))
                connection = CLOSE
            else:
                if file_name == INDEX_FILE_REQUEST:
                    file_name = INDEX_FILE_NAME
                file_path = FILES_DIR + file_name
                file_extension = file_name[file_name.find(DOT):]
                if not os.path.exists(file_path):
                    client_socket.send(MISSING_FILE_MESSAGE.encode('utf-8'))
                    connection = CLOSE
                else:
                    message = (OUTPUT_MESSAGE + connection + LINE_END + CONTENT_LENGTH + str(os.path.getsize(file_path)) + LINE_END + LINE_END).encode('utf-8')
                    if file_extension == JPG_EXTENSION or file_extension == ICO_EXTENSION:
                        file = open(file_path, "rb")
                        message += file.read()
                    else:
                        file = open(file_path, "r")
                        message += file.read().encode('utf-8')
                    client_socket.send(message)
                    file.close()
            if connection == CLOSE:
                client_socket.close()

main(sys.argv)