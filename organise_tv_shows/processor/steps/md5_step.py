import hashlib
import os
import sys
from datetime import datetime

from organise_tv_shows.processor.steps.step import Step


class Md5Step(Step):
    @staticmethod
    def md5_for_file(path, block_size=256*128):
        md5 = hashlib.md5()

        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(block_size), b''):
                md5.update(chunk)

        return md5.hexdigest()

    def process(self, media, config):
        if not config.md5_check:
            return True

        if media.extension == '.md5':
            # Skip processing the md5 file itself
            return False

        md5_file_path = media.path + '.md5'

        if not os.path.exists(md5_file_path):
            sys.stderr.write(f'{datetime.now()}: MD5 file missing for {media.filename}\n')
            return False

        with open(md5_file_path, 'r') as md5_file:
            md5_hash = md5_file.read().lower().strip()

        if self.md5_for_file(media.path) != md5_hash:
            sys.stderr.write(f'{datetime.now()}: MD5 hash is incorrect for {media.filename}\n')
            return False

        return True
