COURSE = {
    "id": "machine_learning",
    "display_name": "Machine Learning",
    "description": "From traditional ML to neural networks",
    "icon": "🤖",
    "type": "ml",
    
    "topics": {
        # TIER 1 - Foundations
        "ml_basics": {
            "display_name": "ML Fundamentals",
            "tier": 1,
            "prerequisites": [],
            "description": "Core concepts of machine learning",
            "key_concepts": ["Supervised vs Unsupervised", "Train/Test split", "Features/Labels", "Overfitting/Underfitting", "Bias/Variance"],
            "teaching_notes": "Start with the difference between supervised (predict) and unsupervised (find patterns)."
        },
        "scikit_learn": {
            "display_name": "Scikit-learn",
            "tier": 1,
            "prerequisites": ["ml_basics", "numpy_basics"],
            "description": "Python's ML workhorse",
            "key_concepts": ["fit/predict", "StandardScaler", "Pipeline", "Cross-validation", "GridSearchCV"],
            "teaching_notes": "scikit-learn has a consistent API: fit, predict, transform. This is genius design."
        },
        "linear_regression": {
            "display_name": "Linear Regression",
            "tier": 1,
            "prerequisites": ["scikit_learn", "statistics"],
            "description": "Predicting continuous values",
            "key_concepts": ["Simple/Multiple regression", "R-squared", "Coefficients", "Assumptions", "Regularization (Ridge/Lasso)"],
            "teaching_notes": "The 'Hello World' of ML. Emphasize that correlation ≠ causation."
        },

        # TIER 2 - Core Algorithms
        "classification": {
            "display_name": "Classification",
            "tier": 2,
            "prerequisites": ["scikit_learn"],
            "description": "Predicting categories",
            "key_concepts": ["Logistic regression", "Decision trees", "Random forest", "Confusion matrix", "Precision/Recall", "ROC AUC"],
            "teaching_notes": "Accuracy is misleading for imbalanced classes. Use precision/recall or F1 instead."
        },
        "clustering": {
            "display_name": "Clustering",
            "tier": 2,
            "prerequisites": ["scikit_learn"],
            "description": "Finding natural groupings",
            "key_concepts": ["K-means", "Hierarchical clustering", "DBSCAN", "Elbow method", "Silhouette score"],
            "teaching_notes": "K-means needs K. Elbow method helps. DBSCAN finds arbitrary shapes."
        },
        "model_evaluation": {
            "display_name": "Model Evaluation",
            "tier": 2,
            "prerequisites": ["classification", "linear_regression"],
            "description": "Choosing the best model",
            "key_concepts": ["Cross-validation strategies", "Learning curves", "Validation curves", "Feature importance", "Error analysis"],
            "teaching_notes": "Always hold out a test set. Error analysis tells you what to fix next."
        },

        # TIER 3 - Advanced
        "ensembles": {
            "display_name": "Ensemble Methods",
            "tier": 3,
            "prerequisites": ["classification"],
            "description": "Combining multiple models",
            "key_concepts": ["Bagging (Random Forest)", "Boosting (XGBoost)", "Stacking", "Voting classifiers", "Feature importance"],
            "teaching_notes": "XGBoost often wins competitions. Random Forest is great for baseline."
        },
        "neural_networks": {
            "display_name": "Neural Networks",
            "tier": 3,
            "prerequisites": ["classification"],
            "description": "Deep learning foundations",
            "key_concepts": ["Perceptron", "Activation functions", "Backpropagation", "TensorFlow/PyTorch basics", "Overfitting in NNs"],
            "teaching_notes": "Start with a single neuron (perceptron), then add layers. ReLU > sigmoid for hidden layers."
        },
        "deployment_ml": {
            "display_name": "ML Deployment",
            "tier": 3,
            "prerequisites": ["scikit_learn", "model_evaluation"],
            "description": "Putting models into production",
            "key_concepts": ["Model serialization (pickle/joblib)", "FastAPI for serving", "Docker containers", "Model monitoring", "Feature drift"],
            "teaching_notes": "Deployment is harder than training. Monitor for data/c concept drift in production."
        },
    }
}