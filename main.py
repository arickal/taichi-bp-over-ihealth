"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask
from flask import abort, redirect, url_for
from flask import request
import urllib2
import json

login_url = 'https://api.ihealthlabs.com:8443/OpenApiV2/OAuthv2/userauthorization/?client_id=59b4c14167bc4f9ca41035fd04683c1b&response_type=code&redirect_uri=http://taichibp.appspot.com/bpview&APIName=OpenApiBP'
token_url = 'https://api.ihealthlabs.com:8443/OpenApiV2/OAuthv2/userauthorization/?client_id=59b4c14167bc4f9ca41035fd04683c1b&client_secret=9aa2279c68d2403cb9224c5ea83c13cc&grant_type=authorization_code&redirect_uri=http://taichibp.appspot.com/bpview&code='

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/bpview', methods=['GET'])
def bpview():
	if request.args.get('code',''):
		obj = json.loads(urllib2.urlopen( token_url+request.args.get('code','') ).read())
		token = obj['AccessToken']
		userID = obj['UserID']
		target_url = 'https://api.ihealthlabs.com:8443/openapiv2/user/'+ userID +'/bp.json/?client_id=59b4c14167bc4f9ca41035fd04683c1b&client_secret=9aa2279c68d2403cb9224c5ea83c13cc&redirect_uri=http://taichibp.appspot.com/bpview&access_token='+token+'&sc=4CE3AD5EB7B74C6FBB3354C6BC7264EE&sv=97D4A91F0DC849019E287C5CCCCA23B8'
		bp_records = json.loads( urllib2.urlopen( target_url ).read() )
		return str(bp_records['BPDataList'][0])
	else:
		return redirect(login_url)

@app.route('/bpview/dashboard', methods=['GET','POST'])
def dashboard():
    return 'ok :'+request.method

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
