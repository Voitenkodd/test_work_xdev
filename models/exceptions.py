from enum import Enum

from fastapi import HTTPException, status


class ErrorCode(Enum):
    SERVER_ERROR = ("Server error", status.HTTP_500_INTERNAL_SERVER_ERROR)
    ITEM_NOT_FOUND = ("Item not found", status.HTTP_404_NOT_FOUND)
    UNPROCESSABLE_ENTITY = ("Content error", status.HTTP_422_UNPROCESSABLE_ENTITY)
    UNAUTHORIZED = ("Unauthorized access", status.HTTP_401_UNAUTHORIZED)
    BAD_REQUEST = ("Invalid input", status.HTTP_400_BAD_REQUEST)

    def as_http_exception(self, local_message: str = None):
        message, code = self.value
        return HTTPException(status_code=code, detail=local_message or message)
