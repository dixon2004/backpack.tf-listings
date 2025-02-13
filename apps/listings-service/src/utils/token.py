from utils.config import AUTH_TOKEN
from utils.logger import SyncLogger


class AuthorizationToken:

    def __init__(self) -> None:
        """
        Initialize the AuthorizationToken class.
        """
        self.logger = SyncLogger("AuthorizationToken")
    

    def token_valid(self, token: str) -> bool:
        """
        Check if the token is valid.

        Args:
            token (str): Authorization token.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        try:            
            token = token.replace("Token ", "").strip()
            if token == AUTH_TOKEN:
                return True
            else:
                False
        except Exception as e:
            self.logger.write_log("error", f"Failed to check token: {e}")
