import pytest
from semverfastapi.core import Version

class DescribeVersion:
    def it_parses_major_minor(self):
        v = Version("1.0")
        assert v.major == 1
        assert v.minor == 0

    def it_parses_single_digit_as_major(self):
        v = Version("2")
        assert v.major == 2
        assert v.minor == 0

    def it_handles_none_input(self):
        v = Version(None)
        assert not v
        assert v.major is None
        assert v.minor is None

    def it_defaults_to_zeros_for_invalid_strings(self):
        v = Version("invalid")
        assert v.major == 0
        assert v.minor == 0

    def it_compares_versions_correctly(self):
        v1 = Version("1.0")
        v2 = Version("1.1")
        v3 = Version("2.0")

        assert v1 < v2
        assert v2 > v1
        assert v3 > v2
        assert v1 <= v1
        assert v1 >= v1

    def it_handles_comparison_with_none(self):
        v1 = Version("1.0")
        v_none = Version(None)

        # Comparison with None usually returns False in the implementation
        assert not (v1 > v_none)
        assert not (v1 < v_none)
