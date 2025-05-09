import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def preprocess_data(X_train: pd.DataFrame, y_train: pd.DataFrame, merge_col: str, target_col: str, val: bool = False, test_size: float = 0.2, remove_corr: bool = False, corr_threshold: float = 0.95) -> tuple:
    """
    Merge the feature set (X_train) and target (y_train), optionally remove highly correlated features, and split the data into training and validation sets if specified.
    
    Parameters
    ----------
        X_train : pd.DataFrame
            Feature DataFrame.
        y_train : pd.DataFrame
            Target DataFrame.
        merge_col : str
            Column name to merge on.
        target_col : str
            Target column name.
        val : bool, optional
            Whether to split the data into training and validation sets (default is False).
        test_size : float, optional
            Proportion of the dataset to include in the validation split (default is 0.2).
        remove_corr : bool, optional
            Whether to remove highly correlated features (default is False).
        corr_threshold : float, optional
            Correlation threshold for feature removal (default is 0.95).
            
    Returns
    -------
        Touple
            If val is True, returns X_train_split, X_val_split, y_train_split, y_val_split, and dropped_corr_feats.
            If val is False, returns X_processed, y_processed, and dropped_corr_feats."""
    
    merged_data = pd.merge(X_train, y_train, on=merge_col)
    
    if remove_corr:
        X = merged_data.drop(columns=[target_col])
        corr_matrix = X.corr().abs()
        upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        dropped_corr_feats = [column for column in upper_tri.columns if any(upper_tri[column] > corr_threshold)]
        X = X.drop(columns=dropped_corr_feats)
        merged_data = pd.concat([X, merged_data[target_col]], axis=1)
        
    X_processed = merged_data.drop(columns=[target_col])
    y_processed = merged_data[target_col]
    
    if val:
        X_train_split, X_val_split, y_train_split, y_val_split = train_test_split(X_processed, y_processed, test_size=test_size, random_state=42)
        return X_train_split, X_val_split, y_train_split, y_val_split, dropped_corr_feats
    else:
        return X_processed, y_processed, dropped_corr_feats




