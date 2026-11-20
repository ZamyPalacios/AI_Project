"""Simple genre recommender powered by a K-nearest neighbors classifier."""

import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


FEATURE_COLUMNS = ["action", "comedy", "drama", "science_fiction"]
TARGET_COLUMN = "recommendation"

DATA = pd.DataFrame(
    [
        [5, 1, 1, 2, "Action"],
        [4, 1, 2, 1, "Action"],
        [5, 2, 1, 1, "Action"],
        [4, 1, 1, 2, "Action"],
        [1, 5, 2, 1, "Comedy"],
        [2, 4, 1, 1, "Comedy"],
        [1, 5, 1, 2, "Comedy"],
        [2, 4, 2, 1, "Comedy"],
        [1, 2, 5, 1, "Drama"],
        [2, 1, 4, 1, "Drama"],
        [1, 1, 5, 2, "Drama"],
        [1, 2, 4, 2, "Drama"],
        [4, 1, 1, 5, "Science Fiction"],
        [5, 1, 2, 4, "Science Fiction"],
        [4, 2, 1, 5, "Science Fiction"],
        [5, 1, 1, 4, "Science Fiction"],
    ],
    columns=FEATURE_COLUMNS + [TARGET_COLUMN],
)

X = DATA[FEATURE_COLUMNS]
y = DATA[TARGET_COLUMN]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y,
)

MODEL = KNeighborsClassifier(n_neighbors=3)
MODEL.fit(X_train, y_train)


def evaluate() -> float:
    """Return the classifier's accuracy on the held-out test data."""
    return accuracy_score(y_test, MODEL.predict(X_test))


def recommend(preferences: dict[str, float]) -> str:
    """Recommend a genre from 1-5 ratings for each supported genre."""
    missing = [feature for feature in FEATURE_COLUMNS if feature not in preferences]
    if missing:
        raise ValueError(f"Missing preference ratings for: {', '.join(missing)}")

    user_features = pd.DataFrame(
        [{feature: preferences[feature] for feature in FEATURE_COLUMNS}],
        columns=FEATURE_COLUMNS,
    )
    try:
        user_features = user_features.astype(float)
    except (TypeError, ValueError) as error:
        raise ValueError("Preference ratings must be numbers from 1 to 5.") from error

    if user_features.isna().any().any() or (
        (user_features < 1) | (user_features > 5)
    ).any().any():
        raise ValueError("Preference ratings must be numbers from 1 to 5.")

    return str(MODEL.predict(user_features)[0])


if __name__ == "__main__":
    print(f"Accuracy: {evaluate():.2f}")
    sample_preferences = {
        "action": 4,
        "comedy": 1,
        "drama": 2,
        "science_fiction": 5,
    }
    print(f"Recommendation: {recommend(sample_preferences)}")