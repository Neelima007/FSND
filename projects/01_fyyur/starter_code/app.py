#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import json
import datetime
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
from models import db,Venue,Artist,Show
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
#db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


#db.create_all()

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
def show_form_errors(fieldName, errorMessages):
    return flash(
        'Some errors on ' +
        fieldName.replace('_', ' ') +
        ': ' +
        ' '.join([str(message) for message in errorMessages]),
        'warning'
    )

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  final={}
  data=[]
  ind= -1
  city_existing=None
  state_existing=None
  venues = Venue.query.order_by(Venue.state, Venue.city).all()
  for venue in venues:
    num = Show.query.filter(Show.start_time>datetime.now(),Show.venue_id==venue.id).count()
    if venue.city==city_existing:
      #final['venues'].append({"id":venue.id,"name":venue.name,"num_upcoming_shows":num})
      data[ind]['venues'].append({"id":venue.id,"name":venue.name,"num_upcoming_shows":num})
      print(data)
    else:
      ind=ind+1
      final={}
      final['city']=venue.city
      final['state'] = venue.state
      final['venues'] = [{"id":venue.id,"name":venue.name,"num_upcoming_shows":num}]
      data.append(final)
      print(data)
    city_existing=venue.city
    state_existing=venue.state


    #data : [{city:SF,state:CA,venues:[id,...]}]

  
  return render_template('pages/venues.html', areas=data);
  

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  searchword = request.form.get('search_term', '')
  result = db.session.query(Venue).filter(Venue.name.ilike(f'%{searchword}%')).all()
  count=len(result)
  response = {"count":count,"data":[]}
  for i in result:
    num = Show.query.filter(Show.start_time>datetime.now(),Show.venue_id==i.id).count()
    response['data'].append({"id":i.id,"name":i.name,"num_upcoming_shows":num})


  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  venuefilter = Venue.query.filter_by(id=venue_id).first()
  comingupshows = Show.query.join(Artist).filter(Show.start_time>datetime.now(),Show.venue_id==venue_id).all()
  #past_shows = Show.query.filter(Show.start_time<=datetime.now(),Show.venue_id==venue_id).all()
  completedshows = Show.query.join(Artist).filter(Show.start_time<=datetime.now(),Show.venue_id==venue_id).all()
  
  data = {"id": venuefilter.id,
    "name": venuefilter.name,
    "genres": venuefilter.genres.split(','),
    "address": venuefilter.address,
    "city": venuefilter.city,
    "state": venuefilter.state,
    "phone": venuefilter.phone,
    "website_link": venuefilter.website_link,
    "facebook_link": venuefilter.facebook_link,
    "seeking_talent": venuefilter.seeking_talent,
    "seeking_description": venuefilter.seeking_description,
    "image_link":venuefilter.image_link,
    "past_shows":[],
    "upcoming_shows": [],
    "past_shows_count": len(completedshows),
    "upcoming_shows_count": len(comingupshows)}

  for i in comingupshows:
    #art = Artist.query.filter_by(id=i.artist_id).first()
    data["upcoming_shows"].append({"artist_id":i.artist_id,"artist_name":i.Artist.name,"artist_image_link":i.Artist.image_link,"start_time":str(i.start_time)})

  for j in completedshows:
    #art = Artist.query.filter_by(id=j.artist_id).first()
    data["past_shows"].append({"artist_id":j.artist_id,"artist_name":j.Artist.name,"artist_image_link":j.Artist.image_link,"start_time":str(j.start_time)})


  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm()
  error=False
  
  try:
    
    venue=Venue(
      name=request.form['name'],
      city=request.form['city'],
      state = request.form['state'],
      address = request.form['address'],
      phone = request.form['phone'],
      genres = request.form.getlist('genres'),
      image_link = request.form['image_link'],
      facebook_link = request.form['facebook_link'],
      website_link = request.form['website_link'],
      seeking_talent = True if 'seeking_talent' in request.form else False,
      seeking_description = request.form['seeking_description'],
    )
    db.session.add(venue)
    db.session.commit()

  except:
    error=True
    db.session.rollback()
    print(sys.exc_info())

  finally:
    db.session.close()

  if error:
    print('Error occurred!')
    flash('Venue ' + request.form['name'] + ' was not successfully listed!')
  if not error:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  return render_template('pages/home.html')







  # on successful db insert, flash success
  #flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  #return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error=False
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()

  except:
    error=True
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    flash('Error occured while deleting the Venue')
  else:
    flash('Venue was successfully deleted!')
    
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = []
  artists_list = Artist.query.all()
  for artist in artists_list:
    data.append({"id":artist.id, "name":artist.name})
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  searchword = request.form.get('search_term', '')
  result = db.session.query(Artist).filter(Artist.name.ilike(f'%{searchword}%')).all()
  count=len(result)
  response = {"count":count,"data":[]}
  for i in result:
    num = Show.query.filter(Show.start_time>datetime.now(),Show.artist_id==i.id).count()
    response['data'].append({"id":i.id,"name":i.name,"num_upcoming_shows":num})


  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artistfilter = Artist.query.filter_by(id=artist_id).first()
  comingupshows = Show.query.join(Venue).filter(Show.start_time>datetime.now(),Show.artist_id==artist_id).all()
  #past_shows = Show.query.filter(Show.start_time<=datetime.now(),Show.venue_id==venue_id).all()
  completedshows = Show.query.join(Venue).filter(Show.start_time<=datetime.now(),Show.artist_id==artist_id).all()
  
  data = {"id": artistfilter.id,
    "name": artistfilter.name,
    "genres": artistfilter.genres.split(','),
    "city": artistfilter.city,
    "state": artistfilter.state,
    "phone": artistfilter.phone,
    "website_link": artistfilter.website_link,
    "facebook_link": artistfilter.facebook_link,
    "seeking_venue": artistfilter.seeking_venue,
    "seeking_description": artistfilter.seeking_description,
    "image_link":artistfilter.image_link,
    "past_shows":[],
    "upcoming_shows": [],
    "past_shows_count": len(completedshows),
    "upcoming_shows_count": len(comingupshows)}

  for i in comingupshows:
    #art = Artist.query.filter_by(id=i.artist_id).first()
    data["upcoming_shows"].append({"venue_id":i.venue_id,"venue_name":i.Venue.name,"venue_image_link":i.Venue.image_link,"start_time":str(i.start_time)})

  for j in completedshows:
    #art = Artist.query.filter_by(id=j.artist_id).first()
    data["past_shows"].append({"venue_id":j.venue_id,"venue_name":j.Venue.name,"venue_image_link":j.Venue.image_link,"start_time":str(j.start_time)})









  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artistedit = Artist.query.filter_by(id=artist_id).first()
  artist={
    "name": artistedit.name,
    "genres": artistedit.genres.split(','),
    "city": artistedit.city,
    "state": artistedit.state,
    "phone": artistedit.phone,
    "website_link": artistedit.website_link,
    "facebook_link": artistedit.facebook_link,
    "seeking_venue": artistedit.seeking_venue,
    "seeking_description": artistedit.seeking_description,
    "image_link": artistedit.image_link
  }
  form = ArtistForm(data=artist)
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venueedit = Venue.query.filter_by(id=venue_id).first()
  venue={
    "id": venueedit.id,
    "name": venueedit.name,
    "genres": venueedit.genres.split(','),
    "address": venueedit.address,
    "city": venueedit.city,
    "state": venueedit.state,
    "phone": venueedit.phone,
    "website_link": venueedit.website_link,
    "facebook_link": venueedit.facebook_link,
    "seeking_talent": venueedit.seeking_talent,
    "seeking_description": venueedit.seeking_description,
    "image_link": venueedit.image_link
  }
  form = VenueForm(data=venue)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm
    error= False

    try:
      artist=Artist(
      name=request.form['name'],
      city=request.form['city'],
      state = request.form['state'],
      #address = request.form['address'],
      phone = request.form['phone'],
      genres = request.form.getlist('genres'),
      image_link = request.form['image_link'],
      facebook_link = request.form['facebook_link'],
      website_link = request.form['website_link'],
      seeking_venue = True if 'seeking_venue' in request.form else False,
      seeking_description = request.form['seeking_description']
    )
      db.session.add(artist)
      db.session.commit()

    except :
      error=True
      print(sys.exc_info())
      db.session.rollback()

    finally:
      db.session.close()

    if error:
    
      flash('Artist ' + request.form['name'] + ' was not successfully listed!')
    if not error:
      flash('Artist ' + request.form['name'] + ' was successfully listed!')










  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  #flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = Show.query.join(Artist).join(Venue).all()
  data = []
  for showlist in shows:
    #ven = Venue.query.get(showlist.venue_id)
    #artist = Artist.query.get(showlist.artist_id)

    data.append({"venue_id": showlist.venue_id,
      "venue_name": showlist.Venue.name,
      "artist_id": showlist.artist_id,
      "artist_name": showlist.Artist.name,
      "artist_image_link": showlist.Artist.image_link,
      "start_time": str(showlist.start_time)})

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error=False

    try:
      show = Show(artist_id=request.form['artist_id'],
        venue_id=request.form['venue_id'],
        start_time=request.form['start_time'],
      )

      db.session.add(show)
      db.session.commit()

    except:
      error=True
      print(sys.exc_info())
      db.session.rollback()
    finally:
      db.session.close()
    if error:
      error = True
      flash('Show could not be listed')
    else:
      flash('Show was successfully listed!')

    return render_template('pages/home.html')





  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  #flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
