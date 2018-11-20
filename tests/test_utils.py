import utils

class test_utils:
    def test_protocol_from_url(self):
        protocol = utils.protocol_from_url("http://asdf")
        assert protocol == "http"
        protocol = utils.protocol_from_url("://asdf")
        assert protocol is None
        protocol = utils.protocol_from_url("blah")
        assert protocol is None
