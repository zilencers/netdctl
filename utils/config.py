from dataclasses import dataclass


@dataclass
class Config:
    """Class for keeping track of internal configuration """
    netdctl_path: str = '/etc/netdctl/network.d'
    archive_path: str = '/etc/netdctl/archive'
    networkd_path: str = '/etc/systemd/network'
    tmp_path: str = '/tmp/netdctl'
    template_path: str = '/var/lib/netdctl/templates' 
    mac_path: str = '/sys/class/net/{iface}/address'
    backup_dir: str = '/etc/netdctl/backup'
    prefix_spacing: int = 10
    bridge_ext: str = 'netdev'
    link_ext: str = 'link'
    net_ext: str = 'network'
    vlan_ext: str = 'netdev'
    tpl_attach: str = 'attach.network'
    tpl_bridge: str = 'bridge.netdev'
    tpl_dhcp: str = 'dhcp.network'
    tpl_link: str = 'template.link'
    tpl_static: str = 'static.network'
    tpl_vlan: str = 'vlan.netdev'
    arcname: str = 'archive-{datetime}.zip'