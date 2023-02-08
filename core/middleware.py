"""
File in which we have the middleware for Django for Authenticating API requests
"""
import jwt
from decouple import config

from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin

from core.tokens import SessionTokenObtainPairSerializer
from koor.config.common import Common
from users.models import UserSession

# Get JWT secret key
SECRET_KEY = config("DJANGO_SECRET_KEY")


class JWTMiddleware(MiddlewareMixin):
    """
    Custom Middleware Class to process a request before it reached the endpoint.
    It decodes the Authorization Token from the header and if the decode successfull
    we forward the response to endpoint.

    Else, We send the response with `401` status code.
    """

    user_model = get_user_model()  # Get the user model define in the settings `AUTH_USER_MODEL`
    refresh_token_lookup = 'x-refresh'
    access_token_lookup = 'x-access'
    claim_id = Common.SIMPLE_JWT.get('USER_ID_CLAIM', 'user_id')
    algorithms = Common.SIMPLE_JWT.get('ALGORITHM', ['HS256', ])

    def get_access_token_for_user(self, user, session_id):
        '''
        Return the access token for the user.
        '''
        refresh = SessionTokenObtainPairSerializer.get_token(
            user=user,
            session_id=session_id
        )
        return str(refresh.access_token)

    def decode_token(self, token):
        # If the token expired this raise jwt.ExpiredSignatureError
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=self.algorithms)
        return payload

    def get_session(self, payload):
        '''
        Get the session for the given token.
        '''
        try:
            session_id = payload[self.claim_id]
            session = UserSession.objects.get(id=session_id)
            return session
        except UserSession.DoesNotExist:
            return None

    def process_response(self, request, response):
        """
        Custom middleware handler to check authentication for a user with JWT authentication
        :param request: Request header containing authorization tokens
        :type request: Django Request Object
        :return: HTTP Response if authorization fails, else response.status_code = 401
        """
        if 'Authorization' in request.headers:  # Check if the Authorization in the request
            # Get the Authorization from the header
            access_token = request.headers.get('Authorization') \
                .replace('Bearer ', '')
            try:
                # Try to decode the access token and if not possible handle the respective Exception 
                access_token_payload = self.decode_token(access_token)
                self.get_session(access_token_payload)
                # Return the response to respective endpoint
                return response

            except jwt.ExpiredSignatureError:
                # If the access token expired then we process the refresh token
                try:
                    refresh_token = request.headers.get(self.refresh_token_lookup)
                    refresh_token_payload = self.decode_token(refresh_token)
                    session = self.get_session(refresh_token_payload)
                    if session:
                        response.headers.setdefault(self.access_token_lookup,
                                                    self.get_access_token_for_user(session.user, session.id))
                    response.status_code = 200
                    return response

                # if the session does not exists
                except UserSession.DoesNotExist:
                    response.status_code = 401
                    return response

                # check if the token is already expired
                except jwt.ExpiredSignatureError:
                    response.status_code = 401
                    return response

            # check if any other exception occur
            except [
                jwt.DecodeError,
                jwt.InvalidTokenError,
                jwt.InvalidSignatureError,
            ]:
                response.status_code = 401
                return response
        else:
            return response
