#!/usr/bin/env python
# -*- coding: utf-8 -*-

urls = [
    (r'^$', 'index'),
    (r'^comment\/?$', 'comment'),
    (r'^view\/?$', 'view'),
    (r'^stat\/?$', 'stat'),
    (r'^stat/(?P<area_id>[0-9]+)\/?$', 'stat_area'),
    (r'^refbook\/?$', 'refbook'),
    (r'^refbook/area\/?$', 'area'),
    (r'^refbook/area-add\/?$', 'area_add'),
    (r'^refbook/area-rm\/?$', 'area_rm'),
    (r'^refbook/city\/?$', 'city'),
    (r'^refbook/city-add\/?$', 'city_add'),
    (r'^refbook/city-rm\/?$', 'city_rm'),
    (r'^get-city\/?$', 'get_city'),
    (r'^fill-tables\/?$', 'fill_tables'),
]
