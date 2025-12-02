import streamlit as st
import base64

# ==== Vigenère UTF-8 Encryption / Decryption ====
def vigenere_encrypt_utf8(plaintext, key):
    plaintext_bytes = plaintext.encode("utf-8")
    key_bytes = key.encode("utf-8")
    encrypted_bytes = bytearray()
    for i in range(len(plaintext_bytes)):
        encrypted_bytes.append((plaintext_bytes[i] + key_bytes[i % len(key_bytes)]) % 256)
    return base64.b64encode(encrypted_bytes).decode()

def vigenere_decrypt_utf8(ciphertext_b64, key):
    ciphertext_bytes = base64.b64decode(ciphertext_b64)
    key_bytes = key.encode("utf-8")
    decrypted_bytes = bytearray()
    for i in range(len(ciphertext_bytes)):
        decrypted_bytes.append((ciphertext_bytes[i] - key_bytes[i % len(key_bytes)]) % 256)
    return decrypted_bytes.decode("utf-8")

# ==== Streamlit Page ====
def show_vigenere_page():
    st.markdown("""
    <style>
    body {background: linear-gradient(135deg, #0b0c10, #1c1f2a); color: #e0e0e0; font-family: 'Inter', sans-serif;}
    .vig-card {background: rgba(255,255,255,0.03); backdrop-filter: blur(16px); border-radius: 25px; padding: 25px; margin-bottom: 30px;
               box-shadow: 0 6px 18px rgba(0,0,0,0.25); transition: transform 0.3s ease, box-shadow 0.3s ease;}
    .vig-card:hover {transform: translateY(-8px); box-shadow: 0 14px 32px rgba(0,0,0,0.35);}
    .vig-title {color: #a8c0ff; font-size: 24px; font-weight: 700; margin-bottom: 15px;}
    .vig-output {background: rgba(255,255,255,0.05); padding: 12px; border-radius: 15px; font-family: monospace; color: #fff;
                 margin-top: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); word-break: break-all;}
    .vig-btn {background: linear-gradient(90deg, #627daa, #a8c0ff); border: none; color: white; font-weight: 600;
              padding: 12px 28px; border-radius: 15px; cursor: pointer; transition: all 0.3s ease; margin-top: 12px; font-size: 16px;}
    .vig-btn:hover {background: linear-gradient(90deg, #a8c0ff, #fbc2eb); transform: scale(1.08); box-shadow: 0 8px 24px rgba(168,192,255,0.4);}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 style="color:#a8c0ff; font-weight:700; margin-bottom:25px;">Vigenère Cipher UTF-8</h1>', unsafe_allow_html=True)

    # Encryption
    st.markdown('<div class="vig-card">', unsafe_allow_html=True)
    st.markdown('<div class="vig-title">Encryption</div>', unsafe_allow_html=True)
    plaintext = st.text_area("Plaintext")
    key = st.text_input("Key")
    if st.button("Encrypt"):
        if plaintext and key:
            encrypted = vigenere_encrypt_utf8(plaintext, key)
            st.markdown(f'<div class="vig-output">{encrypted}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Decryption
    st.markdown('<div class="vig-card">', unsafe_allow_html=True)
    st.markdown('<div class="vig-title">Decryption</div>', unsafe_allow_html=True)
    ciphertext = st.text_area("Ciphertext (Base64)")
    key2 = st.text_input("Key for Decryption")
    if st.button("Decrypt"):
        if ciphertext and key2:
            try:
                decrypted = vigenere_decrypt_utf8(ciphertext, key2)
                st.markdown(f'<div class="vig-output">{decrypted}</div>', unsafe_allow_html=True)
            except:
                st.error("Invalid ciphertext or key")
    st.markdown('</div>', unsafe_allow_html=True)
