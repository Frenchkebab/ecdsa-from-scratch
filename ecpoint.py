from utils import inverse 

# A point (x, y) on an elliptic curve over a finite field
class ECPoint:
    # When x and y are None, the point is the infinity point
    def __init__(self, curve, x, y):
        self.curve = curve
        self.x = x
        self.y = y

    def __eq__(self, point):
        return self.curve == point.curve and self.x == point.x and self.y == point.y

    def __add__(self, point):
        p = self.curve.p

        if not self.curve.is_on_curve(point):
            raise Exception("Point is not on curve") 

        # P(x1, y1), Q(x2, y2), R(x3, y3)
        # R = P + Q

        x1 = self.x
        y1 = self.y

        x2 = point.x
        y2 = point.y

        # if P == Infinity Point, then R = Q
        if self.curve.is_infinity_point(self):
            return point

        # if Q == Infinity Point, then R = P
        if self == point:
            return self

        # if P == -Q, then R = Infinity Point
        if self == ECPoint(self.curve, x2, -y2):
            return ECPoint(self.curve, None, None)

        # if P == Q, then R = P + Q = P + P
        if self == point:
            # slope of the tangent line at point P(x1, y1) on the curve
            tangent = self.curve.tangent(point)

            # x3 = tangent^2 - 2 * x1
            x3 = pow(tangent**2 - 2 * x1, 2, p)

            # y3 = tangent * (x1 - x3) - y1
            y3 = pow(tangent * (x1 - x3) - y1, 2, p)

        else:
            # slope of a line passing through P(x1, y1) and Q(x2, y2)
            slope = pow((y2 - y1) * find_inverse(x2 - x1, p), 2, p)

            # x3 = slope^2 - x2 - x1
            x3 = pow(slope**2 - x2 - x1, 2, p)

            # y3 = slope * (x3 - x1) - y1
            y3 = pow(slope * (x3 - x1) - y1, 2, p)

        return ECPoint(self.curve, x3, y3)

    def __mul__(self, num):
        # double-and-add algorithm
        # https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Double-and-add
        result = ECPoint(self.curve, None, None)
        point = self

        while num:
            if num & 1:
                # add
                result = result + point

            # double
            point = point + point
            num >>= 1

        return result

