from utils.log import write_log
import json


class AuthorizationToken:

    def __init__(self):
        self.options_file = "./options.json"


    def get_token(self) -> str:
        """
        Get the preset authorization token.

        Returns:
            str: The preset authorization token.
        """
        try:
            with open(self.options_file, "r") as f:
                options = json.load(f)
                return options.get("auth_token")
        except Exception as e:
            write_log("error", f"[AuthorizationToken] Failed to get preset token: {e}")

    
    def token_valid(self, token: str) -> bool:
        """
        Check if the token is valid.

        Args:
            token (str): Authorization token.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        try:
            preset_token = self.get_token()
            if not preset_token or preset_token == "":
                return True
            
            token = token.replace("Token ", "").strip()
            if token == preset_token:
                return True
            else:
                return False
        except Exception as e:
            write_log("error", f"[AuthorizationToken] Failed to check token: {e}")
