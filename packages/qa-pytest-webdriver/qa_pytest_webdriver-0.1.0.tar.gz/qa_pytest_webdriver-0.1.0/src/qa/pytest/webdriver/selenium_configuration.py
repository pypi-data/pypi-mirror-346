# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from functools import cached_property
from typing import final
from qa.pytest.commons.base_configuration import BaseConfiguration
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumConfiguration(BaseConfiguration):

    @cached_property
    @final
    def ui_url(self) -> str:
        return self.parser["ui"]["url"]

    @cached_property
    @final
    def web_driver_service(self) -> Service:
        # NOTE may add support for providing different services per configuration
        return Service(ChromeDriverManager().install())
