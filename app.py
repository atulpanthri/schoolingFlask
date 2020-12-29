from flask import Flask,request
from flask_restful import Api
from security import authenticate,identity
from flask_jwt import JWT
from resources.users import UserRegister
from resources.item import Item,ItemList
from resources.store import Store,StoreList

items = [] 

app = Flask(__name__)
app.secret_key = 'jose'

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] =False

JWT(app,authenticate,identity)  #auth
api = Api(app)


api.add_resource(Item,'/item/<string:name>') # http://127.0.0.1/item/<string:name>
api.add_resource(ItemList,'/items') #http://127.0.0.1/items
api.add_resource(UserRegister,'/register')

api.add_resource(Store,'/store/<string:name>') # http://127.0.0.1/store/<string:name>
api.add_resource(StoreList,'/stores') # http://127.0.0.1/stores


if __name__=='__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)