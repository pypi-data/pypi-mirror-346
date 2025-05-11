import pytest
from xmkckks.rq import Rq
from xmkckks.rlwe import RLWE
import numpy as np
import pickle
import os

from xmkckks.rlwe import discrete_gaussian

dir_path = os.path.dirname(os.path.realpath(__file__))
# append to the path the file we want to open
file_path = os.path.join(dir_path, 'flatparameters.pkl')

def test_rlwe_xmkckks(capsys):
    with capsys.disabled():
        print("Testing...")

    n = 2 ** 20  # power of 2
    # q=67108289
    # t=1021
    q = 100_000_000_003  # prime number, q = 1 (mod 2n)
    t = 200_000_001  # prime number, t < q
    std = 3  # standard deviation of Gaussian distribution

    flatparameters = []
    with open(file_path, 'rb') as f:
        flatparameters = pickle.load(f)

    with capsys.disabled():
        print(f'the n is: {n}')
        print(f'some flatten parameters{flatparameters[925:935]}')

    rlwe = RLWE(n, q, t, std)
    rlwe.generate_vector_a()

    (sec1, pub1) = rlwe.generate_keys()
    (sec2, pub2) = rlwe.generate_keys()
    (sec3, pub3) = rlwe.generate_keys()

    with capsys.disabled():

        print(f"secret key client 1: {sec1}")
        print(f"secret key client 2: {sec2}")
        print(f"secret key client 3: {sec3}")

        print(f"the public key for client 1 is:{pub1[0]}")
        print(f"the public key for client 2 is:{pub2[0]}")
        print(f"the public key for client 3 is:{pub3[0]}")
        print(f"the public key for client 1 + 2 is:{pub1[0] + pub2[0]}")
    # allpub = (pub1[0] + pub2[0], pub1[1] + pub2[1])
    allpub = (pub1[0] + pub2[0] + pub3[0], pub2[1])

    # m0 = Rq(np.array([300, 20, 300, 200, 400, 6, 7, 8]), t)  # plaintext
    # m1 = Rq(np.array([100, 2, 3, 4, 5, 6, 7, 400]), t)  # plaintext
    m0 = Rq(np.random.randint(int(t / 20), size=n), t)  # plaintext
    m1 = Rq(np.random.randint(int(t / 20), size=n), t)  # plaintext
    m2 = Rq(np.random.randint(int(t / 20), size=n), t)  # plaintext

    # m0 = Rq(np.random.randint(int(t/2), size=n), t)  # plaintext
    # m1 = Rq(np.random.randint(int(t/2), size=n), t)  # plaintext
    # m2 = Rq(np.random.randint(int(t/2), size=n), t)  # plaintext

    test = list(m0.poly.coeffs)
    test = Rq(np.array(test), t)

    c0 = rlwe.encrypt(m0, allpub)
    c1 = rlwe.encrypt(m1, allpub)
    c2 = rlwe.encrypt(m2, allpub)

    csum0 = c0[0] + c1[0] + c2[0]
    csum1 = c0[1] + c1[1] + c2[1]
    csum = (csum0, csum1)

    with capsys.disabled():
        print(f"cypher text sum part 0 is: {csum0}")
        print(f"cypher text sum part 1 is: {csum1}")

    e1star = discrete_gaussian(n, q, 5)  # larger variance than error distr from public key generation (3)
    # d1 = sec1 * csum1 + e1star
    # d1 = rlwe.decrypt(csum, sec1)
    d1 = rlwe.decrypt(csum1, sec1, e1star)

    with capsys.disabled():
        print(f"plain text for client 1 is: {m0}")
        print(f"decryption share for client 1 is: {d1}")
        print()
    # print(f"d1: {d1}")

    e2star = discrete_gaussian(n, q, 5)
    # d2 = sec2 * csum1 + e2star
    # d2 = rlwe.decrypt(csum, sec2)
    d2 = rlwe.decrypt(csum1, sec2, e2star)

    with capsys.disabled():
        print(f"plain text for client 2 is: {m1}")
        print(f"decryption share for client 2 is: {d2}")
        print()

    e3star = discrete_gaussian(n, q, 5)
    d3 = rlwe.decrypt(csum1, sec3, e3star)

    with capsys.disabled():
        print(f"plain text for client 3 is: {m2}")
        print(f"decryption share for client 3 is: {d3}")
        print()

    test = csum0 + d1 + d2 + d3
    test = Rq(test.poly.coeffs, t)
    # rlwe.decrypt(test, )

    with capsys.disabled():
        print(f"all clients plain text (1, 2 and 3): {m0 + m1 + m2}")
        print(f"decrypted cyphertext: {test}")


    # check the confections
    # foo = csum0 + d1
    # foo = Rq(foo.poly.coeffs, t)
    #
    # with capsys.disabled():
    #     print(foo)
    #
    # foo = csum0 + d2
    # foo = Rq(foo.poly.coeffs, t)
    #
    # with capsys.disabled():
    #     print(foo)


if __name__ == "__main__":
    pytest.main()