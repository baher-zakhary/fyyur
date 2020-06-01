#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import config
from flask_migrate import Migrate
from models import create_app, Venue, Show, Artist, State, Genre
import sys
from datetime import datetime
# from seed_data import seed_states_data, seed_genres_data

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app, db = create_app()
moment = Moment(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# moved in models.py file

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  result = State.query.with_entities(Venue.city, Venue.state_id).distinct().all()
  newData = []
  for city, state_id in result:
    newData.append({
      "city": city,
      "state": State.query.filter_by(id=state_id).first().name,
      "venues": Venue.query.filter_by(city=city).filter_by(state_id=state_id).all()
    })
  return render_template('pages/venues.html', areas=newData);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  search_term = request.form['search_term']
  results = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  response = {
    "count": len(results),
    "data": results
  }
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  result = Venue.query.filter(Venue.id == venue_id).first()
  result.past_shows = []
  result.upcoming_shows = []
  for show in result.shows:
    if show.start_time < datetime.now():
      result.past_shows.append({
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": str(show.start_time)
      })
    else:
      result.upcoming_shows.append({
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": str(show.start_time)
      })
  result.upcoming_shows_count = len(result.upcoming_shows)
  result.past_shows_count = len(result.past_shows)
  return render_template('pages/show_venue.html', venue=result)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  try:
    # TODO: insert form data as a new Venue record in the db, instead
    venue = Venue()
    venue.name = request.form['name']
    venue.city = request.form['city']
    state = State.query.filter_by(name=request.form['state']).first()
    venue.state = state
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.facebook_link = request.form['facebook_link']
    venue.genres = Genre.query.filter(Genre.name.in_(request.form.getlist('genres'))).all() 
    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  # TODO: modify data to be the data object returned from db insertion
  if not error:
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    error = True
    print(sys.exc_info())
    db.session.rollback()
  finally:
    db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  if not error:
    flash('Venue deleted successfully')
    return render_template('pages/venues.html')
  else:
    flash('Venue deletion Failed !')
    return render_template(url_for('show_venue', venue_id=venue_id))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form['search_term']
  results = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
  response = {
    "count": len(results),
    "data": results
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  result = Artist.query.filter(Artist.id == artist_id).first()
  result.upcoming_shows = []
  result.past_shows = []
  for show in result.shows:
    if show.start_time < datetime.now():
      result.past_shows.append({
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": str(show.start_time)
      })
    else:
      result.upcoming_shows.append({
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": str(show.start_time)
      })
  result.upcoming_shows_count = len(result.upcoming_shows)
  result.past_shows_count = len(result.past_shows)
  return render_template('pages/show_artist.html', artist=result)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  result = Artist.query.filter(Artist.id == artist_id).first()
  artist={
    'id': result.id,
    'name': result.name,
    'city': result.city,
    'state': result.state.name,
    'phone': result.phone,
    'image_link': result.image_link,
    'genres': list(map(lambda genre: genre.name, result.genres)),
    'facebook_link': result.facebook_link,
  }
  form = ArtistForm(data=artist)
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  print(request.form)
  error = False
  try:
    artist = Artist.query.filter(Artist.id == artist_id).first()
    artist.name = request.form['name']
    artist.city = request.form['city'] 
    artist.state = State.query.filter(State.name == request.form['state']).first()    
    artist.phone = request.form['phone'] 
    artist.image_link = request.form['image_link']
    artist.facebook_link = request.form['facebook_link']
    artist.genres = Genre.query.filter(Genre.name.in_(request.form.getlist('genres'))).all()
    db.session.commit()
  except:
    print(sys.exc_info())
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if not error:
    flash('Artist updated successfully', 'error')
  else:
    flash('Artist not updated')
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  result = Venue.query.filter(Venue.id == venue_id).first()
  venue={
    "id": result.id,
    "name": result.name,
    "genres": list(map(lambda genre: genre.name, result.genres)),
    "address": result.address,
    "city": result.city,
    "state": result.state.name,
    "phone": result.phone,
    "website": result.website,
    "facebook_link": result.facebook_link,
    "seeking_talent": result.seeking_talent,
    "seeking_description": result.seeking_description,
    "image_link": result.image_link
  }
  # TODO: populate form with values from venue with ID <venue_id>
  form = VenueForm(data=venue)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  try:
    venue = Venue.query.filter(Venue.id == venue_id).first()
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = State.query.filter(State.name == request.form['state']).first()
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.facebook_link = request.form['facebook_link']
    venue.genres = Genre.query.filter(Genre.name.in_(request.form.getlist('genres'))).all()
    db.session.commit()
  except:
    error = True
    print(sys.exc_info())
    db.session.rollback()
  finally:
    db.session.close()
  if not error:
    flash('Venue updated successfully')
  else:
    flash('Venue not updated')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False
  try:
  # TODO: insert form data as a new artist record in the db, instead
    artist = Artist()
    artist.name = request.form['name']
    artist.city = request.form['city']
    state = State.query.filter_by(name=request.form['state']).first()
    artist.state = state
    artist.phone = request.form['phone']
    for name in request.form.getlist('genres'):
      genre = Genre.query.filter_by(name=name).first()
      artist.genres.append(genre) 
    artist.facebook_link = request.form['facebook_link']

    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  # TODO: modify data to be the data object returned from db insertion
  # on successful db insert, flash success
  if not error:
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows = Show.query.all()
  data = []
  for show in shows:
    if show.start_time >= datetime.now():
      data.append({
        "venue_id": show.id,
        "venue_name": show.venue.name,
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": str(show.start_time)
      })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  try:
    show = Show()
    show.start_time = request.form['start_time']
    venue = Venue.query.filter_by(id=request.form['venue_id']).first()
    venue.shows.append(show)
    artist = Artist.query.filter_by(id=request.form['artist_id']).first()
    artist.shows.append(show)
    db.session.commit()
  except:
    error = True
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be listed.')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  # on successful db insert, flash success
  if not error:
    flash('Show was successfully listed!')

  return render_template('pages/home.html')

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
    # seed_states_data(app, db)
    # seed_genres_data(app, db)
    app.run(debug=config.DEBUG)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
