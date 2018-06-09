import hashlib
import random

id_bits = 128


class Utils:
    @staticmethod
    def largest_differing_bit(value1, value2):
        distance = value1 ^ value2
        length = -1
        while distance:
            distance >>= 1
            length += 1
        return max(0, length)

    @staticmethod
    def hash_function(data, algo='sha256'):
        if algo == 'md5':
            return int(hashlib.md5(data.encode('ascii')).hexdigest(), 16)
        if algo == 'sha256':
            return int(hashlib.sha256(data.encode('utf8')).hexdigest(), 16)

    @staticmethod
    def random_id(seed=None):
        if seed:
            random.seed(seed)
        return random.randint(0, (2 ** id_bits) - 1)

