from rest_framework_simplejwt.authentication import JWTAuthentication

from koor.config.common import Common

from users.models import UserSession


class CustomJWTAuthentication(JWTAuthentication):
    claim_id = Common.SIMPLE_JWT.get('USER_ID_CLAIM', 'user_id')

    def get_user(self, validated_token):
        """
        This function attempts to find and return a user using the given validated token.

        Args:
            validated_token (Dict[str, Any]): The validated JWT token.

        Returns:
            User: The user associated with the given token if found and active, otherwise raises an exception.

        Raises:
            InvalidToken: If the token contains no recognizable user identification.
            AuthenticationFailed: If the user is not found or is inactive.
        """
        try:
            session_id = validated_token[self.claim_id]
            user = UserSession.objects.get(id=session_id).user
        except KeyError:
            raise InvalidToken(_("Token contained no recognizable user identification"))
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed(_("User not found"), code="user_not_found")

        if not user.is_active:
            raise AuthenticationFailed(_("User is inactive"), code="user_inactive")

        return user
