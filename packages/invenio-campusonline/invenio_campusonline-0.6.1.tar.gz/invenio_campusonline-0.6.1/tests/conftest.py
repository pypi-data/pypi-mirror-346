# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

from collections.abc import Callable
from pathlib import Path
from xml.etree.ElementTree import Element, parse

import pytest
from _pytest.fixtures import FixtureFunctionMarker
from invenio_app.factory import create_api as _create_api


@pytest.fixture(scope="module")
def create_app(instance_path: FixtureFunctionMarker) -> Callable:
    """Application factory fixture."""
    return _create_api


@pytest.fixture
def minimal_record() -> Element:
    """Create minimal record."""
    return parse(Path(__file__).parent / "minimal_record.xml")
