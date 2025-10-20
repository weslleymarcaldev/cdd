# core/lazy.py preguiçoso
def sklearn():
    # Carrega só quando for chamado
    from sklearn.compose import ColumnTransformer
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LinearRegression, LogisticRegression
    from sklearn.metrics import (
        accuracy_score,
        confusion_matrix,
        f1_score,
        mean_absolute_error,
        mean_squared_error,
        precision_score,
        r2_score,
        recall_score,
    )
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    return {
        "ColumnTransformer": ColumnTransformer,
        "RandomForestClassifier": RandomForestClassifier,
        "RandomForestRegressor": RandomForestRegressor,
        "SimpleImputer": SimpleImputer,
        "LinearRegression": LinearRegression,
        "LogisticRegression": LogisticRegression,
        "accuracy_score": accuracy_score,
        "confusion_matrix": confusion_matrix,
        "f1_score": f1_score,
        "mean_absolute_error": mean_absolute_error,
        "mean_squared_error": mean_squared_error,
        "precision_score": precision_score,
        "r2_score": r2_score,
        "recall_score": recall_score,
        "train_test_split": train_test_split,
        "Pipeline": Pipeline,
        "OneHotEncoder": OneHotEncoder,
        "StandardScaler": StandardScaler,
    }


def tabula():
    import tabula  # requer Java instalado

    return tabula


def camelot():
    import camelot

    return camelot
