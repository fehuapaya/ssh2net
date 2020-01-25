#!/usr/bin/env python
from datetime import datetime

from netmiko import ConnectHandler

IOSXE_TEST = {
    "host": "172.18.0.11",
    "username": "vrnetlab",
    "password": "VR-netlab9",
    "device_type": "cisco_xe",
    "test_commands": ["show run", "show version"],
}

NXOS_TEST = {
    "host": "172.18.0.12",
    "username": "vrnetlab",
    "password": "VR-netlab9",
    "device_type": "cisco_nxos",
    "test_commands": ["show run", "show version"],
}

IOSXR_TEST = {
    "host": "172.18.0.13",
    "username": "vrnetlab",
    "password": "VR-netlab9",
    "device_type": "cisco_iosxr",
    "test_commands": ["show run", "show version"],
}

EOS_TEST = {
    "host": "172.18.0.14",
    "username": "vrnetlab",
    "password": "VR-netlab9",
    "device_type": "arista_eos",
    "test_commands": ["show run", "show version"],
}

JUNOS_TEST = {
    "host": "172.18.0.15",
    "username": "vrnetlab",
    "password": "VR-netlab9",
    "device_type": "juniper_junos",
    "test_commands": ["show configuration", "show version"],
}

test_hosts = [IOSXE_TEST]


def main():
    for host in test_hosts:
        commands = host.pop("test_commands")
        conn = ConnectHandler(**host)
        for command in commands:
            print(f"Sending command: '{command}'")
            print("*" * 80)
            command_start_time = datetime.now()
            r = conn.send_commands(command)
            command_end_time = datetime.now()
            print(r)
            print("*" * 80)
            print(
                f"Sending command: '{command}' took {command_end_time - command_start_time} seconds!"
            )
            print("*" * 80)
            print()


if __name__ == "__main__":
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    print(f"Full test took {end_time - start_time} seconds!")
