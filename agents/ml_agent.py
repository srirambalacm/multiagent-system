import os
import re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, r2_score, root_mean_squared_error
from agents.base_agent import BaseAgent


class MLAgent(BaseAgent):
    name = "MLAgent"

    def handle(self, prompt: str, csv_path: str = None) -> str:
        if not csv_path:
            return f"[{self.name}] I need a CSV file to build a model. Please provide a file path."
        if not os.path.exists(csv_path):
            return f"[{self.name}] Could not find file: {csv_path}"
        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            return f"[{self.name}] Could not read the CSV: {e}"

        target = self.detect_target(prompt, df.columns)
        if target is None:
            cols = ", ".join(df.columns)
            return (f"[{self.name}] I couldn't tell which column to predict. "
                    f"Mention one of these in your question: {cols}")

        return self.build_model(df, target)

    def detect_target(self, prompt, columns):
        p = prompt.lower()
        candidates = []
        for col in columns:
            variants = {col.lower(), col.lower().replace("_", " "), col.lower().split("_")[-1]}
            for v in variants:
                candidates.append((v, col))
        # most specific (longest) phrase wins
        candidates.sort(key=lambda x: len(x[0]), reverse=True)
        for v, col in candidates:
            if re.search(r"\b" + re.escape(v) + r"\b", p):
                return col
        return None

    def build_model(self, df, target):
        df = df.dropna(subset=[target])
        y = df[target]
        X = pd.get_dummies(df.drop(columns=[target]))

        # Decide classification vs regression
        is_classification = (not pd.api.types.is_numeric_dtype(y)) or (y.nunique() <= 10)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42
        )

        lines = [f"[{self.name}] Building a model to predict '{target}'"]

        if is_classification:
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            acc = accuracy_score(y_test, preds)
            lines.append("Problem type: Classification")
            lines.append(f"Accuracy: {acc:.2%}")
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            r2 = r2_score(y_test, preds)
            rmse = root_mean_squared_error(y_test, preds)
            lines.append("Problem type: Regression")
            lines.append(f"R-squared: {r2:.3f}")
            lines.append(f"RMSE: {rmse:,.2f}")

        # Top feature importances
        importances = sorted(
            zip(X.columns, model.feature_importances_),
            key=lambda t: t[1], reverse=True
        )[:5]
        lines.append("")
        lines.append("Most important features:")
        for feat, imp in importances:
            lines.append(f"  {feat}: {imp:.3f}")

        return "\n".join(lines)