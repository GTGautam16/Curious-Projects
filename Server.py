import http.server
import os
import mimetypes
import subprocess # 👈 Modern replacement for popen2

class ServerException(Exception):
    pass

# =====================================================================
# 🧰 THE TOOLBOX (Parent Class)
# =====================================================================
class base_case(object):
    '''Parent for case handlers. Holds shared tools.'''

    def handle_file(self, handler, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            
            content_type, _ = mimetypes.guess_type(full_path)
            handler.send_content(content, 200, content_type or "text/html")
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(full_path, msg)
            handler.handle_error(msg)

    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')

    def test(self, handler):
        assert False, 'Not implemented.'

    def act(self, handler):
        assert False, 'Not implemented.'

# =====================================================================
# 🏛️ THE CLERKS (Inheriting from base_case)
# =====================================================================

class case_no_file(base_case):
    def test(self, handler):
        return not os.path.exists(handler.full_path)

    def act(self, handler):
        raise ServerException("'{0}' not found".format(handler.path))

class case_cgi_file(base_case):
    '''NEW: Runs an external Python script!'''
    def test(self, handler):
        return os.path.isfile(handler.full_path) and handler.full_path.endswith('.py')

    def act(self, handler):
        self.run_cgi(handler, handler.full_path)
        
    def run_cgi(self, handler, full_path):
        # Modern Python 3 way to run a background script and capture output
        try:
            output = subprocess.check_output(["python", full_path], text=True)
            handler.send_content(output)
        except Exception as e:
            handler.handle_error(f"CGI Script Failed: {e}")

class case_existing_file(base_case):
    def test(self, handler):
        return os.path.isfile(handler.full_path)

    def act(self, handler):
        self.handle_file(handler, handler.full_path)

class case_directory_index_file(base_case):
    def test(self, handler):
        return os.path.isdir(handler.full_path) and os.path.isfile(self.index_path(handler))

    def act(self, handler):
        self.handle_file(handler, self.index_path(handler))

class case_directory_no_index_file(base_case):
    def test(self, handler):
        return os.path.isdir(handler.full_path) and not os.path.isfile(self.index_path(handler))

    def act(self, handler):
        self.list_dir(handler, handler.full_path)
        
    def list_dir(self, handler, full_path):
        try:
            entries = os.listdir(full_path)
            bullets = ["<li><a href='{0}/{1}'>{1}</a></li>".format(handler.path.rstrip('/'), e) 
                       for e in entries if not e.startswith('.')]
            page = handler.Listing_Page.format(path=handler.path, bullet_points='\n'.join(bullets))
            handler.send_content(page)
        except OSError as msg:
            msg = "'{0}' cannot be listed: {1}".format(handler.path, msg)
            handler.handle_error(msg)

class case_always_fail(base_case):
    def test(self, handler):
        return True

    def act(self, handler):
        raise ServerException("Unknown object '{0}'".format(handler.path))

# =====================================================================
# 🚦 THE MAIN REQUEST HANDLER (The Boss)
# =====================================================================

class RequestHandler(http.server.BaseHTTPRequestHandler):

    # Look how clean the boss's checklist is now!
    Cases = [
        case_no_file(),
        case_cgi_file(),
        case_existing_file(),
        case_directory_index_file(),
        case_directory_no_index_file(),
        case_always_fail()
    ]

    Error_Page = """\
        <html><body><h1>Error accessing {path}</h1><p>{msg}</p></body></html>
        """

    Listing_Page = """\
        <html><body><h1>Directory Listing for {path}</h1><ul>{bullet_points}</ul></body></html>
        """

    def do_GET(self):
        try:
            self.full_path = os.getcwd() + self.path
            for case in self.Cases:
                if case.test(self):
                    case.act(self)
                    break
        except Exception as msg:
            self.handle_error(msg)

    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(content, status=404)

    def send_content(self, content, status=200, content_type="text/html"):
        self.send_response(status)
        self.send_header("Content-type", content_type)
        if isinstance(content, str):
            content = content.encode('utf-8')
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = http.server.HTTPServer(serverAddress, RequestHandler)
    print("Final Extensible Server running on port 8080...")
    server.serve_forever()