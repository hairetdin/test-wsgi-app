#!/usr/bin/env python
# -*- coding: utf-8 -*-

with open('templates/style.css') as f:
    css_style = f.read()

def read_tempate(file_name, js_header=''):
    """
    read html or error from templates
    """
    html_body = ''
    html_error = ''
    try:
        with open(file_name) as f:
            html_body = f.read()
            #response['html'] = html
    except IOError as e:
        print(e)
        html_error = e

    html = html_base % {
        'css_style': css_style,
        'js_header': js_header,
        'html_menu': html_menu,
        'html_body': html_body,
        'html_error': html_error
        }
    return html


html_base = """
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8">
        <style>
          %(css_style)s
        </style>
        %(js_header)s

      </head>
      <body>
        <div id="body">
        %(html_menu)s
        %(html_body)s
        <div>%(html_error)s</div>
        </div>
      </body>
    </html>
    """

html_menu = """
    <a href="/">Home</a>
    <a href="/comment/">Comment</a>
    <a href="/view/">View</a>
    <a href="/stat/">Stat</a>
    <a href="/refbook/">Reference book</a>
    """
