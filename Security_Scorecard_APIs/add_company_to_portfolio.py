"""
Filename: add_company_to_portfolio.py
Description: Uses API call to add company domain to portfolio in Security Scorecard.
Called from main.py file.
"""

import requests


def add_company(company):
    """
    Uses API call to add company domain to portfolio, takes 1 parameter (company) from 
    the read_email.py that gets company domain from email.
    """

    #token = "nHEAPGxHEOdKlQUogdTIRFmjllxo"  # bot token
    token = "BoM3ndYGcesDJ07Hr2WB2Ns2fR6R"  # user token

    portfolio = "61dca0a97d551b001cad4e63"
    url = "https://api.securityscorecard.io/portfolios/" + portfolio + "/companies/" + company
    headers = {
        "Accept": "application/json; charset=utf-8",
        "Authorization": "Token " + token
    }
    response = requests.request("PUT", url, headers=headers)
    #print(response.text)

    return 0
