from mongoengine import connect

def connect_to_db(db_name):
    return connect(db_name)