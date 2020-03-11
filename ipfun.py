#!/usr/bin/env python3


from ipaddress import ip_address, ip_network, IPv4Network, IPv6Network


def isIpInSubnet(ip: str, subnet: str, ipv6_host_mask: int = 64) -> bool:
    valid_ip = ip_address(ip)
    valid_subnet = ip_network(subnet)

    host_mask = str(ipv6_host_mask) if valid_ip.version == 6 else "32"
    valid_ip_prefix = ip_network(f"{ip}/{host_mask}", strict=False)

    return valid_subnet.overlaps(valid_ip_prefix)


def isIpInSubnetManual(ip: str, subnet: str) -> bool:
    pass


# for method in (isIpInSubnet, isIpInSubnetManual):
for method in (isIpInSubnet,):
    print(f"-- Using {method.__name__}")
    print(isIpInSubnet("1.1.1.1", "1.1.1.0/25"))  # True
    print(isIpInSubnet("1.1.1.129", "1.1.1.0/25"))  # False
    print(isIpInSubnet("1.1.1.1", "1.1.1.0/25"))  # True
    print(isIpInSubnet("69::69", "69::/64"))  # True
    print(isIpInSubnet("69:a::69", "69::/64"))  # False
