# pretty_prompt_compare

A python package for comparing prompts/responses with pretty print.

https://github.com/user-attachments/assets/ef152000-a954-4e3e-ad05-47f840d0db09

In the age of LLMs, a lot of prompt engineering comes down to comparing prompts and their responses. This Python package helps by pretty-printing pairs of prompts and responses, making it easier to see differences and embed this workflow into your Python development environment.

## Installation

```bash
pip install pretty_prompt_compare
```

## Usage

> [!IMPORTANT]  
> This project leverages a parameterized infix operator (`|PrettyCompare|`) to simplify comparing prompts/responses using readable syntax.

- **To compare prompts**, use the `compare_prompt=True` argument. The prompt will be printed in the console with differences highlighted, and f-string expressions shown in a different color.


  ```python
  from pretty_prompt_compare import PrettyCompare

  # to compare differences in prompts
  pretty_compare = PrettyCompare(compare_prompt=True)
  "Hello beautiful {world}" |pretty_compare| "Hello brave {world}"
  ```

  <img src="https://github.com/com3dian/pretty_prompt_compare/blob/main/img/output_prompt.png" width="600"/>

  The two prompts on either side of the `|pretty_compare|` operation will be printed using the following format:

  ```python
  - {first prompt}
  + {second prompt}
  ```

  If `print_separator=True`, a separator line will be printed between the two prompts.

  In the printed second prompt:

  - Characters that appear only in the first prompt will be highlighted using `COLOR_PALETTE["delete"]` and shown with a ~~strikethrough~~.
  - Characters that appear only in the second prompt will be highlighted using `COLOR_PALETTE["insert"]`.

  In both prompts, the `{f-string expressions}` will be highlighted in value of `COLOR_PALETTE["f-string expression"]`.


- **To compare responses**, use the `compare_response=True` argument. The responses will be printed in the console with differences highlighted, and target strings highlighted in a different color.

  ```python
  from pretty_prompt_compare import PrettyCompare

  # to compare differences in responses
  pretty_compare = PrettyCompare(compare_response=True, target=["brave", "beautiful", "world"])
  "Hello beautiful {world}" |pretty_compare| "Hello brave {world}"
  ```

  <img src="https://github.com/com3dian/pretty_prompt_compare/blob/main/img/output_response.png" width="600"/>

  The responses are displayed in a similar format to the prompts, with the additional feature that target strings are highlighted using `COLOR_PALETTE["focus"]` with <ins>underline</ins> and **bold**.

- **To Change the color palette**, use the `color_palette` argument.

  ```python
  # compare differences in prompts with custom color palette
  pretty_compare = PrettyCompare(compare_prompt=True, color_palette=...)
  ```
  The default color palette can be found at
  https://github.com/com3dian/pretty_prompt_compare/blob/7cbad091065d0b962fb7288b090333bc95ede305/src/pretty_prompt_compare.py#L34-L40


## Note

The prompts/responses are compared using the `difflib.SequenceMatcher` class. The algorithm for text comparison is based on the [Ratcliff/Obershelp pattern recognition algorithm](https://en.wikipedia.org/wiki/Gestalt_pattern_matching). For more reference please visit https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher.


## License

MIT License

