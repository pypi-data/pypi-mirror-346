import pytest
from PIL import ImageGrab

FULL_INSTALLATION_MARKER = 'full_installation'
MINIMAL_INSTALLATION_MARKER = 'minimal_installation'
SNAPSHOT_MARKER = 'snapshot'
SUITE_FULL = 'full'
SUITE_MINIMAL = 'minimal'
SUITE_SNAPSHOT = 'snapshot'



def pytest_addoption(parser):
    parser.addoption('--suite', choices=[SUITE_FULL, SUITE_MINIMAL, SUITE_SNAPSHOT])


@pytest.fixture
def snapshot_path(request):
    def func(suffix=''):
        return request.config.rootdir.join('tests', 'snapshots', request.node.name + suffix + '.png')
    return func


def pytest_configure(config):
    config.addinivalue_line('markers', f'{FULL_INSTALLATION_MARKER}: Test requires optional dependencies')
    config.addinivalue_line('markers',
                            f'{MINIMAL_INSTALLATION_MARKER}: Test requires optional dependencies to be absent')
    config.addinivalue_line('markers', f'{SNAPSHOT_MARKER}: Visual snapshot test (requires Xvfb)')


def pytest_collection_modifyitems(config, items):
    suite = config.getoption('--suite')
    new_items = []
    for item in items:
        if FULL_INSTALLATION_MARKER in item.keywords and suite == SUITE_MINIMAL:
            continue
        if MINIMAL_INSTALLATION_MARKER in item.keywords and suite in [SUITE_FULL, SUITE_SNAPSHOT]:
            continue
        if SNAPSHOT_MARKER in item.keywords and suite in [SUITE_FULL, SUITE_MINIMAL]:
            continue
        if SNAPSHOT_MARKER not in item.keywords and suite == SUITE_SNAPSHOT:
            continue
        new_items.append(item)
    items[:] = new_items


@pytest.fixture
def take_screenshot():
    def func():
        return ImageGrab.grab()

    return func
