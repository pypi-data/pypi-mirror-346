import requests
from anyvec.exceptions import APIConnectionError
import numpy as np


class Vectorizer:
    def __init__(self, client):
        self.client = client

    def vectorize(self, text: str, images: list[bytes]):
        """
        Vectorizes a file and returns the vector

        Args:
            text (str): Text content.
            images list[bytes]: Image content.
            file_name (str): Full file name (e.g., "document.pdf").
            **kwargs: Additional parameters.
        Returns:
            dict: Success status and collection name.
        """
        req_body = {
            "texts": [text],
            "images": images,
        }
        
        try:
            res = requests.post(self.client.url + "/vectorize", json=req_body)
            resBody = res.json()
            text_vectors = resBody["textVectors"]
            image_vectors = resBody["imageVectors"]

            vectors = np.array(text_vectors + image_vectors)
            aggregated_vector = np.mean(vectors, axis=0)
            return aggregated_vector.tolist()

        except requests.RequestException as e:
            raise APIConnectionError(self.client.url, f"Request failed: {e}")
