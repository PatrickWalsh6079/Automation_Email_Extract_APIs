"""
Filename: get_all_companies_in_portfolio.py
Description: Retrieves all the company domains found within a
particular portfolio. Queries on portfolio ID.
"""


import requests

#token = "nHEAPGxHEOdKlQUogdTIRFmjllxo"  # bot token
token = "BoM3ndYGcesDJ07Hr2WB2Ns2fR6R"  # user token
portfolio = "61dca0a97d551b001cad4e63"  # portfolio ID

url = "https://api.securityscorecard.io/portfolios/" + portfolio + "/companies"
headers = {
    "Accept": "application/json; charset=utf-8",
    "Authorization": "Token " + token
}
response = requests.request("GET", url, headers=headers)

print(response.text)
