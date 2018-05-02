import argparse
import sys
from pprint import pprint
from pyzabbix import ZabbixAPI, ZabbixAPIException

SERVER_ZABBIX = 'http://192.168.33.65/zabbix'
LOGIN_ZABBIX = 'kolas'
PASSWORD_ZABBIX = ''

z = ZabbixAPI(SERVER_ZABBIX)
z.login(user=LOGIN_ZABBIX, password=PASSWORD_ZABBIX)


def get_users(z):
    try:
        response = z.do_request(method="user.get", params={
            "filter": "alias",
            "output": ["userid", "alias"]
        })
        result = response['result']
    except ZabbixAPIException as e:
        print(e)
    print(result)


def get_user_info(z, user_name):
    try:
        response = z.do_request(method="user.get", params={
            "search": {"alias": user_name},
            "output": "extend"
        })
    except ZabbixAPIException as e:
        print(e)
    nick_name = response['result'][0]['alias']
    attempt_ip = response['result'][0]['attempt_ip']
    name = response['result'][0]['name']
    surname = response['result'][0]['surname']
    user_id = response['result'][0]['userid']

    pprint("nick name = " + nick_name)
    pprint("ip = " + attempt_ip)
    pprint("name = " + name)
    pprint("surname = " + surname)
    pprint("user id = " + user_id)


def get_user_id(z, user_name):
    try:
        response = z.do_request(method="user.get", params={
            "search": {"alias": user_name},
            "output": "extend"
        })
    except ZabbixAPIException as e:
        print(e)
    pprint(response['result'][0]["userid"])


def get_user_maps(z, user_name):
    id = get_user_id(user_name)
    try:
        response = z.do_request(method="map.get", params={
            "output": ["label"],
            "userids": id
        })
    except ZabbixAPIException as e:
        print(e)
    pprint(response)


def change_elements_label(z, sysmapid):
    for id in sysmapid:
        # pprint(sysmapid)
        new_request = []
        try:
            response = z.do_request(method="map.get", params={
                "sysmapids": id,
                "selectSelements": "extend",
                "output": "extend"
            })['result'][0]['selements']

            # pprint(response)

            for item in response:
                item["label"] = "{HOST.NAME}\n{HOST.IP}"
                new_request.append(item)
                # pprint(new_request)

        except ZabbixAPIException as e:
            print(e)
        else:
            try:
                resp = z.do_request(method="map.update", params={
                    "sysmapid": id,
                    "selements": new_request,
                })
            except ZabbixAPIException as e:
                print(e, id)

                def get_sysmapid():
                    ids = []
                    try:
                        response = z.do_request(method="map.get", params={
                            "output": "extends"
                        })
                        for id in response['result']:
                            i = id['sysmapid']
                            ids.append(i)
                    except ZabbixAPIException as e:
                        print(e)
                        return []
                    else:
                        return ids


def get_elements(z, sysmapid):
    try:
        response = z.do_request(method="map.get", params={
            "sysmapids": sysmapid,
            "output": "extend",
            "selectSelements": "extend",
            "selectLinks": "extend",
            "selectUsers": "extend",
            "selectUserGroups": "extend",
            "selectShapes": "extend",
            "selectLines": "extend"
        })

        # pprint(response['result'][0]['links'])

    except ZabbixAPIException as e:
        print(e)


def change_label_type(z, sysmapid):
    for id in sysmapid:
        # pprint(sysmapid)
        new_request = []
        try:
            response = z.do_request(method="map.get", params={
                "sysmapids": id,
                "output": "extend"
            })['result'][0]['label_type']

            #pprint(response)

            for item in response:
                item = "0"
                new_request.append(item)
                # pprint(new_request)

        except ZabbixAPIException as e:
            print(e)
        else:
            try:
                resp = z.do_request(method="map.update", params={
                    "sysmapid": id,
                    "selements": new_request,
                })
            except ZabbixAPIException as e:
                print(e, id)


def add_template_on_group(z, template_id, group_id):
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


def add_template_on_host(z, template_id, host_id):
    try:
        response = z.do_request(method="template.massadd", params={
            "templates": [
                {
                    "templateid": template_id
                }
            ],
            "hosts": [
                {
                    "hostid": host_id
                },
            ]
        })
        pprint(response)
    except ZabbixAPIException as e:
        print(e)


def search_hosts_duplicates(z, group_id):
    ids = z.do_request(method="host.get", params={
        "output": ["hostid"],
        "filter": {
            "groupids": group_id
        }
    })

    ips = []
    duplicates = []
    for i, host in enumerate(ids['result']):
        try:
            response = z.do_request(method="hostinterface.get", params={
                "output": ["ip", "hostid"],
                "hostids": host['hostid']
            })
        except ZabbixAPIException as e:
            print(e)
        else:
            ip = response['result'][0]['ip']
            if ip in ips:
                duplicates.append({
                    'ip': ip,
                    'id': response['result'][0]['hostid']
                })
            else:
                ips.append(ip)
    pprint(duplicates)

