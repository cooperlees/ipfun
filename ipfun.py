#!/usr/bin/env python3


from ipaddress import ip_address, ip_network, IPv4Network, IPv6Network


def isIpInSubnet(ip: str, subnet: str, ipv6_host_mask: int = 64) -> bool:
    valid_ip = ip_address(ip)
    valid_subnet = ip_network(subnet)

    host_mask = str(ipv6_host_mask) if valid_ip.version == 6 else "32"
    valid_ip_prefix = ip_network(f"{ip}/{host_mask}", strict=False)

    return valid_subnet.overlaps(valid_ip_prefix)


def ipToInt(ip: str) -> int:
    o = list(map(int, ip.split('.')))
    return (2^24 * o[0]) + (2^16 * o[1]) + (2^8 * o[2]) + o[3]


# TODO: IPv6 support
def isIpInSubnetManual(ip: str, subnet: str) -> bool:
    ip_int = ipToInt(ip)
    print(f"IP Addr Int:\t{ip_int}")
    ip_bin = "{0:b}".format(ip_int)

    subnet_addr, subnet_mask = subnet.split("/")

    wildcard_mask = 32 - int(subnet_mask)
    subnet_int = ipToInt(subnet_addr)
    print(f"Subnet Int:\t{subnet_int}")
    subnet_bin = "{0:b}".format(subnet_int)
    print(f"Subnet Bits:\t{subnet_bin}")
    print(f"IP Addr Bits:\t{ip_bin}")

    chop_amount = 0
    for i in range(wildcard_mask):
        if i < len(subnet_bin):
            chop_amount += int(subnet_bin[len(subnet_bin)-1-i]) * 2**i

    min_addr = subnet_int - chop_amount
    max_addr = min_addr + 2**wildcard_mask - 1

    return min_addr <= ip_int and ip_int <= max_addr


for method in (isIpInSubnet, isIpInSubnetManual):
    print(f"-- Using {method.__name__}")
    print(method("1.1.1.1", "1.1.1.0/25"))  # True
    print(method("1.1.1.129", "1.1.1.0/25"))  # False
    print(method("1.1.1.1", "1.1.1.0/25"))  # True
    print(method("255.1.1.1", "255.1.1.0/25"))  # True
    if method.__name__ == "isIpInSubnet":
        print(method("69::69", "69::/64"))  # True
        print(method("69:a::69", "69::/64"))  # False
    print()
