import hashlib
import os
import sys
from datetime import datetime

from organise_tv_shows.processor.steps.step import Step


class HashStep(Step):
    @staticmethod
    def hash_for_file(path, block_size=256 * 128):
        blake2b = hashlib.blake2b()

        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(block_size), b''):
                blake2b.update(chunk)

        return blake2b.hexdigest()

    def process(self, media, config):
        if not config.hash_check:
            return True

        if media.extension == '.hash':
            # Skip processing the hash file itself
            return False

        hash_file_path = media.path + '.hash'

        if not os.path.exists(hash_file_path):
            sys.stderr.write(f'{datetime.now()}: hash file missing for {media.filename}\n')
            return False

        with open(hash_file_path, 'r') as hash_file:
            hash = hash_file.read().lower().strip()

        if self.hash_for_file(media.path) != hash:
            sys.stderr.write(f'{datetime.now()}: hash hash is incorrect for {media.filename}\n')
            return False

        return True
