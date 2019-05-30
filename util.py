def usd(amount, from_currency, rate):
    eur = amount / rate[from_currency]
    return eur * rate['USD']
