import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):

    parse =reqparse.RequestParser()
    parse.add_argument("price",
                        type=float,
                        required=True,
                        help = 'this filed cannot be blank' )

    parse.add_argument("store_id",
                        type=int,
                        required=True,
                        help = 'every item must have store id')

    @jwt_required()
    def get(self,name):
        
        item = ItemModel.find_item_by_name(name)
        if item:
            return item.json()
        else:
            return {'message':'item not found'},404


    def post(self,name):

        item = ItemModel.find_item_by_name(name)
        
        if item:
           return {'message':f'item {name} already exists'},400 
        
        req_data =Item.parse.parse_args()
        
        item = ItemModel(name,req_data['price'],req_data['store_id'])
        item.save_to_db()

        return item.json(),201

    def delete(self,name):
        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete()
        
        return {'message':'item is deleted'}

    def put(self,name):
        req_data = Item.parse.parse_args()

        item = ItemModel.find_item_by_name(name)
        
        if item is None:
            item = ItemModel(name,req_data['price'],req_data['store_id'])

        else:
            item.price = req_data['price']
            item.store_id = req_data['store_id']

        item.save_to_db()

        return item.json()

class ItemList(Resource):
    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]}
