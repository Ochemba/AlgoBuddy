COURSE = {
    "id": "data_engineering",
    "display_name": "Data Engineering",
    "description": "Building robust data pipelines and infrastructure",
    "icon": "⚙️",
    "type": "data_engineering",
    
    "topics": {
        # TIER 1 - Foundations
        "sql_advanced": {
            "display_name": "Advanced SQL",
            "tier": 1,
            "prerequisites": [],
            "description": "Complex queries and optimization",
            "key_concepts": ["Window functions", "CTEs", "Subqueries", "Indexing", "Query optimization", "Transactions"],
            "teaching_notes": "Window functions (ROW_NUMBER, LAG, LEAD) are essential for data engineers."
        },
        "etl_basics": {
            "display_name": "ETL Fundamentals",
            "tier": 1,
            "prerequisites": ["sql_advanced"],
            "description": "Extract, Transform, Load patterns",
            "key_concepts": ["Extract from APIs/DBs", "Transform with pandas", "Load strategies", "Incremental loads", "Idempotency"],
            "teaching_notes": "ETL vs ELT (modern approach). Always design for rerunnability."
        },
        "data_modeling": {
            "display_name": "Data Modeling",
            "tier": 1,
            "prerequisites": ["sql_advanced"],
            "description": "Designing efficient data structures",
            "key_concepts": ["Star schema", "Snowflake schema", "Normalization", "Denormalization", "Fact vs Dimension tables"],
            "teaching_notes": "Kimball vs Inmon. Star schemas are standard for analytics."
        },

        # TIER 2 - Core Engineering
        "airflow_basics": {
            "display_name": "Apache Airflow",
            "tier": 2,
            "prerequisites": ["etl_basics"],
            "description": "Workflow orchestration",
            "key_concepts": ["DAGs", "Operators", "Tasks", "Sensors", "XComs", "Task dependencies"],
            "teaching_notes": "Airflow = Python code defining workflows. DAGs should be idempotent."
        },
        "data_warehousing": {
            "display_name": "Data Warehousing",
            "tier": 2,
            "prerequisites": ["data_modeling"],
            "description": "Cloud data warehouses",
            "key_concepts": ["Columnar storage", "Partitioning", "Clustering", "Materialized views", "Warehouse vs Lake"],
            "teaching_notes": "Snowflake/BigQuery/Redshift. Columnar storage changes performance considerations."
        },
        "pipeline_testing": {
            "display_name": "Pipeline Testing",
            "tier": 2,
            "prerequisites": ["etl_basics", "airflow_basics"],
            "description": "Ensuring data quality",
            "key_concepts": ["Data validation (Great Expectations)", "Unit tests for transforms", "Integration tests", "Data contracts"],
            "teaching_notes": "Test data, not just code. Great Expectations is the industry standard."
        },

        # TIER 3 - Advanced
        "streaming": {
            "display_name": "Streaming Data",
            "tier": 3,
            "prerequisites": ["etl_basics"],
            "description": "Real-time data processing",
            "key_concepts": ["Kafka", "Event streaming", "Windowed aggregations", "Exactly-once semantics", "CDC"],
            "teaching_notes": "Streaming is hard. Start with batch mental model, then add time windows."
        },
        "dbt": {
            "display_name": "dbt (Data Build Tool)",
            "tier": 3,
            "prerequisites": ["sql_advanced", "data_modeling"],
            "description": "Transformations in the warehouse",
            "key_concepts": ["Models", "Materializations", "Tests", "Documentation", "Macros", "Lineage"],
            "teaching_notes": "dbt brings software engineering best practices to SQL transformations."
        },
        "data_ops": {
            "display_name": "DataOps",
            "tier": 3,
            "prerequisites": ["airflow_basics", "pipeline_testing"],
            "description": "CI/CD for data pipelines",
            "key_concepts": ["Version control for data", "Environment promotion", "Monitoring/Alerting", "Data observability"],
            "teaching_notes": "Apply DevOps principles to data. Data versioning (dvc) is powerful."
        },
    }
}