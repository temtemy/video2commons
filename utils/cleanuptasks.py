#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright (C) 2015 Zhuyifei1999
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>
#

"""Remove expired tasks (title forgotten) from user task list."""

import os
import sys
from redis import Redis

sys.path.append(os.path.dirname(os.path.realpath(__file__)) +
                "/../video2commons")
from config import redis_pw, redis_host  # NOQA

redisconnection = Redis(host=redis_host, db=3, password=redis_pw)

for userkey in redisconnection.keys('tasks:*') + ['alltasks']:
    for taskid in redisconnection.lrange(userkey, 0, -1):
        if not redisconnection.exists('titles:' + taskid):
            redisconnection.lrem(userkey, taskid)
            print "delete %s from %s" % (taskid, userkey)

for pattern in ['params:*', 'restarted:*']:  # 'tasklock:*'
    for key in redisconnection.keys(pattern):
        taskid = key.split(':')[1]
        if not redisconnection.exists('titles:' + taskid):
            redisconnection.delete(key)
            print "delete %s" % (key)
