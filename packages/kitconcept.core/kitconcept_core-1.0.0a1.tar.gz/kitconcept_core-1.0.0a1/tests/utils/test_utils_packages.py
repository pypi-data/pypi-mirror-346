from kitconcept.core.utils import packages as pkg_utils


class TestUtilsPackages:
    def test_package_version(self):
        from kitconcept.core import __version__

        result = pkg_utils.package_version("kitconcept.core")
        assert result == __version__
