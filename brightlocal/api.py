# stdlib imports
import base64
import calendar
import hashlib
import hmac
import os
import sys
import time
import urllib
# third-party imports
import requests


VERSION = '1.0'


class BrightLocalAPIError(Exception):
	pass

class BrightLocalAPI(object):

	HTTP_METHOD_POST = 'post';
	HTTP_METHOD_GET = 'get';
	HTTP_METHOD_PUT = 'put';
	HTTP_METHOD_DELETE = 'delete';

	ALLOWED_HTTP_METHODS = frozenset((
		HTTP_METHOD_POST,
		HTTP_METHOD_GET,
		HTTP_METHOD_PUT,
		HTTP_METHOD_DELETE,
	))

	ENDPOINT = 'https://tools.brightlocal.com/seo-tools/api'
	MAX_EXPIRY = 1800;

	key = None
	secret = None

	def __init__(self, key, secret):
		self.key = key
		self.secret = secret

		self._last_http_code = None
		self._session = None
		return

	def _get_session(self):
		if self._session is None:
			self._session = requests.Session()
			self._session.headers.update({'user-agent': 'PyBrightLocal/{0}'.format(VERSION)})
			pass

		return self._session

	def call(self, method, params=None, http_method=HTTP_METHOD_POST):
		if not http_method in BrightLocalAPI.ALLOWED_HTTP_METHODS:
			raise BrightLocalAPIError( 'Invalid HTTP method specified' )

		method = method.replace('/seo-tools/api', '')
		params = dict() if params is None else dict(params)

		sig, expires = self.get_sig_and_expires()

		params.update({
			'api-key': self.key,
			'sig': sig,
			'expires': expires,
		})

		session = self._get_session()
		url = BrightLocalAPI.ENDPOINT.rstrip('/') + '/' + method.lstrip('/')

		if http_method == BrightLocalAPI.HTTP_METHOD_GET:
			r = session.get(url, params=params)
			pass
		else:
			verb  = getattr(session, http_method)
			r = verb(url, data=params)
			pass
		self._last_http_code = r.status_code

		return r.json()

	def get_last_http_code(self):
		return self._last_http_code

	def get_sig_and_expires(self, expiry=None):
		expires = calendar.timegm( time.gmtime() ) + ( BrightLocalAPI.MAX_EXPIRY if expiry is None else expiry )

		data = self.key + str(expires)

		digest = hmac.new(self.secret, data, digestmod=hashlib.sha1).digest()
		sig = base64.standard_b64encode(digest)

		return sig, expires

	def get(self, method, params=None):
		return self.call(method, params, BrightLocalAPI.HTTP_METHOD_GET)

	def post(self, method, params=None):
		return self.call(method, params, BrightLocalAPI.HTTP_METHOD_POST)

	def put(self, method, params=None):
		return self.call(method, params, BrightLocalAPI.HTTP_METHOD_PUT)

	def delete(self, method, params=None):
		return self.call(method, params, BrightLocalAPI.HTTP_METHOD_DELETE)

	pass
