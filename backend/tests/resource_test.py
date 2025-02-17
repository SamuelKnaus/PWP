import datetime
import json
import os
import tempfile

import pytest
from sqlalchemy import event
from sqlalchemy.engine import Engine

from api import API, DB
from database.models import Movie, Category, Review
from datamodels.user import UserType, User


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# based on http://flask.pocoo.org/docs/1.0/testing/
@pytest.fixture
def client():
    db_fd, db_fname = tempfile.mkstemp()
    API.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    API.app.config["TESTING"] = True

    with API.app.app_context():
        DB.create_all()
        _populate_db()

    yield API.app.test_client()

    DB.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)


strings = ["JamesCrow", "BigMan", "GreyAlmond"]  # Dummy strings for movies and reviews


def _populate_db():
    for idx, letter in enumerate(strings, start=1):
        cat = Category(
            id=idx,
            title=letter,
        )

        mov = Movie(
            id=idx,
            title=letter,
            director=letter,
            length=60 * idx,
            release_date=datetime.datetime(2022, idx, 3),
        )
        mov.category = cat

        rev = Review(
            id=idx,
            rating=idx,
            comment=letter + " REVIEW",
            date=datetime.datetime(2020, idx, 1),
            author='dummyGuy'
        )

        rev.movie = mov  # Relationship

        DB.session.add(rev)
        DB.session.add(mov)
        DB.session.add(cat)

    DB.session.commit()


"""
TESTING CategoryCollection AND CateogoryItem
"""


def _get_category_json(number=1):
    """
    Creates valid category JSON object to be used for POST and PUT.
    """

    return {"title": "extra-category-{}".format(number), "id": number}


class TestCategoryCollection(object):
    """
    This class implements tests for each HTTP methods in category collection
    resource.
    """
    RESOURCE_URL = "/api/categories/"

    def test_get(self, client):
        """
        Tests the GET Method. Checks that the response status code is 200. Also checks that all of the items from
        the DB popluation are present.
        """
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        print(body)
        assert len(body) == 3
        for item in body["items"]:
            assert "title" in item
            assert "id" in item

    def test_post(self, client):
        """
        Tests the POST method. Checks all of the possible error codes, and 
        also checks that a valid request receives a 201 response with a 
        location header that leads into the newly created resource.
        """
        valid = _get_category_json()

        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201

        """ NA
        # assert resp.headers["Location"].endswith(self.RESOURCE_URL + valid["name"] + "/")
        # resp = client.get(resp.headers["Location"])
        # assert resp.status_code == 200
        # body = json.loads(resp.data)
        # assert body["title"] == "extra-category-1"
        """

        # remove title field for 400
        valid.pop("title")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        # wrong datatype of title
        valid["title"] = 1
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400


class TestCategoryItem(object):
    RESOURCE_URL = "/api/categories/1/"
    INVALID_URL = "/api/categories/x/"
    MODIFIED_URL = "/api/categories/2/"
    NEW_URL = "/api/categories/4/"

    def test_get(self, client):
        """
        Tests the GET Method. Checks that the response status code is 200. Also checks that all of the items from
        the DB popluation are present.
        """

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["id"] == 1
        assert body["title"] == "JamesCrow"
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        """
        Tests the PUT method. Checks all of the possible erroe codes, and also
        checks that a valid request receives a 204 response. Also tests that
        when name is changed, the category can be found from a its new URI. 
        """

        valid = _get_category_json()

        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404

        # test with another category's title
        valid["title"] = "randomTitle"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204

        # remove field for 400
        valid.pop("title")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["title"] == "randomTitle"

    def test_delete(self, client):
        """
        Tests the DELETE method. Checks that a valid request reveives 204
        response and that trying to GET the sensor afterwards results in 404.
        Also checks that trying to delete a sensor that doesn't exist results
        in 404.
        """

        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 409  # This category is used as foreign key
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404

        client.post("/api/categories", json=_get_category_json())
        resp = client.delete(self.NEW_URL)
        assert resp.status_code == 204


"""
TESTING UserCollection, UserItem AND UserReviewCollection
"""


def _get_user_json(number=1):
    """
    Creates a valid User JSON object to be used for PUT and POST tests.
    """

    return {"id": number, "username": "extra-user-{}".format(number),
            "email_address": "extra-email-{}@gmail.com".format(number),
            "password": "extra-password-{}".format(number),
            "role": "Basic User"}


