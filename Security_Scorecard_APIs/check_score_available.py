"""
Filename: check_score_available.py
Description: Checks whether score is available for specific company domain. Takes
in 1 input (company domain) and returns boolean value of whether score is ready.
"""


import requests
import json

#token = "nHEAPGxHEOdKlQUogdTIRFmjllxo"  # bot token
token = "BoM3ndYGcesDJ07Hr2WB2Ns2fR6R"  # user token
#company = "zmytimberlakeapts.com"

def check_score(company):
    """
    Checks if score is ready. Takes in 1 input (company domain) and returns boolean value
    of whether score is ready.
    """
    score_available = False  # initialize to False
    
    url = "https://api.securityscorecard.io/companies/" + company

    headers = {
        "Accept": "application/json; charset=utf-8",
        "Authorization": "Token " + token
    }

    response = requests.request("GET", url, headers=headers)

    #print(response.text)

    score = json.loads(response.text)  # convert JSON from string to dictionary
    print(score)

    # if company is not found in portfolio
    if 'error' in score:
        if 'company must be added to a portfolio first:' in score['error']['message']:
            raise Exception("Company {} not found in portfolio!".format(company))
    # if company is found in portfolio
    else:
        score = score['grade']
        if score != '?':  # if score is available
            score_available = True
        else:  # if score still generating
            raise Exception("Company {} score not ready yet!".format(company))
    

    return score_available
