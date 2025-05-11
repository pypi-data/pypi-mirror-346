from typing import Any

from aiomexc.methods import MexcMethod
from aiomexc.types import MexcType


class MexcClientError(Exception):
    """
    Base exception for all mexc client errors.
    """


class DetailedMexcClientError(MexcClientError):
    """
    Base exception for all mexc client errors with a detailed message.
    """

    def __init__(self, message: str):
        self.message = message

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.message})"


class MexcAPIError(DetailedMexcClientError):
    """
    Base exception for all mexc API errors.
    """

    label: str = "Mexc server says"

    def __init__(
        self,
        method: MexcMethod[MexcType],
        message: str,
    ) -> None:
        super().__init__(message=message)
        self.method = method

    def __str__(self) -> str:
        original_message = super().__str__()
        return f"{self.label} - {original_message}"


class MexcBadRequest(MexcAPIError):
    """
    Exception raised when request is malformed.
    """


class MexcNotFound(MexcAPIError):
    """
    Exception raised when order not found.
    """


class MexcApiKeyInvalid(MexcAPIError):
    """
    Exception raised when API key is invalid.
    """


class MexcApiKeyMissing(MexcAPIError):
    """
    Exception raised when API key is missing.
    """


class MexcApiIpNotAllowed(MexcAPIError):
    """
    Exception raised when API key is not allowed to access the IP.
    """


class MexcApiInvalidListenKey(MexcAPIError):
    """
    Exception raised when listen key is invalid.
    """


class MexcApiSignatureInvalid(MexcAPIError):
    """
    Exception raised when signature is invalid.
    """


class MexcApiOpenOrdersTooMany(MexcAPIError):
    """
    Exception raised when open orders are too many.
    """


class MexcApiInsufficientRights(MexcAPIError):
    """
    Exception raised when user has insufficient rights.
    """


class MexcApiRateLimitExceeded(MexcAPIError):
    """
    Exception raised when rate limit is exceeded.
    """


class MexcApiRequireKyc(MexcAPIError):
    """
    Exception raised when user requires KYC.
    """


class MexcApiOversold(MexcAPIError):
    """
    Exception raised when order is oversold.
    """


class MexcApiInsufficientBalance(MexcAPIError):
    """
    Exception raised when user has insufficient balance.
    """


class ClientDecodeError(MexcClientError):
    """
    Exception raised when client can't decode response. (Malformed response, etc.)
    """

    def __init__(self, message: str, original: Exception, data: Any) -> None:
        self.message = message
        self.original = original
        self.data = data

    def __str__(self) -> str:
        original_type = type(self.original)
        return (
            f"{self.message}\n"
            f"Caused from error: "
            f"{original_type.__module__}.{original_type.__name__}: {self.original}\n"
            f"Content: {self.data}"
        )


class MexcWsStreamsLimit(MexcClientError):
    """
    Exception raised when too many streams are subscribed.
    """


class MexcWsNoStreamsProvided(MexcClientError):
    """
    Exception raised when no streams are provided.
    """


class MexcWsNoCredentialsProvided(MexcClientError):
    """
    Exception raised when no credentials are provided.
    """


class MexcWsInvalidStream(MexcClientError):
    """
    Exception raised when an invalid stream is provided.
    """

    def __init__(self, stream: str):
        self.stream = stream

    def __str__(self) -> str:
        return f"Invalid stream: {self.stream}"


class MexcWsPrivateStream(MexcClientError):
    """
    Exception raised when a private stream is provided to a public connection.
    """

    def __init__(self, stream: str):
        self.stream = stream

    def __str__(self) -> str:
        return f"Private stream: {self.stream}"


class MexcWsConnectionClosed(MexcClientError):
    """
    Exception raised when the connection is closed.
    """

    def __str__(self) -> str:
        return "Connection closed"


class MexcWsConnectionError(MexcClientError):
    """
    Exception raised when the connection is not established.
    """

    def __str__(self) -> str:
        return "Connection error"


class MexcWsConnectionNotEstablished(MexcClientError):
    """
    Exception raised when the connection is not established.
    """

    def __str__(self) -> str:
        return "Connection not established"
