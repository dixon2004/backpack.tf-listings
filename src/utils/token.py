from utils.config import AUTH_TOKEN
from utils.log import write_log


class AuthorizationToken:
    
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
            write_log("error", f"[AuthorizationToken] Failed to check token: {e}")
