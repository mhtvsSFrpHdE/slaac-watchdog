import os.path    # nopep8
import sys    # nopep8
import ipaddress    # nopep8
import subprocess    # nopep8

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))    # nopep8
import get_address    # nopep8
import same_subnet    # nopep8

from argparse import ArgumentParser    # nopep8
argParser = ArgumentParser()
argParser.add_argument("-p", "--prefixEvent", required=True,
                       help='Latest prefix from router, find with "ip monitor route dev eth0", line with "/" and "proto kernel"')
argParser.add_argument("-a", "--adapterName", required=True,
                       help='Which network adapter to monitor, find with "ip addr" or "/etc/network/interfaces"')
args = argParser.parse_args()

# Use parameter
argumentPrefixEvent = args.prefixEvent
argumentAdapterName = args.adapterName
print("Received prefix event: {prefixEvent}, on interface: {adapterName}".format(prefixEvent=argumentPrefixEvent, adapterName=argumentAdapterName))

# Get subnet
subnetString = argumentPrefixEvent.split("/", 1)[0]
subnet = ipaddress.ip_address(subnetString)
if subnet.is_private:
    print("Private subnet, ignore")
    exit()

# Get address
getAddress = get_address.getIpAddress6()
allAddrInfo = None
for interface in getAddress:
    if interface["ifname"] == "eth0":
        allAddrInfo = interface["addr_info"]
        break


def removeAddress(address: str):
    # ip address delete {local}/{prefixlen} dev {ifname}
    commandResult = subprocess.run(['ip', 'address', 'delete', address, "dev",
                                   argumentAdapterName], stdout=subprocess.PIPE, universal_newlines=True)
    print("Removing: {address}".format(address=address))
    needAdminPermission = 2
    if (commandResult.returncode == needAdminPermission):
        print("ip address delete error, check root permission")
        return
    if (commandResult.returncode != 0):
        print("ip address delete error, reason is unknown")
        return


# Remove old addresses and temporary addresses not belong to the new subnet
for addrInfo in allAddrInfo:
    addressString = addrInfo["local"]
    prefixLength = addrInfo["prefixlen"]
    address = ipaddress.ip_address(addressString)
    if address.is_private:
        continue
    shouldRemove = same_subnet.sameSubnet(
        subnetString, addressString, prefixLength) == False
    if shouldRemove:
        removeAddress(
            "{address}/{prefixLength}".format(address=addressString, prefixLength=prefixLength))
        continue
