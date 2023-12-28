import os
from blunt.combine import combine
from blunt.combine import resolve
from blunt.combine import get_word
from blunt.utils import load
from blunt.utils import save
from typing import Tuple

CHECK_POINT = "L"


def get_test_data(text_name: str) -> Tuple[str, str]:
    text_basename = os.path.basename(text_name)
    text_basename = os.path.splitext(text_basename)[0]
    original = load(f"assets/{text_basename}.md")
    subtitle = load(f"assets/{text_basename}.srt")
    return original, subtitle


def get_combine_result(text_name: str) -> str:
    original, subtitle = get_test_data(text_name)
    result = combine(resolve(subtitle), get_word(original))
    return result


def get_combine_lines(text_name: str) -> list[str]:
    return get_combine_result(text_name).split("\n")


def test_less_original():
    lines = get_combine_lines("less_text.srt")
    assert lines[2][22] == CHECK_POINT


def test_more_original():
    lines = get_combine_lines("more_text.srt")
    assert lines[2][22] == CHECK_POINT
    assert len(lines) == 4


def test_equal_original():
    lines = get_combine_lines("equal_text.srt")
    assert lines[6][4] == CHECK_POINT
    assert lines[18][10] == CHECK_POINT
    assert len(lines) == 26


def test_multiline():
    file_name = "multiple_line_text.srt"
    lines = get_combine_lines(file_name)
    assert lines[2][22] == CHECK_POINT
    assert lines[6][::-1][22] == CHECK_POINT


def test_resolve():
    _, subtitle = get_test_data("multiple_line_text.srt")
    subtitle_result = resolve(subtitle)
    assert len(subtitle_result.new_line_poses) == 1


def test_cli():
    file_name = "equal_text.srt"
    output_dir = "output"
    result = get_combine_result(file_name)
    save(result, file_name, output_dir)
    assert os.path.exists(output_dir + "/" + file_name)
