import pandas as pd
from sklearn.neighbors import NearestNeighbors

LOG_FILE = "data/user_logs.csv"

def recommend_similar_routes(distance, elevation, surface, username=None, k=3):
    try:
        df = pd.read_csv(LOG_FILE)

        if df.empty:
            return ["No user data found."]

        # Optionally filter by username
        if username:
            df = df[df["username"] == username]
            if df.empty:
                return [f"No history found for user '{username}'"]

        # Drop rows with missing surface or route match
        df = df[df["surface"].notnull() & df["matched_route"].notnull()]

        if df.empty or len(df) < k:
            return ["Not enough data to generate recommendations."]

        # Encode surface types
        surface_types = df["surface"].unique().tolist()
        df["surface_encoded"] = df["surface"].apply(lambda x: surface_types.index(x) if x in surface_types else -1)

        features = df[["distance", "elevation", "surface_encoded"]]

        model = NearestNeighbors(n_neighbors=min(k, len(features)))
        model.fit(features)

        input_vector = [[
            distance,
            elevation,
            surface_types.index(surface) if surface in surface_types else -1
        ]]

        distances, indices = model.kneighbors(input_vector)

        return df.iloc[indices[0]]["matched_route"].tolist()

    except Exception as e:
        return [f"Error in recommendation: {e}"]
