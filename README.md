# HTTP-server
Handles requests in HTTP format using TCP
<br>
The server supports the following features:
- Sending text and image files requested using HTTP format, all the available files should be saved in a directory called 'files'. that's in the same location as 'HTTP_server.py'
- Connection field: 'keep-alive' or 'close'
- Closing the connection if a request times out, if a request is empty or if a request is not in HTTP format
- A request for a file named '/' is redirected to a file named 'index.html'
- Supported HTTP codes:
  - 200 OK
  - 301 Moved Permanently
  - 404 Not Found
<br>

## Command Line Arguments and Testing
Run the server using its port's number as the first and only argument. <br>
Test the server using your online browser by typing '[Server IP]:[Server port][RequestedFilePath]' into the address bar.
