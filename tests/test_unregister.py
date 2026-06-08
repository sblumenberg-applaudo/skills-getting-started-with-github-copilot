import src.app as app_module


def test_unregister_removes_existing_participant(
    client,
    valid_activity_name,
    existing_participant_email,
):
    # Arrange
    endpoint = f"/activities/{valid_activity_name}/signup"
    params = {"email": existing_participant_email}

    # Act
    response = client.delete(endpoint, params=params)

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {existing_participant_email} from {valid_activity_name}"
    }
    assert (
        existing_participant_email
        not in app_module.activities[valid_activity_name]["participants"]
    )


def test_unregister_rejects_unknown_activity(client, invalid_activity_name, new_participant_email):
    # Arrange
    endpoint = f"/activities/{invalid_activity_name}/signup"
    params = {"email": new_participant_email}

    # Act
    response = client.delete(endpoint, params=params)

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_rejects_non_member(client, valid_activity_name, new_participant_email):
    # Arrange
    endpoint = f"/activities/{valid_activity_name}/signup"
    params = {"email": new_participant_email}

    # Act
    response = client.delete(endpoint, params=params)

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}


def test_signup_then_unregister_flow(client, valid_activity_name, new_participant_email):
    # Arrange
    endpoint = f"/activities/{valid_activity_name}/signup"
    params = {"email": new_participant_email}

    # Act
    signup_response = client.post(endpoint, params=params)
    unregister_response = client.delete(endpoint, params=params)

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert new_participant_email not in app_module.activities[valid_activity_name]["participants"]
