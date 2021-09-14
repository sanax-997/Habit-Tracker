import pytest
from HabitManagement import create_app
from flask import url_for


def test_home():
    """
    Checks if the response of the "/" page is valid
    """
    app = create_app()
    client = app.test_client()
    url = '/'
    response = client.get(url)

    # Check for response 200 (Successfull request)
    assert response.status_code == 200

    # Checks if the jpg is in html return
    assert b'habit_tracker.jpg' in response.get_data()

    # Check if content returned is html
    #assert response.content_type == "home.html"

    # assert response.get_data() == {
    # {'static', 'habit_tracker.jpg'}}
