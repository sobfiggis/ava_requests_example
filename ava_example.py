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
        self.clan_activity_url = self.base_url + "clan_activity.php"
        self.clan_ranks_url = self.base_url + "clan_ranks.php"
        self.clan_buildings_url = self.base_url + "clan_buildings.php"
        self.clan_members_url = self.base_url + "clan_members.php"
        self.clan_bans_url = self.base_url + "clan_bans.php"
        self.clan_profile_url = self.base_url + "clan_view.php"
        self.crystal_boost_url = self.base_url + "boosts.php"
        self.training_boost_url = self.base_url + "training.php"
        self.market_url = self.base_url + "market.php"
        self.activity_url = self.base_url + "account_activity.php"

        #   Create Session to magically handle our cookies and stuff
        self.session = requests.Session()

        #   Authenticate!
        self.authenticate(username, password)

    def authenticate(self, username, password):
        """authenticate

        :param username: A username.
        :param password: A password.
        """
        #   Vsyn does his stuff here, uses a single dictionary entry and has the data under "info"
        #   Normally a payload would look like:
        #   {"USERNAME": "figgis", "PASSWORD": "THISISTOTALLYMYPASSWORD"}
        payload = {"info": "acctname={}&password={}".format(username, password)}
        response = self.session.post(self.login_url, data=payload)
        #   We can return the response in case we want to poke at this later.
        #   Probably would be best just returning nothing in practice though.

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

    def get_clan_activity(self, page, type0=True, type1=True, type2=True, type3=True, type4=True):
        """
        order (open the damn clan activity log and look at the options if you are confused): 
            type0 = Administration
            type1 = Member Activity
            type2 = Clan Levels
            type3 = Buildings
            type4 = Donations
        """
        payload = {"Type0": "true",
                   "Type1": "true",
                   "Type2": "true",
                   "Type3": "true",
                   "Type4": "true"}

        if not type0:
            payload['Type0'] = "false"
        if not type1:
            payload['Type1'] = "false"
        if not type2:
            payload['Type2'] = "false"
        if not type3:
            payload['Type3'] = "false"
        if not type4:
            payload['Type4'] = "false"
        self.session.post(self.clan_activity_url, data=payload)

    def get_clan_bans(self):
        """get_clan_bans"""
        return self.session.post(self.clan_bans_url)

    def get_clan_members(self, clan_id):
        """get_clan_members

        :param clan_id:
        """
        payload = {'clan_id': clan_id}
        return self.session.post(self.clan_members_url, data=payload)

    def get_clan_ranks(self, clan_id):
        """get_clan_ranks

        :param clan_id:
        """
        payload = {'clan_id': clan_id}
        return self.session.post(self.clan_ranks_url, data=payload)

    def get_clan_profile(self, clan_id):
        payload = {'clan_id': clan_id}
        return self.session.post(self.clan_profile_url, data=payload)

    def get_crystal_boosts(self):
        return self.session.post(self.crystal_boost_url)

    def get_training_boosts(self):
        return self.session.post(self.training_boost_url)

    def get_market(self, item_type, page=0):
        payload = {'type': item_type,
                   'page': page,
                   'q': '',
                   'll': '',
                   'hl': '',
                   'st': ''}
        return self.session.post(self.market_url, data=payload)


def example_usage(username, password):
    """example_usage"""
    #   Create class which logs us in.
    ava = Avabur(username=username, password=password)

    #   lets get data and format it as json
    #   We need to use the ".content" to get data out of a requests(imported module) response
    donations = json.loads(ava.get_clan_donations(clan_id=26).content)
    funds = json.loads(ava.get_clan_treasury(clan_id=26).content)

    #   lets write some of this data to a file
    with open("donations.json", "w+") as file:
        file.write(json.dumps(donations))
    with open("funds.json", "w+") as file:
        file.write(json.dumps(funds))

    #   This is the point where we would do something with the Google Sheets API
    #   Uploading the content, etc. Their guide walks through it and super easy.
