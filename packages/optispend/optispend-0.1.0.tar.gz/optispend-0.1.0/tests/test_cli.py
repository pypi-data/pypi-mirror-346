# tests/test_cli.py

import sys
import pytest
from unittest import mock
from optispend import cli

@mock.patch("optispend.cli.boto3.Session")
def test_cli_optimize_mode(mock_boto_session, capsys):
    # Mock AWS CE client and usage data
    mock_client = mock.Mock()
    mock_client.get_cost_and_usage.return_value = {
        "ResultsByTime": [
            {
                "Groups": [{"Metrics": {"UnblendedCost": {"Amount": "1.0"}}}],
            }
        ]
    }

    mock_boto_session.return_value.client.return_value = mock_client

    test_args = ["optispend", "--optimize"]
    with mock.patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):  # Because CLI calls exit()
            cli.main()

    captured = capsys.readouterr()
    assert "Optimizing commitment recommendations" in captured.out
    assert "Projected Monthly Cost" in captured.out


@mock.patch("optispend.cli.boto3.Session")
def test_cli_manual_mode_default_commitment(mock_boto_session, capsys):
    mock_client = mock.Mock()
    mock_client.get_cost_and_usage.return_value = {
        "ResultsByTime": [
            {
                "Groups": [{"Metrics": {"UnblendedCost": {"Amount": "2.0"}}}],
            }
        ]
    }
    mock_boto_session.return_value.client.return_value = mock_client

    test_args = ["optispend"]
    with mock.patch.object(sys, "argv", test_args):
        cli.main()

    captured = capsys.readouterr()
    assert "Suggested Commitment" in captured.out
    assert "$" in captured.out
