#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wsgiref.simple_server import make_server
import re
from urls import urls
from views import *
from conf import *


class Server:

    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '').lstrip('/')
        for url, callback in urls:
            match = re.search(url, path)
            if match is not None:
                environ['myapp.url_args'] = match.groupdict()
                if type(callback) is str:
                    callback = eval(callback)
                response = callback(environ)
                if response[0] == 'response_ok':
                    status = '200 OK'
                    headers = [('Content-type', 'text/html')]
                    start_response(status, headers)
                    return [response[1]]
                if response[0] == 'redirect':
                    #redirect to anouther page
                    status = '302 Found'
                    start_response(status ,[('Location',response[1])])
                    return []
        status = '400 NOT FOUND'
        headers = [('Content-type', 'text/html')]
        start_response(status, headers)
        return not_found()

    def run(self):
        wsgi_server = make_server(self.host, self.port, self)
        print('WSGI serving on {host}:{port}'.format(host=self.host, port=self.port))
        wsgi_server.serve_forever()


def create_db(db):
    #create sql table area
    sql_new_table = '''
        CREATE TABLE IF NOT EXISTS area
        (
        name VARCHAR(255)
        );
        '''
    db.execute(sql_new_table)

    #create sql table city
    sql_new_table = '''
        CREATE TABLE IF NOT EXISTS city
        (
        name VARCHAR(255),
        area INTEGER,
        FOREIGN KEY (area) REFERENCES area(rowid)
        ON UPDATE SET NULL
        ON DELETE SET NULL
        );
        '''
    db.execute(sql_new_table)

    #create sql table people_info
    sql_new_table = '''
        CREATE TABLE IF NOT EXISTS people_info
        (
        last_name VARCHAR(100),
        first_name VARCHAR(100),
        patronymic_name VARCHAR(100),
        area integer,
        city integer,
        phone VARCHAR(255),
        email VARCHAR(255),
        additional text,
        FOREIGN KEY (area) REFERENCES area(rowid),
        FOREIGN KEY (city) REFERENCES city(rowid)
        ON UPDATE SET NULL
        ON DELETE SET NULL
        );
        '''
    db.execute(sql_new_table)


if __name__ == '__main__':

    create_db(db)

    # run wsgi server
    server = Server(host=host,port=port)
    server.run()
