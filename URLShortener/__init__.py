from flask import Flask, request, redirect, jsonify
from redis import Redis
from URLShortener.shorten import UrlShortener

import re


app = Flask(__name__)
shrt = UrlShortener()

#redis = Redis(host='redis', port=6379)
def url_valid(url):
	"""Validates a url by parsing it with a regular expression.

	Parameters:
	url - string representing a url to be validated.

	Return values:
	Boolean, indicating the validity of the url.
	"""
	regex = re.compile(
			r'^(?:http)s?://'
			r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
			r'localhost|'
			r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
			r'(?::\d+)?'
			r'(?:/?|[/?]\S+)$', re.IGNORECASE)
		
	return re.match(regex, url) is not None

def bad_request(message):
	"""Takes a supplied message and attaches it to a HttpResponse with code 400.

	Parameters:
	message - string containing the error message.

	Return values:
	An object with a message string and a status_code set to 400.
	"""
	response = jsonify({'message': message})
	response.status_code = 400
	return response

@app.route('/')
def root(): 
	return 'Working!'

@app.route('/<URLCode>')
def getURLCode (URLCode): 
	"""Takes a supplied message and attaches it to a HttpResponse with code 400.

	Parameters:
	message - string containing the error message.

	Return values:
	An object with a message string and a status_code set to 400.
	"""
	url = shrt.lookup(URLCode)
	if not url:
		return redirect('/404')
	else:
		return redirect(url)

@app.route('/shortenUrl', methods=['POST','GET'])
def getShortenURL(): 
	"""POST endpoint that looks for a supplied string called "url",
	contained inside a json object. Then validates this url and
	either returns an error response as appropriate, or generates a
	shortened url, stores the shortened url, and then returns it - if valid.

	Parameters:
	The string representing a shortened url.

	Return values:
	A response signifying success or error.
	Successes contain the shortened url, errors contain an appropriate message.
	"""
	if request.method == 'POST':
		if not request.json:
			return bad_request('Url must be provided in json format.')
		
		if 'url' not in request.json:
			return bad_request('Url parameter not found.')
		
		url = request.json['url']		

		if not url_valid(url):
			return bad_request('Provided url is not valid.')

		response = shrt.shorten(url)
		return response
				
	else:
		return bad_request('Must use POST.')
		
	
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)