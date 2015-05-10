import csv
import json
import os

from .lib import facepp

CACHE_FILE = os.path.join(os.path.dirname(__file__), '../data/facepp_cache.tsv')


class Faces:

    def __init__(self, key, secret, server='http://api.us.faceplusplus.com/'):
        self._cache = {}
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
        already_cached = False

        if profile_image in self._cache:
            answer = self._cache[profile_image]
            already_cached = True
        else:
            try:
                answer = self._api.detection.detect(url=profile_image)
            except facepp.APIError:
                answer = {}

        self._cache[profile_image] = answer
        if not already_cached:
            self._store_answer(profile_image, answer)

        if 'face' in answer and len(answer['face']) == 1:
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
            with open(CACHE_FILE, 'r', encoding='utf-8') as file:
                for line in file:
                    url, json_data = line.split('\t')
                    self._cache[url] = json.loads(json_data.replace('\'', '"'))
        except FileNotFoundError:
            pass

    def _store_answer(self, profile_image, answer):
        """
        Stores an answer from Face++ into the cache file.

        Params:
            profile_image (string): URL of the profile image used in the request.
            answer (dict): Answer returned by Face++.
        """
        with open(CACHE_FILE, 'a+', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow([profile_image, answer])