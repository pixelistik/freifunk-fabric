import unittest
import logging
import fabfile

class TestFabfile(unittest.TestCase):
    def setUp(self):
        pass

    def test_model_to_firmware_url(self):
        result = fabfile._model_to_firmware_url("TP-Link TL-WR741N/ND v4")
        expected = "http://images.freifunk-rheinland.net/images/fsm/current/duesseldorf-ar71xx-attitude_adjustment/openwrt-ar71xx-generic-tl-wr741nd-v4-squashfs-sysupgrade.bin"
        self.assertEqual(result, expected)

        result = fabfile._model_to_firmware_url("TP-Link TL-WR741N/ND v2")
        expected = "http://images.freifunk-rheinland.net/images/fsm/current/duesseldorf-ar71xx-attitude_adjustment/openwrt-ar71xx-generic-tl-wr741nd-v2-squashfs-sysupgrade.bin"
        self.assertEqual(result, expected)

        result = fabfile._model_to_firmware_url("TP-Link TL-WR841N/ND v7")
        expected = "http://images.freifunk-rheinland.net/images/fsm/current/duesseldorf-ar71xx-attitude_adjustment/openwrt-ar71xx-generic-tl-wr841nd-v7-squashfs-sysupgrade.bin"
        self.assertEqual(result, expected)


if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	unittest.main()