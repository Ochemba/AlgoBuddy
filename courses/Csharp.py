# courses/csharp.py - C# Programming Course Definition

COURSE = {
    "id": "csharp",
    "display_name": "C# Programming",
    "description": "Learn C# for .NET development, from basics to OOP and beyond",
    "icon": "🔷",
    "type": "programming",

    "topics": {
        "csharp_basics": {
            "display_name": "C# Basics & .NET Overview",
            "tier": 1,
            "prerequisites": [],
            "description": "Structure of a C# program, .NET runtime, and basic syntax",
            "key_concepts": ["using statements", "namespace", "Main method", ".NET CLR",
                             "Console.WriteLine", "Semicolons", "Comments"],
            "teaching_notes": "C# sits between Java and Python in feel. .NET ecosystem context helps motivation."
        },
        "csharp_types": {
            "display_name": "Data Types & Variables",
            "tier": 1,
            "prerequisites": ["csharp_basics"],
            "description": "Value types, reference types and type inference",
            "key_concepts": ["int", "double", "bool", "string", "char", "var keyword",
                             "const", "Type casting", "Nullable types (int?)"],
            "teaching_notes": "var is great for introducing type inference. Nullable types are a C# strength."
        },
        "csharp_conditionals": {
            "display_name": "Conditionals & Switch",
            "tier": 1,
            "prerequisites": ["csharp_types"],
            "description": "Decision making and pattern matching",
            "key_concepts": ["if/else if/else", "switch statement", "switch expressions (C# 8+)",
                             "Ternary operator", "Logical operators"],
            "teaching_notes": "Modern switch expressions are a C# highlight worth showing early."
        },
        "csharp_loops": {
            "display_name": "Loops & Iteration",
            "tier": 1,
            "prerequisites": ["csharp_conditionals"],
            "description": "Loops and iteration in C#",
            "key_concepts": ["for", "while", "do-while", "foreach",
                             "break", "continue"],
            "teaching_notes": "foreach over collections is idiomatic C# — emphasise it early."
        },
        "csharp_arrays_lists": {
            "display_name": "Arrays & Lists",
            "tier": 2,
            "prerequisites": ["csharp_loops"],
            "description": "Collections in C#",
            "key_concepts": ["Arrays", "List<T>", "Add()", "Remove()", "Count",
                             "Dictionary<K,V>", "Generics introduction"],
            "teaching_notes": "List<T> is the everyday workhorse. Generics syntax <T> is new but important."
        },
        "csharp_methods": {
            "display_name": "Methods & Parameters",
            "tier": 2,
            "prerequisites": ["csharp_arrays_lists"],
            "description": "Defining and using methods in C#",
            "key_concepts": ["Return types", "void", "Parameters", "Optional parameters",
                             "Named arguments", "ref and out parameters", "Method overloading"],
            "teaching_notes": "ref/out are unique to C# — no Python equivalent. Show sparingly at first."
        },
        "csharp_oop": {
            "display_name": "OOP: Classes & Objects",
            "tier": 3,
            "prerequisites": ["csharp_methods"],
            "description": "Object-oriented programming in C#",
            "key_concepts": ["class", "Constructor", "Properties (get/set)", "Access modifiers",
                             "this keyword", "Static members", "Object initializers"],
            "teaching_notes": "C# properties (get/set) are cleaner than Java getters/setters. Highlight this."
        },
        "csharp_inheritance": {
            "display_name": "Inheritance & Polymorphism",
            "tier": 3,
            "prerequisites": ["csharp_oop"],
            "description": "Class hierarchies in C#",
            "key_concepts": [":", "base keyword", "virtual/override", "sealed",
                             "abstract classes", "Polymorphism"],
            "teaching_notes": "virtual/override is explicit in C# — good design principle."
        },
        "csharp_interfaces": {
            "display_name": "Interfaces & Abstract Classes",
            "tier": 3,
            "prerequisites": ["csharp_inheritance"],
            "description": "Contracts and abstraction in C#",
            "key_concepts": ["interface", "implements (:)", "IEnumerable", "IComparable",
                             "Abstract class vs interface"],
            "teaching_notes": "C# interfaces are very similar to Java — good cross-course connection."
        },
        "csharp_linq": {
            "display_name": "LINQ Basics",
            "tier": 4,
            "prerequisites": ["csharp_interfaces", "csharp_arrays_lists"],
            "description": "Language Integrated Query for collections",
            "key_concepts": ["Where()", "Select()", "OrderBy()", "FirstOrDefault()",
                             "Lambda expressions =>", "Method syntax vs query syntax"],
            "teaching_notes": "LINQ is one of C#'s best features. Connect Where() to Python list comprehensions."
        },
        "csharp_exceptions": {
            "display_name": "Exception Handling",
            "tier": 3,
            "prerequisites": ["csharp_methods"],
            "description": "Error handling in C#",
            "key_concepts": ["try/catch/finally", "throw", "Custom exceptions",
                             "Exception filters (when)", "Common exceptions"],
            "teaching_notes": "Similar to Java but no checked exceptions — a key difference."
        },
    }
}