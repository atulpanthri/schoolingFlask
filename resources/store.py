from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self,name):
        store = StoreModel.get_store_by_name(name)
        if store:
            return store.json()
        
        return {'message':'store not found'}, 404
    
    def post(self,name):
        
        if StoreModel.get_store_by_name(name):
            return {'message':f'Store {name} already available'},400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'message':'some inter error'},500

        return store.json()

    def put(self,name):
        
        store = StoreModel(name)
        store.save_to_db()
        return {'message':'store updated'}, 201

    def delete(self,name):
        
        store = StoreModel.get_store_by_name(name)
        if store:
            store.delete()
            return {'message':f'Store {name} is deleted'}

        return {'message':f'Store {name} not found'}


class StoreList(Resource):
    def get(self):
        return {'stores':[store.json() for store in StoreModel.query.all()]}