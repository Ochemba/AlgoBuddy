# courses/dsa.py - Data Structures & Algorithms Course Definition

COURSE = {
    "id": "dsa",
    "display_name": "Data Structures & Algorithms",
    "description": "Core CS fundamentals — how to store data and solve problems efficiently",
    "icon": "🗂️",
    "type": "mixed",  # theory + code

    "topics": {
        "big_o": {
            "display_name": "Big O Notation & Complexity",
            "tier": 1,
            "prerequisites": [],
            "description": "Measuring algorithm efficiency",
            "key_concepts": ["O(1)", "O(n)", "O(n²)", "O(log n)", "O(n log n)",
                             "Time complexity", "Space complexity", "Best/worst/average case"],
            "teaching_notes": "Use real-world analogies: finding a name in a phone book = O(log n) with binary search."
        },
        "arrays_intro": {
            "display_name": "Arrays & Dynamic Arrays",
            "tier": 1,
            "prerequisites": ["big_o"],
            "description": "The most fundamental data structure",
            "key_concepts": ["Indexing", "Fixed vs dynamic size", "Memory layout",
                             "Access O(1)", "Insert/delete O(n)", "Resizing"],
            "teaching_notes": "Relate to Python lists or Java arrays depending on student background."
        },
        "linked_lists": {
            "display_name": "Linked Lists",
            "tier": 2,
            "prerequisites": ["arrays_intro"],
            "description": "Node-based linear data structures",
            "key_concepts": ["Singly linked list", "Doubly linked list", "Node structure",
                             "Head/tail", "Traversal", "Insert/delete", "vs Arrays tradeoffs"],
            "teaching_notes": "Draw nodes and arrows on paper — visual learners need this. Compare to arrays."
        },
        "stacks_queues": {
            "display_name": "Stacks & Queues",
            "tier": 2,
            "prerequisites": ["arrays_intro"],
            "description": "LIFO and FIFO data structures",
            "key_concepts": ["Stack (LIFO)", "push/pop/peek", "Queue (FIFO)",
                             "enqueue/dequeue", "Applications", "Implementation with arrays/lists"],
            "teaching_notes": "Stack of plates (LIFO), queue at a shop (FIFO). Real-world analogies are key."
        },
        "hash_tables": {
            "display_name": "Hash Tables",
            "tier": 2,
            "prerequisites": ["arrays_intro"],
            "description": "Key-value storage with O(1) average lookup",
            "key_concepts": ["Hash function", "Buckets", "Collision handling",
                             "Chaining vs open addressing", "Load factor", "O(1) average case"],
            "teaching_notes": "Connect to Python dicts and Java HashMaps students already know."
        },
        "trees_intro": {
            "display_name": "Trees & Binary Trees",
            "tier": 3,
            "prerequisites": ["linked_lists"],
            "description": "Hierarchical data structures",
            "key_concepts": ["Root", "Parent/child/leaf nodes", "Height/depth",
                             "Binary tree", "Tree traversal (inorder/preorder/postorder)"],
            "teaching_notes": "File system is a great real-world tree example."
        },
        "binary_search_tree": {
            "display_name": "Binary Search Trees",
            "tier": 3,
            "prerequisites": ["trees_intro"],
            "description": "Ordered trees for efficient search",
            "key_concepts": ["BST property", "Insert", "Search", "Delete",
                             "Balanced vs unbalanced", "O(log n) vs O(n) worst case"],
            "teaching_notes": "Show how an unbalanced BST degrades to O(n) — motivates AVL/balanced trees."
        },
        "sorting": {
            "display_name": "Sorting Algorithms",
            "tier": 2,
            "prerequisites": ["arrays_intro", "big_o"],
            "description": "Classic algorithms for ordering data",
            "key_concepts": ["Bubble sort O(n²)", "Selection sort O(n²)",
                             "Insertion sort O(n²)", "Merge sort O(n log n)",
                             "Quick sort O(n log n) avg", "Stability"],
            "teaching_notes": "Always trace through small arrays by hand. Visualise comparisons and swaps."
        },
        "searching": {
            "display_name": "Searching Algorithms",
            "tier": 2,
            "prerequisites": ["arrays_intro", "big_o"],
            "description": "Finding elements efficiently",
            "key_concepts": ["Linear search O(n)", "Binary search O(log n)",
                             "Precondition (sorted)", "Iterative vs recursive binary search"],
            "teaching_notes": "Binary search is a perfect introduction to divide-and-conquer."
        },
        "recursion_dsa": {
            "display_name": "Recursion",
            "tier": 2,
            "prerequisites": ["arrays_intro"],
            "description": "Solving problems by breaking them into smaller versions",
            "key_concepts": ["Base case", "Recursive case", "Call stack",
                             "Factorial", "Fibonacci", "When to use recursion vs iteration"],
            "teaching_notes": "Draw the call stack. Stack overflow is a real risk with deep recursion."
        },
        "graphs_intro": {
            "display_name": "Graphs",
            "tier": 4,
            "prerequisites": ["trees_intro", "hash_tables"],
            "description": "Networks of nodes and edges",
            "key_concepts": ["Vertices & edges", "Directed vs undirected", "Weighted graphs",
                             "Adjacency matrix vs list", "BFS", "DFS"],
            "teaching_notes": "Social networks, maps, and the internet are all graphs — great motivation."
        },
        "dynamic_programming": {
            "display_name": "Dynamic Programming",
            "tier": 4,
            "prerequisites": ["recursion_dsa", "big_o"],
            "description": "Optimising recursive solutions with memoisation",
            "key_concepts": ["Overlapping subproblems", "Optimal substructure",
                             "Memoisation (top-down)", "Tabulation (bottom-up)",
                             "Classic problems (knapsack, Fibonacci, LCS)"],
            "teaching_notes": "Start with Fibonacci memoisation — instantly shows the speedup from DP."
        },
    }
}