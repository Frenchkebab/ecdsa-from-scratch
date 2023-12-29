from ecdsa import ECDSA 
from ecurve import ECurve 
from ecpoint import ECPoint

def sign_and_verify(message):
    # secp256k1 curve: y^2 = x^3 + 7 (mod p) 
    # where p = 2^256 - 2^32 - 977
    # -> a = 0, b = 7, p = 2**256 - 2**32 - 977

    a = 0
    b = 7
    p = 2**256 - 2**32 - 977

    g_x = 55066263022277343669578718895168534326250603453777594175500187360389116729240
    g_y = 32670510020758816978083085130507043184471273380659243275938904335757337482424
    
    # Generate secp256k1 curve
    curve = ECurve(0, 7, p)

    # Generator point G
    G = ECPoint(curve, g_x, g_y)

    # ECDSA
    ecdsa = ECDSA(curve, G)

    # Generate a random number in a range [1, p-1]
    priv_key = None
    pub_key = None
    while True:
        priv_key = ecdsa.generate_priv_key()
        
        # Calculate pub_key = priv_key * G
        pub_key = ecdsa.generate_pub_key(priv_key)

        # Check if pub_key is on the curve
        if ecdsa.curve.is_on_curve(pub_key):
            break

    # Sign
    r, s = ecdsa.sign(priv_key, message)

    # Verify
    if(ecdsa.verify(pub_key, message, r, s)):
        print("Signature is valid")

sign_and_verify("Hello world!")