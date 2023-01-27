"""
Filename: read_email.py
Description: Reads email and extracts company domain to be passed to
add_company_to_portfolio.py file. Called from main.py file. Uses
filters for datetime sent and Subject line for reading the email.
"""

from datetime import datetime, timedelta
import win32com.client


# create Outlook and MAPI objects
outlook = win32com.client.Dispatch('outlook.application')
mapi = outlook.GetNamespace("MAPI")

# this shows email account in use
'''
for account in mapi.Accounts:
	print(account.DeliveryStore.DisplayName)
'''


def get_website():
    """
    Reads email and gets the website domain from the body of the email.
    """

    # create inbox and messages objects
    inbox = mapi.GetDefaultFolder(6)
    messages = inbox.Items

    # Filter on emails received within certain time and with certain Subject line
    received_dt = datetime.now() - timedelta(minutes=199)
    received_dt = received_dt.strftime('%m/%d/%Y %H:%M %p')
    messages = messages.Restrict("[ReceivedTime] >= '" + received_dt + "'")
    #messages = messages.Restrict("[SenderEmailAddress] = 'pwalsh@syscom.com'")  # filter not working
    messages = messages.Restrict("[Subject] = 'Attack Surface Summary Report (test)'")

    # initialize variable
    website = ''


    # read through body of email to find domain
    for i in messages:
	    #print(i.Body)
        compartmented_body = i.Body.split()
        #print(compartmented_body)

        # find website
        counter = 0
        for j in compartmented_body:
            #print(i)
            if j == 'Website:':
                website = compartmented_body[counter + 1]
                break
            counter += 1

    # if no email found according to filter specifications above
    if website == '':
	    #print("No email found according to the given filter specifications")
        raise Exception("No email found according to the given filter specifications")
    print("\nWebsite: " + website)

    return website
