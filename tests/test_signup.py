import src.app as app_module


def test_signup_adds_new_participant(
    client,
    valid_activity_name,
    new_participant_email,
):
    # Arrange
    endpoint = f"/activities/{valid_activity_name}/signup"
    params = {"email": new_participant_email}

    # Act
    response = client.post(endpoint, params=params)

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {new_participant_email} for {valid_activity_name}"
    }
    assert new_participant_email in app_module.activities[valid_activity_name]["participants"]


def test_signup_rejects_duplicate_participant(
    client,
    valid_activity_name,
    existing_participant_email,
):
    # Arrange
    endpoint = f"/activities/{valid_activity_name}/signup"
    params = {"email": existing_participant_email}

    # Act
    response = client.post(endpoint, params=params)

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_rejects_unknown_activity(client, invalid_activity_name, new_participant_email):
    # Arrange
    endpoint = f"/activities/{invalid_activity_name}/signup"
    params = {"email": new_participant_email}

    # Act
    response = client.post(endpoint, params=params)

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
