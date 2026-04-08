import face_recognition
import numpy as np
from PIL import Image
import io


def generate_face_descriptor(file_bytes: bytes):
    try:
        # Convertir bytes a imagen
        image = Image.open(io.BytesIO(file_bytes))
        image = np.array(image)
    except:
        return None

    # Detectar rostro
    face_locations = face_recognition.face_locations(image)

    if len(face_locations) == 0:
        return None

    # Obtener encoding
    face_encodings = face_recognition.face_encodings(image, face_locations)

    return face_encodings[0].tolist()