import os
import time
import socket
import pytest
from subprocess import Popen, PIPE
from pathlib import Path
from random import randint

from ru.hse.client.Client import Client


def _wait_port(host: str, port: int, timeout_s: float = 10.0) -> None:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.3):
                return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError(f"Server did not start on {host}:{port} within {timeout_s}s")


class TestServerClientSystem:
    @pytest.fixture(scope="module", autouse=True)
    def server_for_tests(self):
        server_url = os.getenv("SERVER_URL")
        if server_url:
            yield "external-server"
            return

        project_root = Path(__file__).resolve().parents[4]
        server_dir = project_root / "server"
        jar_path = server_dir / "HomeTask04Java.jar"

        # Start the Java server on port 7000
        server_process = Popen(
            ["java", "-jar", str(jar_path), "7000"],
            stdout=PIPE,
            stderr=PIPE
        )

        _wait_port("127.0.0.1", 7000, timeout_s=12)

        yield "local-server"

        # Terminate the server process after tests
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except Exception:
            server_process.kill()

    def setup_method(self):
        self.client = Client(os.getenv("SERVER_URL", "http://localhost:7000"), None)

    def test_client_register_success(self):
        #arrange
        rand_value = randint(0, 2000)
        login = f"loginRegisterCorrect_{rand_value}"

        #act
        account = self.client.register(login, "somePassword")

        #assert
        assert account is not None
        assert account.active_session is not None

        self.client.logout(account)

    def test_client_login_success(self):
        #arrange
        rand_value = randint(0, 2000)
        login = f"loginCorrectForRelogin_{rand_value}"
        account = self.client.register(login, "somePassword")
        self.client.logout(account)

        #act
        account = self.client.login(login, "somePassword")

        #assert
        assert account is not None
        assert account.active_session is not None

        self.client.logout(account)