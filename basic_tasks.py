import requests
import re
import credentials
import time

LOGIN_URL = 'https://uf17-fdev.unifas.jp/UNIFAS/MS/webapi/v1/admin/authenticate.php'
SECURITY_GROUPS_URL = 'https://uf17-fdev.unifas.jp/UNIFAS/MS/admin/securityGroupList.php'
SSID_CREATION_URL = 'https://uf17-fdev.unifas.jp/UNIFAS/MS/webapi/v1/admin/securityGroupAdd.php'
SSID_DELETION_URL = 'https://uf17-fdev.unifas.jp/UNIFAS/MS/webapi/v1/admin/securityGroupList.php'

class UnifasAutomator:
    def __init__(self):
        self.csrf_token = None
        self.session = requests.Session()
        self.login_data = credentials.login_data
        # self.request_headers = {'Content-Type': 'application/json'}

    def login(self):
        import pdb; pdb.set_trace()
        login_session = self.session.post(LOGIN_URL, data=self.login_data)
        return login_session.ok

    def create_csrf_token(self):
        security_session = self.session.get(SECURITY_GROUPS_URL)
        token_match = re.findall(r'csrfToken\"\s*value=\"([0-9a-f]+)\">', security_session.text)
        self.csrf_token = token_match[0]
        return self.csrf_token

    def create_new_security_group(self, ssid_name, group_name, wpa2pwd):
        ssid_data = {"csrfToken": self.csrf_token, "essid": ssid_name, "gname": group_name,
                     "vlan": -2, "qos": 3, "stealth": 1, "wlan_separator": 0, "actmode": 0, "mac_filter_level": 1,
                     "auth": 0, "crypt": 3, "wpakey": wpa2pwd, "wpakey_span": 7200, "pmf": 0,
                     "act1_host": "", "act1_port": 1813, "act1_cred": "", "act2_host": "", "act2_port": 1813,
                     "act2_cred": "", "act_delim": 0, "act_interim": 0, "scj_defmode": 1, "acustom": 0, "afast_mode": 0,
                     "sns_custom": 0, "byod_custom": 0}
        query_params = {"context": "save"}

        ssid_session = self.session.post(SSID_CREATION_URL, params=query_params, data=ssid_data)
        return ssid_session.ok

    def delete_security_group(self, ssid_name):
        # Todo
        ssid_data = None
        '''csrfToken
        4edb9550294a3e3654650571292d2cd92271b33df32a0c2c
        sg-list-table_length
        300
        sg_delete[]
        2999
        '''
        query_params = {"context": "save"}

    def get_security_group_list(self):
        # Todo
        url = 'https://uf17-fdev.unifas.jp/UNIFAS/MS/webapi/v1/admin/securityGroupList.php'
        query_params = {"_": int(time.time())}
        get_session = self.session.get(url, params=query_params)
        print(get_session)

    def verify_session_and_rebuild(self, build_csrf_token):
        if not self.session:
            self.session = requests.Session()
            self.login()
            if build_csrf_token:
                self.create_csrf_token()

if __name__ == '__main__':
    unifas = UnifasAutomator()
    unifas.login()
    unifas.get_security_group_list()
    unifas.create_csrf_token()
    unifas.create_new_security_group("HydTestConnection", "HydTestGroup", "HydTestConnection")
