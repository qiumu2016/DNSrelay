import argparse

parser = argparse.ArgumentParser(description='Domain Name System')

group = parser.add_mutually_exclusive_group()
group.add_argument("-d", action="store_true", help="Level-1 Debuging")
group.add_argument("-dd", action="store_true", help="Level-2 Debuging")

parser.add_argument("--addr", help="DNS server IP address", type=str)
parser.add_argument("--file", help="Default hostfile: \"dnsrelay.txt\"", type=str)
args = parser.parse_args()