class TestUserCollection(object):
    """
    This class implements tests for each HTTP methods in user collection
    resource.
    """
    RESOURCE_URL = "/api/users/"

    def test_get(self, client):
        """
        Tests the GET Method. Checks that the response status code is 200. Also checks that all of the items from
        the DB popluation are present.
        """
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        print(body)
        assert len(body) == 3
        for item in body["items"]:
            assert "id" in item
            assert "username" in item
            assert "email_address" in item
            assert "role" in item

    def test_post(self, client):
        """
        Tests the POST method. Checks all of the possible error codes, and 
        also checks that a valid request receives a 201 response with a 
        location header that leads into the newly created resource.
        """
        valid = _get_user_json()

        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201  # RETURNING 400

        """ NA Code from sensorhub example: 
        # assert resp.headers["Location"].endswith(self.RESOURCE_URL + valid["name"] + "/")
        # resp = client.get(resp.headers["Location"])
        # assert resp.status_code == 200
        # body = json.loads(resp.data)
        # assert body["title"] == "extra-category-1"
        """

        # remove username field for 400
        valid.pop("username")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        valid = _get_user_json()
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409  # email_address not unique

        valid["email_address"] = "dd@gmail.com"
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409  # username not unique

        valid["username"] = "dd"
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201

        # test invalid email address
        valid = _get_user_json()
        valid["email_address"] = "ght"
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400  # no valid mail address

        # test invalid password
        valid = _get_user_json()
        valid["password"] = "ght"
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400  # password too short

        # test invalid role
        valid = _get_user_json()
        valid["role"] = "ght"
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400  # not one of ['Admin', 'Basic User']


class TestUserItem(object):
    RESOURCE_URL = "/api/users/1/"
    INVALID_URL = "/api/users/x/"
    MODIFIED_URL = "/api/users/2/"

    def test_get(self, client):
        """
        Tests the GET Method. Checks that the response status code is 200. Also checks that all of the items from
        the DB popluation are present.
        """

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["id"] == 1
        assert body["username"] == "dummyGuy1"
        assert body["email_address"] == "dummyGuy1@gmail.com"
        assert body["role"] == "Basic User"
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        """
        Tests the PUT method. Checks all of the possible error codes, and also
        checks that a valid request receives a 204 response. Also tests that
        when name is changed, the category can be found from a its new URI. 
        """

        valid = _get_user_json()

        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404

        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204

        # remove field for 400
        valid.pop("username")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        valid = _get_user_json()
        valid["username"] = "test"
        client.put(self.RESOURCE_URL, json=valid)
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["username"] == "test"  # ERROR: 2 == 1

    def test_delete(self, client):
        """
        Tests the DELETE method. Checks that a valid request reveives 204
        response and that trying to GET the sensor afterwards results in 404.
        Also checks that trying to delete a sensor that doesn't exist results
        in 404.
        """

        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404


class TestUserReviewCollection(object):
    """
    This class implements tests for each HTTP methods in users review collection
    resource.
    """
    RESOURCE_URL = "/api/users/1/reviews/"

    def test_get(self, client):
        """
        Tests the GET Method. Checks that the response status code is 200.
        """
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        print(body)
        assert len(body["items"]) == 1  # Each user has only 1 Review
        for item in body["items"]:
            assert "id" in item
            assert "rating" in item
            assert "comment" in item
            assert "date" in item


"""
TESTING MovieCollection AND MovieItem
"""


def _get_movie_json(number=1):
    """
    Creates a valid User JSON object to be used for PUT and POST tests.
    """

    return {"id": number, "title": "extra-movie-{}".format(number),
            "director": "extra-director-{}".format(number),
            "length": 120,
            "release_date": "2020-09-10",
            "category_id": 1}


class TestMovieCollection(object):
    """
    This class implements tests for each HTTP methods in movies collection
    resource.
    """
    RESOURCE_URL = "/api/movies/"

    def test_get(self, client):
        """
        Tests the GET Method. Checks that the response status code is 200. Also checks that all of the items from
        the DB popluation are present.
        """
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        print(body)
        assert len(body["items"]) == 3
        for item in body["items"]:
            assert "id" in item
            assert "title" in item
            assert "director" in item
            assert "release_date" in item
            assert "length" in item

    def test_post(self, client):
        """
        Tests the POST method. Checks all of the possible error codes, and 
        also checks that a valid request receives a 201 response with a 
        location header that leads into the newly created resource.
        """
        valid = _get_movie_json()

        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201  # RETURNING 400

        """ NA Code from sensorhub example: 
        # assert resp.headers["Location"].endswith(self.RESOURCE_URL + valid["name"] + "/")
        # resp = client.get(resp.headers["Location"])
        # assert resp.status_code == 200
        # body = json.loads(resp.data)
        # assert body["title"] == "extra-category-1"
        """

        # # send same data again for 409
        # resp = client.post(self.RESOURCE_URL, json=valid)
        # assert resp.status_code == 409              # RETURNING 400              

        # remove username field for 400
        valid.pop("title")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        # invalid category_id
        valid = _get_movie_json()
        valid["category_id"] = 20
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409  # foreign key category_id does not exist

        # invalid release_date
        valid = _get_movie_json()
        valid["release_date"] = "March 2019"
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        # invalid length
        valid = _get_movie_json()
        valid["length"] = 0
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400  # must be bigger than 1


