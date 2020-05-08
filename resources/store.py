from flask_restful import  Resource,reqparse
from flask_jwt import jwt_required
import sqlite3
from models.store import StoreModel


class Store(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float, required=True,help='This field cant be left blank')
    parser.add_argument('store_id',type=int, required=True,help='Every item needs store_id')


    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'It doesnt exist '}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "a store '{}' already exists".format(name)}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message": "An error has occured"}, 500 #internale server error

        return store.json(), 201

    def delete(self, name):
        store= StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}



class StoreList(Resource):
    def get(self):

        return {"stores": [store.json() for store in StoreModel.find_all()]}
        # {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}
