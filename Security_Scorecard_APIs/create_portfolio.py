"""
Filename: create_portfolio.py
Description: Creates portfolio in Security Scorecard. Able to set portfolio
name and description.
"""

import requests


name = "Practice Portfolio"
desc = ""
#token = "nHEAPGxHEOdKlQUogdTIRFmjllxo"  # bot token
token = "BoM3ndYGcesDJ07Hr2WB2Ns2fR6R"  # user token


url = "https://api.securityscorecard.io/portfolios"

payload = {
    "name": name,
    "description": desc
}
headers = {
    "Accept": "application/json; charset=utf-8",
    "Content-Type": "application/json",
    "Authorization": "Token " + token
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
