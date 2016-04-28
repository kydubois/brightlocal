BrightLocal API
===============

A simpler Python wrapper to inteface with the BrightLocal REST API. The wrapper abstracts authentication and calls to the standard endpoint.




API Reference
--------

API documentation for BrightLocal: http://apidocs.brightlocal.com/




Examples
--------

```python
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
```




Tests
-----

Test methods expect a JSON file named `credentials.json` with your unique `key` and `secret` for using the API.


