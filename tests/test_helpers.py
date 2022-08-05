import unittest
from utils.config import config
from utils.helpers import (
    get_mac_addr, 
    write_config, 
    gen_filename
)

class TestHelpers(unittest.TestCase):

    def test_gen_filename(self):
        digit = 10
        word = "ad0"
        ext = config['LINK_EXT']
        dir = config['NET_CFG_PATH']
        p = dir + digit + word + ext
        self.assertEqual(p, '/etc/systemd/network/10-ad0.link')

    def test_get_mac_addr():
        pass

    def test_write_config():
        pass

if __name__ == '__main__':
    unittest.main()
