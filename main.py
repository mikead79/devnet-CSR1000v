from ncclient import manager
from xml.dom.minidom import *
from tabulate import *
import xmltodict


m = manager.connect(
    host="192.168.56.101",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
    )

def print_interfaces():
    netconf_filter = """
    <filter>
        <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
    </filter>
    """

    netconf_reply = m.get(filter = netconf_filter)

    netconf_reply_dict = xmltodict.parse(netconf_reply.xml)

    ietf_list = []
    i = 0
    for interface in netconf_reply_dict["rpc-reply"]["data"]["interfaces-state"]["interface"]:
        i += 1
        interf = [i, interface['name'], interface['phys-address']]
        ietf_list.append(interf)
    table_header = ['ID', 'Name', 'MAC add']
    print(tabulate(ietf_list, table_header))


def create_interface(name, description, ip, subnet):
    new_interface = """<config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
              <name>{int_name}</name>
              <description>{int_desc}</description>
              <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
              <enabled>true</enabled>
              <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                      <ip>{ip_address}</ip>
                      <netmask>{subnet_mask}</netmask>
                    </address>
              </ipv4>
            </interface>
      </interfaces>
    </config>""".format(int_name=name,
                        int_desc=description,
                        ip_address=ip,
                        subnet_mask=subnet)

    try:
        netconf_reply = m.edit_config(new_interface, target="running")
        print("The interface was created!")
    except:
        print("There was an error on trying to create de interface")


def del_interface(name):
    to_delete = """<config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface operation='delete'>
              <name>{int_name}</name>
            </interface>
      </interfaces>
    </config>""".format(int_name=name)

    try:
        netconf_reply = m.edit_config(to_delete, target="running")
        print("The interface was deleted!")
    except:
        print("There was an error on trying to delete de interface")


def tabla_routing():
    pass


print("""
Available operations on CSR1000v router:
    1. Show the interfaces and their addresses
    2. Create a loopback interface
    3. Delete a loopback interface
    4. Show the routing table Obtener la tabla de routing y crear una tabla con Identificador (0,1,2...), Red de destino, e Interfaz de salida.
""")

while True:
    op = input("Choose an operation (by entering the corresponding number or 0 to exit): ")
    if op == '1':
        print_interfaces()
    elif op == '2':
        name = input("Enter the name of the interface (ex: Loopback22): ")
        desc = input("Enter a short description: ")
        ipv4 = input("Enter the IP address of the interface (ex: 22.22.22.22): ")
        subnet = input("Enter the subnet mask: ")
        create_interface(name, desc, ipv4, subnet)
    elif op == '3':
        print_interfaces()
        name = input("Enter the loopback interface you want to delete from the list above: ")
        del_interface(name)
    elif op == '4':
        print_routes()
    elif op == '0':
        break
    print()

m.close_session()






