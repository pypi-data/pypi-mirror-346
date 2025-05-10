from typing import Type

import pytest

from clipboard_processor.cli import PLUGINS
from clipboard_processor.plugins import Plugin, AwsAccountIdPlugin


@pytest.mark.parametrize('plugin', PLUGINS)
def test_examples_are_present(plugin: Type[Plugin]):
    assert plugin.example_input() is not None


@pytest.mark.parametrize('plugin', PLUGINS)
@pytest.mark.full_installation
def test_smoke_plugin_parses_example(plugin: Type[Plugin]):
    assert plugin.example_input() is not None

    if plugin is AwsAccountIdPlugin:
        pytest.skip('AwsAccountIdPlugin requires a config file to be present')

    plugin_instance = plugin()
    result = plugin_instance.process(plugin.example_input())
    assert result is not None
    assert isinstance(result, list)
    assert len(result) > 0
