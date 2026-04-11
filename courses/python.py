# courses/python.py - Python Programming Course Definition

COURSE = {
    "id": "python",
    "display_name": "Python Programming",
    "description": "Learn Python from absolute basics to object-oriented programming",
    "icon": "🐍",
    "type": "programming",  # affects how AI teaches (code-focused)
    
    "topics": {

        # TIER 1 - Absolute Beginner
        "variables": {
            "display_name": "Variables & Data Types",
            "tier": 1,
            "prerequisites": [],
            "description": "Storing and naming data in Python",
            "key_concepts": ["Variable assignment", "int", "float", "str", "bool", "type()", "f-strings"],
            "teaching_notes": "Focus on the 'box that stores a value' analogy. Emphasise snake_case naming."
        },
        "strings": {
            "display_name": "Strings",
            "tier": 1,
            "prerequisites": ["variables"],
            "description": "Working with text in Python",
            "key_concepts": ["len()", "Indexing", "Slicing", "upper()/lower()", "split()", "join()", "f-strings"],
            "teaching_notes": "Strings are sequences — connect to lists early. Immutability is key."
        },
        "conditionals": {
            "display_name": "Conditionals (if/elif/else)",
            "tier": 1,
            "prerequisites": ["variables"],
            "description": "Making decisions in code",
            "key_concepts": ["if/elif/else", "Comparison operators", "Boolean operators (and/or/not)", "Nested conditions"],
            "teaching_notes": "Indentation errors are very common here. Watch for them."
        },
        "loops": {
            "display_name": "Loops (for & while)",
            "tier": 1,
            "prerequisites": ["variables", "conditionals"],
            "description": "Repeating actions in Python",
            "key_concepts": ["for loop", "while loop", "range()", "break", "continue", "enumerate()"],
            "teaching_notes": "Start with for loops. range() confusion (0-indexed, exclusive end) is very common."
        },

        # TIER 2 - Beginner
        "lists": {
            "display_name": "Lists",
            "tier": 2,
            "prerequisites": ["variables", "loops"],
            "description": "Ordered, mutable collections",
            "key_concepts": ["Indexing", "Slicing", "append()", "remove()", "sort()", "len()", "Nested lists"],
            "teaching_notes": "Mutable vs immutable is key. Connect append() to a growing shopping list."
        },
        "dictionaries": {
            "display_name": "Dictionaries",
            "tier": 2,
            "prerequisites": ["variables", "lists"],
            "description": "Key-value pairs for structured data",
            "key_concepts": ["Creating dicts", "get()", "keys()", "values()", "items()", "Nested dicts"],
            "teaching_notes": "Real-world analogy: a phone book. KeyError is a common pitfall — teach .get() early."
        },
        "functions": {
            "display_name": "Functions",
            "tier": 2,
            "prerequisites": ["variables", "loops", "conditionals"],
            "description": "Reusable blocks of code",
            "key_concepts": ["def", "Parameters vs arguments", "return", "Default parameters", "Scope", "Docstrings"],
            "teaching_notes": "Scope confusion (local vs global) is very common. Teach single-responsibility early."
        },
        "tuples_and_sets": {
            "display_name": "Tuples & Sets",
            "tier": 2,
            "prerequisites": ["lists"],
            "description": "Immutable sequences and unique collections",
            "key_concepts": ["Tuple immutability", "Tuple unpacking", "Set uniqueness", "Union/Intersection/Difference"],
            "teaching_notes": "Key message: tuples = immutable lists, sets = unique unordered collections."
        },

        # TIER 3 - Intermediate
        "list_comprehensions": {
            "display_name": "List Comprehensions",
            "tier": 3,
            "prerequisites": ["lists", "loops", "conditionals"],
            "description": "Elegant one-line list creation",
            "key_concepts": ["Basic syntax", "With conditions", "Dict comprehensions", "When to use vs loops"],
            "teaching_notes": "Always show the loop equivalent first, then refactor to comprehension."
        },
        "error_handling": {
            "display_name": "Error Handling (try/except)",
            "tier": 3,
            "prerequisites": ["functions", "conditionals"],
            "description": "Handling errors gracefully",
            "key_concepts": ["try/except", "Common exceptions", "finally", "raise", "Custom exceptions"],
            "teaching_notes": "Bare except: is an antipattern — always specify the error type."
        },
        "file_handling": {
            "display_name": "File Handling",
            "tier": 3,
            "prerequisites": ["functions", "error_handling"],
            "description": "Reading and writing files",
            "key_concepts": ["open()", "read()/write()", "with statement", "File modes", "CSV", "JSON"],
            "teaching_notes": "Always use 'with open()' — teach it as the only correct way."
        },
        "classes_oop": {
            "display_name": "Classes & OOP",
            "tier": 3,
            "prerequisites": ["functions", "dictionaries"],
            "description": "Object-oriented programming",
            "key_concepts": ["class", "__init__", "self", "Methods", "Inheritance", "super()", "__str__"],
            "teaching_notes": "Blueprint analogy: class = blueprint, object = house. self confusion is very common."
        },
        "recursion": {
            "display_name": "Recursion",
            "tier": 3,
            "prerequisites": ["functions", "conditionals"],
            "description": "Functions that call themselves",
            "key_concepts": ["Base case", "Recursive case", "Call stack", "Factorial", "Fibonacci"],
            "teaching_notes": "Always start with the base case. Draw the call stack visually."
        },
    }
}