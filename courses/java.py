# courses/java.py - Java Programming Course Definition

COURSE = {
    "id": "java",
    "display_name": "Java Programming",
    "description": "Learn Java from syntax basics to object-oriented design",
    "icon": "☕",
    "type": "programming",

    "topics": {

        "java_basics": {
            "display_name": "Java Basics & Syntax",
            "tier": 1,
            "prerequisites": [],
            "description": "Java program structure, compilation, and basic syntax",
            "key_concepts": ["main method", "System.out.println", "JVM concept",
                             "Semicolons", "Case sensitivity", "Comments"],
            "teaching_notes": "Compare to Python where helpful. Java is more verbose but strict typing catches bugs early."
        },
        "java_data_types": {
            "display_name": "Data Types & Variables",
            "tier": 1,
            "prerequisites": ["java_basics"],
            "description": "Primitive and reference types in Java",
            "key_concepts": ["int", "double", "boolean", "char", "String",
                             "final keyword", "Type casting", "Wrapper classes"],
            "teaching_notes": "Static typing is the biggest shift from Python. Declare type before variable name."
        },
        "java_conditionals": {
            "display_name": "Conditionals & Operators",
            "tier": 1,
            "prerequisites": ["java_data_types"],
            "description": "Decision making in Java",
            "key_concepts": ["if/else if/else", "switch statement", "Ternary operator",
                             "Comparison operators", "Logical operators (&&, ||, !)"],
            "teaching_notes": "switch is more common in Java than Python. Introduce it early."
        },
        "java_loops": {
            "display_name": "Loops",
            "tier": 1,
            "prerequisites": ["java_conditionals"],
            "description": "Repetition and iteration in Java",
            "key_concepts": ["for loop", "while loop", "do-while loop",
                             "break", "continue", "Enhanced for-each loop"],
            "teaching_notes": "do-while is new for Python students. for-each is cleaner for arrays."
        },
        "java_arrays": {
            "display_name": "Arrays",
            "tier": 2,
            "prerequisites": ["java_loops"],
            "description": "Fixed-size ordered collections in Java",
            "key_concepts": ["Array declaration", "Indexing", "array.length",
                             "2D arrays", "ArrayIndexOutOfBoundsException"],
            "teaching_notes": "Fixed size is the key difference from Python lists."
        },
        "java_methods": {
            "display_name": "Methods",
            "tier": 2,
            "prerequisites": ["java_arrays"],
            "description": "Reusable code blocks in Java",
            "key_concepts": ["Method signature", "Return types", "void",
                             "Overloading", "static vs instance methods"],
            "teaching_notes": "Return type must be declared — very different from Python."
        },
        "java_strings": {
            "display_name": "Strings in Java",
            "tier": 2,
            "prerequisites": ["java_data_types"],
            "description": "String manipulation in Java",
            "key_concepts": ["String immutability", "equals() vs ==",
                             "substring()", "split()", "StringBuilder"],
            "teaching_notes": "equals() vs == is a critical gotcha that trips up almost every beginner."
        },
        "java_arraylist": {
            "display_name": "ArrayList & Collections",
            "tier": 2,
            "prerequisites": ["java_arrays", "java_methods"],
            "description": "Dynamic lists and basic collections",
            "key_concepts": ["ArrayList", "add()", "get()", "size()",
                             "Generics basics", "HashMap introduction"],
            "teaching_notes": "ArrayList = Python list. HashMap = Python dict."
        },
        "java_oop_basics": {
            "display_name": "OOP: Classes & Objects",
            "tier": 3,
            "prerequisites": ["java_methods"],
            "description": "Core object-oriented programming in Java",
            "key_concepts": ["Constructor", "Instance variables", "this keyword",
                             "Getters/Setters", "Encapsulation", "Access modifiers"],
            "teaching_notes": "Getters/setters are standard Java practice unlike Python."
        },
        "java_inheritance": {
            "display_name": "Inheritance & Polymorphism",
            "tier": 3,
            "prerequisites": ["java_oop_basics"],
            "description": "Extending classes and method overriding",
            "key_concepts": ["extends", "super()", "Method overriding",
                             "@Override", "Polymorphism", "Abstract classes"],
            "teaching_notes": "Single inheritance only in Java. Polymorphism is the big concept here."
        },
        "java_interfaces": {
            "display_name": "Interfaces",
            "tier": 3,
            "prerequisites": ["java_inheritance"],
            "description": "Contracts and multiple interface implementation",
            "key_concepts": ["interface keyword", "implements", "Multiple interfaces",
                             "Interface vs abstract class"],
            "teaching_notes": "Real-world analogy: an interface is a contract."
        },
        "java_exceptions": {
            "display_name": "Exception Handling",
            "tier": 3,
            "prerequisites": ["java_methods"],
            "description": "Handling errors in Java",
            "key_concepts": ["try/catch/finally", "throws keyword",
                             "Checked vs unchecked exceptions", "Custom exceptions"],
            "teaching_notes": "Checked exceptions are unique to Java — Python has nothing equivalent."
        },
    }
}