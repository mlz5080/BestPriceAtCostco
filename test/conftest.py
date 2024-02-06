def pytest_addoption(parser):
    """Add argument parser to pytest. We can pass parameters to pytest.
    """
    parser.addoption("--online", action="store", default="false")


def pytest_generate_tests(metafunc):
    """Convert parser arguments to parameters
    """
    option_value = metafunc.config.option.online
    if 'online' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("online", [option_value=="true"])
