import face_recognition


"""
    Calculate_face_encoding take image path and generate the face encoding .
    It requries face_recognition==1.3.0 package . :)

    Args:
        image_path (str): A path of image file. example "./image.png".

    Returns:
         numpy.ndarray : Return a 128 points array of face_encoding of given image.
"""

def calculate_face_encoding(img_path):
    image = face_recognition.load_image_file(img_path)
    face_encoding = face_recognition.face_encodings(image)[0]
    return face_encoding