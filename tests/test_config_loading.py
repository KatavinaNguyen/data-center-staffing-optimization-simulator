import pytest
import yaml
import argparse
from pathlib import Path
from unittest import mock
from src.config_loader import load_config, parse_args

def test_load_valid_config(tmp_path):
    sample_yaml = """
    incident_interval: 5
    staffing:
      L1: 3
      L2: 2
      L3: 1
    handling_time:
      L1: 10
      L2: 15
      L3: 20
    """
    config_file = tmp_path / "test_config.yaml"
    config_file.write_text(sample_yaml)

    config = load_config(str(config_file))
    assert config["incident_interval"] == 5
    assert config["staffing"]["L2"] == 2
    assert config["handling_time"]["L3"] == 20

def test_load_invalid_yaml(tmp_path):
    bad_yaml = """
    incident_interval: [5, 10
    """
    config_file = tmp_path / "bad_config.yaml"
    config_file.write_text(bad_yaml)

    with pytest.raises(yaml.YAMLError):
        load_config(str(config_file))

def test_parse_args_default(monkeypatch):
    monkeypatch.setattr("sys.argv", ["program"])
    args = parse_args()
    assert args.config == "config.yaml"

def test_parse_args_custom():
    test_args = ["program", "--config", "custom_config.yaml"]
    with mock.patch("sys.argv", test_args):
        args = parse_args()
        assert args.config == "custom_config.yaml"
