import argparse
import os
from .utils import load, save
from dataclasses import dataclass

SEARCH_STEP = 2
SEARCH_LENGTH = 4
SEARCH_SECTION_LENGTH = 20
SEARCH_TIMES = 10
SEARCH_NEW_LINE_WORD = 3


@dataclass(frozen=True)
class SubtitleResult:
    word: str
    new_line_poses: list
    source: str


def combine(subtitle_result: SubtitleResult, original: str) -> str:
    result = ""
    subtitle = subtitle_result.word
    subtitle_new_line_poses = subtitle_result.new_line_poses
    original_len = len(original)
    subtitle_len = len(subtitle)
    idx = 0
    matched_idx = 0

    while idx < len(original):
        char = original[idx]

        print(f"original:{char}[{idx}] subtitle:{subtitle[matched_idx]}[{matched_idx}]")
        if char.casefold() == subtitle[matched_idx].casefold():
            result += char
            idx += 1
            matched_idx += 1
            continue

        next_idx = idx + SEARCH_STEP
        if (next_idx >= original_len - SEARCH_LENGTH) or (
            matched_idx >= subtitle_len - SEARCH_LENGTH
        ):
            # combine remainder
            result += original[idx:]
            print(f"combine remained")
            break

        times = 0
        search_idx = matched_idx + 1
        next_idx_end = next_idx + SEARCH_LENGTH

        # find the next same sentence
        while (
            sub_matched_idx := subtitle[search_idx : search_idx + SEARCH_SECTION_LENGTH]
            .casefold()
            .find(original[next_idx:next_idx_end].casefold())
        ) == -1 and times < SEARCH_TIMES:
            search_idx += 1
            # the subsequent search position is 2^n
            next_idx += 2**times
            next_idx_end += 1
            times += 1
            print(f"next_idx:{next_idx} next_idx_end:{next_idx_end}")
        else:
            if sub_matched_idx == -1:
                break

            # complete the text before the match
            add_text = original[idx:next_idx_end]
            result += add_text

            # calculate the offset of the complement
            offset = (next_idx_end - idx - SEARCH_LENGTH) - (
                search_idx + sub_matched_idx - matched_idx
            )

            # reindex the position of newlines in the subtitle
            if offset != 0:
                for i, v in enumerate(subtitle_new_line_poses):
                    if v > matched_idx:
                        subtitle_new_line_poses[i] += offset

            # next position
            idx = next_idx_end
            matched_idx = search_idx + sub_matched_idx + SEARCH_LENGTH
            print(f"matched_idx:{matched_idx}")

    # add newlines to the resulting text
    n_number = 0
    for new_line in subtitle_new_line_poses:
        n_pos = new_line + n_number
        if n_pos >= len(result):
            break
        result = result[:n_pos] + "\n" + result[n_pos:]
        n_number += 1

    # merge original content into the subtitle.
    def merge(from_text: str, to_text: str) -> str:
        result = ""
        from_lines = from_text.split("\n")
        to_lines = to_text.split("\n")
        j = 0

        for i, line in enumerate(to_lines):
            if (i - 2) % 4 == 0 and j < len(from_lines):
                result += f"{from_lines[j]}\n"
                j += 1
            else:
                result += f"{line}\n"

        # merge the remaining sections of the original.
        while j < len(from_lines):
            result += f"{from_lines[j]}"
            j += 1

        return result

    return merge(result, subtitle_result.source)


def resolve(subtitle: str) -> SubtitleResult:
    result = ""
    new_line_poses = list()
    new_line_offset = 0
    lines = subtitle.split("\n")

    for i, line in enumerate(lines):
        if (i - 2) % 4 == 0:
            result += f"{line}"
            line_len = len(line)
            new_line_offset += line_len
            new_line_poses.append(new_line_offset)

    return SubtitleResult(word=result, new_line_poses=new_line_poses, source=subtitle)


def get_word(original: str) -> str:
    return original.replace("\n", "")


def cli():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("subtitle", type=str, help="a .srt file to combine")
    parser.add_argument("original", type=str, help="a full original text file")
    parser.add_argument(
        "--output_dir",
        "-o",
        type=str,
        default="output",
        help="directory to save the outputs",
    )

    args = parser.parse_args().__dict__
    subtitle_path = args.pop("subtitle")
    original_path = args.pop("original")
    output_dir = args.pop("output_dir")

    text_basename = os.path.basename(subtitle_path)
    text_basename = os.path.splitext(text_basename)[0] + ".bl" + ".srt"

    subtitle = load(subtitle_path)
    original = load(original_path)

    result = combine(resolve(subtitle), get_word(original))
    save(result, text_basename, output_dir)


if __name__ == "__main__":
    cli()
