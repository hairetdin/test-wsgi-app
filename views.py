#!/usr/bin/env python
# -*- coding: utf-8 -*-

from template import read_tempate
from conf import db, request_dict
from db_insert_test_value import fill_db
from cgi import escape


def index(environ):
    """
    Index page
    """
    html = read_tempate('templates/index.html')

    type_response = "response_ok"
    response = (type_response, html)
    return response


def fill_tables(environ):
    """
    Fill sql tables with test data
    """
    fill_db(db)
    #redirect to view
    type_response = "redirect"
    redirect_url = '/view/'
    response = (type_response, redirect_url)
    return response


def comment(environ):
    """
    Comment page
    """
    #get dictionary from request
    d = request_dict(environ)

    lname = d.get('lname', [''])[0]
    fname = d.get('fname', [''])[0]
    pname = d.get('pname', [''])[0]
    area = d.get('area', [''])[0]
    city = d.get('city', [''])[0]
    phone = d.get('phone', [''])[0]
    email = d.get('email', [''])[0]
    comment = d.get('comment', [''])[0]

    # Always escape user input to avoid script injection
    lname = escape(lname)
    fname = escape(fname)
    pname = escape(pname)
    area = escape(area)
    city = escape(city)
    phone = escape(phone)
    email = escape(email)
    comment = escape(comment)

    #get area
    sql_response_area = db.execute('SELECT rowid, * FROM area')
    areas_dict = {}
    for row in sql_response_area:
        areas_dict[str(row[0])] = (row[1]).encode('utf-8')

    #create options for areas
    areas_option = '<option value="">--------</option>'
    for k,v in areas_dict.items():
        areas_option+='<option value="' + k + '">' + areas_dict[k] + '</option>'

    comment_added = ""
    #insert data to table people_info
    sql_data='''
            INSERT INTO people_info
            VALUES (?,?,?,?,?,?,?,?);
            '''
    if d:
        insert_value = (
            lname.decode('utf-8'),
            fname.decode('utf-8'),
            pname.decode('utf-8') or None,
            area or None,
            city or None,
            phone.decode('utf-8') or None,
            email.decode('utf-8') or None,
            comment.decode('utf-8')
        )
        db.execute(sql_data, insert_value)
        comment_added = 'Your comment added to database'

    html = read_tempate('templates/comment.html')
    html_response = html % {
        'areas_option': areas_option,
        'comment_added': comment_added,
    }
    type_response = "response_ok"
    response = (type_response, html_response)
    return response


def get_city( environ):
    """
    Get cities for area
    """
    #get dictionary from request
    d = request_dict(environ)

    area = d.get('area', [''])[0]
    area = escape(str(area))
    if area:
        sql_get_city='''
            SELECT rowid,* FROM city
            WHERE area = ({area_id});
            '''.format(area_id=str(area))
        cities = db.execute(sql_get_city)
    html = ''
    html+='<select name="city">'
    for city in cities:
        html+='<option value="' + str(city[0]) + '">' + city[1].encode('utf-8') + '</option>'
    html+='</select>'

    type_response = "response_ok"
    response = (type_response, html)
    return response


