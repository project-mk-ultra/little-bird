class Utils:
    @staticmethod
    def largest_differing_bit(value1, value2):
        distance = value1 ^ value2
        length = -1
        while distance:
            distance >>= 1
            length += 1
        return max(0, length)
