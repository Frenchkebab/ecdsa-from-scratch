import hashlib
import random
from utils import inverse

class ECDSA:
    def __init__(self, curve, g):
        self.curve = curve # Elliptic curve
        self.G = g # Generator point

        if not self.curve.is_on_curve(self.G):
            raise Exception("Generator point is not on curve")

    def generate_priv_key(self):
        # Generate a random number in a range [1, p-1]
        return random.randint(1, self.curve.p - 1)

    def generate_pub_key(self, priv_key):
        # Calculate pub_key = priv_key * G
        return (self.G) * priv_key

    def sign(self, priv_key, message):
        

        # Generate a random number k in a range [1, p-1]
        k = random.randint(1, self.curve.p - 1)

        # Calculate r = (k * G).x (mod p)
        R = (self.G) * k
        r = pow(R.x, 1, self.curve.p)

        # Calculate s = k^-1 * (z + r * priv_key) (mod p)
        z = int(hashlib.sha256(message.encode()).hexdigest(), 16)
        s = pow(inverse(k, self.curve.p) * (z + r * priv_key), 1, self.curve.p)

        print("[sign] message: ", message)
        print("[sign] Hashed message: ", z)
        print("")

        return (r, s)

    def verify(self, pub_key, message, r, s):
        # check if uG + vP = R
        # G: Generator point
        # P: Public key
        # R: kG (k is a random number) (r, R.y)

        # u: z * s^-1 (mod p)
        # v: r * s^-1 (mod p)

        # Calculate z = hash(message)
        z = int(hashlib.sha256(message.encode()).hexdigest(), 16)

        # Calculate u = z * s^-1 (mod p)
        u = pow(z * inverse(s, self.curve.p), 0, self.curve.p)

        # Calculate v = r * s^-1 (mod p)
        v = pow(r * inverse(s, self.curve.p), 0, self.curve.p)

        # Calculate uG + vP
        uG = (self.G) * u
        vP = pub_key * v
        R_expected = uG + vP

        print("[verify] message: ", message)
        print("[verify] Hashed message: ", z)
        print("")

        assert R_expected.x == r, "Invalid signature"

        return True


