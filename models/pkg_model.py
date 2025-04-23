import os
import json
from hashlib import sha256
from charm.toolbox.pairinggroup import PairingGroup, G1, ZR, pair
from dotenv import load_dotenv

load_dotenv()

PKG_DIR = os.getenv("PKG_KEY_DIR")
MASTER_FILE = os.path.join(PKG_DIR, "ibe_ctx.json")

group = PairingGroup('SS512')

def _ensure_pkg_dir():
    os.makedirs(PKG_DIR, exist_ok=True)

def generate_master_keys():
    _ensure_pkg_dir()
    if os.path.exists(MASTER_FILE):
        return  # 이미 존재 시 재생성 안 함

    # 1. Boneh–Franklin 구성
    g = group.random(G1)
    alpha = group.random(ZR)
    g_alpha = g ** alpha

    # 2. 직렬화하여 저장
    with open(MASTER_FILE, "w") as f:
        json.dump({
            "mpk": {
                "g": group.serialize(g).hex(),
                "g^alpha": group.serialize(g_alpha).hex()
            },
            "msk": {
                "alpha": group.serialize(alpha).hex()
            }
        }, f)

def load_master_keys():
    with open(MASTER_FILE, "r") as f:
        data = json.load(f)
        g = group.deserialize(bytes.fromhex(data["mpk"]["g"]))
        g_alpha = group.deserialize(bytes.fromhex(data["mpk"]["g^alpha"]))
        alpha = group.deserialize(bytes.fromhex(data["msk"]["alpha"]))

        mpk = { "g": g, "g^alpha": g_alpha }
        msk = { "alpha": alpha }

    return mpk, msk

def extract_user_private_key(email: str) -> bytes:
    mpk, msk = load_master_keys()
    Q_id = group.hash(email, G1)
    sk = Q_id ** msk['alpha']  # SK_ID = Q_ID^alpha ∈ G1
    return group.serialize(sk)

def kem_encrypt(email: str):
    mpk, _ = load_master_keys()
    r = group.random(ZR)
    Q_id = group.hash(email, G1)
    U = mpk['g'] ** r  # g^r
    pairing_result = pair(Q_id, mpk['g^alpha']) ** r
    shared_key = sha256(pairing_result.__str__().encode()).digest()  # 256-bit symmetric key
    U_bytes = group.serialize(U)
    return shared_key, U_bytes

def kem_decrypt(email: str, U_bytes: bytes):
    _, msk = load_master_keys()
    Q_id = group.hash(email, G1)
    sk = Q_id ** msk['alpha']  # 복호화 키: SK_ID = Q_ID^alpha
    U = group.deserialize(U_bytes)
    g_id = pair(sk, U)
    shared_key = sha256(g_id.__str__().encode()).digest()
    return shared_key
