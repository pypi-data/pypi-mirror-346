import pytest

from ..smarty_streets import SmartyStreets


class MockData:
    # Mock data returned by address_lookup method
    mock_components = {"street": "1600 Penns", "city": "Cupertino", "zipcode": "95014", "state": "CA"}
    mock_metadata = {"address_data": "test_address_data"}
    mock_analysis = {"analysis_data": "test_analysis_data"}

    def __init__(self, data=None):
        if data and isinstance(data, dict):
            self.__dict__ = data
        elif data:
            self.components = data(self.mock_components)
            self.metadata = data(self.mock_metadata)
            self.analysis = data(self.mock_analysis)

    def send_lookup(self, lookup):
        assert lookup.street == "1600 Penns"
        assert lookup.state == "CA"
        lookup.result = [MockData(MockData)]

    def send(self, lookup):
        lookup.result = [MockData(self.mock_metadata)]


class TestSmartyStreets:
    @pytest.fixture
    def smarty_streets(self, monkeypatch=pytest.MonkeyPatch()):
        smarty_streets = SmartyStreets()

        # Mock the client and auto_complete_client API calls.
        monkeypatch.setattr(smarty_streets, "client", MockData())
        monkeypatch.setattr(smarty_streets, "auto_complete_client", MockData())

        return smarty_streets

    def test_address_lookup(self, smarty_streets):
        addresses = smarty_streets.address_lookup(street="1600 Penns", state="CA")

        assert addresses == [
            {
                "components": {"street": "1600 Penns", "city": "Cupertino", "zipcode": "95014", "state": "CA"},
                "metadata": {
                    "address_data": "test_address_data",
                },
                "analysis": {"analysis_data": "test_analysis_data"},
            }
        ]

    def test_auto_complete_address_lookup(self, smarty_streets):
        addresses = smarty_streets.auto_complete_address_lookup("1600 Penns")

        assert addresses == [{"address_data": "test_address_data"}]


# # TODO: def test_extract_address()
