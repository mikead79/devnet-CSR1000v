from ncclient import manager

m = manager.connect(
    host="192.168.56.101",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
    )

print("The suported capabilities are:")
for capability in m.server_capabilities:
    if "Cisco-IOS-XE-cdp" in capability:
        print(capability)
