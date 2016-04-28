# stdlib imports
import json
import pprint
# library imports
from brightlocal import BrightLocalAPI, BrightLocalBatch


def testFetchUrls():
	import json
	
	with open('credentials.json', 'rb') as fcredentials:
		credentials = json.load(fcredentials)
		
		api_key = credentials['key'].encode('utf-8')
		api_secret = credentials['secret'].encode('utf-8')
		
		pass
	
	directories = ('google', 'citysearch', 'dexknows', 'kudzu', 'manta')
	
	# setup api wrappers
	api = BrightLocalAPI(key=api_key, secret=api_secret)
	batchapi = BrightLocalBatch(api=api)
	
	# Step 1: create a new batch
	batch_id = batchapi.create()
	
	assert( batch_id )
	
	print( 'Created batch ID {}'.format(batch_id) )
	
	# Step 2: add directory jobs to batch
	for directory in directories:
		result = api.call(
			method='/v4/ld/fetch-profile-url',
			params={
				'batch-id':  batch_id,
				'local-directory': directory,
				'business-names': 'Eleven Madison Park',
				'country': 'USA',
				'city': 'New York',
				'postcode': '10010'
			}
		)
		
		if ( result['success'] ):
			print( 'Added job with ID {}'.format(result['job-id']) );
			pass
		
		pass
	
	# Step 3: Commit batch (to signal all jobs added, processing starts)
	success_or_failure = batchapi.commit(batch_id)
	
	if success_or_failure:
		print( 'Committed batch successfully.' )
		pass
	
	return

def testBatchResults():
	batch_id = 9834613
	
	with open('credentials.json', 'rb') as fcredentials:
		credentials = json.load(fcredentials)
		
		api_key = credentials['key'].encode('utf-8')
		api_secret = credentials['secret'].encode('utf-8')
		
		pass
	
	directories = ('google', 'citysearch', 'dexknows', 'kudzu', 'manta')
	
	# setup api wrappers
	api = BrightLocalAPI(key=api_key, secret=api_secret)
	batchapi = BrightLocalBatch(api=api)
	
	# get results
	batchresponse = batchapi.get_results(batch_id)
	batchresults  = batchresponse['results']
	
	pp = pprint.PrettyPrinter(depth=4)
	
	for jobset_key, jobset in batchresults.items():
		print jobset_key
		print
		
		for job in jobset:
			print 'Job', job['job-id']
			print
			
			pp.pprint( job['payload'] )
			pp.pprint( job['results'] )
			pass
		pass
	
	return


if __name__ == '__main__':
	testBatchResults()
	pass
