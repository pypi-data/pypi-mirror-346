# -*- coding: utf-8 -*-
"""
DNS Authenticator for DDNSS.de
"""

# checkout internal DNS plugins https://github.com/certbot/certbot and also
# the non-internal plugins like duckdns etc.

import logging

from typing import Callable
from typing import Dict

from urllib import parse
from urllib import request
from urllib import response

from certbot.errors import PluginError
from certbot.plugins import dns_common


logger = logging.getLogger(__name__)


class Authenticator(dns_common.DNSAuthenticator):
    """
    DNS Authenticator for ddnss.de DNS Provider

    This Authenticator uses the ddnss.de DNS API to add and delete TXT
    records with a DNS entry in order to perform a DNS-01 challenge.
    """

    description = ("Obtain certificates for domains hosted with 'ddnss.de' "
                   "using DNS-01 challenges")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._api_token = None

    @classmethod
    def add_parser_arguments(cls, add: Callable[..., None],
                             default_propagation_seconds: int = 60) -> None:
        """Populate Authenticator with additional parser arguments"""
        super().add_parser_arguments(add, default_propagation_seconds)
        add("credentials", help="ddnss.de credentials INI file")
        add("token", help="Token for accessing ddnss.de API")

    def more_info(self) -> str:
        """Provide more detailed information about this Plugin."""
        info_str = ("This Plugin (dns_ddnss) provides the methods for adding "
                    "TXT records to domain entries registered with ddnss.de "
                    "enabling DNS-01 challenges with ddnss.de")
        return info_str

    def _setup_credentials(self) -> None:
        """
        Verify and Setup the provided API Token.

        Note that we do not actually verify anything here but simply check
        that an API token was actually passed.
        """
        # first check if an API token was provided ...
        if self.conf('token'):
            self._api_token = self.conf('token')
            return

        # ... if not we request a credentials file
        self._credentials = self._configure_credentials(
            'credentials',
            'ddnss.de credentials INI file',
            {'token': 'Token for accessing ddnss.de API'},
        )
        self._api_token = self._credentials.conf('token')

    def _perform(self, domain: str, validation_name: str,
                 validation: str) -> None:
        self._get_ddnss_client().add_txt_record(domain, validation)

    def _cleanup(self, domain: str, validation_name: str,
                 validation: str) -> None:
        self._get_ddnss_client().del_txt_record(domain)

    def _get_ddnss_client(self):
        if not self._api_token:
            msg = ("Plugin has not been prepared properly - No API token "
                   "found")
            raise PluginError(msg)
        return _DDNSSClient(self._api_token)


class _DDNSSClient(object):
    """Class for interfacing with the DDNSS.de API.

    Implements all methods for adding and deleting TXT entries based
    on the DDNSS.de API reachable via its API URL.

    :param str api_token: API token used for API requests with ddnss.de.
    """
    def __init__(self, api_token: str) -> None:
        self._api_token = api_token

    def add_txt_record(self, domain: str, txt_record: str) -> None:
        """Add the TXT record to the DNS entry.

        :param str domain: Domain for which the record shall be set.
        :param str txt_record: Content of the TXT record.
        """
        # get the API parameters required to add the TXT record
        api_add_params = self.get_api_request_add_params(self._api_token,
                                                         domain, txt_record)
        # build and perform API request with ddnss.de_
        api_add_request = self.get_api_request_for_params(api_add_params)
        response = request.urlopen(api_add_request)

        # verify and raise if response is not OK
        self.verify_response(response)

    def del_txt_record(self, domain) -> None:
        """Delete a TXT record from the DNS entry."""
        # get the API parameters required to delete a TXT record
        api_del_params = self.get_api_request_del_params(self._api_token,
                                                         domain)
        # build and perform API request with ddnss.de
        api_del_request = self.get_api_request_for_params(api_del_params)
        response = request.urlopen(api_del_request)

        # verify and raise if response is not OK
        self.verify_response(response)

    def verify_response(self, response: response.addinfourl) -> None:
        """Verify the recieved reponse and raise if needed

        :param response.addinfourl reponse: response recived from API url

        :raises: PluginError if recieved response does not meet the defined
            criteria
        """
        # check response status
        if response.status != 200:
            msg = (f"Failed to update TXT record - API request returned with "
                   f"status code: {response.status}")
            raise PluginError(msg)
        # check HTML header for expected message
        expected_message = "DDNSS-Message: Your hostname has been updated"
        if expected_message not in response.headers.as_string():
            msg = (f"Failed to update TXT record - API request returned with "
                   f"status code {response.status} but expected "
                   f"DDNSS-Message 'Your hostname has been updated' is not "
                   f"found in returned response Header")
            raise PluginError(msg)

    def get_api_request_for_params(self, api_params: Dict) -> str:
        """Build the complete request from passed parameters

        :param str api_params: Parameter used to build the API request.

        :returns: URL performing the requested API call
        :rtype: str

        """
        complete_api_request_url = (f"{self.get_ddnss_api_base_url()}?"
                                    f"{parse.urlencode(api_params)}")
        return complete_api_request_url

    def get_ddnss_api_base_url(self) -> str:
        """DDNSS.de API URL

        :returns: URL at which the ddnss.de API can be reached
        :rtype: str

        """
        return "https://www.ddnss.de/upd.php"

    def get_api_request_add_params(self, api_token: str, domain: str,
                                   txt_record: str) -> Dict:
        """API parameters for adding a TXT record.

        :param str api_token: API token to be used with the request.
        :param str domain: Domain for which the record shall be set.
        :param str txt_record: Content of the TXT record.

        :returns: parameters required to perform the API call.
        :rtype: dict

        """
        params = {
            "key": api_token,
            "host": domain,
            "txtm": 1,
            "txt": txt_record,
        }
        return params

    def get_api_request_del_params(self, api_token: str, domain: str) -> Dict:
        """API parameters for deleting a TXT record.

        :param str api_token: API token to be used with the request.
        :param str domain: Domain for which the record shall be deleted.

        :returns: parameters required to perform the API call.
        :rtype: dict

        """
        params = {
            "key": api_token,
            "host": domain,
            "txtm": 2,
        }
        return params
