import concurrent.futures
import socketserver
from http.server import BaseHTTPRequestHandler
from rauth import OAuth2Service
import json
import webbrowser


class OAuth:
    _redirect_host = 'localhost'
    _port = 5000
    _redirect_uri = f'http://{_redirect_host}:{_port}'

    def __init__(self, client_id, client_secret, base_url, access_token_url, authorize_url):
        """Create a secure session to interact with an API."""
        self._service = OAuth2Service(name="",
                                      client_id=client_id,
                                      client_secret=client_secret,
                                      base_url=base_url,
                                      access_token_url=access_token_url,
                                      authorize_url=authorize_url
                                      )

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_token = executor.submit(self._get_code)
            future_authenticate = executor.submit(self._authenticate)
            token = future_token.result()
            self.session = self._get_session(token)

    @staticmethod
    def utf8_decoder(payload):
        """json.loads does not work in .get_auth_session."""
        return json.loads(payload.decode('utf-8'))

    def _get_code(self):
        """Creates a server to get code from API"""
        class SingleRequestHandler(BaseHTTPRequestHandler):
            params = None

            def do_GET(self):  # !important to use 'do_POST' with Capital POST
                params = {x.split('=')[0]: x.split('=')[1] for x in self.path[2:].split('&')}
                self.send_response(200)
                self.end_headers()
                SingleRequestHandler.params = params

        httpd = socketserver.TCPServer((self._redirect_host, self._port), SingleRequestHandler)
        httpd.handle_request()
        httpd.server_close()
        return SingleRequestHandler.params['code']

    def _authenticate(self):
        """Opens a web browser tab to authenticate"""
        authorize_url = self._service.get_authorize_url(redirect_uri=OAuth._redirect_uri, scope='me',
                                                        response_type='code')
        webbrowser.open_new_tab(authorize_url)

    def _get_session(self, code):
        """Takes input from _get_token, and gets a valid token from the API"""
        data = {
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': OAuth._redirect_uri
        }
        return self._service.get_auth_session(data=data, decoder=self.utf8_decoder)


if __name__ == '__main__':
    with open("keys.json") as f:
        KEYS = json.load(f)
    genius = OAuth(client_id=KEYS["GENIUS_API_ID"],
                   client_secret=KEYS["GENIUS_API_SECRET"],
                   access_token_url='https://api.genius.com/oauth/token',
                   authorize_url='https://api.genius.com/oauth/authorize',
                   base_url='https://api.genius.com/')

    params = {'q': 'Kendrick Lamar'}
    r = genius.session.get('search', params=params)
    print(r.json())
