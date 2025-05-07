# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""The module is used to import/export from/to the CampusOnline System."""


from .ext import InvenioCampusonline
from .proxies import current_campusonline
from .services import CampusOnlineRESTService
from .types import CampusOnlineID, ThesesFilter

__version__ = "0.6.1"

__all__ = (
    "CampusOnlineID",
    "CampusOnlineRESTService",
    "InvenioCampusonline",
    "ThesesFilter",
    "__version__",
    "current_campusonline",
)
