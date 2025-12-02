import streamlit as st
import base64
import re

# ==== Vigenère UTF-8 Encryption / Decryption ====
def vigenere_encrypt_utf8(plaintext, key):
    """تشفير النص باستخدام Vigenère Cipher مع دعم UTF-8 الكامل"""
    if not key:
        raise ValueError("المفتاح لا يمكن أن يكون فارغًا")
    
    plaintext_bytes = plaintext.encode("utf-8")
    key_bytes = key.encode("utf-8")
    encrypted_bytes = bytearray()
    
    for i in range(len(plaintext_bytes)):
        # تشفير كل byte مع المفتاح (معاملة byte كـ 0-255)
        encrypted_byte = (plaintext_bytes[i] + key_bytes[i % len(key_bytes)]) % 256
        encrypted_bytes.append(encrypted_byte)
    
    return base64.b64encode(encrypted_bytes).decode("utf-8")

def vigenere_decrypt_utf8(ciphertext_b64, key):
    """فك تشفير النص باستخدام Vigenère Cipher مع دعم UTF-8 الكامل"""
    if not key:
        raise ValueError("المفتاح لا يمكن أن يكون فارغًا")
    
    try:
        ciphertext_bytes = base64.b64decode(ciphertext_b64)
    except:
        raise ValueError("نص مشفر غير صالح (يجب أن يكون Base64 صحيح)")
    
    key_bytes = key.encode("utf-8")
    decrypted_bytes = bytearray()
    
    for i in range(len(ciphertext_bytes)):
        # فك تشفير كل byte
        decrypted_byte = (ciphertext_bytes[i] - key_bytes[i % len(key_bytes)]) % 256
        decrypted_bytes.append(decrypted_byte)
    
    # فك الترميز
    return decrypted_bytes.decode("utf-8", errors="replace")

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
                 margin-top: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); word-break: break-all; white-space: pre-wrap;}
    .vig-btn {background: linear-gradient(90deg, #627daa, #a8c0ff); border: none; color: white; font-weight: 600;
              padding: 12px 28px; border-radius: 15px; cursor: pointer; transition: all 0.3s ease; margin-top: 12px; font-size: 16px;}
    .vig-btn:hover {background: linear-gradient(90deg, #a8c0ff, #fbc2eb); transform: scale(1.08); box-shadow: 0 8px 24px rgba(168,192,255,0.4);}
    .error-message {color: #ff6b6b; background: rgba(255,107,107,0.1); padding: 10px; border-radius: 10px; margin-top: 10px;}
    .success-message {color: #51cf66; background: rgba(81,207,102,0.1); padding: 10px; border-radius: 10px; margin-top: 10px;}
    .warning-message {color: #ffd43b; background: rgba(255,212,59,0.1); padding: 10px; border-radius: 10px; margin-top: 10px;}
    .lang-badge {display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; margin: 2px;}
    .arabic-badge {background: rgba(41, 128, 185, 0.3); color: #3498db;}
    .english-badge {background: rgba(46, 204, 113, 0.3); color: #2ecc71;}
    .numbers-badge {background: rgba(155, 89, 182, 0.3); color: #9b59b6;}
    .symbols-badge {background: rgba(241, 196, 15, 0.3); color: #f1c40f;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 style="color:#a8c0ff; font-weight:700; margin-bottom:15px;">Vigenère Cipher UTF-8</h1>', unsafe_allow_html=True)
    
    # شارات اللغات المدعومة
    st.markdown("""
    <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px;">
        <span class="lang-badge arabic-badge">🇸🇦 العربية</span>
        <span class="lang-badge english-badge">🇺🇸 الإنجليزية</span>
        <span class="lang-badge numbers-badge">🔢 الأرقام</span>
        <span class="lang-badge symbols-badge">🔣 الرموز</span>
    </div>
    """, unsafe_allow_html=True)

    # Encryption
    st.markdown('<div class="vig-card">', unsafe_allow_html=True)
    st.markdown('<div class="vig-title">🔒 التشفير</div>', unsafe_allow_html=True)
    
    plaintext = st.text_area("النص الأصلي", height=120, 
                            placeholder="أدخل النص المراد تشفيره (العربية، الإنجليزية، الأرقام، الرموز)")
    
    key = st.text_input("المفتاح السري", 
                       placeholder="أدخل المفتاح السري (يمكن أن يكون نصًا بأي لغة)")
    
    if st.button("🔐 تشفير", key="encrypt_btn", use_container_width=True):
        if not plaintext:
            st.markdown('<div class="error-message">⚠️ الرجاء إدخال نص للتشفير</div>', unsafe_allow_html=True)
        elif not key:
            st.markdown('<div class="error-message">⚠️ الرجاء إدخال مفتاح سري</div>', unsafe_allow_html=True)
        else:
            try:
                # تحليل النص المدخل
                arabic_count = len(re.findall(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]', plaintext))
                english_count = len(re.findall(r'[a-zA-Z]', plaintext))
                numbers_count = len(re.findall(r'[0-9]', plaintext))
                symbols_count = len(re.findall(r'[^\w\s\u0600-\u06FF]', plaintext))
                
                # عرض إحصائيات النص
                st.markdown(f'''
                <div style="margin:10px 0; padding:10px; background:rgba(168,192,255,0.05); border-radius:10px;">
                📊 <b>تحليل النص:</b><br>
                <span style="color:#3498db;">• حروف عربية: {arabic_count}</span><br>
                <span style="color:#2ecc71;">• حروف إنجليزية: {english_count}</span><br>
                <span style="color:#9b59b6;">• أرقام: {numbers_count}</span><br>
                <span style="color:#f1c40f;">• رموز: {symbols_count}</span><br>
                <span style="color:#e0e0e0;">• إجمالي الأحرف: {len(plaintext)}</span>
                </div>
                ''', unsafe_allow_html=True)
                
                # التشفير
                encrypted = vigenere_encrypt_utf8(plaintext, key)
                
                st.markdown('<div class="success-message">✅ تم التشفير بنجاح!</div>', unsafe_allow_html=True)
                st.markdown('<div class="vig-title" style="font-size:18px; margin-top:15px;">النص المشفر (Base64):</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="vig-output">{encrypted}</div>', unsafe_allow_html=True)
                
                # زر النسخ
                st.code(encrypted, language="text")
                
            except Exception as e:
                st.markdown(f'<div class="error-message">❌ خطأ في التشفير: {str(e)}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Decryption
    st.markdown('<div class="vig-card">', unsafe_allow_html=True)
    st.markdown('<div class="vig-title">🔓 فك التشفير</div>', unsafe_allow_html=True)
    
    ciphertext = st.text_area("النص المشفر (Base64)", height=120,
                             placeholder="أدخل النص المشفر بصيغة Base64")
    
    key2 = st.text_input("المفتاح لفك التشفير", key="decrypt_key",
                        placeholder="أدخل نفس المفتاح المستخدم في التشفير")
    
    if st.button("🔑 فك التشفير", key="decrypt_btn", use_container_width=True):
        if not ciphertext:
            st.markdown('<div class="error-message">⚠️ الرجاء إدخال نص مشفر</div>', unsafe_allow_html=True)
        elif not key2:
            st.markdown('<div class="error-message">⚠️ الرجاء إدخال مفتاح</div>', unsafe_allow_html=True)
        else:
            try:
                decrypted = vigenere_decrypt_utf8(ciphertext, key2)
                
                # تحليل النص المفكوك
                arabic_count = len(re.findall(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]', decrypted))
                english_count = len(re.findall(r'[a-zA-Z]', decrypted))
                numbers_count = len(re.findall(r'[0-9]', decrypted))
                symbols_count = len(re.findall(r'[^\w\s\u0600-\u06FF]', decrypted))
                
                st.markdown('<div class="success-message">✅ تم فك التشفير بنجاح!</div>', unsafe_allow_html=True)
                
                # عرض إحصائيات النص المفكوك
                st.markdown(f'''
                <div style="margin:10px 0; padding:10px; background:rgba(81,207,102,0.05); border-radius:10px;">
                📊 <b>تحليل النص المفكوك:</b><br>
                <span style="color:#3498db;">• حروف عربية: {arabic_count}</span><br>
                <span style="color:#2ecc71;">• حروف إنجليزية: {english_count}</span><br>
                <span style="color:#9b59b6;">• أرقام: {numbers_count}</span><br>
                <span style="color:#f1c40f;">• رموز: {symbols_count}</span><br>
                <span style="color:#e0e0e0;">• إجمالي الأحرف: {len(decrypted)}</span>
                </div>
                ''', unsafe_allow_html=True)
                
                st.markdown('<div class="vig-title" style="font-size:18px; margin-top:15px;">النص الأصلي:</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="vig-output">{decrypted}</div>', unsafe_allow_html=True)
                
                # زر النسخ للنص المفكوك
                st.code(decrypted, language="text")
                
            except ValueError as e:
                st.markdown(f'<div class="error-message">❌ خطأ في فك التشفير: {str(e)}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="error-message">❌ خطأ غير متوقع: {str(e)}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # إضافة قسم للمساعدة
    st.markdown('<div class="vig-card">', unsafe_allow_html=True)
    st.markdown('<div class="vig-title">❓ كيفية الاستخدام</div>', unsafe_allow_html=True)
    st.markdown('''
    <div style="color:#e0e0e0; line-height:1.6;">
    <h4 style="color:#a8c0ff; margin-top:10px;">✅ <b>اللغات المدعومة:</b></h4>
    <div style="display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0;">
        <span class="arabic-badge" style="padding: 6px 14px;">🇸🇦 اللغة العربية</span>
        <span class="english-badge" style="padding: 6px 14px;">🇺🇸 اللغة الإنجليزية</span>
        <span class="numbers-badge" style="padding: 6px 14px;">🔢 الأرقام (0-9)</span>
        <span class="symbols-badge" style="padding: 6px 14px;">🔣 الرموز (!@#$%^&*...)</span>
    </div>
    
    <h4 style="color:#a8c0ff; margin-top:20px;">🔐 <b>خطوات التشفير:</b></h4>
    <ol>
        <li>أدخل النص المراد تشفيره (يمكن أن يكون خليط من العربية والإنجليزية والأرقام والرموز)</li>
        <li>أدخل مفتاح سري قوي (يمكن أن يكون نصًا بأي لغة)</li>
        <li>انقر على زر <b>"تشفير"</b></li>
        <li>انسخ النص المشفر الناتج (صيغة Base64)</li>
    </ol>
    
    <h4 style="color:#a8c0ff; margin-top:20px;">🔓 <b>خطوات فك التشفير:</b></h4>
    <ol>
        <li>الصق النص المشفر (Base64) في حقل النص المشفر</li>
        <li>أدخل <b style="color:#ff6b6b;">نفس المفتاح السري</b> المستخدم في التشفير</li>
        <li>انقر على زر <b>"فك التشفير"</b></li>
        <li>ستظهر النتيجة الأصلية مع تحليلها</li>
    </ol>
    
    <div style="margin-top:20px; padding:15px; background:rgba(168,192,255,0.1); border-radius:10px;">
    <h4 style="color:#ffd43b; margin-top:0;">💡 <b>نصائح مهمة:</b></h4>
    <ul>
        <li>المفتاح <b>حساس لحالة الأحرف</b> (الكبيرة والصغيرة مختلفة)</li>
        <li>احتفظ بالمفتاح في مكان آمن - بدون المفتاح لا يمكن فك التشفير</li>
        <li>يمكن استخدام أي رموز في المفتاح (!@#$%^&*)</li>
        <li>التشفير يحافظ على المسافات والتنسيق الأصلي</li>
        <li>يفضل استخدام مفتاح طويل ومعقد لأمان أفضل</li>
    </ul>
    </div>
    
    <h4 style="color:#a8c0ff; margin-top:20px;">🎯 <b>أمثلة للاختبار:</b></h4>
    <div style="padding:10px; background:rgba(255,255,255,0.05); border-radius:10px; font-family:monospace;">
    <b>نص مختلط:</b> "مرحبا Hello 123! @#$"<br>
    <b>مفتاح:</b> "MySecretKey2024!"<br>
    <b>نص مشفر:</b> (سيظهر بعد التشفير)
    </div>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# اختبار مباشر
if __name__ == "__main__":
    show_vigenere_page()