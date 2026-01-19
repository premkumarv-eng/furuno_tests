import requests
import re
import credentials
import time

LOGIN_URL = 'https://uf17-fdev.unifas.jp/UNIFAS/MS/webapi/v1/admin/authenticate.php'
SECURITY_GROUPS_URL = 'https://uf17-fdev.unifas.jp/UNIFAS/MS/admin/securityGroupList.php'
ALL_SECURITY_GROUPS = 'https://uf17-fdev.unifas.jp/UNIFAS/MS/webapi/v1/admin/securityGroupList.php'
SSID_CREATION_URL = 'https://uf17-fdev.unifas.jp/UNIFAS/MS/webapi/v1/admin/securityGroupAdd.php'
SSID_DELETION_URL = 'https://uf17-fdev.unifas.jp/UNIFAS/MS/webapi/v1/admin/securityGroupList.php?context=delete'

class UnifasAutomator:
    def __init__(self):
        self.csrf_token = None
        self.session = requests.Session()
        self.login_data = credentials.login_data
        self.request_headers = {'Content-Type': 'application/json'}

    def login(self):
        login_session = self.session.post(LOGIN_URL, data=self.login_data)
        self.session.headers.update({
                                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
                                        "Accept": "application/json, text/javascript, */*; q=0.01",
                                        "X-Requested-With": "XMLHttpRequest"})
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

    def delete_security_group(self, ssid_name, group_name):
        group_id = None
        security_groups = unifas.get_security_group_list()
        for security_group in security_groups:
            if security_group[3] == ssid_name:
                group_id = re.findall(r'value=.*(\d{4})', "".join(security_group))
                break
        if group_id is None:
            print("SSID not deleted")
            return None
        data = {'csrfToken': self.csrf_token, 'sg-list-table_length': '300', 'sg_delete[]': f'{group_id[0]}'}
        result = self.session.post(SSID_DELETION_URL, data=data)
        result = result.json()
        if result['success'] and group_name in result['message']:
            return True
        return False

    def get_security_group_list(self):
        query_params = {"_": int(time.time() * 1000)}
        get_session = self.session.get(ALL_SECURITY_GROUPS, params=query_params)
        print(get_session)
        if get_session.ok:
            return get_session.json()['data']
        return None

    def verify_session_and_rebuild(self, build_csrf_token):
        if not self.session:
            self.session = requests.Session()
            self.login()
            if build_csrf_token:
                self.create_csrf_token()

if __name__ == '__main__':
    unifas = UnifasAutomator()
    unifas.login()
    unifas.create_csrf_token()
    unifas.create_new_security_group("HydTestConnection2", "HydTestGroup", "HydTestConnection")
    unifas.delete_security_group("HydTestConnection2", 'HydTestGroup')
