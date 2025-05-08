import asyncio
import logging
import socket
import ipaddress
from typing import List, Tuple, Optional

import typer

logger = logging.getLogger(__name__)

app = typer.Typer()


COS_AVAILABLE_REGIONS = [
    "ap-beijing-1",
    "ap-beijing",
    "ap-nanjing",
    "ap-shanghai",
    "ap-guangzhou",
    "ap-chengdu",
    "ap-hongkong",
    "ap-chongqing",
    "ap-shenzhen-fsi",
    "ap-shanghai-fsi",
    "ap-beijing-fsi",
    "ap-hongkong",
    "ap-singapore",
    "ap-jakarta",
    "ap-seoul",
    "ap-bangkok",
    "ap-tokyo",
    "na-siliconvalley",
    "na-ashburn",
    "sa-saopaulo",
    "eu-frankfurt"
]


def is_internal_ip(ip: str) -> bool:
    """判断IP是否为内网IP"""
    try:
        ip_addr = ipaddress.ip_address(ip)
        return (
            ip_addr.is_private
            or ip_addr.is_loopback
            or ip_addr.is_link_local
            or ip_addr.is_reserved
            or ip_addr.is_multicast
        )
    except ValueError:
        return False

async def resolve_domain(domain: str) -> Tuple[str, Optional[List[str]]]:
    """异步解析域名并返回IP列表"""
    try:
        sockaddr = await asyncio.get_event_loop().getaddrinfo(
            domain, None, proto=socket.IPPROTO_TCP, family=socket.AF_INET
        )
        ips = list({addr[4][0] for addr in sockaddr})
        return (domain, ips)
    except (socket.gaierror, UnicodeError) as e:
        logger.error(f"Failed to resolve {domain}: {e}")
        return (domain, None)

async def check_domains_parallel(domains: List[str]) -> List[Tuple[str, List[str], bool]]:
    """并行检查域名列表的内网IP情况
        Args:
            domains (List[str]): 域名列表
            
        Returns:
            List[Tuple[str, List[str], bool]]: 解析结果列表, 每个元素包含域名、IP列表和是否包含内网IP的布尔值
    """
    tasks = [resolve_domain(domain) for domain in domains]
    results = await asyncio.gather(*tasks)
    
    processed_results = []
    for domain, ips in results:
        if not ips:
            processed_results.append((domain, [], False))
            continue
            
        has_internal = any(is_internal_ip(ip) for ip in ips)
        processed_results.append((domain, ips, has_internal))
    
    return processed_results


def format_cos_endpoint(region: str) -> str:
    return f"cos.{region}.myqcloud.com"

def get_region_from_cos_domain(domain: str) -> str:
    return domain.split('.')[1]


def detect_region():
    domains = [format_cos_endpoint(region) for region in COS_AVAILABLE_REGIONS]    
    for domain, _, has_internal_ip in asyncio.run(check_domains_parallel(domains)):
        if has_internal_ip:
            return get_region_from_cos_domain(domain)

@app.command(help="get the region info of the current network enviroment.")
def get_region():
    region = detect_region()
    
    if not region:
        typer.echo("Cannot detect your current region.")
        return
    
    typer.echo(f"Current region is: {region}")

if __name__ == "__main__":
    print(f"检测到的区域为: {detect_region()}")