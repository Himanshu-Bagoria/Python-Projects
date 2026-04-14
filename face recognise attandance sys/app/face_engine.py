import cv2
from deepface import DeepFace
import numpy as np
import streamlit as st

# Configuration
MODEL_NAME = "SFace"           # Fast & accurate
DETECTOR_BACKEND = "yunet"     # More reliable than opencv
ENFORCE_DETECTION = False
ANTI_SPOOFING = False

# SFace cosine-distance threshold — 0.593 is DeepFace's default, we use 0.65 to be more tolerant
MATCH_THRESHOLD = 0.65

@st.cache_resource
def load_deepface_model():
    """Warms up the DeepFace model cache."""
    DeepFace.build_model(MODEL_NAME)
    return True

def extract_embedding(image):
    """
    Extracts face embedding using DeepFace.
    Returns (embedding_list, status_string).
    """
    try:
        load_deepface_model()

        results = DeepFace.represent(
            image,
            model_name=MODEL_NAME,
            enforce_detection=ENFORCE_DETECTION,
            detector_backend=DETECTOR_BACKEND,
        )
        if results and len(results) > 0:
            return results[0]["embedding"], "Success"

    except Exception as e:
        print(f"[face_engine] extract_embedding error: {e}")
        # Fallback: try with opencv if yunet fails
        try:
            results = DeepFace.represent(
                image,
                model_name=MODEL_NAME,
                enforce_detection=False,
                detector_backend="opencv",
            )
            if results and len(results) > 0:
                return results[0]["embedding"], "Success"
        except Exception as e2:
            print(f"[face_engine] fallback error: {e2}")

    return None, "Error"


def _cosine_distance(a, b):
    """Safe cosine distance between two lists/arrays."""
    a = np.array(a, dtype=np.float64)
    b = np.array(b, dtype=np.float64)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 1.0
    return 1 - np.dot(a, b) / (norm_a * norm_b)


def get_best_match(target_embedding, user_profiles, threshold=MATCH_THRESHOLD):
    """
    Finds the best matching user from a list of profiles.
    user_profiles: list of dicts with 'id', 'name', 'embedding'
    """
    best_match = None
    min_dist = float("inf")

    for profile in user_profiles:
        stored_emb = profile.get("embedding")
        if stored_emb is None:
            continue
        try:
            dist = _cosine_distance(target_embedding, stored_emb)
            print(f"[face_engine] {profile['name']} → dist={dist:.4f} (threshold={threshold})")
            if dist < threshold and dist < min_dist:
                min_dist = dist
                best_match = profile
        except Exception as e:
            print(f"[face_engine] compare error for {profile.get('name')}: {e}")

    return best_match
