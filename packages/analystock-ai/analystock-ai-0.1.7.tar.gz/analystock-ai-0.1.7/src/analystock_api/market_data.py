from analystock_api.query_generic import _make_request


def get_instruments_quotes(api_key, tickers=None):
    """Retrieve real-time stock quotes and prices."""
    params = {'tickers': ','.join(tickers)} if tickers else None
    return _make_request("instruments_quotes/", api_key, params)


def get_price_histo(api_key, tickers=None):
    """Retrieve historical price data."""
    params = {'tickers': ','.join(tickers)} if tickers else None
    return _make_request("price_histo/", api_key, params)


def get_fx_histo(api_key, tickers=None):
    """Get historical FX rates (e.g., EURUSD=X)."""
    params = {'tickers': ','.join(tickers)} if tickers else None
    return _make_request("fx_histo/", api_key, params)


def get_price_histo_dates(api_key, start_date, end_date, tickers=None):
    """Retrieve historical price data between two dates"""
    params = {'tickers': ','.join(tickers), 'start_date': start_date, 'end_date': end_date} if (
                tickers and start_date and end_date) else None
    return _make_request("price_histo_dates/", api_key, params)


def get_fx_histo_dates(api_key, start_date, end_date, tickers=None):
    """Get historical FX rates (e.g., EURUSD=X). between two dates"""
    params = {'tickers': ','.join(tickers), 'start_date': start_date, 'end_date': end_date} if (
                tickers and start_date and end_date) else None
    return _make_request("fx_histo_dates/", api_key, params)