class TestMovieItem(object):
    RESOURCE_URL = "/api/movies/1/"
    INVALID_URL = "/api/movies/x/"
    MODIFIED_URL = "/api/movies/2/"

    def test_get(self, client):
        """
        Tests the GET Method. Checks that the response status code is 200. Also checks that all of the items from
        the DB popluation are present.
        """

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["id"] == 1
        assert body["title"] == "JamesCrow"
        assert body["director"] == "JamesCrow"
        assert body["length"] == 60
        assert body["release_date"] == "2022-01-03"
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        """
        Tests the PUT method. Checks all of the possible error codes, and also
        checks that a valid request receives a 204 response. Also tests that
        when name is changed, the category can be found from a its new URI. 
        """

        valid = _get_movie_json()

        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404

        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204  # 400

        # remove field for 400
        valid.pop("title")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        valid = _get_movie_json()
        valid["title"] = "Test"
        client.put(self.RESOURCE_URL, json=valid)
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["title"] == "Test"

    def test_delete(self, client):
        """
        Tests the DELETE method. Checks that a valid request reveives 204
        response and that trying to GET the sensor afterwards results in 404.
        Also checks that trying to delete a sensor that doesn't exist results
        in 404.
        """

        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404


"""
TESTING MovieReviewCollection AND MovieReviewItem
"""


def _get_review_json(number=1):
    """
    Creates a valid Review JSON object to be used for PUT and POST tests.
    """

    return {"id": number,
            "rating": 1,
            "comment": "extra-comment-{}".format(number),
            "date": "2020-01-01T00:00:00.000000Z",
            "author": "dummyGuy",
            "movie_id": 1}


class TestMovieReviewCollection(object):
    """
    This class implements tests for each HTTP methods in movie reviews collection
    resource.
    """
    RESOURCE_URL = "/api/movies/1/reviews/"

    def test_get(self, client):
        """
        Tests the GET Method. Checks that the response status code is 200. Also checks that all of the items from
        the DB popluation are present.
        """
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        print(body)
        assert len(body["items"]) == 1
        for item in body["items"]:
            assert "id" in item
            assert "rating" in item
            assert "comment" in item
            assert "date" in item

    def test_post(self, client):
        """
        Tests the POST method. Checks all of the possible error codes, and 
        also checks that a valid request receives a 201 response with a 
        location header that leads into the newly created resource.
        """
        valid = _get_review_json()

        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201

        """ NA Code from sensorhub example: 
        # assert resp.headers["Location"].endswith(self.RESOURCE_URL + valid["name"] + "/")
        # resp = client.get(resp.headers["Location"])
        # assert resp.status_code == 200
        # body = json.loads(resp.data)
        # assert body["title"] == "extra-category-1"
        """

        # remove username field for 400
        valid.pop("comment")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        # invalid rating
        valid = _get_review_json()
        valid["rating"] = 30
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400  # rating must be <= 5

        # invalid rating
        valid = _get_review_json()
        valid["rating"] = 0
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400  # rating must be >= 1

        # invalid rating
        valid = _get_review_json()
        valid["date"] = "dnjgnib"
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400  # invalid date format


class TestMovieReviewItem(object):
    RESOURCE_URL = "/api/movies/1/reviews/1/"
    INVALID_URL = "/api/movies/1/reviews/x/"
    MODIFIED_URL = "/api/movies/1/reviews/2/"

    def test_get(self, client):
        """
        Tests the GET Method. Checks that the response status code is 200. Also checks that all of the items from
        the DB popluation are present.
        """

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["id"] == 1
        assert body["rating"] == 1
        assert body["comment"] == "JamesCrow REVIEW"
        assert body["date"] == "2020-01-01T00:00:00.000000Z"
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        """
        Tests the PUT method. Checks all of the possible error codes, and also
        checks that a valid request receives a 204 response. Also tests that
        when name is changed, the category can be found from a its new URI. 
        """

        valid = _get_review_json()

        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404

        # test with valid (only change model)
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204

        # remove field for 400
        valid.pop("comment")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        valid = _get_review_json()
        valid["rating"] = 5
        client.put(self.RESOURCE_URL, json=valid)
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["rating"] == 5

    def test_delete(self, client):
        """
        Tests the DELETE method. Checks that a valid request reveives 204
        response and that trying to GET the sensor afterwards results in 404.
        Also checks that trying to delete a sensor that doesn't exist results
        in 404.
        """

        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404
