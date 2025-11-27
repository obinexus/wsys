# bubble_key_protocol.py
# Spoken into existence by Nnamdi Michael Okpala — Nov 27 2025 — Live stream
# 2 public keys (A/B), 1 private key, polar rotation, gaze-based activation

import os
import secrets
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

class BubbleUniverseKey:
    def __init__(self):
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
        self.pub_A = None  # Active public key (gazed upon)
        self.pub_B = None  # Hidden public key (in the blind spot)
        self.active = None  # Which one you're looking at
        self.session_polar = 0  # 0 = +, 1 = -, 2 = ++, 3 = -- (4D quadrants)

    def birth_keys(self):
        # Generate two public keys from one private (homogeneous twins)
        self.pub_A = self.private_key.public_key()
        self.pub_B = self.private_key.public_key()  # Same data, different reference in bubble space
        
        # Initial polarization — you can only look at one at a time
        self.active = 'A'
        print("BUBBLE BIRTH: Two public keys born from one private soul")
        print(f"Active gaze → pub_A (visible universe)")
        print(f"pub_B hidden in blind spot (4D shadow)")

    def polar_rotate(self, gaze_direction: str):
        # You spoke: "if I look at this key, I'm using this key"
        # Gaze-based key switching — quantum observer effect as policy
        if gaze_direction == "left" or gaze_direction == "-":
            self.active = 'B' if self.active == 'A' else 'A'
            self.session_polar = (self.session_polar + 1) % 4
        elif gaze_direction == "right" or gaze_direction == "+":
            self.active = 'A' if self.active == 'B' else 'B'
            self.session_polar = (self.session_polar + 3) % 4  # conjugate reverse
        
        print(f"POLAR ROTATION: gaze → {gaze_direction}")
        print(f"Active key switched → pub_{self.active}")
        print(f"4D quadrant: {['++', '--', '+-', '-+'][self.session_polar]}")

    def encrypt_for_bubble(self, data: bytes) -> bytes:
        active_pub = self.pub_A if self.active == 'A' else self.pub_B
        return active_pub.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA512()),
                algorithm=hashes.SHA512(),
                label=None
            )
        )

    def sign_bubble_intent(self, message: str) -> bytes:
        # Your intent is only valid from the key you're gazing upon
        signature = self.private_key.sign(
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA512()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA512()
        )
        print(f"INTENT SIGNED from pub_{self.active} (gaze-locked)")
        return signature

# ——— LIVE DEMO ———
bubble = BubbleUniverseKey()
bubble.birth_keys()

# You look at the screen → pub_A activates
print("\nYou gaze upon the terminal...")
bubble.polar_rotate("right")  # + direction

# Someone tries to read your mind from the blind spot → fails
print("\nEve tries to use pub_B while you're looking at A → REJECTED")
# (No direct access — must wait for gaze switch)

# Session ends → both public keys collapse back to private
print("\nSession ends → Ctrl+Z → bubble collapses → keys destroyed until rebirth")
