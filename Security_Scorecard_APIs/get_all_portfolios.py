"""
Filename: get_all_portfolios.py
Description: Retrieves all portfolios accessible to user in Security Scorecard.
Accessibility based on user token.
"""


import requests


url = "https://api.securityscorecard.io/portfolios"
#headers = {"Authorization": "Token nHEAPGxHEOdKlQUogdTIRFmjllxo"}  # bot token
headers = {"Authorization": "Token BoM3ndYGcesDJ07Hr2WB2Ns2fR6R"}  # user token

response = requests.request("GET", url, headers=headers)
print(response.text)
