
from enum import IntEnum

ROOT_DB_PATH = "."
ROOT_CSV_PATH = "."

JWT_SECRET = "kakao"
AUTH_ALGORITHM = 'HS256'


class ResponseCode(IntEnum):
    AUTH_ERROR = 401
    RESPONSE_ERROR = 403


class ExitCode(IntEnum):
    SUCCEEDED = 0
    COMMAND_IS_WRONG = 1