import re
import sys
import requests
from bs4 import BeautifulSoup

login = "guillaume.comte10@gmail.com"
password = "xxx"  # TODO get it from env

login_url = "https://kiezelpay.com/login"
login_form_url = "https://kiezelpay.com/webservices/authentication.php"
dashboard_url = "https://kiezelpay.com/account/dashboard"

if __name__ == "__main__":
    sess = requests.Session()
    resp = sess.get(login_url)
    csrf = re.search(r"csrf: '(\w+)'", resp.text).group(1)
    # print(csrf)
    resp = sess.post(
        login_form_url,
        data={
            "action": "login",
            "actionData[email]": login,
            "actionData[password]": password,
            "actionData[rememberMe]": "true",
            "actionData[csrf]": csrf,
        },
    )
    # print(resp.text)
    if not resp.ok:
        print("Could not login to KiezelPay")
        print(resp.text)
        sys.exit(-1)
    resp = sess.get(dashboard_url)
    if not resp.ok:
        print("Could not open KiezelPay dashboard")
        print(resp.text)
        sys.exit(-1)
    soup = BeautifulSoup(resp.text, "html.parser")
    # print(soup.prettify())
    print(soup.find_all("h2"))
