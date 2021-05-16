import os
import requests
import sqlalchemy as alch
import sys

#sys.path.append("../")



tok1 = os.getenv('Client_Id')
tok2 = os.getenv('Client_Secret')
tok3 = os.getenv('SQL')


connectionData = f'mysql+pymysql://root:admin@localhost/diary'
engine = alch.create_engine(connectionData)

engine.execute('USE diary')