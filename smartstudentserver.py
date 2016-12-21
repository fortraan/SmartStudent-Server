from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import pickledb
from urlparse import urlparse, parse_qs

class RequestHandler(BaseHTTPRequestHandler):
    db = None
    server_version = "0.1.4"
    def do_GET(s):
        s.db = pickledb.load("kid.db", False)
        s.send_response(200)
        #s.send_header('Content-type', 'text/html')
        s.end_headers()

        if s.path == "/favicon.ico":
            s.wfile.write(file("favicon.ico"))

        if s.path == "/":
            for key in s.db.getall():
                s.wfile.write(str(key) + "\n")
                for dkey in s.db.dkeys(key):
                    s.wfile.write(str(dkey) + " : " + str(s.db.dget(key, dkey)) + "\n")
        elif s.path[1:] in s.db.getall():
            for dkey in s.db.dkeys(s.path[1:]):
                s.wfile.write(str(dkey) + " : " + str(s.db.dget(s.path[1:], dkey)) + "\n")
        
        s.db.dump()
        #s.wfile.write("<h1>Hi</h1>")
        #s.wfile.write("<button type=\"button\">Click me!</button>")
    def do_POST(s):
        s.db = pickledb.load("kid.db", False)
        
        s.send_response(200)
        s.end_headers()
        
        length = int(s.headers.getheader('content-length'))
        field_data = s.rfile.read(length)
        fields = parse_qs(field_data)

        # key and action are the minimum parameters
        # action=set expects key=keyOfValueToSet&value=valueToSetTo
        # action=remove expects key=keyToRemove
        if ('action' not in fields) or ('name' not in fields):
            s.send_error(400, "Invalid parameters")
            return
        if fields['action'][0] == 'set':
            if ('value' not in fields) or ('trait' not in fields):
                s.send_error(400)
                return
            if fields['name'][0] not in s.db.getall():
                s.send_error(404)
            s.db.dpop(fields['name'][0], fields['trait'][0])
            s.db.dadd(fields['name'][0], tuple([fields['trait'][0], fields['value'][0]]))
            s.db.dump()
            return
        elif fields['action'][0] == 'remove':
            if ('value' in fields) or ('trait' in fields):
                s.send_error(400, "Invalid parameters")
                return
            if (fields['name'][0] not in s.db.getall()):
                s.send_error(404, "Does not exist")
                return
            s.db.drem(fields['name'][0])
            s.db.dump()
            return
        elif fields['action'][0] == "add":
            if ('value' in fields) or ('trait' in fields):
                s.send_error(400)
                return
            if (fields['name'][0] in s.db.getall()):
                s.send_error(403)
                return
            s.db.dcreate(fields['name'][0])
            s.db.dadd(fields['name'][0], tuple(["b", 0]))
            s.db.dadd(fields['name'][0], tuple(["f", 0]))
            s.db.dadd(fields['name'][0], tuple(["g", 0]))
            s.db.dump()
        else:
            s.send_error(400, "Invalid action: " + fields['action'][0])
            return

server = HTTPServer(('', 8080), RequestHandler)

server.serve_forever()
