from ncclient import manager
from xml.dom.minidom import *

m = manager.connect(
    host="192.168.56.101",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
    )

netconf_filter = """
<filter>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native" />
</filter> """

netconf_filtered_reply = m.get_config(source="running", filter=netconf_filter)
print(parseString(netconf_filtered_reply.xml).toprettyxml())
