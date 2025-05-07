# twrap

A thin CLI wrapper around python `textwrap.fill` function to wrap text.

## Requirements

- `Python3` and that's it, you're good to go.

## Usage

```text
usage: textwrap [-h] [-v] [-c | -i | -o OUTPUT] [-w WIDTH] [-I INITIAL_INDENT]
                [-s SUBSEQUENT_INDENT] [-e] [-r] [-f] [-b] [-d] [-y]
                [-t TABSIZE] [-m MAX_LINES] [-p PLACEHOLDER] [INPUT ...]

A thin CLI wrapper around python `textwrap` module.

positional arguments:
  INPUT
          files or text to wrap. Use '-' to read from stdin. If multiple files
          are given, their output is concatenated. Default: stdin.


options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -c, --check
        If enabled, checks if input doesn't need to be modified, and exits
        with an error code If the input needs to be modified. Doesn't output
        to files or stdout. Default: disabled.

  -i, --inplace
        Modify files in-place (overwrite files). Default: disabled.

  -o OUTPUT, --output OUTPUT
        Output file, or '-' to write to stdout. Default: stdout.
  -w WIDTH, --width WIDTH

        The maximum length of wrapped lines. As long as there are no
        individual words in the input text longer than width, textwrap
        guarantees that no output line will be longer than width characters.
        Default: 80

  -I INITIAL_INDENT, --initial-indent INITIAL_INDENT

        String that will be prepended to the first line of wrapped output.
        Counts towards the length of the first line. The empty string is not
        indented. Default: empty string.

  -s SUBSEQUENT_INDENT, --subsequent-indent SUBSEQUENT_INDENT

        String that will be prepended to all lines of wrapped output except
        the first. Counts towards the length of each line except the first.
        Default: empty string.

  -e, --expand-tabs
        If enabled, then all tab characters in text will be expanded to
        spaces. Default: disabled.

  -r, --replace-whitespace

        If enabled, after tab expansion but before wrapping, each whitespace
        character will be replaced with a single space. The whitespace
        characters replaced are as follows: tab, newline, vertical tab,
        formfeed, and carriage return ('\t\n\v\f\r').
        Note: If --expand-tabs is disabled and --replace-whitespace is
        enabled, each tab character will be replaced by a single space,
        which is not the same as tab expansion. Default: disabled.

  -f, --fix-sentence-endings

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

  -b, --break-long-words

        If enabled, then words longer than width will be broken in order to
        ensure that no lines are longer than width. If disabled, long words
        will not be broken, and some lines may be longer than width. (Long
        words will be put on a line by themselves, in order to minimize the
        amount by which width is exceeded.) Default: disabled.

  -d, --drop-whitespace

        If enabled, whitespace at the beginning and ending of every line
        (after wrapping but before indenting) is dropped. Whitespace at the
        beginning of the paragraph, however, is not dropped if non-whitespace
        follows it. If whitespace being dropped takes up an entire line, the
        whole line is dropped. Default: disabled.

  -y, --break-on-hyphens

        If enabled, wrapping will occur preferably on whitespaces and right
        after hyphens in compound words, as it is customary in English. If
        disabled, only whitespaces will be considered as potentially good
        places for line breaks, but you need to disable --break-long-words if
        you want truly inseparable words. Default behavior in previous
        versions was to always allow breaking hyphenated words.
        Default: disabled.

  -t TABSIZE, --tabsize TABSIZE

        If --expand-tabs is enabled, then all tab characters in text will be
        expanded to zero or more spaces, depending on the current column and
        the given tab size. Default: 8

  -m MAX_LINES, --max-lines MAX_LINES

        If set, then the output will contain at most --max-lines lines, with
        placeholder appearing at the end of the output. Default: None

  -p PLACEHOLDER, --placeholder PLACEHOLDER

        String that will appear at the end of the output text if it has been
        truncated. Default: '...'
```
