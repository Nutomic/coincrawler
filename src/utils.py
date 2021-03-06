#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# utils.py - Common helper methods.
#
# Copyright (c) Addy Yeow Chin Heng <ayeowch@gmail.com>
# Portions Copyright (c) 2018 Felix Ableitner
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
Common helper methods.
"""

import os
import redis
from ipaddress import ip_network
from ConfigParser import ConfigParser
from binascii import unhexlify
from ast import literal_eval


def new_redis_conn(db=0):
    """
    Returns new instance of Redis connection with the right db selected.
    """
    socket = os.environ.get('REDIS_SOCKET', "/var/run/redis/redis.sock")
    password = os.environ.get('REDIS_PASSWORD', None)
    return redis.StrictRedis(db=db, password=password, unix_socket_path=socket)


def get_keys(redis_conn, pattern, count=500):
    """
    Returns Redis keys matching pattern by iterating the keys space.
    """
    keys = []
    cursor = 0
    while True:
        (cursor, partial_keys) = redis_conn.scan(cursor, pattern, count)
        keys.extend(partial_keys)
        if cursor == 0:
            break
    return keys


def ip_to_network(address, prefix):
    """
    Returns CIDR notation to represent the address and its prefix.
    """
    network = ip_network(unicode("{}/{}".format(address, prefix)),
                         strict=False)
    return "{}/{}".format(network.network_address, prefix)


def create_folder_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def median(lst):
    """
    Calculate median value of a list.
    https://stackoverflow.com/a/20730918
    """
    even = (0 if len(lst) % 2 else 1) + 1
    half = (len(lst) - 1) / 2
    return sum(sorted(lst)[half:half + even]) / float(even)


def parse_config(config_file, section):
    conf = ConfigParser()
    conf.read(config_file)
    conf_dict = {}
    for item in conf.items('general'):
        if item[0] == 'magic_number':
            conf_dict['magic_number'] = unhexlify(conf.get('general', 'magic_number'))
        else:
            conf_dict[item[0]] = eval_config_value(item[1])

    for item in conf.items(section):
        if conf_dict.has_key(item[0]):
            raise Exception("")
        conf_dict[item[0]] = eval_config_value(item[1])

    return conf_dict


def eval_config_value(value):
    try:
        return literal_eval(value)
    except (ValueError, SyntaxError):
        return value
