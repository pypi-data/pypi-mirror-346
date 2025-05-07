# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Audit-Logs is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

import pytest
from flask import g
from invenio_access.permissions import system_identity, system_user_id
from invenio_records_resources.services.errors import PermissionDeniedError

from invenio_audit_logs.proxies import current_audit_logs_service


@pytest.fixture
def service(appctx):
    """Fixture for the current service."""
    return current_audit_logs_service


@pytest.mark.skip("Not certain of what is the permission checking, TODO")
def test_audit_log_create_identity_match(app, db, service, resource_data, current_user):
    """Should succeed when identity matches g.identity."""

    with app.test_request_context():
        g.identity = current_user.identity  # Set context identity
        result = service.create(
            identity=current_user.identity,  # Same identity
            data=resource_data,
        )

        result = service.read(
            identity=system_identity,
            id_=result.id,
        )

        assert result["action"] == "draft.create"
        assert result["resource"]["id"] == "abcd-1234"
        assert result["resource"]["type"] == "record"
        assert result["user"]["name"] == "User"
        assert result["user"]["id"] == "1"


def test_audit_log_create_identity_mismatch(
    app, db, service, resource_data, current_user, authenticated_identity
):
    """Should fail when identity != g.identity."""
    with app.test_request_context():
        g.identity = current_user.identity  # Set context identity

        with pytest.raises(PermissionDeniedError):
            service.create(
                identity=authenticated_identity,  # Different identity
                data=resource_data,
            )


def test_audit_log_create_system_identity(app, db, service, resource_data):
    """Should succeed when identity is system."""
    with app.test_request_context():
        result = service.create(
            identity=system_identity,  # System
            data=resource_data,
        )

        result = service.read(
            identity=system_identity,
            id_=result.id,
        )
        assert result["action"] == "draft.create"
        assert result["resource"]["id"] == "abcd-1234"
        assert result["resource"]["type"] == "record"
        assert result["user"]["id"] == system_user_id
