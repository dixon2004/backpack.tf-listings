from utils.logger import SyncLogger
import asyncio
import time


class SmartRateLimiter:

    def __init__(self) -> None:
        """
        Initialize the SmartRateLimiter class.
        """
        self.min_delay = 0.5
        self.max_delay = 60
        self.backoff_factor = 2
        self.cooldown = 30
        self.success_threshold = 10
        self.token_states = {}
        self.logger = SyncLogger("SmartRateLimiter")


    def get_token_state(self, token: str) -> dict:
        """
        Get the state of the token, initializing it if it doesn't exist.

        Args:
            token (str): The token to get the state for.

        Returns:
            dict: The state of the token.
        """
        if token not in self.token_states:
            self.token_states[token] = {
                "delay": self.min_delay,
                "cooldown_until": 0,
                "success_count": 0
            }
        return self.token_states[token]


    async def wait_for_token(self, token: str) -> None:
        """
        Wait for the token to be available, considering its cooldown and delay.

        Args:
            token (str): The token to wait for.
        """
        state = self.get_token_state(token)
        current_time = time.time()
        wait_time = max(state["cooldown_until"] - current_time, state["delay"])
        if wait_time > 0:
            await asyncio.sleep(wait_time)


    def apply_rate_limit(self, token: str) -> None:
        """
        Apply rate limiting to the token, increasing its delay and setting a cooldown.

        Args:
            token (str): The token to apply rate limiting to.
        """
        state = self.get_token_state(token)
        state["delay"] = min(self.max_delay, state["delay"] * self.backoff_factor)
        state["cooldown_until"] = time.time() + self.cooldown
        state["success_count"] = 0
        self.logger.write_log("info", f"Increasing delay for token {token[:5]}*** to {state['delay']:.2f} seconds")
        

    def reset_token(self, token: str) -> None:
        """
        Reset the token state after a successful request.

        Args:
            token (str): The token to reset.
        """
        state = self.get_token_state(token)
        state["success_count"] += 1
        if state["success_count"] >= self.success_threshold:
            state["delay"] = max(self.min_delay, state["delay"] * 0.9)
            state["cooldown_until"] = 0
            state["success_count"] = 0
            self.logger.write_log("info", f"Decreasing delay for token {token[:5]}*** to {state['delay']:.2f} seconds")
