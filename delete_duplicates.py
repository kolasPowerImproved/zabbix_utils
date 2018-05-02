from pprint import pprint
from pyzabbix import ZabbixAPI, ZabbixAPIException

SERVER_ZABBIX = 'http://192.168.33.65/zabbix'
LOGIN_ZABBIX = 'kolas'
PASSWORD_ZABBIX = ''

z = ZabbixAPI(SERVER_ZABBIX)
z.login(user=LOGIN_ZABBIX, password=PASSWORD_ZABBIX)


