import pytest
import requests_mock
import json
from typing import Any
from ducopy.rest.client import APIClient
from ducopy.rest.models import NodeInfo, ConfigNodeResponse, ActionsResponse, NodesInfoResponse, ActionsChangeResponse

BASE_URL = "http://localhost:5000"


def load_mock_data(filename: str) -> dict[str, Any]:
    """Helper to load JSON mock data from test_data directory."""
    with open(f"tests/test_data/{filename}") as f:
        return json.load(f)


def mock_info_endpoint(mock_requests: requests_mock.Mocker) -> None:
    """Mock the /info endpoint required for API key generation."""
    mock_data = {
        "General": {
            "Lan": {"Mac": {"Val": "00:00:00:00:00:00"}},
            "Board": {"SerialBoardBox": {"Val": "MOCKSERIAL123456"}, "Time": {"Val": 1730471603}},
        }
    }
    mock_requests.get(f"{BASE_URL}/info", json=mock_data)


@pytest.fixture
def client() -> APIClient:
    return APIClient(base_url=BASE_URL)


@pytest.fixture
def mock_requests() -> Any:  # noqa: ANN401
    with requests_mock.Mocker() as m:
        yield m


def test_get_api_info(client: APIClient, mock_requests: requests_mock.Mocker) -> None:
    mock_info_endpoint(mock_requests)
    mock_data = load_mock_data("api_info.json")
    mock_requests.get(f"{BASE_URL}/api", json=mock_data)

    response = client.get_api_info()
    assert response == mock_data


def test_get_nodes(client: APIClient, mock_requests: requests_mock.Mocker) -> None:
    mock_info_endpoint(mock_requests)
    mock_data = load_mock_data("nodes.json")
    mock_requests.get(f"{BASE_URL}/info/nodes", json=mock_data)

    nodes_response = NodesInfoResponse(**mock_data)  # Instantiate NodesInfoResponse directly with data
    assert isinstance(nodes_response, NodesInfoResponse)
    assert len(nodes_response.Nodes) == len(mock_data["Nodes"])


def test_post_action_node(client: APIClient, mock_requests: requests_mock.Mocker) -> None:
    mock_info_endpoint(mock_requests)
    mock_data = load_mock_data("set_actions_node_1.json")
    mock_requests.post(f"{BASE_URL}/action/nodes/1", json=mock_data)

    action_response = ActionsChangeResponse(**mock_data)  # Instantiate ActionsChangeResponse directly with data
    assert isinstance(action_response, ActionsChangeResponse)
    assert action_response.Code == mock_data["Code"]
    assert action_response.Result == mock_data["Result"]


def test_get_node_info(client: APIClient, mock_requests: requests_mock.Mocker) -> None:
    mock_info_endpoint(mock_requests)
    mock_data = load_mock_data("node_1.json")
    mock_requests.get(f"{BASE_URL}/info/nodes/1", json=mock_data)

    node_info = NodeInfo(**mock_data)  # Instantiate NodeInfo directly with data
    assert isinstance(node_info, NodeInfo)
    assert node_info.Node == mock_data["Node"]


def test_get_config_node(client: APIClient, mock_requests: requests_mock.Mocker) -> None:
    mock_info_endpoint(mock_requests)
    mock_data = load_mock_data("config_node_1.json")
    mock_requests.get(f"{BASE_URL}/config/nodes/1", json=mock_data)

    config_response = ConfigNodeResponse(**mock_data)  # Instantiate ConfigNodeResponse directly with data
    assert isinstance(config_response, ConfigNodeResponse)
    assert config_response.Node == mock_data["Node"]


# Uncomment this test if needed
# def test_get_firmware(client, mock_requests):
#     mock_info_endpoint(mock_requests)
#     mock_data = load_mock_data("firmware.json")
#     mock_requests.get(f"{BASE_URL}/firmware", json=mock_data)

#     firmware_response = FirmwareResponse(**mock_data)  # Instantiate FirmwareResponse directly with data
#     assert isinstance(firmware_response, FirmwareResponse)


def test_get_actions_node(client: APIClient, mock_requests: requests_mock.Mocker) -> None:
    mock_info_endpoint(mock_requests)
    mock_data = load_mock_data("actions_node_1.json")
    mock_requests.get(f"{BASE_URL}/action/nodes/1", json=mock_data)

    actions_response = ActionsResponse(**mock_data)  # Instantiate ActionsResponse directly with data
    assert isinstance(actions_response, ActionsResponse)
    assert len(actions_response.Actions) == len(mock_data["Actions"])


def test_get_logs(client: APIClient, mock_requests: requests_mock.Mocker) -> None:
    mock_info_endpoint(mock_requests)
    mock_data = load_mock_data("logs.json")
    mock_requests.get(f"{BASE_URL}/log/api", json=mock_data)

    logs_response = client.get_logs()
    assert logs_response == mock_data
