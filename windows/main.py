import os.path    # nopep8
import json    # nopep8
import sys    # nopep8
import subprocess    # nopep8

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))    # nopep8
import get_address    # nopep8
import same_subnet    # nopep8

from argparse import ArgumentParser    # nopep8
argParser = ArgumentParser()
argParser.add_argument("-p", "--prefix", type=int, required=True,
                       help="IPv6 Subnet prefix length in router settings or from ISP")
argParser.add_argument("-a", "--adapterName", required=True,
                       help='Which network adapter to monitor, find with "ipconfig" or Control Panel > Network and Internet > Network and Sharing Center > Change adapter settings > Rename this connection > Copy name')
argParser.add_argument("-c", "--config", default="known_address.json",
                       help='Config file, default is "known_address.json"')
args = argParser.parse_args()

# Use parameter
argumentSubnetPrefixLength = args.prefix
argumentAdapterName = args.adapterName
knownAddressFileName = args.config

# Create empty file if not exist
fileExist = os.path.isfile(knownAddressFileName)
if fileExist == False:
    knownAddressFileStructure = []
    with open(knownAddressFileName, 'w', encoding='utf-8') as jsonFile:
        json.dump(knownAddressFileStructure, jsonFile,
                  ensure_ascii=False, indent=4)

# Load known addresses from JSON file
knownAddress = None
with open(knownAddressFileName, 'r', encoding='utf-8') as knownAddressFile:
    knownAddress = json.load(knownAddressFile)
if len(knownAddress) == 0:
    print("No known address found. Current addresses considered as known addresses.")

# Try find new addresses, skip temporary addresses in this step
# So known address should never contains temporary addresses
getAddress = get_address.getIpAddress6()
newAddress = []
for item in getAddress[argumentAdapterName]["global"]:
    address = item["address"]

    isTemporary = item["temporary"]
    if isTemporary:
        continue

    if address not in knownAddress:
        newAddress.append(address)
if len(newAddress) == 0:
    print("No new address found.")
    exit()


def removeAddress(address: str):
    # powershell -ExecutionPolicy Bypass -Command "Remove-NetIPAddress -IPAddress {address} -Confirm:$false"
    commandResult = subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-Command',
                                   "Remove-NetIPAddress -IPAddress {address} -Confirm:$false".format(address=address)], stdout=subprocess.PIPE, universal_newlines=True)
    print("Removing: {address}".format(address=address))
    needAdminPermission = "PermissionDenied"
    if (needAdminPermission in commandResult.stdout):
        print("powershell Remove-NetIPAddress error, check admin permission")


# Has new address, remove old addresses and temporary addresses not belong to the same subnet of new address
for item in getAddress[argumentAdapterName]["global"]:
    address = item["address"]

    isTemporary = item["temporary"]
    if isTemporary:
        isSameSubnet = same_subnet.sameSubnet(
            newAddress[0], address, argumentSubnetPrefixLength)
        if isSameSubnet == False:
            removeAddress(address)
        continue

    shouldRemove = (address in knownAddress)
    if shouldRemove:
        removeAddress(address)
        continue

# Old address should all removed, record new addresses as known addresses
with open(knownAddressFileName, 'w', encoding='utf-8') as jsonFile:
    json.dump(newAddress, jsonFile, ensure_ascii=False, indent=4)
