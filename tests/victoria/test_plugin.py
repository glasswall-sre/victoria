import pytest

import victoria.plugin


@pytest.fixture()
def mock_plugin_loading(monkeypatch):
    """Mock python functions used in plugin loading:
    - pkgutil.iter_modules
    - importlib.util.find_spec
    - importlib.util.module_from_spec
    - FileLoader.exec_module()
    """

    import pkgutil
    import importlib.util

    class MockLoader:
        def exec_module(self, module):
            pass

    class MockPluginModule:
        def __init__(self, plugin_obj):
            self.plugin = plugin_obj

    def mock_iter_modules():
        for pkg in ["test_a", "test_b", "victoria_plugin"]:
            yield (None, pkg, True)

    monkeypatch.setattr(pkgutil, "iter_modules", mock_iter_modules)

    def mock_find_spec(module_name):
        data = {
            "victoria_plugin":
            importlib.machinery.ModuleSpec(name="victoria_plugin",
                                           loader=MockLoader()),
            "victoria_nonexistent_plugin_obj":
            importlib.machinery.ModuleSpec(
                name="victoria_nonexistent_plugin_obj", loader=MockLoader()),
            "victoria_wrongtype_plugin_obj":
            importlib.machinery.ModuleSpec(
                name="victoria_wrongtype_plugin_obj", loader=MockLoader()),
            "victoria_nonexistent_spec":
            None
        }
        return data[module_name]

    monkeypatch.setattr(importlib.util, "find_spec", mock_find_spec)

    def mock_module_from_spec(spec):
        data = {
            "victoria_plugin":
            MockPluginModule(victoria.plugin.Plugin("plugin", None)),
            "victoria_nonexistent_plugin_obj":
            object(),
            "victoria_wrongtype_plugin_obj":
            MockPluginModule("")
        }
        return data[spec.name]

    monkeypatch.setattr(importlib.util, "module_from_spec",
                        mock_module_from_spec)


@pytest.mark.parametrize("a,b,expected",
                         [(victoria.plugin.Plugin("plugin", None),
                           victoria.plugin.Plugin("plugin", None), True),
                          (victoria.plugin.Plugin("plugin", None), "", False)])
def test_plugin_eq(a, b, expected):
    result = a == b
    assert result == expected


def test_ls(mock_plugin_loading):
    plugins = [p for p in victoria.plugin.ls()]
    assert plugins == ["plugin"]


@pytest.mark.parametrize("plugin_name,expected",
                         [("plugin", victoria.plugin.Plugin("plugin", None)),
                          ("nonexistent_spec", None),
                          ("nonexistent_plugin_obj", None),
                          ("wrongtype_plugin_obj", None)])
def test_load(mock_plugin_loading, plugin_name, expected):
    result = victoria.plugin.load(plugin_name)
    assert result == expected


def test_load_all(mock_plugin_loading):
    result = victoria.plugin.load_all()
    assert result == [victoria.plugin.Plugin("plugin", None)]


def test_load_all_repeat(monkeypatch, mock_plugin_loading):
    import pkgutil

    def mock_iter_modules():
        for pkg in ["test_a", "test_b", "victoria_plugin", "victoria_plugin"]:
            yield (None, pkg, True)

    monkeypatch.setattr(pkgutil, "iter_modules", mock_iter_modules)

    result = victoria.plugin.load_all()
    assert result == [victoria.plugin.Plugin("plugin", None)]