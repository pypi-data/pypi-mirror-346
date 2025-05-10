"""
MIT License

Copyright (c) 2025 Zehao Lu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from difflib import SequenceMatcher
from rich.console import Console
from rich.text import Text
from rich.color import Color
import re
from infix import make_infix
from functools import wraps

# Default color palette
COLOR_PALETTE = {
    "delete": "#FF90BB",
    "insert": "#7CD9E6",
    "equal": "#A3A3A3",
    "f-string expression": "#87A2FF",
    "separator": "#86D293",
}

def _highlight_fstring_parts(prompt: str, default_style: str, expr_style: str) -> Text:
    """
    Highlight f-string parts in a string.

    Args:
        prompt (str): The string to highlight f-string parts in.
        default_style (str): The default style to apply to the string.
        expr_style (str): The style to apply to the f-string parts.
    """
    text = Text()
    pattern = re.compile(r"({[^{}]+})")
    last_end = 0

    for match in pattern.finditer(prompt):
        start, end = match.span()

        if start > last_end:
            text.append(prompt[last_end:start], style=default_style)
        text.append(prompt[start:end], style=expr_style)
        last_end = end

    if last_end < len(prompt):
        text.append(prompt[last_end:], style=default_style)

    return text


def _highlight_focus_parts(
    content: str, default_style: str, focus_style: str, focus_list: list[str]
) -> Text:
    """
    Highlight focus parts in a string.

    Args:
        content (str): The string to highlight focus parts in.
        default_style (str): The default style to apply to the string.
        focus_style (str): The style to apply to the focus parts.
        focus_list (list[str]): The list of focus strings to highlight.
    """
    text = Text(content, style=default_style)
    for focus in focus_list:
        start = 0
        while True:
            index = content.find(focus, start)
            if index == -1:
                break
            text.stylize(focus_style, index, index + len(focus))
            start = index + len(focus)
    return text


def _highlight_differences(
    prompt_a: str,
    prompt_b: str,
    color_palette: dict = COLOR_PALETTE,
    print_separator: bool = False,
):
    """
    Highlight the differences between two prompts.

    Args:
        prompt_a (str): The first prompt to compare.
        prompt_b (str): The second prompt to compare.
        color_palette (dict, optional): The color palette to use for highlighting.
            Defaults to color_palette.
        print_separator (bool, optional): Whether to print a separator between the two prompts.
            Defaults to False.
    """
    color_delete = color_palette["delete"]
    color_insert = color_palette["insert"]
    color_equal = color_palette["equal"]
    color_expression = color_palette["f-string expression"]
    color_separator = color_palette["separator"]

    matcher = SequenceMatcher(None, prompt_a, prompt_b)

    # Init rich.Text() object
    text_prompt_a = Text()
    text_prompt_b = Text()

    text_prompt_a.append(Text("- ", style=f"bold {color_delete}"))
    text_prompt_a.append(
        _highlight_fstring_parts(prompt_a, color_equal, color_expression)
    )
    text_prompt_b.append(Text("+ ", style=f"bold {color_insert}"))

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            text_prompt_b.append(
                _highlight_fstring_parts(prompt_a[i1:i2], color_equal, color_expression)
            )
        elif tag == "replace":
            # Strike with colored line, default text color
            text_prompt_b.append(Text(prompt_a[i1:i2], style=f"strike {color_delete}"))
            text_prompt_b.append(Text(prompt_b[j1:j2], style=f"{color_insert}"))
        elif tag == "delete":
            text_prompt_b.append(Text(prompt_a[i1:i2], style=f"strike {color_delete}"))
        elif tag == "insert":
            text_prompt_b.append(Text(prompt_b[j1:j2], style=f"{color_insert}"))

    console = Console()
    separator = Text("-" * 79, style=color_separator)
    console.print(text_prompt_a)
    if print_separator:
        console.print(separator)
    console.print(text_prompt_b)


def _highlight_difference_with_focus(
    output_a: str,
    output_b: str,
    target: list[str],
    color_palette: dict = COLOR_PALETTE,
    print_separator: bool = False,
):
    """
    Highlight the differences between two responses with focus on specific target strings.

    Args:
        output_a (str): The first response to compare.
        output_b (str): The second response to compare.
        target (list[str]): The list of target strings to focus on.
        color_palette (dict, optional): The color palette to use for highlighting.
            Defaults to color_palette.
        print_separator (bool, optional): Whether to print a separator between the two responses.
            Defaults to False.
    """
    color_delete = color_palette["delete"]
    color_insert = color_palette["insert"]
    color_equal = color_palette["equal"]
    color_separator = color_palette["separator"]

    matcher = SequenceMatcher(None, output_a, output_b)

    # Init rich.Text() object
    text_output_a = Text()
    text_output_b = Text()
    text_output_b_with_focus = _highlight_focus_parts(
        output_b,
        default_style=f"{color_equal}",
        focus_style=f"underline bold",
        focus_list=target,
    )

    text_output_a.append(Text("- ", style=f"bold {color_delete}"))
    text_output_a.append(
        _highlight_focus_parts(
            output_a,
            default_style=f"{color_equal}",
            focus_style=f"underline bold {color_delete}",
            focus_list=target,
        )
    )

    text_output_b.append(Text("+ ", style=f"bold {color_insert}"))
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            inserted_segment = text_output_b_with_focus[j1:j2].copy()  # Make a copy
            inserted_segment.stylize(f"{color_equal}")
            text_output_b.append(inserted_segment)
        elif tag == "replace":
            # Strike with colored line, default text color
            text_output_b.append(Text(output_a[i1:i2], style=f"strike {color_delete}"))
            inserted_segment = text_output_b_with_focus[j1:j2].copy()  # Make a copy
            inserted_segment.stylize(f"{color_insert}")
            text_output_b.append(inserted_segment)
        elif tag == "delete":
            text_output_b.append(Text(output_a[i1:i2], style=f"strike {color_delete}"))
        elif tag == "insert":
            inserted_segment = text_output_b_with_focus[j1:j2].copy()  # Make a copy
            inserted_segment.stylize(f"{color_insert}")
            text_output_b.append(inserted_segment)

    console = Console()
    separator = Text("-" * 79, style=color_separator)
    console.print(text_output_a)
    if print_separator:
        console.print(separator)
    console.print(text_output_b)


def validate_color_palette_and_args(
    check_str_args: list[int] = None, require_target: bool = False
):
    """
    Decorator to validate the color palette and arguments.

    Args:
        check_str_args (list[int], optional): List of indices of arguments (prompts or
            responses) to check if they are strings.
        require_target (bool, optional): Whether to require the target argument.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Assume color_palette is either in kwargs or in the default args
            color_palette = kwargs.get("color_palette")
            if color_palette is None:
                # fallback: get from default in function signature
                color_palette = func.__defaults__[
                    func.__code__.co_varnames.index("color_palette")
                    - (len(func.__code__.co_varnames) - len(func.__defaults__))
                ]

            color_field = COLOR_PALETTE.keys()
            if not set(color_field).issubset(color_palette.keys()):
                raise ValueError(f"color_palette must have the keys: {color_field}")
            for color_key in color_field:
                try:
                    Color.parse(color_palette[color_key])
                except Exception:
                    raise ValueError(
                        f"Invalid color value for key '{color_key}': {color_palette[color_key]}"
                    )

            # Check that certain arguments are strings
            if check_str_args:
                for i in check_str_args:
                    if not isinstance(args[i], str):
                        raise TypeError(
                            f"Expected str, got {type(args[i])} for argument {i}"
                        )

            # Check that `target` is a list of strings
            if require_target:
                target = kwargs.get("target", args[2] if len(args) > 2 else None)
                if not isinstance(target, list) or not all(
                    isinstance(x, str) for x in target
                ):
                    raise TypeError("`target` must be a list of strings")

            return func(*args, **kwargs)

        return wrapper

    return decorator


