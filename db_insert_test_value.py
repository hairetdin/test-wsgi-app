#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Add test value to db
"""
def fill_db(db):
    db=db
    #add example areas to database
    sql_data='INSERT INTO area VALUES (?)'

    areas = [
        (u'Краснодарский край',),
        (u'Ростовская область',),
        (u'Ставропольский край',)
    ]
    for insert_value in areas:
        if sql_data and insert_value:
            db.execute(sql_data, insert_value)


    #add example city to database
    sql_data='''
            INSERT INTO city
            VALUES (?,?);
            '''

    cities = [
        (u'Краснодар',1),
        (u'Кропоткин',1),
        (u'Славянск',1),
        (u'Ростов',2),
        (u'Шахты',2),
        (u'Батайск',2),
        (u'Ставрополь',3),
        (u'Пятигорск',3),
        (u'Кисловодск',3),
    ]
    for insert_value in cities:
        if sql_data and insert_value:
            db.execute(sql_data, insert_value)


    #add example comments to database
    sql_data='''
            INSERT INTO people_info
            VALUES (?,?,?,?,?,?,?,?);
            '''

    comments = [
        (u'Иванов1', u'Иван', u'Иванович', 1, 1, u'8(999)1234567',u'test@test.com',u'1 Июнь был очень дождливым'),
        (u'Иванов2', u'Иван', u'Иванович', 1, 2, u'8(999)1234567',u'test@test.com',u'2 Июнь был очень дождливым'),
        (u'Иванов3', u'Иван', u'Иванович', 1, 3, u'8(999)1234567',u'test@test.com',u'3 Июнь был очень дождливым'),
        (u'Иванов4', u'Иван', u'Иванович', 1, 1, u'8(999)1234567',None, u'4 Июнь был очень дождливым'),
        (u'Иванов5', u'Иван', u'Иванович', 1, 1, None, u'test@test.com', u'5 Июнь был очень дождливым'),
        (u'Иванов6', u'Иван', u'Иванович', 1, 1, u'8(999)1234567',u'test@test.com',u'6 Июнь был очень дождливым'),
        (u'Петров', u'Петр', None, 2, 4, None, None, u'Я все могу'),
        (u'Петров1', u'Петр', None, 2, 5, None, None, u'И ты сможешь'),
        (u'Петров3', u'Петр', None, 2, 6, None, None, u'Если захочешь'),
        (u'Сидоров', u'Петр', None, 3, 7, None, None, u'Было бы желание'),
        (u'Сидоров1', u'Петр', None, 3, 8, None, None, u'тогда все реализуемо'),
        (u'Сидоров2', u'Петр', None, 3, 9, None, None, u'Урррааааа!'),
    ]

    for insert_value in comments:
        if sql_data and insert_value:
            db.execute(sql_data, insert_value)


if __name__ == '__main__':

    db_file = 'sqlite.db'

    """
    sqlite db
    """
    from sqlite_connect import Db
    db = Db(db_file)

    fill_db(db)

    db.execute()
