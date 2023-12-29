class ECurve:
    # secp256k1 curve: y^2 = x^3 + 7 (mod p) where p = 2^256 - 2^32 - 977
    # a = 0, b = 7, p = 2**256 - 2**32 - 977
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def is_on_curve(self, point):
        if not point:
            return False

        x = point.x
        y = point.y
        p = self.p

        # checks if the point satisfies the curve equation y^2 = x^3 + ax + b (mod p)
        return pow(y**2, 1, p) == pow((x**3 + self.a*x + self.b), 1, p)

    def is_infinity_point(self, point):
        return point.x == None and point.y == None

    def tangent(self, point):
        p = self.p

        # slope of the tangent line at point P(x1, y1) on the curve
        # = (3 * x1^2 + a) / (2 * y1)
        # = (3 * x1^2 + a) * (2 * y1)^-1
        return pow((3 * point.x**2 + self.a) * inverse(2 * point.y, p), 1, p)

    def slope(self, point1, point2):
        p = self.p

        # slope of a line passing through P and Q
        #  = (y2 - y1) / (x2 - x1)
        # = (y2 - y1) * (x2 - x1)^-1
        return pow((point2.y - point1.y) * inverse(point2.x - point1.x, p), 1, p)