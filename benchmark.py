import statistics
import time

import oqs
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from tabulate import tabulate

REPS = 50          # operações rápidas
REPS_KEYGEN = 10   # geração de chave RSA é lenta

OAEP = padding.OAEP(
    mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None,
)

# liboqs mudou o nome da função e dos algoritmos entre versões
list_kems = getattr(oqs, "get_enabled_kem_mechanisms", None) or oqs.get_enabled_KEM_mechanisms


def median_ms(fn, reps=REPS):
    samples = []
    for _ in range(reps):
        t0 = time.perf_counter()
        fn()
        samples.append((time.perf_counter() - t0) * 1000)
    return statistics.median(samples)


def bench_rsa(bits=3072):
    keygen = median_ms(
        lambda: rsa.generate_private_key(65537, bits), reps=REPS_KEYGEN
    )
    priv = rsa.generate_private_key(65537, bits)
    pub = priv.public_key()
    msg = b"mensagem de teste"

    enc = median_ms(lambda: pub.encrypt(msg, OAEP))
    ct = pub.encrypt(msg, OAEP)
    dec = median_ms(lambda: priv.decrypt(ct, OAEP))
    return keygen, enc, dec


def bench_kem(name):
    with oqs.KeyEncapsulation(name) as kem:
        keygen = median_ms(kem.generate_keypair)
        pk = kem.generate_keypair()
        enc = median_ms(lambda: kem.encap_secret(pk))
        ct, _ = kem.encap_secret(pk)
        dec = median_ms(lambda: kem.decap_secret(ct))
    return keygen, enc, dec


def main():
    rows = []

    k, e, d = bench_rsa()
    rows.append(["RSA-3072 (OAEP)", k, e, d])

    enabled = set(list_kems())
    for name in ("ML-KEM-512", "ML-KEM-768", "ML-KEM-1024",
                 "Kyber512", "Kyber768", "Kyber1024"):
        if name in enabled:
            k, e, d = bench_kem(name)
            rows.append([name, k, e, d])

    headers = ["Algoritmo", "keygen (ms)", "encap/enc (ms)", "decap/dec (ms)"]
    print(tabulate(rows, headers=headers, floatfmt=".3f", tablefmt="grid"))


if __name__ == "__main__":
    main()
