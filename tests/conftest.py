import pytest

from nano_lib_py.blocks import Block

from tests.data import BLOCKS


@pytest.fixture(autouse=True)
def low_pow_difficulty(monkeypatch):
    # Use a far lower default difficulty for unit tests
    TEST_DIFFICULTY = "8345468f269004a2"
    monkeypatch.setattr("nano_lib_py.blocks.WORK_DIFFICULTY", TEST_DIFFICULTY)
    monkeypatch.setattr("nano_lib_py.work.WORK_DIFFICULTY", TEST_DIFFICULTY)
    monkeypatch.setattr("nano_lib_py.WORK_DIFFICULTY", TEST_DIFFICULTY)


@pytest.fixture(scope="function")
def block_factory():
    def _create_func(name):
        return Block.from_dict(BLOCKS[name]["data"])

    return _create_func
