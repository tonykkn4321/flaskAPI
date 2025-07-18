from flask import Flask, request, jsonify, make_response
from flask_mongoengine import MongoEngine
from marshmallow import Schema, fields
from bson import ObjectId

# Map ObjectId to String for Marshmallow
Schema.TYPE_MAPPING[ObjectId] = fields.String

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'authors',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine(app)

# MongoDB Document
class Authors(db.Document):
    name = db.StringField(required=True)
    specialisation = db.StringField(required=True)

# Marshmallow Schema
class AuthorsSchema(Schema):
    id = fields.String()  # Include ObjectId as string
    name = fields.String(required=True)
    specialisation = fields.String(required=True)

# API Endpoint
@app.route('/authors', methods=['GET'])
def index():
    get_authors = Authors.objects.all()
    author_schema = AuthorsSchema(many=True)
    authors = author_schema.dump(get_authors)
    return make_response(jsonify({"authors": authors}))



if __name__ == "__main__":
    app.run(debug=True)
