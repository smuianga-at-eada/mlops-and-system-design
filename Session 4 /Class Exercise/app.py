from flask import Flask
from flask_restful import Api

from database import db
from resources import Stock, Stocks

# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///stocks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

api = Api(app)
api.add_resource(Stocks, "/api/stocks")           # collection: GET list, POST
api.add_resource(Stock, "/api/stocks/<int:stock_id>")  # item: GET, PUT, DELETE

# ---------------------------------------------------------------------------
# Create tables on first run
# ---------------------------------------------------------------------------

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
