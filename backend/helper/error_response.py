"""
    Contains the error response helper class
"""
import json
from flask import Response, render_template

from constants import DATA_TYPE_JSON, DATA_TYPE_HTML


class ErrorResponse:
    """
    This helper class is used to enable similar behaviour for all http error responses
    """
    def __init__(self, message, status_code):
        """
        The constructor requires the developer to specify the http error
        input:
            message: A small string explaining the reason for the error
            status_code: The http status code of the response
        """
        self.message = message
        self.status_code = status_code

    def get_http_response(self):
        """
            This function transforms the object to a http response object
            using the information set in the constructor
        """
        json_string = {
            "message": self.message,
        }
        return Response(json.dumps(json_string), status=self.status_code, mimetype=DATA_TYPE_JSON)

    @staticmethod
    def get_unsupported_media_type():
        """
            static helper function to get consistent 415 http error responses
            result:
                A http response with the http error code 415
        """
        return ErrorResponse("Unsupported media type", 415).get_http_response()

    @staticmethod
    def get_unauthorized():
        """
            static helper function to get consistent 401 http error responses
            result:
                A http response with the http error code 401
        """
        return ErrorResponse("Unauthorized", 401).get_http_response()

    @staticmethod
    def get_forbidden():
        """
            static helper function to get consistent 403 http error responses
            result:
                A http response with the http error code 403
        """
        return ErrorResponse("Forbidden", 403).get_http_response()

    @staticmethod
    def get_not_found():
        """
            static helper function to get consistent 404 http error responses
            result:
                A http response with the http error code 404
        """
        return Response(render_template('404.html'), 404, mimetype=DATA_TYPE_HTML)

    @staticmethod
    def get_gateway_timeout():
        """
            static helper function to get consistent 504 http error responses
            result:
                A http response with the http error code 504
        """
        return ErrorResponse("Gateway Timeout", 504).get_http_response()
