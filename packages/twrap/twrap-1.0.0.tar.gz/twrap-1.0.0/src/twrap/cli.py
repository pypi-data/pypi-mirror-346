#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A thin CLI wrapper around python `textwrap.fill` function to wrap text.

The CLI doesn't understand code, or formatting. it handles text as is.
This tool is ideal for wrapping text in text files like LICENSE,
README.txt, etc.

The CLI can read text from stdin, multiple files, or stdin + multiple files.
And it can write results to stdout, a file, or modify original files.
Note that the CLI doesn't accept inplace modification when using stdin in
input.

The CLI also has a check flag, which checks files without modifying them or
writing wrapped text to the output. In case one or more files would be
modified, It outputs the names of files to stdout and exists with an error
code. In case no files would be modified, it exists normally.

How it works:

First, the text line endings (`\n`, `\r`, `\r\n`) are normalized to `\n`,
to prevent inconsistent behavior when a file has mixed line endings.
Then the text is split into paragraphs each two new lines (`\n\n`), and
each paragraph's lines are concatenated into a single line by replacing
new lines (`\n`) with spaces ` `. The resulting line is passed to
`textwrap.fill` along with the options, which outputs a paragraph of
wrapped lines. Then all paragraphs are concatenated together using two
new line characters `\n\n`. Finally, the output is written to the output.

