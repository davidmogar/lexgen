import codecs
import json
import os

from .lib import facepp

CACHE_FILE = os.path.join(os.path.dirname(__file__), 'data/facepp_cache.tsv')


class Faces:

    cache = {}

    def __init__(self, key, secret, server='http://api.us.faceplusplus.com/'):
        self._load_cache()
        self._api = facepp.API(key, secret, server)

    def get_gender_and_confidence(self, profile_image):
        """
        Try to detect a single face on an image and returns the gender of the person and
        value indicating the prediction confidence.

        Params:
            profile_image(string): URL of the image to process.

        Returns:
            The gender detected and the prediction confidence.
        """
        valid_answer = True

        if profile_image in self._faces.cache:
            answer = self._facepp.cache[profile_image]
        else:
            try:
                answer = self._api.detection.detect(url=profile_image)
            except facepp.APIError:
                valid_answer = False

        if valid_answer and len(answer['face']) == 1:
            self.cache[profile_image] = answer
            gender = answer['face'][0]['attribute']['gender']['value']
            confidence = answer['face'][0]['attribute']['gender']['confidence']
            return gender, confidence
        else:
            return None

    def _load_cache(self):
        """
        Load cached data if it was generated previously.
        """
        try:
            with codecs.open(CACHE_FILE, 'r', 'UTF-8') as file:
                for line in file:
                    url, json_data = line.split('\t')
                    self.cache[url] = json.loads(json_data)
        except FileNotFoundError:
            pass