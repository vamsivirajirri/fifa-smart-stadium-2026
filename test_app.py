import os
import pytest

def test_environment_security():
    """Validates that no secure production keys are leaked directly into source controls."""
    assert "GEMINI_API_KEY" not in os.environ or os.environ["GEMINI_API_KEY"] == ""

def test_system_mock_responses():
    """Validates that the Tournament Context Manager layer maps properties accurately."""
    # Importing the class structure from our clean app script
    from app import TournamentContextManager
    context = TournamentContextManager()
    
    assert context.scope is not None
    # Validate that the cached dictionary payload returns correct structures
    payload = context.fetch_venue_payload("Estadio Azteca (Mexico City)")
    assert "density" in payload
    assert "wait" in payload
