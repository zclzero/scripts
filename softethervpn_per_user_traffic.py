import prettytable as pt
import time
import json
import httplib
import ssl


class softether(object):

    def __init__(self, url, port, hubname, password):
        self.url = url
        self.port = port
        self.hubname = hubname
        self.password = password

    def get_session_list(self):
        parameters = {
          "jsonrpc": "2.0",
          "id": "rpc_call_id",
          "method": "EnumSession",
          "params": {
            "HubName_str": self.hubname
          }
        }
        data = json.dumps(parameters)
        headers = {
            "Content-Type": "application/json",
            'Content-Length': len(data),
            "Referer": self.url,
            "Cookie": 'JSESSIONID=2C6BBA00328C1C2F67794E50337D6E3A.N1TS002',
            "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1',
            "X-VPNADMIN-HUBNAME": self.hubname,
            "X-VPNADMIN-PASSWORD": self.password
            }
        conn = httplib.HTTPSConnection(self.url, self.port, context=ssl._create_unverified_context())
        conn.request("POST", "/api", data, headers)
        page = conn.getresponse().read()
        info = json.loads(page)["result"]["SessionList"]

        session_list = []
        field_names = []

        for i in info:
            session_dict = {}
            if i["Username_str"] == "SecureNAT":
                continue
            name = str(i["Name_str"]).split("-")[1].lower()+"-"+str(i["Name_str"]).split("-")[3]
            mbps = i["PacketSize_u64"]/1024/1024
            session_dict[name] = mbps
            session_list.append(session_dict)
            field_names.append(name)
        return field_names, session_list

    def print_title(self, field_names):
        tb = pt.PrettyTable()
        tb.field_names = field_names
        tb.set_style(pt.MSWORD_FRIENDLY)
        print tb

    def print_traffic(self, session_list):
        for i in session_list:
            print "|", str(i[i.keys()[0]]).center(len(i.keys()[0])),
        print "|"


if __name__ == "__main__":
    url = ""
    port = 443
    hubname = ""
    password = ""

    n = 0
    while True:
        st = softether(url, port, hubname, password)
        field_names, session_list = st.get_session_list()
        if n % 10 == 0 or old_field_names != len(field_names):
            st.print_title(field_names)
            st.print_traffic(session_list)
            n = 1
        else:
            st.print_traffic(session_list)
            n += 1
        old_field_names = len(field_names)
        time.sleep(1)
