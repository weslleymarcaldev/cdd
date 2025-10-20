# cdd/core/common.py
import streamlit as st
import pandas as pd
import numpy as np
from core.io import read_json
import datetime as dt

__all__ = ["st", "pd", "np", "dt", "read_json", "lazy"]


class lazy:
    @staticmethod
    def sklearn():
        from sklearn.pipeline import Pipeline
        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import OneHotEncoder, StandardScaler
        from sklearn.linear_model import LogisticRegression, LinearRegression
        from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
        from sklearn.model_selection import train_test_split
        from sklearn.impute import SimpleImputer
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

        return {
            "Pipeline": Pipeline,
            "ColumnTransformer": ColumnTransformer,
            "OneHotEncoder": OneHotEncoder,
            "StandardScaler": StandardScaler,
            "LogisticRegression": LogisticRegression,
            "LinearRegression": LinearRegression,
            "RandomForestClassifier": RandomForestClassifier,
            "RandomForestRegressor": RandomForestRegressor,
            "train_test_split": train_test_split,
            "SimpleImputer": SimpleImputer,
            "accuracy_score": accuracy_score,
            "confusion_matrix": confusion_matrix,
            "f1_score": f1_score,
            "mean_absolute_error": mean_absolute_error,
            "mean_squared_error": mean_squared_error,
            "precision_score": precision_score,
            "r2_score": r2_score,
            "recall_score": recall_score,
        }
