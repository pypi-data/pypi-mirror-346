from pretty_prompt_compare import PrettyCompare

pretty_compare = PrettyCompare(compare_response=True, target=["brave", "beautiful", "world"])

# pretty_compare = PrettyCompare(compare_response=True, print_separator=True)
"Hello beautiful {world}" |pretty_compare| "Hello brave {world}"
