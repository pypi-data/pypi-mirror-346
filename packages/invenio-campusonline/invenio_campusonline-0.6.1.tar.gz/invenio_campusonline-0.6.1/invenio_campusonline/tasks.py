# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2025 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it
# and/or modify it under the terms of the MIT License; see LICENSE
# file for more details.


"""Celery tasks for `invenio-campusonline`."""


from celery import shared_task
from flask import current_app
from invenio_access.permissions import system_identity

from .proxies import current_campusonline


@shared_task(ignore_result=True)
def import_theses_from_campusonline() -> None:
    """Import theses from campusonline."""
    current_app.logger.info("start importing theses from campusonline")

    import_func = current_app.config["CAMPUSONLINE_IMPORT_FUNC"]
    theses_filter = current_app.config["CAMPUSONLINE_THESES_FILTER"]

    cms_service = current_campusonline.campusonline_rest_service
    ids = cms_service.fetch_all_ids(system_identity, theses_filter)

    current_app.logger.info("%s records will be imported", len(ids))

    for cms_id in ids:
        try:
            draft = import_func(system_identity, cms_id, cms_service)

            msg = "campusonline draft.id: %s as been imported successfully"
            current_app.logger.info(msg, draft.id)
        except RuntimeError as e:
            msg = "ERROR campusonline cms_id: %s couldn't be imported because of %s"
            current_app.logger.error(msg, cms_id, str(e))
