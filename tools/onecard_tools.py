import os
import re
from sys import exit, path

import requests


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
path.append(f'{__location__}/.transmogrify')
from credentials import get_credentials # personal package for credentials
u, p = get_credentials() # netid, password, google sheets token


login_url = "https://onecardweb.richmond.edu/login/ldap.php"
balance_history_url = "https://onecardweb.richmond.edu/student/svc_history.php"
balance_query_url = "https://onecardweb.richmond.edu/student/svc_history_view.php"

def clean_date(date):
    if len(date[0]) == 1: # add trailing 0 if single digit
        date[0] = "0"+date[0]

def write_response(response):
    with open("result_page.html", "w") as out_file:
        out_file.write(response.text.strip().replace("\t",""))

def get_session(response):
    return re.findall(r'__sesstok = \'(.*)\'',response.text)[0]

def parse_balance(response):
    results = []
    for match in re.findall(r'<tr class="row\d*">\n.*width="140">(.*)<\/td>\n.*width="120">(.*)<\/td>\n.*\n.*\);">(.*)<\/a>\n.*\n.*[$](.*)<\/td>', response.text.strip().replace("\t","")):
        timestamp, title, plan, amount = match
        results.append((timestamp,title,float(amount)))
    return results

def get_transactions(from_date,to_date):
    with requests.Session() as s:
        #print("getting session...")
        s.head(balance_history_url)
        sid = get_session(s.get(balance_history_url))
        #print(f"session obtained, logging in as {u}...")
        response = s.post(
            url=login_url+"",
            data={'user': u,'pass': p,'__sesstok': sid},
            headers={'Referer': balance_history_url}
        )
        sid = get_session(response)
        #print(f"logged in as {u}, getting spending")
        balance_history_payload = {
            'FromMonth': from_date[0], 'FromDay': from_date[1], 'FromYear': from_date[2],
            'ToMonth': to_date[0], 'ToDay': to_date[1], 'ToYear': to_date[2],
            'plan': 'S_All_',
            '__sesstok': sid
        }
        response = s.post(
            url=balance_query_url,
            data=balance_history_payload,
            headers={'Referer': balance_history_url}
        )
        return parse_balance(response)
        #print(results)


if __name__ == "__main__":
    from_date = ('07','18','2014')
    to_date = ('08','18','2030')

    print(get_transactions(from_date,to_date))