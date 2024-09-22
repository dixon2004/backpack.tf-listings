from utils.log import write_log
import socket
import json


class PortConfiguration:

    def __init__(self) -> None:
        self.reserved_ports = {5000, 7000}
        self.options_file = "./options.json"


    def check_port(self, port: int) -> bool:
        """
        Check if a given port is currently in use.

        Args:
            port (int): Port number to check.

        Returns:
            bool: True if the port is in use, False otherwise.
        """
        try:
            if port in self.reserved_ports:
                return True

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.settimeout(1)
                    s.connect(("localhost", port))
                    return True
                except (socket.timeout, ConnectionRefusedError):
                    return False
        except Exception as e:
            write_log("error", f"[PortConfiguration] Failed to check port: {e}")


    def get_available_port(self) -> int:
        """
        Find an available port in the range 3000-9999 (excluding reserved ports).

        Returns:
            int: Available port number, or the default port if no available port is found.
        """
        try:
            for port in range(3000, 10000):
                if not self.check_port(port):
                    return port
            return None
        except Exception as e:
            write_log("error", f"[PortConfiguration] Failed to get available port: {e}")


    def get_port(self) -> int:
        """
        Get the preset port if it's available, otherwise find an available port.

        Returns:
            int: The port number to use.
        """
        try:
            server_port = self.get_preset_port()
            if not self.check_port(server_port):
                return server_port
            else:
                write_log("info", f"[PortConfiguration] Port {server_port} is in use.")
                available_port = self.get_available_port()
                if available_port:
                    self.save_new_port(available_port)
                return available_port
        except Exception as e:
            write_log("error", f"[PortConfiguration] Failed to get port: {e}")


    def get_preset_port(self) -> int:
        """
        Get the preset port number.

        Returns:
            int: The preset port number.
        """
        try:
            with open(self.options_file, "r") as f:
                options = json.load(f)
                return int(options.get("port"))
        except Exception as e:
            write_log("error", f"[PortConfiguration] Failed to get preset port: {e}")


    def save_new_port(self, port_number: int) -> None:
        """
        Save the new port number to the options file.
        
        Args:
            port_number (int): The new port number.
        """
        try:
            with open(self.options_file, "r") as f:
                options = json.load(f)

            options["port"] = port_number

            with open(self.options_file, "w") as f:
                json.dump(options, f, indent=4)
        except Exception as e:
            write_log("error", f"[PortConfiguration] Failed to save new port: {e}")
            