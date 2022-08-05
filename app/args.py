import argparse
from utils.validate import Validate


class Arguments:
    def __init__(self):
        self._parser = None
        self._args = self._parse()
        self._set_command()

        # if self._args.no_check is False:
        #     Validate.validate(self._args)

    @property
    def get_args(self):
        return self._args


    def _parse(self):
        self._parser = argparse.ArgumentParser(allow_abbrev=False)
        self._parser.add_argument('cmd', choices=['apply',
                                                    'attach',
                                                    'archive',
                                                    'bridge',
                                                    'del', 
                                                    'dhcp', 
                                                    'import', 
                                                    'link', 
                                                    'net', 
                                                    'reload', 
                                                    'show', 
                                                    'vlan', 
                                                    'update',
                                                  ]
                                                )

        self._parser.add_argument('-addr', help='ip address')
        self._parser.add_argument('-dhcp', action='store_true', help='use dhcp')
        self._parser.add_argument('-dns', help='DNS address')
        self._parser.add_argument('-gw', help='gateway address')
        self._parser.add_argument('-iface', help='network interface')
        self._parser.add_argument('-n', '--name', help='archive|vlan name')
        self._parser.add_argument('-nc', '--no-check', action='store_true', 
                            help='turn off validation checks')

        apply_group = self._parser.add_argument_group("apply [options]")
        apply_group.add_argument('-now', action='store_true', 
                            help='apply non-active config and reload')

        archive_group = self._parser.add_argument_group("archive [options]")
        archive_group.add_argument('-r', '--restore', action='store_true', 
                            help='restore from archive')

        bridge_group = self._parser.add_argument_group("bridge [options]")
        bridge_group.add_argument('-vf', default='store_true', help='vlan filtering')
        bridge_group.add_argument('-stp', default='store_false', help='spanning tree protocol')

        dhcp_group = self._parser.add_argument_group("dhcp [options]")
        dhcp_group.add_argument('-bind', help='bind dhcp to iface')
        dhcp_group.add_argument('-df-lease', type=int, help='default lease time in sec')
        dhcp_group.add_argument('-emit-dns', action='store_true', help='assign dns to client')
        dhcp_group.add_argument('-max-lease', type=int, help='max lease time in sec')
        dhcp_group.add_argument('-psize', type=int, help='pool size')
        dhcp_group.add_argument('-offset', type=int, help='pool offset')
        dhcp_group.add_argument('-svr-ip', help='dhcp server address')

        del_group = self._parser.add_argument_group("del [options]")
        del_group.add_argument('-a', action='store_true', 
                            help='delete all active and non-active config')
        del_group.add_argument('-d', choices=['link', 'net', 'vlan'], 
                            help='config file type [link|net|vlan]')

        import_group = self._parser.add_argument_group("import [options]")
        import_group.add_argument('-f', '--file', help='file to import')

        link_group = self._parser.add_argument_group("link [options]")
        link_group.add_argument('-src', help='source iface name')
        link_group.add_argument('-dest', help='destination iface name')
        link_group.add_argument('-desc', help='description of link')

        net_group = self._parser.add_argument_group("net [options]")
        net_group.add_argument('-dhcpsrv', default='false', help='enable dhcp server')
        net_group.add_argument('-icw', default='30', help='sets congestion window size')
        net_group.add_argument('-iarw', default='30', help='sets receive window size')

        show_group = self._parser.add_argument_group("show [options]")
        show_group.add_argument('-s', choices=['link', 'net', 'vlan'], help='')

        update_group = self._parser.add_argument_group("update [options]")
        update_group.add_argument('-u', choices=['net', 'vlan'], help='')

        vlan_group = self._parser.add_argument_group("vlan [options]")
        vlan_group.add_argument('-att', '--attach', help='attach vlan to iface')
        vlan_group.add_argument('-id', type=int, default=1, help='vlan id')
        
        return self._parser.parse_args()


    def _set_command(self):
        self._args.func = self._args.cmd.capitalize() + 'Command'