from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, FamousCities, FamousPlaces

app = Flask(__name__)

engine = create_engine('sqlite:///famousplaces.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
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
	return render_template('showdesc.html',this_place=this_place,this_city=city_name)

@app.route('/catalog/city/new',methods=['GET','POST'])
def addNewCity():
	if request.method=='POST':
		new_city = FamousCities(name=request.form['newCity'])
		session.add(new_city)
		session.commit()
		return redirect(url_for('allFamousCities'))
	else:
		return render_template('newcity.html')

@app.route('/catalog/<string:city_name>/place/new',methods=['GET','POST'])
def addNewPlace(city_name):
	if request.method=='POST':
		new_place = FamousPlaces(name=request.form['newPlace'],description=request.form['description'],address=request.form['address'],famous_city=city_name)
		session.add(new_place)
		session.commit()
		return redirect(url_for('showFamousPlaces',city_name=city_name))
	else:
		return render_template('newplace.html',this_city=city_name)

@app.route('/catalog/<string:city_name>/<string:place_name>/edit',methods=['GET','POST'])
def editPlace(city_name,place_name):
	place_to_edit = session.query(FamousPlaces).filter_by(name=place_name).one()
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
		return render_template('editplace.html',this_place=place_to_edit)

@app.route('/catalog/<string:city_name>/<string:place_name>/delete', methods=['GET','POST'])
def deletePlace(city_name,place_name):
	place_to_delete = session.query(FamousPlaces).filter_by(name=place_name).one()
	if request.method == 'POST':
		session.delete(place_to_delete)
		session.commit()
		return redirect(url_for('showFamousPlaces',city_name=city_name))
	else:
		return render_template('deleteplace.html',this_place=place_to_delete,this_city=city_name)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)