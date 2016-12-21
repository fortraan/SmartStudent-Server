# SmartStudent-Server
The server for SmartStudent Desktop.

### Dependencies
Python 2.7  
[pickledb](https://github.com/patx/pickledb)  
[simplejson](https://pypi.python.org/pypi/simplejson/)  

## How it works
The server uses the BaseHTTPRequestHandler, which allows for somewhat easy to make web servers.  
Whenever the server is queried, the function that handles the type/method of the request is called.  
```python
class handler(BaseHTTPRequestHandler):
  def do_GET(s):
    s.send_response(200)
    s.end_headers()
    s.wfile.write("Hello")
```
