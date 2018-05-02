from pprint import pprint
from pyzabbix import ZabbixAPI, ZabbixAPIException

SERVER_ZABBIX = 'http://192.168.33.65/zabbix'
LOGIN_ZABBIX = 'kolas'
PASSWORD_ZABBIX = ''

z = ZabbixAPI(SERVER_ZABBIX)
z.login(user=LOGIN_ZABBIX, password=PASSWORD_ZABBIX)


def add_template_on_group(template_id, group_id):
    icmp_ping = "10104"
    dude_not_addaed_hosts = "37"
    try:
        response = z.do_request(method="template.massadd", params={
                "templates": [
                    {
                           "templateid": template_id
                    }
                ],
                "groups": [
                    {
                        "groupid": group_id
                    }
                ]
            })
        pprint(response)
    except ZabbixAPIException as e:
        print(e)


def add_template_on_host():
    try:
        response = z.do_request(method="template.massadd", params={
            "templates": [
                {
                    "templateid": "10104"
                }
            ],
            "hosts": [
                {
                    "hostid": "18886"
                },
            ]
        })
        pprint(response)
    except ZabbixAPIException as e:
        print(e)


def get_hosts_ids():
    try:
        # response = z.do_request(method="hostgroup.get", params={
        #     "output": ["hostid"],
        #     "selectGroups": "41"
        #     "filter":
        # })
        # pprint(response)

        response = z.host.get(status=1)
        pprint(response)
    except ZabbixAPIException as e:
        print(e)

get_hosts_ids()