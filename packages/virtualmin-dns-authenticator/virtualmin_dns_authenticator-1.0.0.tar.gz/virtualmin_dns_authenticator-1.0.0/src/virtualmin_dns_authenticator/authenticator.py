import logging
from certbot.plugins import dns_common
from requests.auth import HTTPBasicAuth
import requests

logger = logging.getLogger(__name__)

class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Virtualmin."""

    description = (
        "Obtain certificates using a DNS TXT record by using the Virtualmin API."
    )

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):
        super(Authenticator, cls).add_parser_arguments(
            add, default_propagation_seconds=30)
        add("credentials", help="Virtualmin credentials ini file.")

    def more_info(self):
        return """
            This plugin configures a DNS TXT record to respond to a DNS-01 challenge using
            the Virtualmin HTTP API.
            """

    def _setup_credentials(self):
        dns_common.validate_file_permissions(self.conf('credentials'))
        self.credentials = self._configure_credentials(
            'credentials',
            'Virtualmin credentials ini file',
            {
                'username': 'Virtualmin API username',
                'password': 'Virtualmin API password',
                'api_url': 'URL to the Virtualmin server, including the port (e.g., https://host:port)'
            }
        )

    def _perform(self, domain, validation_name, validation):
        self._get_virtualmin_client().add_txt_record(domain, validation_name, validation)

    def _cleanup(self, domain, validation_name, validation):
        self._get_virtualmin_client().del_txt_record(domain, validation_name, validation)

    def _get_virtualmin_client(self):
        return _VirtualminClient(
            self.credentials.conf('username'),
            self.credentials.conf('password'),
            self.credentials.conf('api_url')
        )


class _VirtualminClient:
    """
    Encapsulates all communication with Virtualmin HTTP API.
    """

    def __init__(self, username, password, api_url):
        self.auth = HTTPBasicAuth(username, password)
        self.api_url = api_url.rstrip('/') + '/virtual-server/remote.cgi'

    def add_txt_record(self, domain, validation_name, validation):
        """Add a TXT record using the Virtualmin API."""
        params = {
            'program': 'modify-dns',
            'domain': domain,
            'add-record': f"{validation_name}. TXT {validation}"
        }
        logger.debug("Adding TXT record: %s", params)
        response = self._make_request(params)
        self._check_response(response, "add TXT record")

    def del_txt_record(self, domain, validation_name, validation):
        """Delete a TXT record using the Virtualmin API."""
        params = {
            'program': 'modify-dns',
            'domain': domain,
            'remove-record': f"{validation_name}. TXT {validation}"
        }
        logger.debug("Deleting TXT record: %s", params)
        response = self._make_request(params)
        self._check_response(response, "delete TXT record")

    def _make_request(self, params):
        """Make an HTTP GET request to the Virtualmin API."""
        try:
            response = requests.get(self.api_url, params=params, auth=self.auth, verify=False)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error("Error during Virtualmin API request: %s", e)
            raise

    def _check_response(self, response, action):
        """Check if the Virtualmin API response indicates success."""
        if "success" not in response.text.lower():
            logger.error("Failed to %s. Response: %s", action, response.text)
            raise RuntimeError(f"Failed to {action}: {response.text}")
        logger.debug("Successfully %s. Response: %s", action, response.text)
