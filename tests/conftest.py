import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def client():
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities_state():
    snapshot = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(snapshot)


@pytest.fixture
def valid_activity_name():
    return "Chess Club"


@pytest.fixture
def invalid_activity_name():
    return "Nonexistent Activity"


@pytest.fixture
def existing_participant_email():
    return "michael@mergington.edu"


@pytest.fixture
def new_participant_email():
    return "new.student@mergington.edu"