def view( environ):
    """
    View page
    """
    #get dictionary from request
    d = request_dict(environ)

    comments = d.get('rm-comments', [])
    comments = [escape(comment) for comment in comments]
    if comments:
        print(comments)
        for comment_id in comments:
            sql_delete_row = '''
                DELETE FROM people_info
                WHERE rowid = {comment_id};'''.format(comment_id=comment_id)
            db.execute(sql_delete_row)

    #get comments from db
    sql_select_comments_innerjoin = '''
        SELECT comment.rowid, last_name, first_name, patronymic_name, area.name,
        city.name, phone, email, additional
        FROM people_info comment
        INNER JOIN area ON comment.area=area.rowid
        INNER JOIN city ON comment.city=city.rowid
        '''
    sql_select_comments = '''
        SELECT rowid, *
        FROM people_info comment
        '''
    sql_response = db.execute(sql_select_comments)
    response_table = ''
    for row in sql_response:
        response_table+='<tr id=' + str(row[0]) + '>'
        response_table+='<td>'
        response_table+='<input type="checkbox" name="rm-comments" value='
        response_table+=str(row[0])
        response_table+='></td>'

        for idx, item in enumerate(row):
            response_table+='<td>'
            if idx==4 and item:
                sql_get_area='''
                        SELECT name FROM area
                        WHERE rowid = ({area_id});
                        '''.format(area_id=str(item))
                area = db.execute(sql_get_area)
                if area:
                    response_table+=(area[0][0]).encode('utf-8')
                else:
                    response_table+=str(item)
            elif idx==5 and item:
                sql_get_city='''
                        SELECT name FROM city
                        WHERE rowid = ({city_id});
                        '''.format(city_id=str(item))
                city = db.execute(sql_get_city)
                if city:
                    response_table+=(city[0][0]).encode('utf-8')
                else:
                    response_table+=str(item)
            elif item is None:
                response_table+=''
            else:
                try:
                    response_table+=item.encode('utf-8')
                except AttributeError:
                    response_table+=str(item)
            response_table+='</td>'
        response_table+='</tr>'

    html = read_tempate('templates/view.html')
    if comments:
        comments_rm = '<p>Comment(s) {comments} deleted</p>'.format(comments=comments)
    else:
        comments_rm = ''

    response_html = html % {
        'response_table': response_table,
        'comments':comments_rm
    }

    type_response = "response_ok"
    response = (type_response, response_html)
    return response


def stat( environ):
    """
    Stat page
    """
    sql_select_areas = '''
        SELECT area, COUNT(*) AS lenght
        FROM people_info
        GROUP BY area
        HAVING COUNT(*) > 5;
        '''
    sql_response = db.execute(sql_select_areas)
    response_table = ''
    for row in sql_response:
        response_table+='<tr>'
        if row[1]:
            for idx, item in enumerate(row):
                response_table+='<td>'

                if idx == 0 and item:
                    #set area name to table
                    sql_get_area='''
                            SELECT name FROM area
                            WHERE rowid = ({area_id});
                            '''.format(area_id=str(item))
                    area = db.execute(sql_get_area)
                    response_table+='<a href="/stat/'+str(item)+'/">'
                    if area:
                        response_table+=(area[0][0]).encode('utf-8')
                    else:
                        response_table+=str(item)
                    response_table+='</a>'
                else:
                    try:
                        response_table+=item.encode('utf-8')
                    except AttributeError:
                        response_table+=str(item)
                response_table+='</td>'
        response_table+='</tr>'


    html = read_tempate('templates/stat.html')

    response_html = html % {
        'response_table': response_table,
    }
    type_response = "response_ok"
    response = (type_response, response_html)
    return response


def stat_area( environ):
    """
    Stat area page
    """
    #get area_id from environ['myapp.url_args']
    area_id = environ['myapp.url_args']['area_id']

    sql_select_areas = '''
        SELECT city, COUNT(*)
        FROM people_info
        WHERE area = ?
        GROUP BY city;
        '''
    sql_response = db.execute(sql_select_areas, area_id)
    response_table = ''
    for row in sql_response:
        response_table+='<tr>'
        if row[1]:
            for idx, item in enumerate(row):
                response_table+='<td>'

                if idx == 0 and item:
                    #set area name to table
                    sql_get_city='''
                            SELECT name FROM city
                            WHERE rowid = ({city_id});
                            '''.format(city_id=str(item))
                    city = db.execute(sql_get_city)

                    if city:
                        response_table+=(city[0][0]).encode('utf-8')
                    else:
                        response_table+=str(item)

                else:
                    try:
                        response_table+=item.encode('utf-8')
                    except AttributeError:
                        response_table+=str(item)
                response_table+='</td>'
        response_table+='</tr>'

    html = read_tempate('templates/stat-area.html')

    response_html = html % {
        'response_table': response_table,
    }
    type_response = "response_ok"
    response = (type_response, response_html)
    return response


def refbook(environ):
    """
    Reference book page
    """
    response_html = read_tempate('templates/refbook.html')
    type_response = "response_ok"
    response = (type_response, response_html)
    return response


