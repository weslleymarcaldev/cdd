# cdd/views/ml_demo.py
from core.common import st, pd, np
from core import lazy


def page():
    sk = lazy.sklearn()  # importa na hora
    ColumnTransformer = sk["ColumnTransformer"]
    Pipeline = sk["Pipeline"]
    SimpleImputer = sk["SimpleImputer"]
    StandardScaler = sk["StandardScaler"]
    OneHotEncoder = sk["OneHotEncoder"]

    LogisticRegression = sk["LogisticRegression"]
    LinearRegression = sk["LinearRegression"]
    RandomForestClassifier = sk["RandomForestClassifier"]
    RandomForestRegressor = sk["RandomForestRegressor"]

    train_test_split = sk["train_test_split"]

    accuracy_score = sk["accuracy_score"]
    precision_score = sk["precision_score"]
    recall_score = sk["recall_score"]
    f1_score = sk["f1_score"]
    confusion_matrix = sk["confusion_matrix"]
    mean_absolute_error = sk["mean_absolute_error"]
    mean_squared_error = sk["mean_squared_error"]
    r2_score = sk["r2_score"]
    st.title("ML Demo")
    st.write("Conteúdo inicial da página **ML Demo**. Edite em `views/ml_demo.py`.")
    st.header("ML Demo — do CSV ao modelo")
    st.write(
        "Faça upload de um CSV, escolha a coluna alvo e treine um modelo em minutos."
    )

    up = st.file_uploader("CSV (separador vírgula)", type=["csv"])
    if up is not None:
        df = pd.read_csv(up)
    else:
        st.caption("Sem arquivo? Usando dataset de exemplo (simulado tipo Titanic).")
        df = pd.DataFrame(
            {
                "survived": np.random.randint(0, 2, 500),
                "pclass": np.random.choice([1, 2, 3], 500),
                "sex": np.random.choice(["male", "female"], 500),
                "age": np.random.normal(30, 14, 500).clip(0, 80),
                "fare": np.random.exponential(30, 500).round(2),
                "embarked": np.random.choice(["S", "C", "Q"], 500),
            }
        )

    st.write("Amostra:", df.head())
    target = st.selectbox("Coluna alvo (y)", options=df.columns)
    problem = st.radio("Tipo de problema", ["Classificação", "Regressão"])
    test_size = st.slider("Tamanho do teste (%)", 10, 40, 20, step=5) / 100.0
    random_state = st.number_input("random_state", 0, 10_000, 42)

    X = df.drop(columns=[target])
    y = df[target]
    num_cols = X.select_dtypes(
        include=["int64", "float64", "int32", "float32"]
    ).columns.tolist()
    cat_cols = [c for c in X.columns if c not in num_cols]

    numeric_transform = Pipeline(
        [("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
    )
    categorical_transform = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    pre = ColumnTransformer(
        [
            ("num", numeric_transform, num_cols),
            ("cat", categorical_transform, cat_cols),
        ],
        remainder="drop",
    )

    if problem == "Classificação":
        model_name = st.selectbox("Modelo", ["Logistic Regression", "Random Forest"])
        if model_name == "Logistic Regression":
            C = st.slider("C (regularização)", 0.01, 10.0, 1.0)
            model = LogisticRegression(max_iter=1000, C=C)
        else:
            n_estimators = st.slider("n_estimators", 50, 500, 200, step=50)
            max_depth = st.slider("max_depth", 2, 30, 10)
            model = RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=random_state,
            )
    else:
        model_name = st.selectbox(
            "Modelo", ["Linear Regression", "Random Forest Regressor"]
        )
        if model_name == "Linear Regression":
            model = LinearRegression()
        else:
            n_estimators = st.slider("n_estimators", 50, 500, 200, step=50)
            max_depth = st.slider("max_depth", 2, 30, 10)
            model = RandomForestRegressor(
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=random_state,
            )

    pipe = Pipeline([("preprocess", pre), ("model", model)])

    if st.button("Treinar"):
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=test_size,
                random_state=random_state,
                stratify=y if problem == "Classificação" else None,
            )
            pipe.fit(X_train, y_train)
            preds = pipe.predict(X_test)

            if problem == "Classificação":
                acc = accuracy_score(y_test, preds)
                prec = precision_score(
                    y_test, preds, average="weighted", zero_division=0
                )
                rec = recall_score(y_test, preds, average="weighted", zero_division=0)
                f1 = f1_score(y_test, preds, average="weighted")
                st.success(
                    f"Acurácia: {acc:.3f} | Precisão: {prec:.3f} | Recall: {rec:.3f} | F1: {f1:.3f}"
                )
                st.write("Matriz de confusão:")
                st.dataframe(
                    pd.DataFrame(confusion_matrix(y_test, preds)),
                    use_container_width=True,
                )
            else:
                mae = mean_absolute_error(y_test, preds)
                rmse = mean_squared_error(y_test, preds, squared=False)
                r2 = r2_score(y_test, preds)
                st.success(f"MAE: {mae:.3f} | RMSE: {rmse:.3f} | R²: {r2:.3f}")

            st.info(
                "Modelo está na sessão. Para produção: salve com joblib/pickle e exponha via FastAPI."
            )
            st.session_state["trained_pipe"] = pipe
            st.session_state["feature_cols"] = X.columns.tolist()
        except Exception as e:
            st.error(f"Erro no treino: {e}")

    if "trained_pipe" in st.session_state:
        st.subheader("Predizer novo registro")
        inputs = {}
        for c in X.columns:
            if c in num_cols:
                default_val = (
                    float(X[c].median())
                    if np.issubdtype(X[c].dtype, np.number)
                    else 0.0
                )
                val = st.number_input(f"{c}", value=default_val)
            else:
                val = st.selectbox(
                    f"{c}", options=sorted(X[c].dropna().astype(str).unique().tolist())
                )
            inputs[c] = val
        if st.button("Prever"):
            new = pd.DataFrame([inputs])
            pred = st.session_state["trained_pipe"].predict(new)[0]
            st.success(f"Predição: **{pred}**")
