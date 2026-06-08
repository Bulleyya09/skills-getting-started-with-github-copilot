"""
Tests for Mergington High School Activities API.
"""


class TestRoot:
    """Tests for the root endpoint."""

    def test_root_redirect(self, client):
        """Test that root redirects to static/index.html."""
        # Arrange
        url = "/"

        # Act
        response = client.get(url, follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]


class TestGetActivities:
    """Tests for the GET /activities endpoint."""

    def test_get_all_activities(self, client):
        """Test retrieving all activities."""
        # Arrange
        url = "/activities"

        # Act
        response = client.get(url)
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert len(data) == 9
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data

    def test_activity_structure(self, client):
        """Test that each activity has required fields."""
        # Arrange
        url = "/activities"

        # Act
        response = client.get(url)
        data = response.json()

        # Assert
        for activity_name, details in data.items():
            assert "description" in details
            assert "schedule" in details
            assert "max_participants" in details
            assert "participants" in details
            assert isinstance(details["participants"], list)
            assert isinstance(details["max_participants"], int)

    def test_chess_club_has_participants(self, client):
        """Test that Chess Club has initial participants."""
        # Arrange
        url = "/activities"

        # Act
        response = client.get(url)
        chess = response.json()["Chess Club"]

        # Assert
        assert len(chess["participants"]) == 2
        assert "michael@mergington.edu" in chess["participants"]
        assert "daniel@mergington.edu" in chess["participants"]


class TestSignupForActivity:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client):
        """Test successful signup for an activity."""
        # Arrange
        url = "/activities/Chess%20Club/signup"
        params = {"email": "newstudent@mergington.edu"}

        # Act
        response = client.post(url, params=params)

        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]

    def test_signup_adds_participant(self, client):
        """Test that signup actually adds the participant."""
        # Arrange
        url = "/activities/Programming%20Class/signup"
        params = {"email": "test@mergington.edu"}

        # Act
        client.post(url, params=params)
        response = client.get("/activities")

        # Assert
        assert "test@mergington.edu" in response.json()["Programming Class"]["participants"]

    def test_signup_nonexistent_activity(self, client):
        """Test signup fails for non-existent activity."""
        # Arrange
        url = "/activities/Fake%20Club/signup"
        params = {"email": "student@mergington.edu"}

        # Act
        response = client.post(url, params=params)

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_fails(self, client):
        """Test that duplicate signup is rejected."""
        # Arrange
        url = "/activities/Chess%20Club/signup"
        params = {"email": "duplicate@mergington.edu"}

        # Act
        response1 = client.post(url, params=params)
        response2 = client.post(url, params=params)

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 400
        assert "already signed up" in response2.json()["detail"].lower()

    def test_signup_multiple_activities(self, client):
        """Test that a student can signup for multiple activities."""
        # Arrange
        first_url = "/activities/Chess%20Club/signup"
        second_url = "/activities/Programming%20Class/signup"
        email = "multi@mergington.edu"

        # Act
        client.post(first_url, params={"email": email})
        client.post(second_url, params={"email": email})
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert email in data["Chess Club"]["participants"]
        assert email in data["Programming Class"]["participants"]


class TestUnregisterParticipant:
    """Tests for the DELETE /activities/{activity_name}/participants endpoint."""

    def test_unregister_success(self, client):
        """Test successful unregistration of a participant."""
        # Arrange
        url = "/activities/Chess%20Club/participants"
        params = {"email": "michael@mergington.edu"}

        # Act
        response = client.delete(url, params=params)

        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]

    def test_unregister_removes_participant(self, client):
        """Test that unregister actually removes the participant."""
        # Arrange
        url = "/activities/Chess%20Club/participants"
        params = {"email": "daniel@mergington.edu"}

        # Act
        client.delete(url, params=params)
        response = client.get("/activities")

        # Assert
        assert "daniel@mergington.edu" not in response.json()["Chess Club"]["participants"]

    def test_unregister_nonexistent_activity(self, client):
        """Test unregister fails for non-existent activity."""
        # Arrange
        url = "/activities/Fake%20Club/participants"
        params = {"email": "student@mergington.edu"}

        # Act
        response = client.delete(url, params=params)

        # Assert
        assert response.status_code == 404

    def test_unregister_not_registered(self, client):
        """Test unregister fails if student is not registered."""
        # Arrange
        url = "/activities/Chess%20Club/participants"
        params = {"email": "notregistered@mergington.edu"}

        # Act
        response = client.delete(url, params=params)

        # Assert
        assert response.status_code == 404
        assert "not registered" in response.json()["detail"].lower()

    def test_unregister_then_signup_again(self, client):
        """Test that a student can re-signup after unregistering."""
        # Arrange
        signup_url = "/activities/Programming%20Class/signup"
        unregister_url = "/activities/Programming%20Class/participants"
        email = "reregister@mergington.edu"

        # Act
        client.post(signup_url, params={"email": email})
        client.delete(unregister_url, params={"email": email})
        response = client.post(signup_url, params={"email": email})

        # Assert
        assert response.status_code == 200


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_activity_name_with_spaces(self, client):
        """Test that activity names with spaces are handled correctly."""
        # Arrange
        url = "/activities/Programming%20Class/signup"
        params = {"email": "test@mergington.edu"}

        # Act
        response = client.post(url, params=params)

        # Assert
        assert response.status_code == 200

    def test_email_with_special_chars(self, client):
        """Test that emails with special characters work."""
        # Arrange
        url = "/activities/Chess%20Club/signup"
        email = "test+special@mergington.edu"

        # Act
        response = client.post(url, params={"email": email})

        # Assert
        assert response.status_code == 200

    def test_participant_count_accuracy(self, client):
        """Test that participant counts remain accurate after operations."""
        # Arrange
        get_url = "/activities"
        signup_url = "/activities/Gym%20Class/signup"
        unregister_url = "/activities/Gym%20Class/participants"
        params = {"email": "count@mergington.edu"}

        # Act
        response = client.get(get_url)
        initial_count = len(response.json()["Gym Class"]["participants"])

        client.post(signup_url, params=params)
        response = client.get(get_url)
        after_signup_count = len(response.json()["Gym Class"]["participants"])

        client.delete(unregister_url, params=params)
        response = client.get(get_url)
        final_count = len(response.json()["Gym Class"]["participants"])

        # Assert
        assert after_signup_count == initial_count + 1
        assert final_count == initial_count
