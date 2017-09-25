from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, FamousCities, FamousPlaces, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu"

engine = create_engine('sqlite:///famousplaces.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/login')
def login():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits)for x in xrange(32))
	login_session['state'] = state
	return render_template('login.html',STATE=state)

@app.route('/gconnect',methods=['POST'])
def gconnect():
        if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter'),401)
		response.headers['Content-Type'] = 'application/json'
		return response
	code = request.data

	try:
		# Upgrade the authorization code into a credentials object
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Check that the access token is valid.
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])
	# If there was an error in the access token info, abort.
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'
		return response

        # Verify that the access token is used for the intended user.
        gplus_id = credentials.id_token['sub']

        if result['user_id'] != gplus_id:
                response = make_response(
                        json.dumps("Token's user ID doesn't match given user ID."), 401)
                response.headers['Content-Type'] = 'application/json'
                return response
        stored_access_token = login_session.get('access_token')
        stored_gplus_id = login_session.get('gplus_id')
        if stored_access_token is not None and gplus_id == stored_gplus_id:
                response = make_response(json.dumps('Current user is already connected.'),
                                         200)
                response.headers['Content-Type'] = 'application/json'
                return response

        # Store the access token in the session for later use.
        login_session['access_token'] = credentials.access_token
        login_session['gplus_id'] = gplus_id

        # Get user info
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': credentials.access_token, 'alt': 'json'}
        answer = requests.get(userinfo_url, params=params)

        data = answer.json()

        login_session['username'] = data['name']
        login_session['picture'] = data['picture']
        login_session['email'] = data['email']

        user_id = getUserId(login_session['email'])
        if not user_id:
                user_id = createUser(login_session)
        login_session['user_id'] = user_id
        

        output = ''
        output += '<h1>Welcome, '
        output += login_session['username']
        output += '!</h1>'
        output += '<img src="'
        output += login_session['picture']
        output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
        flash("you are now logged in as %s" % login_session['username'])
        print "done!"
        return output

@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
        access_token = login_session.get('access_token')
        if access_token is None:
                response = make_response(
                        json.dumps('Current user not connected.'), 401)
                response.headers['Content-Type'] = 'application/json'
                return response
        url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
        h = httplib2.Http()
        result = h.request(url, 'GET')[0]
        if result['status'] == '200':
                del login_session['access_token']
                del login_session['gplus_id']
                del login_session['username']
                del login_session['email']
                del login_session['picture']
                response = make_response(json.dumps('Successfully disconnected.'), 200)
                response.headers['Content-Type'] = 'application/json'
                return redirect('/famouscities')
        else:
                response = make_response(json.dumps('Failed to revoke token for given user.', 400))
                response.headers['Content-Type'] = 'application/json'
                return response

@app.route('/')
@app.route('/famouscities')
def allFamousCities():
	cities = session.query(FamousCities).all()
	return render_template('showallcities.html',cities=cities)

@app.route('/catalog/<string:city_name>/places')
def showFamousPlaces(city_name):
	cities = session.query(FamousCities).all()
	city = session.query(FamousCities).filter_by(name=city_name).one()
	city_id = city.id
	places = session.query(FamousPlaces).filter_by(famous_city_id=city_id).all()
	return render_template('showallplaces.html',places=places,cities=cities,this_city=city_name)

@app.route('/catalog/<string:city_name>/<string:place_name>')
def showPlaceDescription(city_name,place_name):
	this_place = session.query(FamousPlaces).filter_by(name=place_name).one()
	creator = getUserInfo(this_place.user_id)
	if 'username' not in login_session or creator.id != login_session['user_id']:
                return render_template('showdescpublic.html',this_place=this_place, this_city=city_name)
        else:
                return render_template('showdesc.html',this_place=this_place,this_city=city_name)

@app.route('/catalog/<string:city_name>/place/new',methods=['GET','POST'])
def addNewPlace(city_name):
        if 'username' not in login_session:
                return redirect('/login')
        city = session.query(FamousCities).filter_by(name=city_name).one()
	if request.method=='POST':
		new_place = FamousPlaces(name=request.form['newPlace'],
                                         description=request.form['description'],
                                         address=request.form['address'],
                                         famous_city=city_name,
                                         user_id=login_session['user_id'])
		session.add(new_place)
		session.commit()
		return redirect(url_for('showFamousPlaces',city_name=city_name))
	else:
		return render_template('newplace.html',this_city=city_name)

@app.route('/catalog/<string:city_name>/<string:place_name>/edit',methods=['GET','POST'])
def editPlace(city_name,place_name):
        place_to_edit = session.query(FamousPlaces).filter_by(name=place_name).one()
        creator = getUserInfo(place_to_edit.user_id)
        if 'username' not in login_session or creator.id != login_session['user_id']:
                return render_template('showdescpublic.html',this_place=place_to_edit,this_city=city_name)
        
	if request.method=='POST':
		if request.form['name']:
			place_to_edit.name = request.form['name']
		if request.form['description']:
			place_to_edit.description = request.form['description']
		if request.form['address']:
			place_to_edit.address = request.form['address']
		session.add(place_to_edit)
		session.commit()
		return redirect(url_for('showPlaceDescription',city_name=city_name,place_name=place_name))
	else:
		return render_template('editplace.html',this_place=place_to_edit,this_city=city_name)

@app.route('/catalog/<string:city_name>/<string:place_name>/delete', methods=['GET','POST'])
def deletePlace(city_name,place_name):
        place_to_delete = session.query(FamousPlaces).filter_by(name=place_name).one()
        creator = getUserInfo(place_to_delete.user_id)
        if 'username' not in login_session or creator.id != login_session['user_id']:
                return render_template('showdescpublic.html',this_place=place_to_delete,this_city=city_name)

	if request.method == 'POST':
		session.delete(place_to_delete)
		session.commit()
		return redirect(url_for('showFamousPlaces',city_name=city_name))
	else:
		return render_template('deleteplace.html',this_place=place_to_delete,this_city=city_name)

def getUserId(email):
        try:
                user = session.query(User).filter_by(email=email).one()
                return user.id
        except:
                return None

def getUserInfo(user_id):
        user = session.query(User).filter_by(id=user_id).one()
        return user

def createUser(login_session):
        newUser = User(name=login_session['username'], email=login_session['email'],
                       picture=login_session['picture'])
        session.add(newUser)
        session.commit()
        user = session.query(User).filter_by(email=login_session['email']).one()
        return user.id

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)

    