@make_infix("or")
@validate_color_palette_and_args(check_str_args=[0, 1])
def pretty_prompt_compare(
    prompt_a: str,
    prompt_b: str,
    color_palette: dict = COLOR_PALETTE,
    print_separator: bool = False,
) -> None:
    """
    Highlight the differences between two prompts.

    Args:
        prompt_a (str): The first prompt to compare.
        prompt_b (str): The second prompt to compare.
        color_palette (dict, optional): The color palette to use for highlighting. Defaults to color_palette.
        print_separator (bool, optional): Whether to print a separator between the two prompts. Defaults to False.
    """
    _highlight_differences(prompt_a, prompt_b, color_palette, print_separator)


@make_infix("or")
@validate_color_palette_and_args(check_str_args=[0, 1], require_target=True)
def pretty_response_compare(
    response_a: str,
    response_b: str,
    target: list[str],
    color_palette: dict = COLOR_PALETTE,
    print_separator: bool = False,
):
    """
    Highlight the differences between two responses with focus on specific target strings.

    Args:
        response_a (str): The first response to compare.
        response_b (str): The second response to compare.
        target (list[str]): The list of target strings to focus on.
        color_palette (dict, optional): The color palette to use for highlighting.
            Defaults to color_palette.
        print_separator (bool, optional): Whether to print a separator between the two responses.
            Defaults to False.
    """
    _highlight_difference_with_focus(
        response_a, response_b, target, color_palette, print_separator
    )


# Custom wrapper class to include parameters
class PrettyCompare:
    def __init__(
        self,
        *,  # forces keyword-only arguments after this
        color_palette=None,
        target=None,
        print_separator=False,
        compare_prompt=None,
        compare_response=None,
    ):
        if (compare_prompt is None) == (compare_response is None):
            raise ValueError(
                "You must set exactly one of 'compare_prompt=True' or "
                "'compare_response=True'."
            )

        self.compare_prompt = bool(compare_prompt)

        if color_palette is None:
            self.color_palette = COLOR_PALETTE
        else:
            self.color_palette = color_palette

        self.print_separator = print_separator
        if compare_response:
            self.target = target if target is not None else []
        elif target is not None:
            raise ValueError("`target` is only used when `compare_response=True`")

    def __ror__(self, a):
        self._left = a
        return self

    def __or__(self, b):
        if self.compare_prompt:
            return pretty_prompt_compare(
                self._left, b, self.color_palette, self.print_separator
            )
        else:
            return pretty_response_compare(
                self._left, b, self.target, self.color_palette, self.print_separator
            )
