"""
Test configuration and fixtures for FastAPI tests.
"""
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to a known state before each test."""
    from app import activities
    
    original_state = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Competitive soccer practice and seasonal matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["noah@mergington.edu", "liam@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Swim training and water safety for all levels",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["ava@mergington.edu", "mia@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore drawing, painting, and mixed media art projects",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["isabella@mergington.edu", "charlotte@mergington.edu"]
        },
        "Drama Workshop": {
            "description": "Acting, improvisation, and stage production practice",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["lucas@mergington.edu", "amelia@mergington.edu"]
        },
        "Science Club": {
            "description": "Hands-on experiments and STEM explorations",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["harper@mergington.edu", "eid@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop critical thinking through competitive debate practice",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["jacob@mergington.edu", "noah@mergington.edu"]
        }
    }
    
    activities.clear()
    for name, details in original_state.items():
        activities[name] = {
            "description": details["description"],
            "schedule": details["schedule"],
            "max_participants": details["max_participants"],
            "participants": details["participants"].copy()
        }
    
    yield
    
    activities.clear()
    for name, details in original_state.items():
        activities[name] = {
            "description": details["description"],
            "schedule": details["schedule"],
            "max_participants": details["max_participants"],
            "participants": details["participants"].copy()
        }
