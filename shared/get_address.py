import ipaddress    # nopep8
import sys    # nopep8
from subprocess import check_output    # nopep8

# Get IPv6 address
# On Windows platform, you get a relatively simple json structure
# On Linux platform, you get "ip -6 -json address" output parsed as json.loads() object directly


def getIpAddress6():
    addressStructure = {}
    if sys.platform == 'win32':
        rawIpOutput = check_output(
            ["cmd", "/c", "chcp 437 > nul && ipconfig /all"], universal_newlines=True)
        currentInterfaceName = None
        for line in rawIpOutput.splitlines():
            isInterfaceLine = ("adapter" in line) and line.endswith(":")
            if (isInterfaceLine):
                currentInterfaceName = line.split(
                    'adapter ', 1)[1].split(':')[0]
                addressStructure[currentInterfaceName] = {
                    "global": [],
                    "private": []
                }
                continue
            isIPv6AddressLine = line.startswith("   IPv6 Address")
            if isIPv6AddressLine:
                addressSection = line.split(': ', 1)[1].split('(', 1)
                address = addressSection[0]
                preferred = addressSection[1].split(')', 1)[0]
                information = ipaddress.ip_address(address)

                # Preferred or Deprecated
                isDeprecated = preferred == "Deprecated"
                isPrivateAddress = information.is_global == False
                if isPrivateAddress:
                    addressStructure[currentInterfaceName]["private"].append(
                        {"address": address, "deprecated": isDeprecated})
                    continue
                if isPrivateAddress == False:
                    addressStructure[currentInterfaceName]["global"].append(
                        {"address": address, "deprecated": isDeprecated, "temporary": False})
                    continue
            isTemporaryIPv6AddressLine = line.startswith(
                "   Temporary IPv6 Address")
            if isTemporaryIPv6AddressLine:
                addressSection = line.split(': ', 1)[1].split('(', 1)
                address = addressSection[0]
                preferred = addressSection[1].split(')', 1)[0]
                information = ipaddress.ip_address(address)

                # Preferred or Deprecated
                isDeprecated = preferred == "Deprecated"
                addressStructure[currentInterfaceName]["global"].append(
                    {"address": address, "deprecated": isDeprecated, "temporary": True})
    if sys.platform == 'linux':
        import json
        rawIpOutput = check_output(
            ["ip", "-6", "-json", "addr"], universal_newlines=True)
        addressStructure = json.loads(rawIpOutput)

    return addressStructure
