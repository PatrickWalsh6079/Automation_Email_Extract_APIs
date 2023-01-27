"""
Filename: generate_company_summary_report.py
Description: Generates Company Summary report and gets report
URL based on report ID. Times out after certain number of API
calls. Called from main.py file.
"""

import time
import json
import requests


def get_report_url(company):
    """
    Generates Company summary report and returns report URL
    and boolean of whether report was found. Takes 1
    parameter (company) from read_email.py file.
    """

    #token = "nHEAPGxHEOdKlQUogdTIRFmjllxo"  # bot token
    token = "BoM3ndYGcesDJ07Hr2WB2Ns2fR6R"  # user token

    # Generate a company summary report
    url = "https://api.securityscorecard.io/reports/summary"
    payload = {
        "scorecard_identifier": company,
        "branding": "securityscorecard"
    }
    headers = {
        "Accept": "application/json; charset=utf-8",
        "Content-Type": "application/json",
        "Authorization": "Token " + token
    }
    response = requests.request("POST", url, json=payload, headers=headers)

    # get report_id
    report_id = json.loads(response.text)  # convert JSON from string to dictionary
    report_id = report_id['id']
    print("report_id: ", report_id)

    # Get reports you have generated recently
    url = "https://api.securityscorecard.io/reports/recent"
    headers = {
        "Accept": "application/json; charset=utf-8",
        "Authorization": "Token " + token
    }


    # find download_url based on report_id
    report_located = False
    timeout = 10  # timeout after this many API attempts
    attempt = 0  # attempt variable keeps track of how many attempts until timeout reached

    while report_located is False and attempt < timeout:
        # send API call and loops through response to find report_id.
        # resends API call after looping through entire response if report_id not located.
        print("API call attempt", attempt)
        counter = -1
        response = requests.request("GET", url, headers=headers)  # API call
        report_url = json.loads(response.text)  # convert JSON from string to dictionary

        for i in range(len(report_url['entries'])):
            counter += 1
            #print(counter)
            #print(report_url['entries'][counter])

            # check if report is ready
            if 'completed_at' in report_url['entries'][counter]:
                #print('ready')

                # if report is ready, see if it has matching report_id
                if report_url['entries'][counter]['id'] == report_id:
                    #print('MATCH!')
                    report_url = report_url['entries'][counter]['download_url']  # set report_url to correct report
                    report_url = "https://" + report_url[17:]  # remove 'platform-' from API call
                    report_located = True
                    break

        # wait 1 second, then add 1 to the attempt tracker variable
        time.sleep(1)
        attempt += 1

    # if no report was found, the program sends an email letting the customer know it is still being generated
    if report_located is False:
        print('Report still being generated! Will send email later...')
        report_url = 'Report still being generated! Will send email later...'
    else:
        print("Report URL: " + report_url)


    return report_url, report_located