"""

import argparse
import logging as log
import os
import shutil
import sys
import tempfile
import textwrap
from pathlib import Path
from typing import Any, Dict

__version__ = "1.0.0"

logger = log.getLogger(__name__)


class ValidationError(Exception):
    ...


def get_parser() -> argparse.ArgumentParser:
    """Initialize and return argument parser."""

    parser = argparse.ArgumentParser(
        description="""A thin CLI wrapper around python `textwrap.fill`
        function.""",
        prog="twrap",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # version
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    # input
    parser.add_argument(
        "files",
        metavar="INPUT",
        nargs="*",
        type=str,
        default=["-"],
        help="""
        files or text to wrap. Use '-' to read from stdin. If multiple files
        are given, their output is concatenated. Default: stdin.
        """,
    )

    # output
    output = parser.add_mutually_exclusive_group()
    output.add_argument(
        "-c",
        "--check",
        action="store_true",
        help="""
        If enabled, checks if input doesn't need to be modified, and exits
        with an error code If the input needs to be modified. Doesn't output
        to files or stdout. Default: disabled.
        """,
    )
    output.add_argument(
        "-i",
        "--inplace",
        action="store_true",
        help="""
        Modify files in-place (overwrite files). Default: disabled.
        """,
    )
    output.add_argument(
        "-o",
        "--output",
        type=str,
        default="-",
        help="Output file, or '-' to write to stdout. Default: stdout.",
    )

    # wrap options
    parser.add_argument(
        "-w",
        "--width",
        type=int,
        default=80,
        help="""
        The maximum length of wrapped lines. As long as there are no
        individual words in the input text longer than width, textwrap
        guarantees that no output line will be longer than width characters.
        Default: 80
        """,
    )
    parser.add_argument(
        "-I",
        "--initial-indent",
        type=str,
        default="",
        help="""
        String that will be prepended to the first line of wrapped output.
        Counts towards the length of the first line. The empty string is not
        indented. Default: empty string.
        """,
    )
    parser.add_argument(
        "-s",
        "--subsequent-indent",
        type=str,
        default="",
        help="""
        String that will be prepended to all lines of wrapped output except
        the first. Counts towards the length of each line except the first.
        Default: empty string.
        """,
    )
    parser.add_argument(
        "-e",
        "--expand-tabs",
        action="store_true",
        help="""
        If enabled, then all tab characters in text will be expanded to
        spaces. Default: disabled.
        """,
    )
    parser.add_argument(
        "-r",
        "--replace-whitespace",
        action="store_true",
        help="""
        If enabled, after tab expansion but before wrapping, each whitespace
        character will be replaced with a single space. The whitespace
        characters replaced are as follows: tab, newline, vertical tab,
        formfeed, and carriage return ('\\t\\n\\v\\f\\r').
        Note: If --expand-tabs is disabled and --replace-whitespace is
        enabled, each tab character will be replaced by a single space,
        which is not the same as tab expansion. Default: disabled.
        """,
    )
    parser.add_argument(
        "-f",
        "--fix-sentence-endings",
        action="store_true",
        help="""
        If enabled, textwrap attempts to detect sentence endings and ensure
        that sentences are always separated by exactly two spaces. This is
        generally desired for text in a monospaced font. However, the sentence
        detection algorithm is imperfect:
            it assumes that a sentence ending consists of a lowercase letter
            followed by one of '.', '!', or '?', possibly followed by one of
            '"' or "'", followed by a space.
        One problem with this algorithm is that it is unable to detect the
        difference between “Dr.” in "[...] Dr. Frankenstein's monster [...]"
        and “Spot.” in "[...] See Spot. See Spot run [...]" Since the sentence
        detection algorithm relies on the definition of “lowercase letter”,
        and a convention of using two spaces after a period to separate
        sentences on the same line, it is specific to English-language texts.
        Default: disabled.
        """,
    )
    parser.add_argument(
        "-b",
        "--break-long-words",
        action="store_true",
        help="""
        If enabled, then words longer than width will be broken in order to
        ensure that no lines are longer than width. If disabled, long words
        will not be broken, and some lines may be longer than width. (Long
        words will be put on a line by themselves, in order to minimize the
        amount by which width is exceeded.) Default: disabled.
        """,
    )
    parser.add_argument(
        "-d",
        "--drop-whitespace",
        action="store_true",
        help="""
        If enabled, whitespace at the beginning and ending of every line
        (after wrapping but before indenting) is dropped. Whitespace at the
        beginning of the paragraph, however, is not dropped if non-whitespace
        follows it. If whitespace being dropped takes up an entire line, the
        whole line is dropped. Default: disabled.
        """,
    )
    parser.add_argument(
        "-y",
        "--break-on-hyphens",
        action="store_true",
        help="""
        If enabled, wrapping will occur preferably on whitespaces and right
        after hyphens in compound words, as it is customary in English. If
        disabled, only whitespaces will be considered as potentially good
        places for line breaks, but you need to disable --break-long-words if
        you want truly inseparable words. Default behavior in previous
        versions was to always allow breaking hyphenated words.
        Default: disabled.
        """,
    )
    parser.add_argument(
        "-t",
        "--tabsize",
        type=int,
        default=8,
        help="""
        If --expand-tabs is enabled, then all tab characters in text will be
        expanded to zero or more spaces, depending on the current column and
        the given tab size. Default: 8
        """,
    )
    parser.add_argument(
        "-m",
        "--max-lines",
        type=int,
        default=None,
        help="""
        If set, then the output will contain at most --max-lines lines, with
        placeholder appearing at the end of the output. Default: None
        """,
    )
    parser.add_argument(
        "-p",
        "--placeholder",
        type=str,
        default="...",
        help="""
        String that will appear at the end of the output text if it has been
        truncated. Default: '...'
        """,
    )

    return parser


def validate_wrap_options(**options: Dict[str, Any]):
    """check that given paths are to existing files, with read and write
    permissions.

    :param files: a list of paths to files, can be absolute or relative.
    :type files: List[str]
    :param skip: file paths to skip
    :type skip: str
    :param permissions: permissions to check for default: (os.R_OK)
    :type permissions: int
    :return: None if all files
    :rtype: None
    :raises FileNotFoundError: if a file is not found
    :raises TypeError: if a path points to something other than a file
    :raises PermissionError: if the file doesn't have read and write
    permissions for the current user
    """
    # check if stdin us provided as input with inplace
    if options["inplace"]:
        if "-" in options["files"]:
            raise ValidationError("Cannot use --inplace with stdin")

        # in case of --inplace, files should have read + write permissions
        perm = os.R_OK | os.W_OK
    else:
        perm = os.R_OK

    # check that input files exist and have sufficient permissions
    file_list = list(options["files"])
    for file in file_list:
        if file == "-":
            continue

        file_path = Path(file)
        if not file_path.exists():
            raise FileNotFoundError(f"file doesn't exist: {file}")

        if not file_path.is_file():
            raise TypeError(f"path is not a file: {file}")

        if not os.access(file_path, perm):
            raise PermissionError(
                f"you don't have enough permissions to read file: {file_path}")

    # create parent folders for output file
    if options["output"] != "-":
        out_file = str(options["output"])
        Path(out_file).parent.mkdir(parents=True, exist_ok=True)


def atomic_file_write(dst_file: str, content: str) -> None:
    """write content to file. creates a temp file and write text content to
    it, then move the file to destination

    :param dst_file: path to file to write content into
    :type dst_file: str
    :param content: text to write into file
    :type content: str
    """
    try:
        with tempfile.NamedTemporaryFile(mode="w", delete=True) as temp:
            temp.write(content)
            temp.flush()
            shutil.move(temp.name, dst_file)
    except FileNotFoundError:
        pass


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def wrap_text(text: str, options: Dict[str, Any]) -> str:
    res = []
    for paragraph in text.split("\n\n"):
        wrapped = textwrap.fill(
            paragraph.replace("\n", " "),
            width=options["width"],
            initial_indent=options["initial_indent"],
            subsequent_indent=options["subsequent_indent"],
            expand_tabs=options["expand_tabs"],
            tabsize=options["tabsize"],
            replace_whitespace=options["replace_whitespace"],
            fix_sentence_endings=options["fix_sentence_endings"],
            break_long_words=options["break_long_words"],
            break_on_hyphens=options["break_on_hyphens"],
            drop_whitespace=options["drop_whitespace"],
            max_lines=options["max_lines"],
            placeholder=options["placeholder"],
        )
        res.append(wrapped)
    return "\n\n".join(res)


def cli(**options) -> int:
    modified_text = []
    changed_files = []

    validate_wrap_options(**options)

    file_count = len(options["files"])

    for file in options["files"]:
        # get text
        if file == "-":
            text = sys.stdin.read()
        else:
            with open(file, "r", encoding="utf-8") as f:
                text = f.read()

        text_normalized = normalize_text(text)
        text_wrapped = wrap_text(text_normalized, options)

        # skip if no changes in text and input file == output file
        if text_wrapped == text_normalized:
            continue

        # mark file as changed
        changed_files.append(file)

        # write to same input file
        if options["inplace"]:
            atomic_file_write(file, text_wrapped)
            logger.info(f"Changed file: {file}")

        # collect text to be concatenated later for --output
        else:
            modified_text.append(text_wrapped)

    # check if there's no modified text
    # either in --check mode and no changes in input
    # or in --inplace mode and all files were written
    if not modified_text:
        return 0

    # concatenate modfied text from multiple input files
    concatenated = '\n'.join(modified_text)

    # there's some modified text
    if options["check"]:
        for file in changed_files:
            if file == '-':
                continue
            else:
                logger.info(f"Would change text from: {file}")
        logger.info(f"{len(changed_files)}/{file_count} would be modified")
        return 1

    if options["output"] == "-":
        print(concatenated)

    else:
        atomic_file_write(options["output"], concatenated)

    for file in changed_files:
        if file == '-':
            continue
        else:
            logger.info(f"changed text from: {file}")
    logger.info(f"{len(changed_files)}/{file_count} were modified")
    return 0


def main() -> None:
    log.basicConfig(
        level=log.INFO,
        format="twarp:%(levelname)s: %(message)s",
    )
    parser = get_parser()
    args = parser.parse_args()
    options = vars(args)
    logger.debug(f"{options=}")
    ret = cli(**options)
    sys.exit(ret)


if __name__ == "__main__":
    main()