def recommend_approach(X_train_split: pd.DataFrame, y_train_split: pd.DataFrame) -> dict:
    """
    Recommends a modeling approach based on the characteristics of the dataset.
    It suggests appropriate models, checks for data imbalance, and recommends 
    strategies to prevent overfitting.
    
    Parameters:
    ----------
    X_train_split : pd.DataFrame
        The feature dataset (excluding target column).
    y_train_split : pd.DataFrame
        The target DataFrame containing the target column.
    
    Returns:
    -------
    dict
        A dictionary containing recommended models and strategies to prevent overfitting.
    """
    
    recommendations = {}
    
    # Basic dataset characteristics
    n_samples, n_features = X_train_split.shape
    recommendations['dataset_info'] = {
        'samples': n_samples,
        'features': n_features,
        'feature_types': dict(X_train_split.dtypes.value_counts().items())
    }

    # Determine if it's a classification or regression task based on the target variable
    unique_values = y_train_split.nunique()
    if y_train_split.dtype == 'bool' or (pd.api.types.is_numeric_dtype(y_train_split) and unique_values <= 10):
        task_type = "classification"
        
        # Determine if binary or multiclass
        if unique_values <= 2:
            recommendations['task'] = "binary classification"
        else:
            recommendations['task'] = "multiclass classification"
    else:
        task_type = "regression"
        recommendations['task'] = "regression"
    
    # Check if the data is imbalanced (for classification tasks)
    if task_type == "classification":
        class_counts = y_train_split.value_counts(normalize=True)
        imbalance_ratio = class_counts.min() / class_counts.max()
        
        if imbalance_ratio < 0.1:
            recommendations['imbalance'] = {
                'status': "Severe imbalance detected",
                'ratio': float(imbalance_ratio),
                'suggestions': [
                    "Use SMOTE or other oversampling techniques",
                    "Consider class weights in your model",
                    "Use precision-recall curves instead of ROC curves for evaluation",
                    "Look at F1-score or balanced accuracy instead of accuracy"
                ]
            }
        elif imbalance_ratio < 0.25:
            recommendations['imbalance'] = {
                'status': "Moderate imbalance detected",
                'ratio': float(imbalance_ratio),
                'suggestions': [
                    "Consider class weights in your model",
                    "Ensemble methods like Random Forest or Gradient Boosting often handle moderate imbalance well"
                ]
            }
        else:
            recommendations['imbalance'] = {
                'status': "The data is relatively balanced",
                'ratio': float(imbalance_ratio),
                'suggestions': ["Standard modeling techniques should work well"]
            }
    
    # Dataset size considerations
    if n_samples < 1000:
        recommendations['dataset_size'] = {
            'status': "Small dataset",
            'suggestions': [
                "Use simpler models to avoid overfitting",
                "Consider cross-validation with more folds",
                "Feature selection may be important",
                "Data augmentation techniques might help"
            ]
        }
    elif n_samples < 10000:
        recommendations['dataset_size'] = {
            'status': "Medium dataset",
            'suggestions': [
                "Both simple and complex models may work well",
                "Standard cross-validation should be sufficient"
            ]
        }
    else:
        recommendations['dataset_size'] = {
            'status': "Large dataset",
            'suggestions': [
                "Complex models like deep learning or gradient boosting may work well",
                "Consider using a validation set instead of cross-validation for faster iteration"
            ]
        }
    
    # Feature space considerations
    if n_features > 100:
        recommendations['feature_space'] = {
            'status': "High-dimensional data",
            'suggestions': [
                "Consider dimensionality reduction techniques (PCA, UMAP)",
                "Feature selection methods may be important",
                "Regularization will be critical to prevent overfitting",
                "Tree-based models may struggle with very high dimensions"
            ]
        }
    
    # Recommend models based on the task type and data characteristics
    recommendations['recommended_models'] = []
    
    if task_type == "classification":
        if unique_values <= 2:  # Binary classification
            recommendations['recommended_models'].append({
                'name': "Logistic Regression",
                'strengths': ["Good interpretability", "Works well with linear decision boundaries", "Fast to train", "Provides probabilities"],
                'weaknesses': ["May underperform with complex, non-linear relationships", "Sensitive to outliers"],
                'hyperparameters': ["C (regularization strength)", "penalty type (L1/L2)"]
            })
        else:  # Multiclass classification
            recommendations['recommended_models'].append({
                'name': "Multinomial Logistic Regression",
                'strengths': ["Good interpretability", "Works well with linear decision boundaries", "Fast to train"],
                'weaknesses': ["May underperform with complex, non-linear relationships", "Sensitive to outliers"],
                'hyperparameters': ["C (regularization strength)", "penalty type (L1/L2)"]
            })
        
        recommendations['recommended_models'].append({
            'name': "Random Forest Classifier",
            'strengths': ["Handles non-linear relationships well", "Good with high-dimensional data", "Robust to outliers", "Provides feature importance"],
            'weaknesses': ["Less interpretable than linear models", "Can be computationally intensive with large datasets"],
            'hyperparameters': ["n_estimators", "max_depth", "min_samples_leaf", "max_features"]
        })
        
        recommendations['recommended_models'].append({
            'name': "Gradient Boosting Classifier",
            'strengths': ["Often achieves state-of-the-art performance", "Handles non-linear relationships well", "Good with imbalanced data"],
            'weaknesses': ["More prone to overfitting than Random Forest", "More hyperparameters to tune", "Less interpretable"],
            'hyperparameters': ["learning_rate", "n_estimators", "max_depth", "subsample"]
        })
    
    else:  # Regression
        recommendations['recommended_models'].append({
            'name': "Linear Regression",
            'strengths': ["Excellent interpretability", "Fast to train", "Works well when relationships are linear"],
            'weaknesses': ["Cannot capture non-linear relationships", "Sensitive to outliers"],
            'hyperparameters': ["None for basic linear regression"]
        })
        
        recommendations['recommended_models'].append({
            'name': "Ridge Regression",
            'strengths': ["Good for handling multicollinearity", "L2 regularization helps with overfitting", "Still maintains interpretability"],
            'weaknesses': ["Still limited to linear relationships"],
            'hyperparameters': ["alpha (regularization strength)"]
        })
        
        recommendations['recommended_models'].append({
            'name': "Lasso Regression",
            'strengths': ["Good for feature selection", "L1 regularization produces sparse models", "Works well with high-dimensional data"],
            'weaknesses': ["Still limited to linear relationships"],
            'hyperparameters': ["alpha (regularization strength)"]
        })
        
        recommendations['recommended_models'].append({
            'name': "Random Forest Regressor",
            'strengths': ["Handles non-linear relationships well", "Robust to outliers", "Provides feature importance"],
            'weaknesses': ["Less interpretable than linear models", "Can be computationally intensive"],
            'hyperparameters': ["n_estimators", "max_depth", "min_samples_leaf", "max_features"]
        })
        
        recommendations['recommended_models'].append({
            'name': "Gradient Boosting Regressor",
            'strengths': ["Often achieves state-of-the-art performance", "Handles non-linear relationships well"],
            'weaknesses': ["More prone to overfitting than Random Forest", "More hyperparameters to tune", "Less interpretable"],
            'hyperparameters': ["learning_rate", "n_estimators", "max_depth", "subsample"]
        })

    # Suggest strategies to combat overfitting
    recommendations['overfitting_strategies'] = {
        'general': [
            "Use cross-validation to estimate model performance",
            "Monitor training vs. validation performance",
            "Start with simpler models and increase complexity as needed"
        ],
        'regularization': [
            "For linear models: Add L1 or L2 regularization (Ridge or Lasso)",
            "For tree models: Limit tree depth, increase min_samples_leaf"
        ],
        'data': [
            "Feature selection to reduce dimensionality",
            "More data collection if possible",
            "Data augmentation techniques (where applicable)"
        ]
    }
    
    # Evaluation metrics recommendation
    if task_type == "classification":
        if 'imbalance' in recommendations and recommendations['imbalance']['ratio'] < 0.25:
            # For imbalanced classification
            recommendations['suggested_metrics'] = [
                "Precision", "Recall", "F1-score", "Precision-Recall AUC", 
                "Balanced accuracy", "Cohen's Kappa"
            ]
        else:
            # For balanced classification
            if unique_values <= 2:  # Binary
                recommendations['suggested_metrics'] = [
                    "Accuracy", "ROC AUC", "F1-score", "Precision", "Recall"
                ]
            else:  # Multiclass
                recommendations['suggested_metrics'] = [
                    "Accuracy", "Weighted F1-score", "Macro F1-score", 
                    "Confusion matrix", "Cohen's Kappa"
                ]
    else:
        # For regression
        recommendations['suggested_metrics'] = [
            "R² (coefficient of determination)", "Mean Absolute Error (MAE)",
            "Mean Squared Error (MSE)", "Root Mean Squared Error (RMSE)"
        ]

    return recommendations