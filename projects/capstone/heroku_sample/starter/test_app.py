import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actors, Movies

# TEST CASE CLASS


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):

        DATABASE_URL = 'postgresql://postgres:Srinivas2308@localhost:5432/postgres'
        ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRVRFhUdTV0SWhHZ2VuLVJvWGxhbSJ9.eyJpc3MiOiJodHRwczovL2Rldi1wdWhyMjJqYS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJjYzRlZDcxMzZjN2YwMzkyNWY0NmY0IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTY1NzU2NTk1MCwiZXhwIjoxNjU3NTczMTUwLCJhenAiOiJVeEtqNXNkWTJUSXZ3ZHhKYVlrZ0xSaGdHS1N0eHRQQSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.lniXchZrbQDcE4JNSnTkupSVWJToRU7-Rtb_Xv8jNoIi5uvYsVf6G2S5uP_y2zXsx-90JZoNQm0V51-UudSA48xkx_wLA0rsIz3m_L9kaJoT3vaFqPX9dMF6ypdVRpN0Az5QY6Vhe1DmZrfHTvHwMHME3zNfC305lgLOWXbWYq_1j4JFqyqTF4qhu5rL5Oxty7LXBXgZG2WDbBVgtiCsOO9ZIqAGiAES-Xhv5ogqdFszSt6nq4DKG5761L-zp8XGRJbPWA2fZZRQz_bY2ouQX9ceBnAT4gayEO5vc8P9D6IqhJk1Q6pZ8_CbetIL7OalK5tBJ2Q4TnZBGCDKMofWOw'
        DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRVRFhUdTV0SWhHZ2VuLVJvWGxhbSJ9.eyJpc3MiOiJodHRwczovL2Rldi1wdWhyMjJqYS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJjYzRmMzIxMzZjN2YwMzkyNWY0NzE3IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTY1NzU2NjY4OSwiZXhwIjoxNjU3NTczODg5LCJhenAiOiJVeEtqNXNkWTJUSXZ3ZHhKYVlrZ0xSaGdHS1N0eHRQQSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.ZbpdrtsqymshKASTkdYjE3SLSwV8ThnrkYFzlRgMTgatlEn6OUqARWtMvRGAsKZ3YUCOq1BNhq7Rx_eFSVTQRu8jRhla7T4APhcbEMtlMKNu_r4a6j7q2-NnmaqeORPugkIVaHYQ6xpvrF6W-21Cw95m7PR_Q467fHLLXyDyzvXq6RSrF9n1TCU7WlbqXNKbOs-nqEAwkom2XDL_UAG79jh2ztxqKF5898tS_5rPGC_P8fSrl_ygtb_9mhKtpcSGcwuhNsafYEFnIbjPNU1Nn2u8EMs-tNHDE0F6yoHeER_Ibbs2i63AoSqy7LE4CBePjrVcoPwSbZLvhHjam9w_ZA'
        PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRVRFhUdTV0SWhHZ2VuLVJvWGxhbSJ9.eyJpc3MiOiJodHRwczovL2Rldi1wdWhyMjJqYS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJjYzRmNzVkZjMzMTAxNTZmNWYzM2RjIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTY1NzU2ODM1MCwiZXhwIjoxNjU3NTc1NTUwLCJhenAiOiJVeEtqNXNkWTJUSXZ3ZHhKYVlrZ0xSaGdHS1N0eHRQQSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.BqQbJL0DdNJpNfPI024L8QVU2b6dYkFy7z7Bk2oawKS2RyE4HcqgIdFfoREZJiPL7PHrU-gPxszwKlPSuN-8r3E9UTTep-T6WudfHgBZ2pryfJuLE6Bs4NLBqch1H33F6rwlPmbUw3icl3xxDlqe1S3Qg9e3yNGsnuXhmEQls9U2UAId6ntsWZMA1eElsu6YPGG-YKVvep55C3UVTtHbYSrrRBfjbYnTNbAIG2Je6dS0Mh7pVKFMj6c1KHF4eDdh9fBew_glsP-q1Z2kwv2xFwpB4RH07175Qw7CfYTDgb7oDXaNoGNpiqG1dlQyoeS20Lw75nEH-ozyzKFYK4V-Vg'

        self.assistant_auth_header = {'Authorization':
                                      'Bearer ' + ASSISTANT_TOKEN}
        self.director_auth_header = {'Authorization':
                                     'Bearer ' + DIRECTOR_TOKEN}
        self.producer_auth_header = {'Authorization':
                                     'Bearer ' + PRODUCER_TOKEN}
        self.database_path = DATABASE_URL

        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, self.database_path)


