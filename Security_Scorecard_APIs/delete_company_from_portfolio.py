"""
Filename: delete_portfolio.py
Description: Deletes a company from a portfolio in Security Scorecard.
"""


import requests


company = "test.com"  # company domain to be deleted
portfolio = "61dca0a97d551b001cad4e63"  # portfolio ID
url = "https://api.securityscorecard.io/portfolios/" + portfolio + "/companies/" + company
#headers = {"Authorization": "Token nHEAPGxHEOdKlQUogdTIRFmjllxo"}  # bot token
headers = {"Authorization": "Token BoM3ndYGcesDJ07Hr2WB2Ns2fR6R"}  # user token
response = requests.request("DELETE", url, headers=headers)

print(response.text)
print("Success")
