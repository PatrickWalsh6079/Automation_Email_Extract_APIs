"""
Filename: send_email.py
Description: Downloads report as PDF and attaches PDF to
email. If report was not found in generate_company_summary_report.py,
this scripts sends an email letting customer know that report is
still being generated.
"""

import os
import requests
import win32com.client


# create Outlook object
outlook = win32com.client.Dispatch('outlook.application')

def send_report(report, report_located):
    """
    Downloads report as PDF from report URL, sends email to customer
    with report attached, then deletes PDF from download location. Takes
    in 2 parameters, the URL to the report, and a boolean of whether
    report was found.
    """

    # boolean of whether report was found
    report_found = report_located

    # create email to send report
    mail = outlook.CreateItem(0)
    mail.To = 'pwalsh@syscom.com'

    # report_found == True
    if report_found:
        # get report name
        report_name = report.split("/")[-1]
        report_name = report_name.split(".json")[0] + ".pdf"  # strip off .json from report_name
        print(report_name)

        # Download a generated report
        #headers = {"Authorization": "Token nHEAPGxHEOdKlQUogdTIRFmjllxo"}  # bot token
        headers = {"Authorization": "Token BoM3ndYGcesDJ07Hr2WB2Ns2fR6R"}  # user token

        # download report as PDF
        report_download = requests.get(report, headers=headers)
        attachment = r"C:\\Users\\pwalsh\\Downloads\\" + report_name
        with open(attachment, 'wb') as file:
            file.write(report_download.content)

        mail.Subject = 'NEW REPORT! (test)'
        mail.Body = "***REPORT ATTACHED***"
        #mail.Body = response.text
        #mail.HTMLBody = '<h2>HTML Message body</h2>' #this field is optional

        # attach report to email
        mail.Attachments.Add(attachment)

        # cleanup attachment from downloads
        if os.path.exists(attachment):
            os.remove(attachment)
        else:
            print("The file does not exist")

    # report_found is False
    else:
        mail.Subject = 'REPORT BEING GENERATED! (test)'
        mail.Body = report

    # send email
    mail.Send()