# Test data set-up for all tests down under

        self.post_actor = {
            'name': "James",
            'age': 46,
            'gender': 'MALE'
        }

        self.post_actor1 = {
            'name': "Catherine",
            'age': 28,
            'gender': 'FEMALE'
        }

        self.post_actor2 = {
            'name': "Peter",
            'age': 78,
            'gender': 'MALE'
        }

        self.post_actor_name_missing = {
            'age': 34,
            'gender': "MALE"
        }

        self.post_actor_gender_missing = {
            'age': 78,
            'name': "Johns"
        }

        self.patch_actor_on_age = {
            'age': 55
        }

        self.post_movie = {
            'title': "New movie",
            'release_date': "2009-10-10"
        }

        self.post_movie1 = {
            'title': "Funnie Movie",
            'release_date': "2020-10-10"
        }

        self.post_movie2 = {
            'title': "Horror",
            'release_date': "2067-10-10"
        }

        self.post_movie_title_missing = {
            'release_date': "2089-10-10"
        }

        self.post_movie_reldate_missing = {
            'title': "Krishna"
        }

        self.patch_movie_on_reldate = {
            'release_date': "2090-10-10"
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass


# Test cases for the Endpoints related to /actors
# ------------------------------------------------
# GET Positive case - Assistant Role


    def test_get_actors1(self):
        res = self.client().get('/actors?page=1',
                                headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

# GET Positive case - Director Role
    def test_get_actors2(self):
        res = self.client().get('/actors?page=1',
                                headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

# GET Positive case - Producer Role
    def test_get_actors3(self):
        res = self.client().get('/actors?page=1',
                                headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

# POST Positive case - Director Role
    def test_post_new_actor1(self):
        res = self.client().post('/actors',
                                 json=self.post_actor1,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)

        actor = Actors.query.filter_by(id=data['actor-added']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(actor)

# POST Positive case - Producer Role
    def test_post_new_actor2(self):
        res = self.client().post('/actors',
                                 json=self.post_actor2,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        actor = Actors.query.filter_by(id=data['actor-added']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(actor)

# POST Negative Case - Add actor with missing name
# - Director Role
    def test_post_new_actor_name_missing(self):
        res = self.client().post('/actors',
                                 json=self.post_actor_name_missing,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# POST Negative Case - Add actor with missing gender - Director Role
    def test_post_new_actor_gender_missing(self):
        res = self.client().post('/actors',
                                 json=self.post_actor_gender_missing,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# DELETE Positive Case - Deleting an existing actor - Director Role
    def test_delete_actor(self):
        res = self.client().post('/actors', json=self.post_actor,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        actor_id = data['actor-added']

        res = self.client().delete('/actors/{}'.format(actor_id),
                                   headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor-deleted'], actor_id)

# DELETE Negative Case actor not found - Director Role
    def test_delete_actor_not_found(self):
        res = self.client().delete('/actors/69',
                                   headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

# PATCH Positive case - Update age of an existing
# actor - Director Role
    def test_patch_actor(self):
        res = self.client().patch('/actors/2',
                                  json=self.patch_actor_on_age,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor-updated'], 2)

# PATCH Negative case - Update age for non-existent actor
# - Director Role
    def test_patch_actor_not_found(self):
        res = self.client().patch('/actors/89',
                                  json=self.patch_actor_on_age,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

# RBAC - Test Cases:
# RBAC GET actors w/o Authorization header
    def test_get_actors_no_auth(self):
        res = self.client().get('/actors?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'Authorization header is expected.')

# RBAC POST actors with wrong Authorization header - Assistant Role
    def test_post_actor_wrong_auth(self):
        res = self.client().post('/actors',
                                 json=self.post_actor1,
                                 headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

# RBAC DELETE Negative Case - Delete an existing actor
# without appropriate permission
    def test_delete_actor_wrong_auth(self):
        res = self.client().delete('/actors/10',
                                   headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')


# Test cases for the Endpoints related to /movies
# ------------------------------------------------
# GET Positive case - Assistant Role


    def test_get_movies1(self):
        res = self.client().get('/movies?page=1',
                                headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

# GET Positive case - Director Role
    def test_get_movies2(self):
        res = self.client().get('/movies?page=1',
                                headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

# GET Positive case - Producer Role
    def test_get_movies3(self):
        res = self.client().get('/movies?page=1',
                                headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

# POST Positive case - Producer Role
    def test_post_new_movie2(self):
        res = self.client().post('/movies', json=self.post_movie2,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        movie = Movies.query.filter_by(id=data['movie-added']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(movie)

# POST Negative Case - Add movie with missing title
# - Producer Role
    def test_post_new_movie_title_missing(self):
        res = self.client().post('/movies',
                                 json=self.post_movie_title_missing,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# POST Negative Case - Add movie with missing release date
# - Producer Role
    def test_post_new_movie_reldate_missing(self):
        res = self.client().post('/movies',
                                 json=self.post_movie_reldate_missing,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# DELETE Positive Case - Deleting an existing movie - Producer Role
    def test_delete_movie(self):
        res = self.client().post('/movies',
                                 json=self.post_movie,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        #movie_id = data['movie-added']
        movie_id = '4'

        res = self.client().delete('/movies/{}'.format(movie_id),
                                   headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie-deleted'], movie_id)

# DELETE Negative Case movie not found - Producer Role
    def test_delete_movie_not_found(self):
        res = self.client().delete('/movies/777',
                                   headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

# PATCH Positive case - Update Release Date of
# an existing movie - Director Role
    def test_patch_movie(self):
        res = self.client().patch('/movies/2',
                                  json=self.patch_movie_on_reldate,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie-updated'], 2)

# PATCH Negative case - Update Release Date for
# non-existent movie - Director Role
    def test_patch_movie_not_found(self):
        res = self.client().patch('/movies/99',
                                  json=self.patch_movie_on_reldate,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

# RBAC - Test Cases:
# RBAC GET movies w/o Authorization header
    def test_get_movies_no_auth(self):
        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'authorization_header_missing')

# RBAC POST movies with wrong Authorization header - Director Role
    def test_post_movie_wrong_auth(self):
        res = self.client().post('/movies', json=self.post_movie1,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found')

# RBAC DELETE Negative Case - Delete an existing movie
# without appropriate permission
    def test_delete_movie_wrong_auth(self):
        res = self.client().delete('/movies/8',
                                   headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found')


# run 'python test_app.py' to start tests
if __name__ == "__main__":
    unittest.main()
