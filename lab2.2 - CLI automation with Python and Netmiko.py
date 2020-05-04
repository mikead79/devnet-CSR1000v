from netmiko import ConnectHandler

sshCLI = ConnectHandler(
    device_type='cisco_ios',
    host='192.168.56.101',
    port=22,
    username='cisco',
    password='cisco123!'
)

print("Sending 'show ip interface brief' command to the router'...")
output = sshCLI.send_command("show ip interface brief")
print(f"IP interface status and configuration: \n{output}\n")

config_commands = [
    'int loopback 1',
    'ip address 2.2.2.2 255.255.255.0',
    'description Loopback 1']
output = sshCLI.send_config_set(config_commands)
print(f"Config output from the device: {output}")

output = sshCLI.send_command("show ip interface brief")
print(f"IP interface status and configuration: \n{output}\n")

config_commands = [
    'int loopback 2',
    'ip address 2.2.2.2 255.255.255.0',
    'description NewButSame']
output = sshCLI.send_config_set(config_commands)
print(f"Config output from the device: {output}")

output = sshCLI.send_command("show ip interface brief")
print(f"IP interface status and configuration: \n{output}\n")
