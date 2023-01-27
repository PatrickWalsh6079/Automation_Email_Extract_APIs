Description: POC program to demonstrate that Security Scorecard reports can be automatically generated and sent to a customer
when an email is received in Outlook. Makes use of Security Scorecard APIs to add domains to a Security Scorecard portfolio,
generate Company Summary Reports, query available reports based on report ID, download the report as a PDF, and then sends PDF
report to a customer.

Uses the read_email.py, add_company_to_portfolio.py, generate_company_summary_report.py, and send_email.py files.

POC goals:
1. Program can be initiated by receiving an email in Outlook.
2. Program can filter received emails by certain criteria such as time received and Subject line.
3. Program can read content of email and extract website domain and other relevant information.
4. Program can add domain to Security Scorecard through APIs.
5. Program can generate reports using APIs.
6. Reports can be located using a unique report ID using APIs.
7. Reports can be downloaded using APIs.
8. Reports can be saved as a PDF and attached to an email.
9. Program notifies customer if report is taking a long time to generate.

Program can be initiated in 2 ways:
1. Run the main.py file from command line. Keep in mind that this will only work if an email is sitting in the Outlook Inbox 
that meets the following filter criteria from the read_email.py file:
email arrived within a specified time (received_dt = datetime.now() - timedelta(minutes=199)), and email has subject line 
'Attack Surface Summary Report (test)'. If no email is found that matches these criteria, the program will raise an exception and 
send an email to pwalsh@syscom.com with the appropriate error response.
2. Send an email (preferred method since it satisfies POC goal no. 1) from pwalsh@syscom.com to the same email with subject 
line 'Attack Surface Summary Report (test)'. Outlook has a rule setup that checks for this sender and subject line and runs a 
VBA script when triggered (macros must be enabled). The VBA script runs the main.py script.

*******************************************************************************************************************************
High level code walkthrough:

1. Once main.py file is run by one of the two methods described above, the program checks for an email that meets the noted
criteria. When initiated, the main.py program runs the read_email.py file. This file searches the text within the body of 
the email for the word 'Website:'. When this word is found, the read_email.py file assumes the next word is a valid domain such
as google.com. The program currently does not perform any normalization or take into account misspelled words (gogle.com), extra 
spaces (google. com), or other error handling.

2. The read_email.py file returns the domain found in the email using the get_website() function. The main.py file sets this 
domain value to the variable 'company' and uses that variable as input for the next step.

3. The main.py file runs the add_company_to_portfolio.py file, using the 'company' variable as input. The add_company_to_portfolio.py
file uses an API call to add the company domain to the portfolio 'Practice Portfolio'. This step is crucial because a company must
be added to a portfolio before a report can be generated.

4. After company domain has been added to the portfolio, the main.py file runs the check_score_available.py script. This script uses
an API call to check if there is a score available for the company domain. If domain is not in the portfolio, it will return an error
stating so and send an email to the pwalsh@syscom.com email. This should not happen, and if it does, it may mean that the 
add_company_to_portfolio.py script failed. If the domain is in the portfolio, the check_score_available.py script will check whether
there is a score available. If the score is still pending, the script will raise an error and send an email notifying pwalsh@syscom.com.
Otherwise, it will return a boolean value of True stating that the score is available.

5. Once the score has been confirmed is available, the main.py file runs the generate_company_summary_report.py file, using the
same 'company' variable as input. This file does several things. First, it generates a Company Summary Report using an API call. 
Next, it retrieves the report ID from this generated report. The file then queries all available reports (either completed or in
progress) and searches for the report with the same report ID. Sometimes reports can take several minutes or even hours to generate,
so the program uses a timeout feature to stop checking after a specified number of API calls. If the program times out, it will send an
email to pwalsh@syscom.com letting the customer know that a report is currently being generated. The timeout is specified in the
generate_company_summary_report.py file in the variable 'timeout'. By default, this variable is set to 10. This means the program
will timeout after 10 API calls querying the report. Each API call normally takes about 1 second. Reports normally are ready within
2-3 API calls, but it can take longer if the report is for a new domain that was just added to the portfolio. If the report was found,
the file returns two parameters: the URL of the report, and a boolean value of True stating that the report was found. These two
parameters are used for the final step of the process when the send_email.py file is run.

6. The main.py file calls the send_email.py file using the URL of the report and a boolean of whether the report was found. The 
send_email.py takes the URL of the report (if a report was found) and strips off the first part of the name, replacing the .json
portion of the URL with .PDF. It then downloads and saves the report as a PDF. Next, it attaches the PDF report to an email and sends
it to the customer (or in this case, the pwalsh@syscom.com email address). Finally, the PDF is deleted in a cleanup process so that
extra reports are not sitting in the download folder. If the report is not found and the boolean returns False, the script runs
a separate process and sends an email stating that the report is still being generated.