def area(environ):
    """
    Area page
    """
    sql_response = db.execute('SELECT rowid, * FROM area')
    response_table = ''
    for row in sql_response:
        response_table+='<tr id=' + str(row[0]) + '>'
        response_table+='<td>'
        response_table+='<input type="checkbox" name="rm-areas" value='
        response_table+=str(row[0])
        response_table+='></td>'
        for item in row:
            response_table+='<td>'

            try:
                response_table+=item.encode('utf-8')
            except AttributeError:
                response_table+=str(item)
            response_table+='</td>'
        response_table+='</tr>'

    html = read_tempate('templates/area.html')
    response_html = html % {
        'response_table': response_table,
    }
    type_response = "response_ok"
    response = (type_response, response_html)
    return response


def area_add(environ):
    """
    Add area
    """
    #get dictionary from request
    d = request_dict(environ)

    name = d.get('name', [''])[0]
    name = escape(name)

    #insert data to table area
    if name:
        sql_insert_data='''
            INSERT INTO area
            VALUES ('{name}');
            '''.format(name=name)
        db.execute(sql_insert_data)

    #redirect to reference book area
    type_response = "redirect"
    redirect_url = '/refbook/area/'
    response = (type_response, redirect_url)
    return response


def area_rm(environ):
    """
    Area delete
    """
    #get dictionary from request
    d = request_dict(environ)

    areas = d.get('rm-areas', [])
    areas = [escape(area) for area in areas]
    if areas:
        #print(areas)
        for area_id in areas:
            sql_delete_row = '''
                DELETE FROM area
                WHERE rowid = {area_id};'''.format(area_id=area_id)
            db.execute(sql_delete_row)
    #redirect to reference book area
    type_response = "redirect"
    redirect_url = '/refbook/area/'
    response = (type_response, redirect_url)
    return response


def city(environ):
    """
    City page
    """
    #get area
    sql_response_area = db.execute('SELECT rowid, * FROM area')
    areas_dict = {}
    for row in sql_response_area:
        areas_dict[str(row[0])] = (row[1]).encode('utf-8')

    #create options for areas
    areas_option = ''
    for k,v in areas_dict.items():
        areas_option+='<option value="' + k + '">' + areas_dict[k] + '</option>'

    #get city
    sql_response_city = db.execute('SELECT rowid, * FROM city')
    #create city table
    response_table = ''
    for row in sql_response_city:
        response_table+='<tr id=' + str(row[0]) + '>'
        response_table+='<td>'
        response_table+='<input type="checkbox" name="rm-cities" value='
        response_table+=str(row[0])
        response_table+='></td>'

        for idx, item in enumerate(row):
            response_table+='<td>'

            if idx==2 and item:

                sql_get_area='''
                        SELECT name FROM area
                        WHERE rowid = ({area_id});
                        '''.format(area_id=str(item))
                area = db.execute(sql_get_area)
                if area:
                    response_table+=(area[0][0]).encode('utf-8')
                else:
                    response_table+=str(item)
            else:
                try:
                    response_table+=item.encode('utf-8')
                except AttributeError:
                    response_table+=str(item)
            response_table+='</td>'
        response_table+='</tr>'

    html = read_tempate('templates/city.html')
    response_html = html % {
        'response_table': response_table,
        'areas_option': areas_option
    }
    type_response = "response_ok"
    response = (type_response, response_html)
    return response


def city_add(environ):
    """
    City add
    """
    #get dictionary from request
    d = request_dict(environ)

    city = d.get('city', [''])[0]
    area = d.get('area', [''])[0]

    city = escape(city)
    area = escape(area)

    #insert data to table city
    if d:
        sql_insert_data='''
            INSERT INTO city
            VALUES ('{city}', {area});
            '''.format(city=city, area=(area or 'null'))
        db.execute(sql_insert_data)

    #redirect to reference book city
    type_response = "redirect"
    redirect_url = '/refbook/city/'
    response = (type_response, redirect_url)
    return response


def city_rm(environ):
    """
    City delete
    """
    #get dictionary from request
    d = request_dict(environ)

    cities = d.get('rm-cities', [])
    sities = [escape(city) for city in cities]
    if sities:
        for city_id in cities:
            sql_delete_row = '''
                DELETE FROM city
                WHERE rowid = {city_id};'''.format(city_id=city_id)
            db.execute(sql_delete_row)
    #redirect to reference book area
    type_response = "redirect"
    redirect_url = '/refbook/city/'
    response = (type_response, redirect_url)
    return response


def not_found():
    """
    Not found page 404
    """
    response = ["<h1>404 Page not found</h1>"]
    return response
