import json
import os

LANG_FILE = "filelocker/settings.json"

messages = {
    "en": {
        "password_copied": "Password copied to clipboard:\n{}",
        "press_enter": "Press [Enter] and retype the password to continue:",
        "mismatch": "Password mismatch. Lock aborted.",
        "locked": "Locked: {}",
        "only_locked": "Only .locked files can be unlocked.",
        "enter_pw": "[Enter Password] > ",
        "decrypt_fail": "Decryption failed. Wrong password or corrupted file.",
        "unlocked": "Unlocked: {}",
        "lang_set": "Language set to English.",
    },
    "kr": {
        "password_copied": "비밀번호가 클립보드에 복사되었습니다:\n{}",
        "press_enter": "[Enter] 키를 누르고 비밀번호를 다시 입력하세요:",
        "mismatch": "비밀번호가 일치하지 않습니다. 잠금 취소.",
        "locked": "잠금 완료: {}",
        "only_locked": ".locked 파일만 해제할 수 있습니다.",
        "enter_pw": "[비밀번호 입력] > ",
        "decrypt_fail": "복호화 실패: 비밀번호가 틀리거나 파일이 손상되었습니다.",
        "unlocked": "복호화 완료: {}",
        "lang_set": "언어가 한국어로 설정되었습니다.",
    }
}

def get_lang():
    if not os.path.exists(LANG_FILE):
        return "en"
    with open(LANG_FILE, "r") as f:
        return json.load(f).get("lang", "en")

def set_lang(lang_code):
    with open(LANG_FILE, "w") as f:
        json.dump({"lang": lang_code}, f)

def msg(key):
    lang = get_lang()
    return messages[lang].get(key, f"<{key}>")
