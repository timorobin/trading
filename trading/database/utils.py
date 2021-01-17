from mongoengine import connect

def connect_to_db(db_name):
    connect(db_name)