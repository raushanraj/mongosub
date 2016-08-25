import time
import pymongo
from redispublisher import r

DB='gossip'
COLLECTION='girl'
OPERATIONS={

    'i' : ' data inserted',
    'u' : ' data updated',
    'd' : ' data deleted'
}

def parse_insert_doc(doc):
    try:
        operation=doc['op']
        ns=doc['ns']
        namespace=ns.split('.')
        message="Database changed  on : " + ns
        r.publish('all',message)
        print 'namespace',namespace
        if namespace[1]==COLLECTION and namespace[0]== DB:
            field_changed_dict=doc['o']
            field_changed_dict.pop('_id')
            field_changed=field_changed_dict.keys()
            for item in field_changed:
                r.publish(item,item+OPERATIONS[operation]+" on Database: "+ DB + " Collection: "+COLLECTION)
    except Exception ,e:
        print str(e)
        #not handled cases not important
        print "Exception to be silently passed",doc
    return


def tail_oplog():
    client = pymongo.MongoClient()
    oplog = client.local.oplog.rs
    first = oplog.find().sort('$natural', pymongo.ASCENDING).limit(-1).next()
    ts = first['ts']
    while True:
        cursor = oplog.find({'ts': {'$gt': ts}},
                            cursor_type=pymongo.CursorType.TAILABLE_AWAIT,
                            oplog_replay=True)
        while cursor.alive:
            for doc in cursor:
                ts = doc['ts']
                print doc
                parse_insert_doc(doc)
                print(doc)
            time.sleep(1)


if __name__=='__main__':
    tail_oplog()