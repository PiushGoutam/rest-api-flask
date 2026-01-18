from marshmallow import fields, Schema

class PlainItemSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Int(required=True)

class ItemSchema(PlainItemSchema):
    store = fields.Nested(lambda : PlainStoreSchema, dump_only=True)
    tags = fields.List(fields.Nested(lambda : PlainTagSchema), dump_only=True)


class ItemUpdateSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class PlainStoreSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)

    
class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema), dump_only=True)
    tags = fields.List(fields.Nested(lambda: PlainTagSchema), dump_only=True)

class PlainTagSchema(Schema):
    name = fields.Str(required=True)

class TagSchema(PlainTagSchema):
    id = fields.Int()
    store_id = fields.Int(dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema), dump_only=True)

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    password = fields.Str(load_only=True)