from flask import request
from flask_restful import Resource, marshal_with, reqparse

from database import db
from models import StockModel
from schemas import stock_fields, validate_stock_input


class Stocks(Resource):
    """Handles collection-level operations: GET all / POST new stock."""

    @marshal_with(stock_fields)
    def get(self):
        """
        GET /api/stocks
        Returns all stocks, optionally filtered by query parameters:
          - symbol          exact match
          - company_name    case-insensitive substring match
          - min_price       price >= value
          - min_market_cap  market_cap >= value
        """
        
        parser = reqparse.RequestParser()
        parser.add_argument("symbol", type=str, location="args")
        parser.add_argument("company_name", type=str, location="args")
        parser.add_argument(
            "min_price",
            type=float,
            location="args",
            help="min_price must be a valid float number.",
        )
        parser.add_argument(
            "min_market_cap",
            type=float,
            location="args",
            help="min_market_cap must be a valid float number.",
        )

        args = parser.parse_args(strict=False)



        query = StockModel.query

        if args["symbol"] is not None:
            query = query.filter(StockModel.symbol == args["symbol"])

        if args["company_name"] is not None:
           
            query = query.filter(
                StockModel.company_name.ilike(f"%{args['company_name']}%")
            )

        if args["min_price"] is not None:
            query = query.filter(StockModel.price >= args["min_price"])

        if args["min_market_cap"] is not None:
            query = query.filter(StockModel.market_cap >= args["min_market_cap"])

        return query.all(), 200

    @marshal_with(stock_fields)
    def post(self):
        """
        POST /api/stocks
        Creates a new stock entry. Expects a JSON body.
        """
        data = request.get_json(silent=True)
        if not data:
            return {"message": "Request body must be valid JSON."}, 400

        cleaned, error = validate_stock_input(data)
        if error:
            return {"message": error}, 400

        
        existing = StockModel.query.filter_by(symbol=cleaned["symbol"]).first()
        if existing:
            return {"message": f"Stock with symbol '{cleaned['symbol']}' already exists."}, 409

        stock = StockModel(
            symbol=cleaned["symbol"],
            company_name=cleaned["company_name"],
            price=cleaned["price"],
            market_cap=cleaned["market_cap"],
        )
        db.session.add(stock)
        db.session.commit()

        return stock, 201


class Stock(Resource):
    """Handles item-level operations: GET / PUT / DELETE by stock_id."""

    @marshal_with(stock_fields)
    def get(self, stock_id):
        """GET /api/stocks/<stock_id> — retrieve a single stock."""
        stock = StockModel.query.get(stock_id)
        if not stock:
            return {"message": f"Stock with id {stock_id} not found."}, 404
        return stock, 200

    @marshal_with(stock_fields)
    def put(self, stock_id):
        """PUT /api/stocks/<stock_id> — replace a stock's data entirely."""
        stock = StockModel.query.get(stock_id)
        if not stock:
            return {"message": f"Stock with id {stock_id} not found."}, 404

        data = request.get_json(silent=True)
        if not data:
            return {"message": "Request body must be valid JSON."}, 400

        cleaned, error = validate_stock_input(data)
        if error:
            return {"message": error}, 400

        
        conflict = StockModel.query.filter(
            StockModel.symbol == cleaned["symbol"],
            StockModel.id != stock_id,
        ).first()
        if conflict:
            return {"message": f"Symbol '{cleaned['symbol']}' is already used by another stock."}, 409

        stock.symbol = cleaned["symbol"]
        stock.company_name = cleaned["company_name"]
        stock.price = cleaned["price"]
        stock.market_cap = cleaned["market_cap"]

        db.session.commit()
        return stock, 200

    def delete(self, stock_id):
        """DELETE /api/stocks/<stock_id> — remove a stock."""
        stock = StockModel.query.get(stock_id)
        if not stock:
            return {"message": f"Stock with id {stock_id} not found."}, 404

        db.session.delete(stock)
        db.session.commit()
        return "", 204
