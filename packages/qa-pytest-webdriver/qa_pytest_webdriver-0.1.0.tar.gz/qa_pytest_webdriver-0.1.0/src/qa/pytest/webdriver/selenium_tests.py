# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from typing import Any, Generic, TypeVar, override
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

from qa.pytest.webdriver.selenium_configuration import SeleniumConfiguration
from qa.pytest.webdriver.selenium_steps import SeleniumSteps
from qa.pytest.commons.abstract_tests_base import AbstractTestsBase

# NOTE: python limitation; we cannot declare it such as:
# class SeleniumTests[TSteps:SeleniumSteps[TConfiguration], TConfiguration: AbstractConfiguration](AbstractTestsBase[TSteps, TConfiguration]):
TConfiguration = TypeVar("TConfiguration", bound=SeleniumConfiguration)
TSteps = TypeVar("TSteps", bound=SeleniumSteps[Any])


class SeleniumTests(
        Generic[TSteps, TConfiguration],
        AbstractTestsBase[TSteps, TConfiguration]):
    _web_driver: WebDriver  # not thread safe

    @override
    def setup_method(self):
        super().setup_method()

        options = Options()
        options.add_argument("--start-maximized")  # type: ignore
        self._web_driver = Chrome(
            options,
            self._configuration.web_driver_service)

    @override
    def teardown_method(self):
        try:
            self._web_driver.quit()
        finally:
            super().teardown_method()
