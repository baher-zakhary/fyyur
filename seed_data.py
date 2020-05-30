from models import State, Genre
import sys

stateNames = ['AL',
'AK',
'AZ',
'AR',
'CA',
'CO',
'CT',
'DE',
'DC',
'FL',
'GA',
'HI',
'ID',
'IL',
'IN',
'IA',
'KS',
'KY',
'LA',
'ME',
'MT',
'NE',
'NV',
'NH',
'NJ',
'NM',
'NY',
'NC',
'ND',
'OH',
'OK',
'OR',
'MD',
'MA',
'MI',
'MN',
'MS',
'MO',
'PA',
'RI',
'SC',
'SD',
'TN',
'TX',
'UT',
'VT',
'VA',
'WA',
'WV',
'WI',
'WY']

genreNames = ['Alternative',
'Blues',
'Classical',
'Country',
'Electronic',
'Folk',
'Funk',
'Hip-Hop',
'Heavy Metal',
'Instrumental',
'Jazz',
'Musical Theatre',
'Pop',
'Punk',
'R&B',
'Reggae',
'Rock n Roll',
'Soul',
'Other']

def seed_states_data(app, db):
    with app.app_context():
        error = False
        states = []
        for stateName in stateNames:
            state = State(name = stateName)
            states.append(state)
        try:
            db.session.add_all(states)
            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            if not error:
                print('Seeding states data succeeded')
            else:
                print('Seeding states data failed')
            db.session.close()

def seed_genres_data(app, db):
    with app.app_context():
        error = False
        genres = []
        for genreName in genreNames:
            genre = Genre(name = genreName)
            genres.append(genre)
        try:
            db.session.add_all(genres)
            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            if not error:
                print('Seeding genres data succeeded')
            else:
                print('Seeding genres data failed')
            db.session.close()

