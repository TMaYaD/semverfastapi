from semverfastapi.decorators import available

class DescribeAvailableDecorator:
    def it_attaches_all_version_metadata(self):
        @available(introduced="1.0", deprecated="1.5", removed="2.0")
        def my_endpoint():
            pass

        assert my_endpoint._api_version_intro == "1.0"
        assert my_endpoint._api_version_depr == "1.5"
        assert my_endpoint._api_version_rem == "2.0"

    def it_attaches_only_introduced_metadata_by_default(self):
        @available(introduced="1.0")
        def my_endpoint():
            pass

        assert my_endpoint._api_version_intro == "1.0"
        assert my_endpoint._api_version_depr is None
        assert my_endpoint._api_version_rem is None
