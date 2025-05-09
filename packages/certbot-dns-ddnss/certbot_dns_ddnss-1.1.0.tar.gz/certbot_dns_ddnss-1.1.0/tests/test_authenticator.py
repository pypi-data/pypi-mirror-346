# -*- coding: utf-8 -*-
"""
Test Suite for Authenticator Tests
"""


import pytest

from unittest import mock, TestCase

from certbot.plugins import dns_test_common
from certbot.tests import util as test_utils
from certbot.errors import PluginError


class AuthenticatorTest(TestCase, dns_test_common.BaseAuthenticatorTest):

    def setUp(self):
        from certbot_dns_ddnss import Authenticator

        super().setUp()

        # do not add any waiting time for propagation during testing
        self.config = mock.MagicMock(dns_ddnss_propagation_seconds=0)
        # name is prepended to all parameters set, i.e.
        # api_token parameter becomes dns_ddnss_api_token
        self.auth = Authenticator(self.config, 'dns-ddnss')

    @pytest.mark.usefixtures('response_with_ok_header')
    @test_utils.patch_display_util()
    def test_perform(self, unused_mock_get_utility):
        """Test set TXT record"""
        result = self.auth.perform([self.achall])

    @pytest.mark.usefixtures('response_with_ok_header')
    @test_utils.patch_display_util()
    def test_cleanup(self, unused_mock_get_utility):
        """Test delete TXT record"""
        # in order to run the cleanup 'standalone' we need to manually run
        # _setup_credentials() to populate the internal _api_token attribute
        self.auth._setup_credentials()
        self.auth._attempt_cleanup = True
        self.auth.cleanup([self.achall])

    @test_utils.patch_display_util()
    def test_no_api_key_fails(self, unused_mock_get_utility):
        """Test that we fail if API key is not provided"""
        # as we did not run _setup_credentials() to populate the credentials,
        # getting the client should fail as expected
        with pytest.raises(PluginError):
            client = self.auth._get_ddnss_client()


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main(sys.argv[1:] + [__file__]))
