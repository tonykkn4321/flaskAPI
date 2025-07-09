from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

# use mySQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<mysql_username>:<mysql_password>@<mysql_ host>:<mysql_port>/<mysql_db>'

# If you're using the MySQL command-line client, run:
# SELECT USER();
# This will return something like root@localhost, where root is your username.

# Default host: localhost (if MySQL is running on your local machine)
# Default port: 3306

# use SQLite
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/<db_name>.db'

db = SQLAlchemy()

class Author (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    specialisation = db.Column(db.String(50))

    def __init__(self, name, specialisation):
        self.name = name
        self.specialisation = specialisation
    def __repr__(self):
        return f'<Author {self.id}: {self.name}>'

class AuthorSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Author
        sqla_session = db.session        
    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    specialisation = fields.String(required=True)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Aa161616@localhost:3306/mydb'
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

@app.route('/authors', methods = ['GET'])
def index():
    get_authors = Author.query.all()
    author_schema = AuthorSchema(many=True)
    authors = author_schema.dump(get_authors)
    return make_response(jsonify({"authors": authors}))

if __name__ == "__main__":
    app.run(debug=True)

