from flask_restful import fields

# Serialization schema used with @marshal_with to format Stock responses
stock_fields = {
    "id": fields.Integer,
    "symbol": fields.String,
    "company_name": fields.String,
    "price": fields.Float,
    "market_cap": fields.Float,
}


def validate_stock_input(data):
    """
    Validates the parsed JSON body for POST and PUT requests.

    Returns (cleaned_data, error_message). If error_message is not None,
    the request should be rejected with 400.
    """
    errors = []

    # --- symbol ---
    symbol = data.get("symbol")
    if symbol is None or (isinstance(symbol, str) and symbol.strip() == ""):
        errors.append("'symbol' is required and cannot be null or empty.")

    # --- company_name ---
    company_name = data.get("company_name")
    if company_name is None or (isinstance(company_name, str) and company_name.strip() == ""):
        errors.append("'company_name' is required and cannot be null or empty.")

    # --- price ---
    price = data.get("price")
    if price is None:
        errors.append("'price' is required and cannot be null.")
    else:
        
        if isinstance(price, bool):
            errors.append("'price' must be a number, not a boolean.")
        elif not isinstance(price, (int, float)):
            errors.append("'price' must be a numeric value.")
        elif price < 0:
            errors.append("'price' must be a non-negative number.")

    # market_cap
    market_cap = data.get("market_cap")
    if market_cap is not None:
        if isinstance(market_cap, bool):
            errors.append("'market_cap' must be a number, not a boolean.")
        elif not isinstance(market_cap, (int, float)):
            errors.append("'market_cap' must be a numeric value.")
        elif market_cap < 0:
            errors.append("'market_cap' must be a non-negative number.")

    if errors:
        return None, "; ".join(errors)

    return {
        "symbol": symbol.strip() if isinstance(symbol, str) else symbol,
        "company_name": company_name.strip() if isinstance(company_name, str) else company_name,
        "price": float(price),
        "market_cap": float(market_cap) if market_cap is not None else None,
    }, None
