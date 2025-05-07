# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it
# and/or modify it under the terms of the MIT License; see LICENSE
# file for more details.

"""Jobs for invenio-campusonline."""

from invenio_jobs.jobs import JobType

from .tasks import import_theses_from_campusonline


class ImportThesesFromCampusonlineJob(JobType):
    """Import theses from campusonline."""

    id = "import_theses_from_campusonline"
    title = "Import theses from campusonline"
    description = "Import theses from campusonline"

    task = import_theses_from_campusonline
