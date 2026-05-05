import os
import io
import numpy as np
from PIL import Image

# Intentar importar la librería nativa opcionalmente
try:
    import face_recognition  # type: ignore
    FACE_RECO_AVAILABLE = True
except Exception:
    face_recognition = None
    FACE_RECO_AVAILABLE = False


def _face_unavailable_error():
    raise RuntimeError(
        "Face recognition functionality is not available in this environment. "
        "Install native dependencies or deploy via Docker with native libs."
    )


def generate_face_descriptor(file_bytes: bytes):
    """Genera un descriptor facial para una sola cara.

    Lanza RuntimeError si la librería nativa no está disponible.
    """
    if not FACE_RECO_AVAILABLE or os.environ.get("FACE_RECO_ENABLED", "1") == "0":
        _face_unavailable_error()

    try:
        image = Image.open(io.BytesIO(file_bytes))
        image = np.array(image)
    except Exception:
        return None

    face_locations = face_recognition.face_locations(image)

    if len(face_locations) == 0:
        return None

    face_encodings = face_recognition.face_encodings(image, face_locations)

    return face_encodings[0].tolist()


def generate_multiple_descriptors(file_bytes: bytes):
    """Genera descriptores para múltiples caras en una imagen.

    Lanza RuntimeError si la librería nativa no está disponible.
    """
    if not FACE_RECO_AVAILABLE or os.environ.get("FACE_RECO_ENABLED", "1") == "0":
        _face_unavailable_error()

    try:
        image = Image.open(io.BytesIO(file_bytes))
        image = np.array(image)
    except Exception:
        return []

    face_locations = face_recognition.face_locations(image)

    if len(face_locations) == 0:
        return []

    face_encodings = face_recognition.face_encodings(image, face_locations)

    descriptors = [encoding.tolist() for encoding in face_encodings]

    return descriptors