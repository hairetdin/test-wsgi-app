from cgi import parse_qs
from sqlite_connect import Db

#server config
host = 'localhost'
port = 8060
db_file = 'sqlite.db'
db = Db(db_file)

def request_dict(environ):
    """
    detect request methon and return request dictionary
    """
    request_method = environ.get('REQUEST_METHOD')
    if request_method == 'POST':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0

        request_body = environ['wsgi.input'].read(request_body_size)
        return parse_qs(request_body)
    if request_method == 'GET':
        return parse_qs(environ['QUERY_STRING'])
