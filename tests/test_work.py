import time
from hashlib import blake2b

import pytest
from nano_lib_py.exceptions import (InvalidDifficulty, InvalidMultiplier,
                                InvalidWork, InvalidBlockHash)
from nano_lib_py.util import dec_to_hex
from nano_lib_py.work import (derive_work_difficulty, derive_work_multiplier,
                          parse_difficulty, parse_work, get_work_value,
                          solve_work, validate_difficulty, validate_work)

VALID_BLOCK_HASH = \
    "B585D9363B8265CFD5993F30A3D6DE6B5CA5CC7879E0AFA94D13F08B713B9FFD"
VALID_WORK = "5b064dcc70b9db0a"


def test_low_difficulty_used_for_tests():
    """
    Check that a lower work difficulty is used for tests
    """
    from nano_lib_py.work import WORK_DIFFICULTY

    assert int(WORK_DIFFICULTY, 16) < int("ffffffc000000000", 16)


def test_parse_work():
    """
    Test nano_lib_py.parse_work
    """
    with pytest.raises(InvalidWork):
        # Work has to be 16 chars long
        parse_work("A"*15)

    with pytest.raises(InvalidWork):
        # Woirk has to be in hex
        parse_work("x"*16)

    # parse_work returns lowercase hex string
    assert parse_work("A"*16) == "a"*16


def test_get_work_value():
    assert get_work_value("a"*64, "f"*16) == 5108225079566541904
    assert get_work_value("a"*64, "f"*16, as_hex=True) == "46e40fa5344e2450"

    with pytest.raises(InvalidBlockHash):
        get_work_value("f"*65, "a"*16)

    with pytest.raises(InvalidWork):
        get_work_value("f"*64, "a"*17)


def test_validate_work():
    with pytest.raises(InvalidWork):
        # Invalid work
        validate_work(block_hash=VALID_BLOCK_HASH, work="e"*16)

    assert validate_work(block_hash=VALID_BLOCK_HASH, work=VALID_WORK)


def test_validate_difficulty():
    assert validate_difficulty("FFFFFFC000000000") == "ffffffc000000000"

    with pytest.raises(InvalidDifficulty):
        # Not a hex string
        validate_difficulty("GGFFFFFFFFFFFFFF")

    with pytest.raises(InvalidDifficulty):
        # Not a 16-character hex string
        validate_difficulty("A"*17)


def test_parse_difficulty():
    assert parse_difficulty("FFFFFFC000000000") == 18446743798831644672

    with pytest.raises(InvalidDifficulty):
        # Not a hex string
        parse_difficulty("GGFFFFFFFFFFFFFF")

    with pytest.raises(InvalidDifficulty):
        # Not a 16-character hex string
        parse_difficulty("A"*17)


def test_derive_work_difficulty():
    assert derive_work_difficulty(
        multiplier=0.125, base_difficulty="ffffffc000000000"
    ) == "fffffe0000000000"

    assert derive_work_difficulty(
        multiplier=2, base_difficulty="ffffffc000000000"
    ) == "ffffffe000000000"

    with pytest.raises(InvalidMultiplier):
        # Not a float
        derive_work_difficulty(multiplier="invalid")

    with pytest.raises(InvalidMultiplier):
        # Zero or lower
        derive_work_difficulty(multiplier=0)

    with pytest.raises(InvalidDifficulty):
        # Invalid difficulty
        derive_work_difficulty(
            multiplier=1, base_difficulty=hex(2**64)[2:]
        )

    with pytest.raises(ValueError):
        # Resulting difficulty is too large
        derive_work_difficulty(
            multiplier=268435456, base_difficulty="ffffffc000000000")


def test_derive_work_multiplier():
    assert derive_work_multiplier(
        difficulty="fffffe0000000000", base_difficulty="ffffffc000000000"
    ) == pytest.approx(0.125)
    assert derive_work_multiplier(
        difficulty="ffffffe000000000", base_difficulty="ffffffc000000000"
    ) == pytest.approx(2)

    # 'base_difficulty' defaults to 'fffffff800000000'
    assert derive_work_multiplier(difficulty="fffffff800000000") == 1

    with pytest.raises(InvalidDifficulty):
        assert derive_work_multiplier(
            difficulty="invalid", base_difficulty="ffffffc000000000")

    with pytest.raises(InvalidDifficulty):
        assert derive_work_multiplier(
            difficulty="ffffffc000000000", base_difficulty="invalid")


def test_solve_work():
    fake_hash = blake2b(b"fakeBlock", digest_size=32).hexdigest()

    # Use a very low difficulty
    test_difficulty = dec_to_hex(1028, 8)

    result = solve_work(fake_hash, difficulty=test_difficulty)

    assert validate_work(fake_hash, work=result, difficulty=test_difficulty)


def test_work_timeout():
    """
    Try solving a work with timeout and make sure it times out
    after the time has passed
    """
    fake_hash = blake2b(b"fakeBlock", digest_size=32).hexdigest()

    start = time.time()

    # Use the maximum possible difficulty to make the PoW essentially
    # impossible to solve
    result = solve_work(fake_hash, difficulty="f"*16, timeout=0.5)
    end = time.time()

    assert result is None

    # Operation should timeout after 0.5 seconds. Since it's a blocking
    # operation, give it some time to stop
    assert (end - start) > 0.5 and (end - start) < 1
