import pytest
from dash.testing.application_runners import import_app

@pytest.fixture
def dash_app(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)
    return dash_duo

def test_header_present(dash_app):
    """Test that the header is visible on the page."""
    dash_app.wait_for_element("h1", timeout=10)
    header = dash_app.find_element("h1")
    assert header is not None
    assert "Pink Morsel" in header.text

def test_chart_present(dash_app):
    """Test that the line chart visualisation is present."""
    dash_app.wait_for_element("#sales-chart", timeout=10)
    chart = dash_app.find_element("#sales-chart")
    assert chart is not None

def test_region_picker_present(dash_app):
    """Test that the region radio buttons are present."""
    dash_app.wait_for_element("#region-filter", timeout=10)
    region_picker = dash_app.find_element("#region-filter")
    assert region_picker is not None