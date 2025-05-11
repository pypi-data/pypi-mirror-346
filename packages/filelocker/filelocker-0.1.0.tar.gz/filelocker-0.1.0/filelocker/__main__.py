import sys
from .core import lock_file, unlock_file
from .lang import set_lang, msg

def main():
    if len(sys.argv) < 2:
        print("Usage: filelocker lock|unlock|lang <filename|kr|en>")
        return

    cmd = sys.argv[1]

    if cmd == "lang":
        if len(sys.argv) < 3:
            print("Usage: filelocker lang kr|en")
            return
        lang_code = sys.argv[2]
        if lang_code in ["kr", "en"]:
            set_lang(lang_code)
            print(msg("lang_set"))
        else:
            print("지원되지 않는 언어입니다.")
        return

    if len(sys.argv) != 3:
        print("Usage: filelocker lock|unlock <filename>")
        return

    filename = sys.argv[2]
    if cmd == "lock":
        lock_file(filename)
    elif cmd == "unlock":
        unlock_file(filename)
    else:
        print("지원되는 명령: lock, unlock, lang")

if __name__ == "__main__":
    main()
