# -*- coding: utf-8 -*-
"""
Test Suite for _DDNSSClient Tests
"""


import pytest


def test_get_ddnss_api_base_url(ddnssclient):
    """Test for correct API base domain"""
    expected_api_base_url = "https://www.ddnss.de/upd.php"
    returned_api_base_url = ddnssclient.get_ddnss_api_base_url()
    assert returned_api_base_url == expected_api_base_url


def test_get_api_request_add_params(ddnssclient):
    """Test returned parameter set for add TXT requests"""
    api_token = "a1b2c3d4"
    domain = "example.com"
    txt_record = "dns_txt_record"
    params = ddnssclient.get_api_request_add_params(api_token, domain,
                                                    txt_record)
    # check that dict is returned
    assert isinstance(params, dict)
    # pop all expected keys from the dictionary
    returned_api_token = params.pop("key")
    assert returned_api_token == api_token
    returned_domain = params.pop("host")
    assert returned_domain == domain
    returned_api_type = params.pop("txtm")
    assert returned_api_type == 1
    returned_txt_record = params.pop("txt")
    assert returned_txt_record == txt_record
    # finally check that dict is empty
    assert len(params) == 0


def test_get_api_request_del_params(ddnssclient):
    """Test returned parameter set for add TXT requests"""
    api_token = "a1b2c3d4"
    domain = "example.com"
    params = ddnssclient.get_api_request_del_params(api_token, domain)
    # check that dict is returned
    assert isinstance(params, dict)
    # pop all expected keys from the dictionary
    returned_api_token = params.pop("key")
    assert returned_api_token == api_token
    returned_domain = params.pop("host")
    assert returned_domain == domain
    returned_api_type = params.pop("txtm")
    assert returned_api_type == 2
    # finally check that dict is empty
    assert len(params) == 0


def test_get_api_request_for_params_add(ddnssclient):
    """Test the generated API url for adding TXT records"""
    base_url = "https://www.ddnss.de/upd.php"
    api_token = "a1b2c3d4"
    domain = "example.com"
    txt_record = "dns_txt_record"
    expected_api_url = (f"{base_url}?key={api_token}&host={domain}&txtm=1&"
                        f"txt={txt_record}")
    add_params = ddnssclient.get_api_request_add_params(api_token, domain,
                                                        txt_record)
    generated_api_url = ddnssclient.get_api_request_for_params(add_params)
    assert generated_api_url == expected_api_url


def test_get_api_request_for_params_del(ddnssclient):
    """Test the generated API url for deleting TXT records"""
    base_url = "https://www.ddnss.de/upd.php"
    api_token = "a1b2c3d4"
    domain = "example.com"
    expected_api_url = f"{base_url}?key={api_token}&host={domain}&txtm=2"
    del_params = ddnssclient.get_api_request_del_params(api_token, domain)
    generated_api_url = ddnssclient.get_api_request_for_params(del_params)
    assert generated_api_url == expected_api_url


@pytest.mark.parametrize('status', [200, 401])
@pytest.mark.parametrize('header_ok', [True, False])
def test_verify_response(status, header_ok):
    """Test that responses are verified correctly"""
    from certbot.errors import PluginError
    from urllib.request import urlopen

    from certbot_dns_ddnss.dns_ddnss import _DDNSSClient

    # generate some random response and update with the parameters for the
    # current run
    response = urlopen('http://www.example.com')
    response.status = status
    if header_ok:
        response.headers.add_header('DDNSS-Message',
                                    'Your hostname has been updated')
    # try to verify the result in and set success to False in case
    # the function raises a PluginError exception
    client = _DDNSSClient(None)
    try:
        client.verify_response(response)
        verification_success = True
    except PluginError:
        verification_success = False
    # we only expect this to not raise and error if both status is 200
    # **and** headers are OK, thusj
    expected_verification_success = ((status == 200) & header_ok)
    assert expected_verification_success == verification_success
