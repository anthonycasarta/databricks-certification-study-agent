from pytest import raises

from study_agent.ingestion.metadata import calculate_content_hash, determine_file_type


def test_wrong_file_extension_raises_value_error():
    with raises(ValueError):
        determine_file_type("image.png")


def test_file_name_without_extension():
    with raises(ValueError):
        determine_file_type("image")


def test_same_input_produces_same_hash():
    a = b"This is content one."
    b = b"This is content one."

    first_hash_pair = calculate_content_hash(a)
    second_hash_pair = calculate_content_hash(b)

    assert first_hash_pair == second_hash_pair


def test_different_input_produces_different_hash():
    a = b"This is content one."
    b = b"This is content two."

    first_hash = calculate_content_hash(a)
    second_hash = calculate_content_hash(b)

    assert first_hash != second_hash


def test_hash_contains_sixty_four_characters():
    a = b"This is content one."
    b = b"This is content two."

    first_hash = calculate_content_hash(a)
    second_hash = calculate_content_hash(b)

    assert len(first_hash) == 64
    assert len(second_hash) == 64
