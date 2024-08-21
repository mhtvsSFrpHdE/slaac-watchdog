import ipaddress    # nopep8

# Test if address 2 is in the same subnet as address 1


def sameSubnet(address1String: str, address2String: str, prefixLength: int):
    maskString = ipaddress.ip_network(
        "::0/{prefixLength}".format(prefixLength=prefixLength)).hostmask.exploded
    networkTemplate = '0000:0000:0000:0000:0000:0000:0000:0000'
    subnetArray = list(networkTemplate)
    explodedAddress1String = ipaddress.ip_address(address1String).exploded
    for index, item in enumerate(maskString):
        if item != "f":
            subnetArray[index] = (explodedAddress1String[index])
        else:
            break
    subnetString = "{address}/{prefixLength}".format(
        address="".join(subnetArray), prefixLength=prefixLength)
    subnet = ipaddress.ip_network(subnetString)

    address2 = ipaddress.ip_network(address2String)
    isSameSubnet = address2.subnet_of(subnet)
    return isSameSubnet
