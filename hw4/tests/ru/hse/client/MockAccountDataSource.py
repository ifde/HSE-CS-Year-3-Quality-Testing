from ru.hse.IAccountDataSource import IAccountDataSource
from ru.hse.OperationResponse import OperationResponse


class MockAccountDataSource(IAccountDataSource):
    def __init__(self):
        self.balances = {}
        self.active_sessions = {}

    def withdraw(self, login: str, session: int, delta: float) -> OperationResponse:
        if login not in self.active_sessions:
            return OperationResponse(OperationResponse.NOT_LOGGED)

        if self.active_sessions[login] != session:
            return OperationResponse(OperationResponse.INCORRECT_SESSION)

        if login not in self.balances:
            self.balances[login] = 0.0

        current_balance = self.balances[login]

        if current_balance < delta:
            return OperationResponse(OperationResponse.NO_MONEY, current_balance)

        new_balance = current_balance - delta
        self.balances[login] = new_balance

        return OperationResponse(OperationResponse.SUCCEED, new_balance)

    def deposit(self, login: str, session: int, delta: float) -> OperationResponse:
        if login not in self.active_sessions:
            return OperationResponse(OperationResponse.NOT_LOGGED)

        if self.active_sessions[login] != session:
            return OperationResponse(OperationResponse.INCORRECT_SESSION)

        if login not in self.balances:
            self.balances[login] = 0.0

        new_balance = self.balances[login] + delta
        self.balances[login] = new_balance

        return OperationResponse(OperationResponse.SUCCEED, new_balance)

    def get_balance(self, login: str, session: int) -> OperationResponse:
        if login not in self.active_sessions:
            return OperationResponse(OperationResponse.NOT_LOGGED)

        if self.active_sessions[login] != session:
            return OperationResponse(OperationResponse.INCORRECT_SESSION)

        if login not in self.balances:
            self.balances[login] = 0.0

        return OperationResponse(OperationResponse.SUCCEED, self.balances[login])
