from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from koor.config.common import Common

USER_CLAIM_ID = Common.SIMPLE_JWT.get('USER_ID_CLAIM', 'user_id')
class SessionTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer class that extends the functionality of TokenObtainPairSerializer.
    The class adds the session_id to the token data.
    
    Args:
    user (User): The User model instance.
    session_id (str): The session id that needs to be added to the token data.
    
    Returns:
    dict: The token data with added session_id.
    """
    @classmethod
    def get_token(cls, user, session_id):
        """
        Method to generate token data by calling the parent class's `get_token` method and adding the session_id to it.
        
        Args:
        user (User): The User model instance.
        session_id (str): The session id that needs to be added to the token data.
        
        Returns:
        dict: The token data with added session_id.
        """
        token = super().get_token(user)
        token[USER_CLAIM_ID] = str(session_id)

        return token

class SessionTokenObtainPairView(TokenObtainPairView):
    """
    View class that extends the functionality of TokenObtainPairView.
    The class sets the serializer class as `SessionTokenObtainPairSerializer` which adds the session_id to the token data.
    """
    serializer_class = SessionTokenObtainPairSerializer
