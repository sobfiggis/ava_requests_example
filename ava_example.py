"""
Avabur HTTP(s) example.

We will use this to retrieve data from Avabur.

To upload this data into google sheets you can add to this script using the
Google Sheets python API
https://developers.google.com/sheets/api/quickstart/python
"""
#   We will use requests since it has a Session handler automatically taking care
#   Of any cookies
import requests
import json


class Avabur(object):
    """avabur"""
    def __init__(self, username, password, base_url="https://avabur.com/"):
        """__init__

        :param username: The username you are authenticating with.
        :param password: The password you are authenticating with.
        """
        #   Setup URLs
        self.base_url = base_url
        self.login_url = self.base_url + "login.php"
        self.clan_donation_url = self.base_url + "clan_donations.php"
        self.clan_treasury_url = self.base_url + "clan_treasury.php"

        #   Create Session to magically handle our cookies and stuff
        self.session = requests.Session()

        #   Authenticate!
        self.authenticate(username, password)

    def authenticate(self, username, password):
        #   Vsyn does his stuff here, uses a single dictionary entry and has the data under "info"
        #   Normally a payload would look like:
        #   {"USERNAME": "figgis", "PASSWORD": "THISISTOTALLYMYPASSWORD"}
        payload = {"info": "acctname={}&password={}".format(username, password)}
        response = self.session.post(self.login_url, data=payload)
        #   We can return the response in case we want to poke at this later.
        #   Probably would be best just returning nothing in practice though.
        print(response.content)
        # return response

    def get_clan_donations(self, clan_id):
        """get_clan_donations

        :param clan_id: Your clan ID. You may not check other clan info. Legion is 26
        """
        payload = {"clan": clan_id}
        return self.session.post(self.clan_donation_url, data=payload)

    def get_clan_treasury(self, clan_id):
        """get_clan_treasury

        :param clan_id: Your clan ID. You may not check other clan info. Legion is 26
        """
        payload = {"clan": clan_id}
        return self.session.post(self.clan_treasury_url, data=payload)


def example_usage(username, password):
    """example_usage"""
    #   Create class which logs us in.
    ava = Avabur(username=username, password=password)

    #   lets get data and format it as json
    #   We need to use the ".content" to get data out of a requests(imported module) response
    donations = json.loads(ava.get_clan_donations(clan_id=26).content)
    funds = json.loads(ava.get_clan_treasury(clan_id=26).content)

    #   lets write this data to a file
    with open("donations.json", "w+") as file:
        file.write(json.dumps(donations))
    with open("funds.json", "w+") as file:
        file.write(json.dumps(funds))

    #   This is the point where we would do something with the Google Sheets API
    #   Uploading the content, etc. Their guide walks through it and super easy.
