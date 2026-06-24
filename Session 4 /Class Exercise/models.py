from database import db


class StockModel(db.Model):
    """Represents a publicly traded company's stock entry in the database."""

    __tablename__ = "stocks"

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), nullable=False, unique=True)
    company_name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    market_cap = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<Stock {self.symbol}>"
