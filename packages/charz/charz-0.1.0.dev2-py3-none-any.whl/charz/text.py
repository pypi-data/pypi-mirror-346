"""
Text utility module
===================

Utility for flipping characters/lines. Support for rotating characters

Includes
--------

- `fill`
- `flip_h`
- `flip_v`
- `fill_lines`
- `flip_lines_h`
- `flip_lines_v`
- `rotate`
"""

from __future__ import annotations as _annotations

from math import tau as _TAU


# IDEA: make TextTranslator (as in Transform props),
#       as public export,
#       and wrap methods of 1 default instance with module functions in this file


# predefined horizontal conversions
_h_conversions: dict[str, str] = {  # horizontal flip
    "/": "\\",
    "(": ")",
    "[": "]",
    "{": "}",
    ">": "<",
    "´": "`",
    "d": "b",
    "q": "p",
}
# mirroring `_h_conversions`
# fmt: off
_h_conversions.update({
    value: key
    for key, value in _h_conversions.items()
})
# unmirrored `_h_conversions` for monodirectional translations
_h_conversions.update({
    "7": "<"
})
# fmt: on
# predefined vertical conversions
_v_conversions: dict[str, str] = {  # vertical flip
    "/": "\\",
    ".": "'",
    ",": "`",
    "¯": "_",
    "b": "p",
    "q": "d",
    "w": "m",
    "W": "M",
    "v": "^",
    "V": "A",
}
# mirroring `_v_conversions`
# fmt: off
_v_conversions.update({
    value: key
    for key, value in _v_conversions.items()
})
# fmt: on
# unmirrored `_v_conversions` for monodirectional translations
# fmt: off
# _v_conversions.update({
#     # none for now...
# })
# fmt: on
# predefined rotational conversions
_r_conversions: dict[str, tuple[str, ...]] = {  # rotational
    "|": ("|", "\\", "-", "/"),
    ".": (".", "'"),
    "b": ("b", "p", "q", "d"),
    "9": ("9", "6"),
}
# (I marked vars with underscore as they are not for export, and this is a public module)
# creating mirrored {char: variants} pairs, for pairs already defined in `_r_conversions`
# mirror `_r_conversions` (adds variants as their own keys)
for _options in list(_r_conversions.values()):
    for _idx, _value in enumerate(_options):
        if _idx == 0:  # does not need to re-add the initial pair
            continue
        assert _value not in _r_conversions, "cannot add existing value: " + repr(_value)
        _before = _options[:_idx]
        _after = _options[_idx:]
        _new_values = (*_after, *_before)
        _r_conversions[_value] = _new_values
# unmirrored `_r_conversions` for spesific lookup translations
# fmt: off
# _r_conversions.update({
#     # none for now...
# })
# fmt: on


def fill(line: str, *, width: int, fill_char: str = " ") -> str:
    """Fills a single left-justified line with a string of length 1

    Args:
        line (str): line to be filled
        width (int): maximum width of output string
        fill_char (str, optional): string of length 1 to fill line with. Defaults to " ".

    Returns:
        str: line filled with fill character
    """
    return line.ljust(width, fill_char)


def flip_h(line: str, /) -> str:
    """Flips a single line horizontally. Also works with a single character

    Args:
        line (list[str]): content to ble flipped

    Returns:
        list[str]: flipped line or character
    """
    return "".join(_h_conversions.get(char, char) for char in reversed(line))


def flip_v(line: str, /) -> str:
    """Flips a single line vertically. Also works with a single character

    Args:
        line (list[str]): content to ble flipped

    Returns:
        list[str]: flipped line or character
    """
    return "".join(_v_conversions.get(char, char) for char in line)


def fill_lines(lines: list[str], *, fill_char: str = " ") -> list[str]:
    """Fill lines with fill character, based on longest line.
    Usefull for filling textures, so that it gets a nice rectangular shape.
    Good for centering and flipping textures.

    Args:
        lines (list[str]): lines to be filled
        fill_char (str, optional): string of length 1 to fill line with. Defaults to " ".

    Returns:
        list[str]: rectangular filled lines
    """
    if not any(lines):  # allow empty lines
        return []  # but still return unique list
    longest = len(max(lines, key=len))
    return [fill(line, width=longest, fill_char=fill_char) for line in lines]


def flip_lines_h(lines: list[str], /) -> list[str]:
    """Flips lines horizontally. Usefull for flipping textures

    Args:
        lines (list[str]): lines of strings or texture

    Returns:
        list[str]: flipped content
    """
    return [flip_h(line) for line in lines]


def flip_lines_v(lines: list[str], /) -> list[str]:
    """Flips lines vertically. Usefull for flipping textures

    Args:
        lines (list[str]): lines of strings or texture

    Returns:
        list[str]: flipped content
    """
    return [flip_v(line) for line in reversed(lines)]


def rotate(char: str, /, angle: float) -> str:
    """Returns symbol when rotated by angle counter clockwise

    Args:
        char (str): character to rotate
        angle (float): counter clockwise rotation in radians

    Returns:
        str: rotated character or original character
    """
    if char in _r_conversions:
        sector_count = len(_r_conversions[char])
        sector_rads = _TAU / sector_count
        half_sector_rads = sector_rads / 2
        total_rads = (angle + half_sector_rads) % _TAU
        index = int(total_rads / sector_rads) % sector_count
        return _r_conversions[char][index]
    return char
