# Import the necessary modules and classes for testing
from pathlib import Path

import astropy.units as u
import pytest
import yaml
from calibpipe.database.connections import CalibPipeDatabase
from calibpipe.database.interfaces import TableHandler
from calibpipe.utils.observatory import (
    Observatory,
)
from traitlets.config import Config


# Fixture to provide a database connection
@pytest.fixture()
def test_config():
    # Setup and connect to the test database
    config_path = Path(__file__).parent.joinpath(
        "../../../../../docs/source/examples/utils/configuration/"
    )
    with open(config_path.joinpath("upload_observatory_data_db.yaml")) as yaml_file:
        config_data = yaml.safe_load(yaml_file)
    config_data = config_data["UploadObservatoryData"]

    with open(config_path.joinpath("db_config.yaml")) as yaml_file:
        config_data |= yaml.safe_load(yaml_file)
    return config_data


@pytest.fixture()
def test_container(test_config):
    return Observatory(config=Config(test_config["observatories"][0])).containers[0]


# Test cases for TableHandler class and other functions in the module
class TestTableHandler:
    # Test get_database_table_insertion method
    @pytest.mark.db()
    def test_get_database_table_insertion(self, test_container):
        # Prepare a mock container and call the method
        table, kwargs = TableHandler.get_database_table_insertion(test_container)

        # Assert that the table and kwargs are not None
        assert table is not None
        assert kwargs is not None

    # Test read_table_from_database method
    @pytest.mark.db()
    def test_read_table_from_database(self, test_container, test_config):
        TableHandler.prepare_db_tables(
            [
                test_container,
            ],
            test_config["database_configuration"],
        )
        condition = "c.elevation == 3000"
        with CalibPipeDatabase(**test_config["database_configuration"]) as connection:
            qtable = TableHandler.read_table_from_database(
                type(test_container), connection, condition
            )

        # Assert that qtable is not None and has the expected columns
        assert qtable is not None
        assert "elevation" in qtable.colnames
        assert qtable["elevation"].unit == u.m
