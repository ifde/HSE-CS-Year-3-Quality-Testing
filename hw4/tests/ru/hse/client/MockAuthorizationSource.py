from ru.hse.IAuthorizationSource import IAuthorizationSource
from ru.hse.OperationResponse import OperationResponse


class MockAuthorizationSource(IAuthorizationSource):
    def __init__(self):
        self.registered_users = {}
        self.active_sessions = {}
        self.session_counter = 1

    def register(self, login: str, password: str) -> OperationResponse:
        if login in self.registered_users:
            return OperationResponse(OperationResponse.ALREADY_INITIATED)
        if login in self.active_sessions:
            return OperationResponse(OperationResponse.ALREADY_LOGGED, self.active_sessions[login])

        self.registered_users[login] = password
        session_id = self.session_counter
        self.session_counter += 1
        self.active_sessions[login] = session_id
        return OperationResponse(OperationResponse.SUCCEED, session_id)

    def login(self, login: str, password: str) -> OperationResponse:
        if login not in self.registered_users:
            return OperationResponse(OperationResponse.NO_USER_INCORRECT_PASSWORD)

        if self.registered_users[login] != password:
            return OperationResponse(OperationResponse.NO_USER_INCORRECT_PASSWORD)

        if login in self.active_sessions:
            return OperationResponse(OperationResponse.ALREADY_LOGGED, self.active_sessions[login])

        session_id = self.session_counter
        self.session_counter += 1
        self.active_sessions[login] = session_id
        return OperationResponse(OperationResponse.SUCCEED, session_id)

    def logout(self, login: str, active_session: int) -> OperationResponse:
        if login not in self.active_sessions:
            return OperationResponse(OperationResponse.NOT_LOGGED)

        if self.active_sessions[login] != active_session:
            return OperationResponse(OperationResponse.INCORRECT_SESSION)

        del self.active_sessions[login]
        return OperationResponse(OperationResponse.SUCCEED)