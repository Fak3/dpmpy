import unittest
import os

import pytest
import requests
import responses
from mock import patch

from dpm.client import Client, DpmException, ConfigError, NetworkError, JSONDecodeError, HTTPStatusError
from .base import BaseTestCase

dp1_path = 'tests/fixtures/dp1'


class BaseClientTestCase(BaseTestCase):
    # Valid config for tests.
    config = {
        'username': 'user',
        'password': 'password',
        'server': 'http://127.0.0.1:5000'
    }


class ClientInitTest(BaseClientTestCase):
    """
    `Client.__init__()` should raise exceptions if config is malformed or
    datapackage is missing.
    """
    def test___init__fails_no_data_package(self):
        with pytest.raises(DpmException):
            client = Client(self.config)
        try:
            client = Client(self.config)
        except DpmException as e:
            assert e.message.startswith('No Data Package found at %s' %
                    os.getcwd())
    
    def test___init__datapackage_ok(self):
        client = Client(self.config, dp1_path)
        assert client.datapackage
        assert client.datapackage.base_path.endswith(dp1_path)

    def test__init__config_password_missing(self):
        """
        When the 'password' is missing in the config, the client should raise ConfigError.
        """
        config = {'username': 'user', 'server': 'server'}
        with pytest.raises(ConfigError):
            client = Client(config, dp1_path)

        try:
            client = Client(config, dp1_path)
        except ConfigError as e:
            assert "'password' is required" in str(e)

    def test__init__config_username_missing(self):
        """
        When the 'username' is missing in the config, the client should raise ConfigError.
        """
        config = {'password': 'pwd', 'server': 'server'}
        with pytest.raises(ConfigError):
            client = Client(config, dp1_path)

        try:
            client = Client(config, dp1_path)
        except ConfigError as e:
            assert "'username' is required" in str(e)

    def test__init__config_server_missing(self):
        """
        When the 'server' is missing in the config, the client should raise ConfigError.
        """
        config = {'username': 'user', 'password': 'pwd'}

        with pytest.raises(ConfigError):
            client = Client(config, dp1_path)

        try:
            client = Client(config, dp1_path)
        except ConfigError as e:
            assert "'server' is required" in str(e)


class ClientApirequestTest(BaseClientTestCase):
    def setUp(self):
        # GIVEN client instance with valid auth token
        self.client = Client(self.config, dp1_path)
        self.client.token = '123'

    def test_connerror_oserror(self):
        # GIVEN socket that throws OSError
        with patch("socket.socket.connect", side_effect=OSError) as mocksock:
            # WHEN client._apirequest is invoked
            try:
                result = self.client._apirequest(method='POST', url=self.client.server)
            except Exception as e:
                result = e

            # THEN ConnectionError should be raised
            assert isinstance(result, requests.ConnectionError)

    def test_json_decode_error(self):
        # GIVEN the server that responds with some invalid JSON
        responses.add(
            responses.POST, 'http://127.0.0.1:5000',
            body="some invalid json",
            status=200)

        # WHEN client._apirequest is invoked
        try:
            result = self.client._apirequest(method='POST', url=self.client.server)
        except Exception as e:
            result = e

        # THEN JSONDecodeError should be raised
        assert isinstance(result, JSONDecodeError)

    def test_http_status_error(self):
        # GIVEN the server that responds with unsuccessful status_code (400)
        responses.add(
            responses.POST, 'http://127.0.0.1:5000',
            json={'message': 'some error'},
            status=400)

        # WHEN client._apirequest is invoked
        try:
            result = self.client._apirequest(method='POST', url=self.client.server)
        except Exception as e:
            result = e

        # THEN HTTPStatusError should be raised
        assert isinstance(result, HTTPStatusError)

    def test_success(self):
        # GIVEN the server that responds with successful and valid response
        responses.add(
            responses.POST, 'http://127.0.0.1:5000',
            json={'message': 'ok'},
            status=200)

        # WHEN client._apirequest is invoked
        result = self.client._apirequest(method='POST', url=self.client.server)

        # THEN result should be Response instance
        assert isinstance(result, requests.Response)

    # TODO: test validate

