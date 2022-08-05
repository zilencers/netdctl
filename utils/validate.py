from ipaddress import AddressValueError, IPv4Interface
import psutil
import sys


class Validate():
    _args = None
    _ip_addrs = ['addr', 'gw', 'dns']
    _iface = ['iface', 's']
   
    @classmethod
    def validate(cls, args):
        cls._args = {k:v for (k,v) in vars(args).items() if v is not None}

        match cls._args['mode']:
            case 'link':
                cls._validate_iface()
                cls._validate_link()
            case 'net':
                cls._validate_ip()
                cls._validate_iface()
                cls._validate_net()
            case 'vlan':
                cls._validate_ip()
                cls._validate_iface()
                cls._validate_vlan()


    @classmethod
    def _validate_ip(cls):
        ips = {k:v for (k,v) in cls._args.items() if k in cls._ip_addrs}
        
        try:
            {IPv4Interface(v) for (k,v) in ips.items()}
        except AddressValueError as err:
            print(err, file=sys.stderr)
            sys.exit(1)


    @classmethod
    def _validate_iface(cls):
        iface = {k:v for (k,v) in cls._args.items() if k in cls._iface}

        interfaces = psutil.net_if_addrs()

        try:
            {k:v for (k,v) in iface.items() if interfaces[v]}  
        except Exception as e:
            print("interface not found: {}".format(iface), file=sys.stderr)
            sys.exit(1)


    @classmethod
    def _validate_link(cls):
        try:
            cls._args['d']
            cls._args['s']
        except Exception as e:
            print("Missing argument: ", e, file=sys.stderr)
            sys.exit(1)


    @classmethod
    def _validate_net(cls):
        match cls._args['type']:
            case 'add':
                try:
                    if cls._args['dhcp']:
                        cls._args['iface']
                    elif cls._args['addr']:
                        cls._args['iface']
                except Exception as e:
                    print("Missing argument: ", e, file=sys.stderr)
                    sys.exit(1)
            case 'del':
                try:
                    cls._args['iface']
                except Exception as e:
                    print("Missing argument: ", e, file=sys.stderr)
            case 'update':
                try:
                    cls._args['iface']
                except Exception as e:
                    print("Missing argument: ", e, file=sys.stderr)


    @classmethod
    def _validate_vlan(cls):
        pass
