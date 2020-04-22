from flask_restful import  Resource,reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float, required=True,help='This field cant be left blank')
    parser.add_argument('store_id',type=int, required=True,help='Every item needs store_id')


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'It doesnt exist '}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "an item '{}' already exists".format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error has occured"}, 500 #internale server error

        return item.json(), 201

    def delete(self, name):
        item= ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):

        return {"items": [item.json() for item in ItemModel.query.all()]}
        # {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}
