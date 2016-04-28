# local imports
from .api import BrightLocalAPI


class BrightLocalBatchV4(object):

	api = None

	def __init__(self, api):
		self.api = api
		return

	def create(self, stop_on_error=False):
		result = self.api.call(
			method='/v4/batch',
			params={
				'stop-on-job-error': (1 if stop_on_error else 0),
			}
		)

		return result['batch-id'] if result.get('success', False) else False

	def commit(self, batch_id):
		result = self.api.call(
			method='/v4/batch',
			params={
				'batch-id': batch_id
			},
			http_method=BrightLocalAPI.HTTP_METHOD_PUT
		)

		return result['success']

	def delete(self, batch_id):
		results = self.api.call(
			method='/v4/batch',
			params={
				'batch-id': batch_id
			},
			http_method=BrightLocalAPI.HTTP_METHOD_DELETE
		)

		return results['success']

	def get_results(self, batch_id):
		return self.api.call(
			method='/v4/batch',
			params={
				'batch-id': batch_id
			},
			http_method=BrightLocalAPI.HTTP_METHOD_GET
		)

	pass

BrightLocalBatch = BrightLocalBatchV4