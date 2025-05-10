# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from enum import Enum
from typing import Self, final
from hamcrest import is_  # type: ignore
import requests

from requests import Request, Response

from qa.pytest.rest.rest_configuration import RestConfiguration
from qa.pytest.commons.generic_steps import GenericSteps
from qa.testing.utils.logger import traced
from hamcrest.core.matcher import Matcher


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class RestSteps[TConfiguration: RestConfiguration](
    GenericSteps[TConfiguration]
):
    _rest_session: requests.Session

    @final
    def _invoke(self, request: Request) -> Response:
        return self._rest_session.send(
            self._rest_session.prepare_request(request))

    @traced
    @final
    def invoking(self, request: Request) -> Self:
        return self.eventually_assert_that(
            lambda: self._invoke(request).ok, is_(True))

    @traced
    @final
    def the_invocation(
            self, request: Request, by_rule: Matcher[Response]) -> Self:
        return self.eventually_assert_that(
            lambda: self._invoke(request),
            by_rule)
