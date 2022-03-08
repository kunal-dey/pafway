from contextlib import contextmanager
from mongoengine import connect, disconnect

from utils.config import DATABASE_URI

@contextmanager
def connect_to_db():
    connect(
        host= 'mongodb://kunal-admin:Ivan123@cluster0-shard-00-00.boiwn.mongodb.net:27017,cluster0-shard-00-01.boiwn.mongodb.net:27017,cluster0-shard-00-02.boiwn.mongodb.net:27017/banners?ssl=true&replicaSet=atlas-fbuxje-shard-0&authSource=admin&retryWrites=true&w=majority',
    )
    yield 
    disconnect()