COURSE = {
    "id": "data_science",
    "display_name": "Data Science",
    "description": "From data manipulation to machine learning and visualization",
    "icon": "📊",
    "type": "data_science",
    
    "topics": {
        # TIER 1 - Foundations
        "numpy_basics": {
            "display_name": "NumPy Basics",
            "tier": 1,
            "prerequisites": [],
            "description": "Numerical computing with arrays",
            "key_concepts": ["Arrays", "Shape", "Indexing", "Vectorization", "Broadcasting", "ufuncs"],
            "teaching_notes": "NumPy arrays are the foundation of data science. Emphasize vectorization over loops."
        },
        "pandas_series": {
            "display_name": "Pandas Series",
            "tier": 1,
            "prerequisites": ["numpy_basics"],
            "description": "One-dimensional labeled arrays",
            "key_concepts": ["Series creation", "Indexing", "Vectorized ops", "Missing data (NaN)", "Boolean filtering"],
            "teaching_notes": "Series = dictionary + array. The index is what makes pandas powerful."
        },
        "data_cleaning": {
            "display_name": "Data Cleaning",
            "tier": 1,
            "prerequisites": ["pandas_series"],
            "description": "Handling messy real-world data",
            "key_concepts": ["Missing values (isnull/dropna/fillna)", "Duplicates", "Data types", "String cleaning", "Outliers"],
            "teaching_notes": "Real data is messy. 80% of data science is cleaning. Teach practical regex for text cleaning."
        },

        # TIER 2 - Core Data Analysis
        "pandas_dataframes": {
            "display_name": "Pandas DataFrames",
            "tier": 2,
            "prerequisites": ["pandas_series", "data_cleaning"],
            "description": "Two-dimensional tabular data",
            "key_concepts": ["DataFrame creation", "loc vs iloc", "GroupBy", "Aggregation", "Merge/Join", "Pivot tables"],
            "teaching_notes": "SQL-like operations in pandas. groupby().agg() is the most powerful pattern."
        },
        "data_visualization": {
            "display_name": "Data Visualization",
            "tier": 2,
            "prerequisites": ["pandas_dataframes"],
            "description": "Communicating insights through plots",
            "key_concepts": ["Matplotlib basics", "Seaborn", "Plot types (bar/line/scatter/hist)", "Customization", "Subplots"],
            "teaching_notes": "Start with seaborn for beautiful defaults. Teach what each plot type reveals."
        },
        "eda": {
            "display_name": "Exploratory Data Analysis (EDA)",
            "tier": 2,
            "prerequisites": ["pandas_dataframes", "data_visualization"],
            "description": "Systematic exploration of datasets",
            "key_concepts": ["Summary statistics (describe)", "Correlation", "Distribution analysis", "Missing patterns", "Feature relationships"],
            "teaching_notes": "EDA is a cycle: visualize → ask → transform → repeat. No single 'right' approach."
        },

        # TIER 3 - Advanced Analytics
        "statistics": {
            "display_name": "Statistics for Data Science",
            "tier": 3,
            "prerequisites": ["eda"],
            "description": "Statistical foundations",
            "key_concepts": ["Descriptive stats", "Probability distributions", "Hypothesis testing", "Confidence intervals", "p-values"],
            "teaching_notes": "Connect concepts to pandas code (mean/median/std, scipy stats tests)."
        },
        "feature_engineering": {
            "display_name": "Feature Engineering",
            "tier": 3,
            "prerequisites": ["pandas_dataframes", "statistics"],
            "description": "Creating better features for models",
            "key_concepts": ["Scaling/Normalization", "Encoding categories", "Feature creation", "Feature selection", "Polynomial features"],
            "teaching_notes": "Better features beat better models. Domain knowledge is crucial here."
        },
        "time_series": {
            "display_name": "Time Series Analysis",
            "tier": 3,
            "prerequisites": ["pandas_dataframes", "statistics"],
            "description": "Working with temporal data",
            "key_concepts": ["DatetimeIndex", "Resampling", "Rolling windows", "Trend/Seasonality", "Forecasting basics"],
            "teaching_notes": "Time series has special challenges: no random sampling, autocorrelation, trends."
        },
    }
}