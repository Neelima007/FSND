import os
import json
from flask import Flask, request, abort, jsonify
from models import setup_db, Actors, Movies
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
#from auth import AuthError, requires_auth
from auth import AuthError, requires_auth


RECS_PER_PAGE = 12

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)


    '''
    Cors headers 
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    '''
    Pagination 
    '''

    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * RECS_PER_PAGE
        end = start + RECS_PER_PAGE

        recs_format = [record.format() for record in selection]
        page_recs = recs_format[start:end]
        return page_recs
    
    '''
    /GET Actors 
    '''
    @app.route('/actors', methods=['GET'])
    @requires_auth(permission='get:actors')
    def get_actors(payload):
        try:
            result = Actors.query.order_by(Actors.id).all()
            resultant_actors = paginate_questions(request, result)
            
            return jsonify({
                'success': True,
                'actors': resultant_actors,
                
            })
        except Exception:
            abort(422)
    '''
    Post Actors 
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors(payload):
        add_actor = request.get_json()
        #add_actor =json.loads(request.data.decode('utf-8'))
        name = add_actor.get('name')
        gender = add_actor.get('gender')
        age = add_actor.get('age')

        if name is None:
            abort(422)

        if gender is None:
            abort(422)

        if age is None:
            abort(422)

        try:
            new_actor = Actors(name=name,
                               gender=gender,
                               age=age)
            new_actor.insert()

            return jsonify({
                "success": True,
                "actor-added": new_actor.id
            })

        except Exception:
            abort(422)


    '''
    PATCH /actors/<id
    '''
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:actors')
    def patch_actors(payload, id):
        actor = Actors.query.filter(Actors.id == id).first()
        if not actor:
            abort(404)

        updateactor_req = request.get_json()

        if updateactor_req is None:
            abort(422)

        try:
            if 'name' in updateactor_req:
                actor.name = updateactor_req['name']

            if 'gender' in updateactor_req:
                actor.gender = updateactor_req['gender']

            if 'age' in updateactor_req:
                actor.age = updateactor_req['age']

            actor.update()

            return jsonify({
                "success": True,
                "actor-updated": actor.id
            })

        except Exception:
            abort(422)
    '''
    Delete actors
    '''
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors')
    def delete_actors(payload, id):
        actor = Actors.query.filter(Actors.id == id).first()
        if not actor:
            abort(404)
        try:
            actor.delete()
            return jsonify({
                "success": True,
                "actor-deleted": actor.id
            })

        except Exception:
            abort(422)

    '''
    /Get Movies

    '''


    @app.route('/movies', methods=['GET'])
    @requires_auth(permission='get:movies')
    def get_movies(payload):
        try:
            result = Movies.query.order_by(Movies.id).all()
            paged_movies = paginate_questions(request, result)
            
            return jsonify({
                'success': True,
                'movies': paged_movies,
                
            })
        except Exception:
            abort(422)
    
    '''
    post movies 
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth(permission='post:movies')
    def post_movies(payload):
        add_movie = request.get_json()
        movie_name = add_movie.get('title')
        movie_release = add_movie.get('release_date')

        if movie_name is None:
            abort(422)

        if movie_release is None:
            abort(422)

        try:
            new_movie = Movies(title=movie_name,
                               release_date=movie_release)
            new_movie.insert()

            return jsonify({
                "success": True,
                "movie-added": new_movie.id
            })

        except Exception:
            abort(422)
    '''
    Movie update 
    '''

    
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:movies')
    def patch_movies(payload, id):
        movie = Movies.query.filter(Movies.id == id).first()

        if not movie:
            abort(404)

        update_movie = request.get_json()

        if update_movie is None:
            abort(422)

        try:
            if 'title' in update_movie:
                movie.title = update_movie['title']

            if 'release_date' in update_movie:
                movie.release_date = update_movie['release_date']

            movie.update()

            return jsonify({
                "success": True,
                "movie-updated": movie.id
            })

        except Exception:
            abort(422)

    '''
    delete movie

    '''
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:movies')
    def delete_movies(payload, id):
        movie = Movies.query.filter(Movies.id == id).first()

        if not movie:
            abort(404)
        try:
            movie.delete()
            return jsonify({
                "success": True,
                "movie-deleted": movie.id
            })

        except Exception:
            abort(422)



    
    '''
    error handling
    '''

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(403)
    def accessForbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Access Denied/Forbidden"
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(405)
    def notAllowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not Allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def serverError(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify({
            "success": False,
            "error": e.status_code,
            "message": e.error
        }), e.status_code

    return app

app = create_app()

if __name__ == "__main__":
    app.debug = True
    app.run()