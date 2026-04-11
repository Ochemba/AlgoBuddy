# courses/databases.py - Database Systems / SQL Course Definition

COURSE = {
    "id": "databases",
    "display_name": "Database Systems & SQL",
    "description": "Relational databases, SQL querying, and database design",
    "icon": "🗄️",
    "type": "mixed",  # theory + practical SQL

    "topics": {
        "db_intro": {
            "display_name": "Introduction to Databases",
            "tier": 1,
            "prerequisites": [],
            "description": "What databases are and why we use them",
            "key_concepts": ["Database vs file storage", "DBMS", "Relational vs non-relational",
                             "Tables, rows, columns", "Schema", "ACID properties intro"],
            "teaching_notes": "Spreadsheet analogy works well. Ask students where data is stored in apps they use."
        },
        "sql_basics": {
            "display_name": "SQL Basics: SELECT",
            "tier": 1,
            "prerequisites": ["db_intro"],
            "description": "Querying data with SELECT statements",
            "key_concepts": ["SELECT", "FROM", "WHERE", "ORDER BY", "LIMIT",
                             "Comparison operators", "AND/OR/NOT", "LIKE", "NULL handling"],
            "teaching_notes": "Start with SELECT * then narrow down. WHERE is where most mistakes happen."
        },
        "sql_functions": {
            "display_name": "SQL Functions & Aggregates",
            "tier": 2,
            "prerequisites": ["sql_basics"],
            "description": "Transforming and summarising data",
            "key_concepts": ["COUNT()", "SUM()", "AVG()", "MIN()", "MAX()",
                             "GROUP BY", "HAVING", "String functions", "Date functions"],
            "teaching_notes": "HAVING vs WHERE is a classic exam question. Nail this distinction."
        },
        "sql_joins": {
            "display_name": "SQL JOINs",
            "tier": 2,
            "prerequisites": ["sql_basics"],
            "description": "Combining data from multiple tables",
            "key_concepts": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN",
                             "JOIN ON condition", "Aliases", "Multiple joins"],
            "teaching_notes": "Venn diagram explanation works well. INNER JOIN is most common — start there."
        },
        "data_modelling": {
            "display_name": "Data Modelling & ERDs",
            "tier": 2,
            "prerequisites": ["db_intro"],
            "description": "Designing database structure before building it",
            "key_concepts": ["Entity", "Attribute", "Relationship", "ER Diagram",
                             "One-to-one", "One-to-many", "Many-to-many", "Cardinality notation"],
            "teaching_notes": "ER diagrams are almost always in exams. Practice drawing them by hand."
        },
        "normalisation": {
            "display_name": "Normalisation",
            "tier": 3,
            "prerequisites": ["data_modelling"],
            "description": "Organising data to reduce redundancy",
            "key_concepts": ["Anomalies (insert/update/delete)", "Functional dependency",
                             "1NF", "2NF", "3NF", "BCNF",
                             "When to denormalise"],
            "teaching_notes": "1NF-3NF are the most tested. Walk through a running example step by step."
        },
        "sql_ddl": {
            "display_name": "SQL DDL: Creating Tables",
            "tier": 2,
            "prerequisites": ["sql_basics", "data_modelling"],
            "description": "Creating and modifying database structure",
            "key_concepts": ["CREATE TABLE", "Data types", "PRIMARY KEY", "FOREIGN KEY",
                             "NOT NULL", "UNIQUE", "DEFAULT", "ALTER TABLE", "DROP TABLE"],
            "teaching_notes": "Constraints are often skipped by beginners but are exam-critical."
        },
        "sql_dml": {
            "display_name": "SQL DML: Modifying Data",
            "tier": 2,
            "prerequisites": ["sql_ddl"],
            "description": "Inserting, updating, and deleting data",
            "key_concepts": ["INSERT INTO", "UPDATE ... SET", "DELETE FROM",
                             "WHERE clause importance", "Transactions intro",
                             "COMMIT", "ROLLBACK"],
            "teaching_notes": "Warn about UPDATE/DELETE without WHERE — a classic dangerous mistake."
        },
        "transactions_acid": {
            "display_name": "Transactions & ACID",
            "tier": 3,
            "prerequisites": ["sql_dml"],
            "description": "Ensuring data integrity with transactions",
            "key_concepts": ["Atomicity", "Consistency", "Isolation", "Durability",
                             "BEGIN TRANSACTION", "COMMIT", "ROLLBACK",
                             "Concurrency issues (dirty read, phantom read)"],
            "teaching_notes": "Bank transfer example perfectly illustrates why atomicity matters."
        },
        "indexes": {
            "display_name": "Indexes & Query Optimisation",
            "tier": 4,
            "prerequisites": ["sql_joins", "normalisation"],
            "description": "Making queries faster",
            "key_concepts": ["What an index is", "B-tree indexes", "CREATE INDEX",
                             "When indexes help vs hurt", "EXPLAIN/EXPLAIN ANALYZE",
                             "Query execution plan"],
            "teaching_notes": "Index = book index analogy. Show EXPLAIN output to make it concrete."
        },
    }
}