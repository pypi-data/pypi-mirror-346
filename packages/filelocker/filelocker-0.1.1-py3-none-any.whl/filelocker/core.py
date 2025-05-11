import os, getpass, hashlib, pyperclip, random, string
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from .lang import msg, get_lang

BLOCK_SIZE = 16

def pad(data):
    padding = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([padding]) * padding

def unpad(data):
    return data[:-data[-1]]

def get_key(password):
    return hashlib.sha256(password.encode()).digest()

def generate_password(length=16):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def lock_file(filepath):
    password = generate_password()
    pyperclip.copy(password)
    print(msg("password_copied").format(password))
    raw_input = input(msg("press_enter") + "\n> ")

    if raw_input.strip() != password:
        print(msg("mismatch"))
        return

    key = get_key(password)
    cipher = AES.new(key, AES.MODE_CBC)
    with open(filepath, 'rb') as f:
        data = f.read()
    ct_bytes = cipher.encrypt(pad(data))
    locked_path = filepath + '.locked'
    with open(locked_path, 'wb') as f:
        f.write(cipher.iv + ct_bytes)
    os.remove(filepath)
    print(msg("locked").format(locked_path))

def unlock_file(filepath):
    if not filepath.endswith('.locked'):
        print(msg("only_locked"))
        return
    password = getpass.getpass(msg("enter_pw"))
    key = get_key(password)
    with open(filepath, 'rb') as f:
        iv = f.read(16)
        ct = f.read()
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct))
    except:
        print(msg("decrypt_fail"))
        return
    original_path = filepath.replace('.locked', '')
    with open(original_path, 'wb') as f:
        f.write(pt)
    os.remove(filepath)
    print(msg("unlocked").format(original_path))
