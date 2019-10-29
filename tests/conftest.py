import pytest


@pytest.fixture(name='yaml')
def yaml_module():
    try:
        import yaml
        return yaml
    except ImportError:
        pass
    pytest.skip("Module 'PyYAML' is required")
