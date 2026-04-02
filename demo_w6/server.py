from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = "random_secret"

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id='client_id',
    client_secret='client_secret',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.route('/login')
def login():
    return google.authorize_redirect(
        redirect_uri=url_for('callback', _external=True)
    )

@app.route('/callback')
def callback():
    token = google.authorize_access_token()
    
    user_info = token.get('userinfo')

    return {
        "user": user_info
    }

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)