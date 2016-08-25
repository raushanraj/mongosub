import gevent.monkey
gevent.monkey.patch_socket()
import gevent
from gevent.pool import Pool
import time
import redis

config = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

r = redis.StrictRedis(**config)
ALL_FIELDS=['all','name','age','about','profession']
pool=Pool(5)
#
# def send_in_room():
#     socketio.emit('my response',{'data':'subscribed to all changes in database'},room='field_one')


