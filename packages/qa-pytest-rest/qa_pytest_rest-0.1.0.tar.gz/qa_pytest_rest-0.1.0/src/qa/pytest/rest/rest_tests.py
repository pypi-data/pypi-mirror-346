# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from typing import Any, Generic, TypeVar, override

from qa.pytest.rest.rest_configuration import RestConfiguration
from qa.pytest.rest.rest_steps import RestSteps
from qa.pytest.commons.abstract_tests_base import AbstractTestsBase
import requests

# NOTE: python limitation; we cannot declare it such as:
# class SeleniumTests[TSteps:SeleniumSteps[TConfiguration], TConfiguration: AbstractConfiguration](AbstractTestsBase[TSteps, TConfiguration]):
TConfiguration = TypeVar("TConfiguration", bound=RestConfiguration)
TSteps = TypeVar("TSteps", bound=RestSteps[Any])


class RestTests(
        Generic[TSteps, TConfiguration],
        AbstractTestsBase[TSteps, TConfiguration]):
    _rest_session: requests.Session  # not thread safe

    @override
    def setup_method(self):
        super().setup_method()
        self._rest_session = requests.Session()

    @override
    def teardown_method(self):
        try:
            self._rest_session.close()
        finally:
            super().teardown_method()
