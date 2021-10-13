from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    # Parsing - um nicht item.update(data) auszuführen, sondern gezielt nur ein Element
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item need a store id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exists'}, 400

        # data = request.get_json()  # data will be a dictionary
        data = Item.parser.parse_args()

        # item = {'name': name, 'price': data['price']}  # created JSON as item
        item = ItemModel(name, data['price'], data['store_id'])
        
        try:
            # ItemModel.insert(item)
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500  # Internal Server Error

        # 201 created, item ist JSON - {'name': 'test', 'price': 15.99}
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:  # wenn Artikel nicht exisiert
            item = ItemModel(name, data['price'], data['store_id'])

        else:  # wenn exisiert, wird upgedatet
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}  # das Gleiche mit map
