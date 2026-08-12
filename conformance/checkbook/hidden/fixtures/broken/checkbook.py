"""Deliberately incomplete fixture for the hidden-suite self-test."""


class CheckbookError(Exception):
    def __init__(self, code, operation_id=None):
        super().__init__(code)
        self.code = code
        self.operation_id = operation_id


class Checkbook:
    def __init__(self, database_path):
        self.database_path = database_path

    def create_account(self, account_id, currency, opening, operation_id):
        return {
            "account_id": account_id,
            "currency": currency,
            "opening_balance_minor": opening,
            "closed_through": None,
        }
