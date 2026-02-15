#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


API_BASE = "https://api.telegram.org/bot{token}/{method}"


def call_api(token: str, method: str, payload: dict | None = None, timeout: int = 70):
    url = API_BASE.format(token=token, method=method)
    data = None
    headers = {}
    if payload is not None:
        encoded = urllib.parse.urlencode(payload).encode("utf-8")
        data = encoded
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8")
        parsed = json.loads(raw)
        if not parsed.get("ok"):
            raise RuntimeError(f"Telegram API error: {parsed}")
        return parsed["result"]


def notify_macos(title: str, message: str):
    safe_title = title.replace('"', '\\"')
    safe_message = message.replace('"', '\\"')
    script = f'display notification "{safe_message}" with title "{safe_title}"'
    subprocess.run(["osascript", "-e", script], check=False)


def format_message(msg: dict) -> str:
    chat = msg.get("chat", {})
    sender = msg.get("from", {})
    chat_id = chat.get("id", "?")
    chat_title = chat.get("title") or sender.get("first_name") or "Unknown"

    if "text" in msg:
        body = msg["text"]
    elif "caption" in msg:
        body = f"[media] {msg['caption']}"
    else:
        body = "[text olmayan bir mesaj geldi]"

    return f"[chat:{chat_id} | {chat_title}] {body}"


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN_ect_crypto_bot")
    allowed_chat_id = os.environ.get("TELEGRAM_ALLOWED_CHAT_ID")

    if not token:
        print("Hata: TELEGRAM_BOT_TOKEN_ect_crypto_bot ortam değişkeni yok.")
        print("Örnek: export TELEGRAM_BOT_TOKEN_ect_crypto_bot='123456:ABC...'")
        sys.exit(1)

    print("Bot başlatıldı. Ctrl+C ile durdurabilirsiniz.")
    if allowed_chat_id:
        print(f"Sadece şu chat id kabul edilecek: {allowed_chat_id}")
    else:
        print("Uyarı: TELEGRAM_ALLOWED_CHAT_ID tanımlı değil, gelen tüm chat'ler dinlenecek.")

    offset = None
    while True:
        try:
            payload = {"timeout": 60}
            if offset is not None:
                payload["offset"] = offset
            updates = call_api(token, "getUpdates", payload=payload, timeout=70)

            for upd in updates:
                offset = upd["update_id"] + 1
                msg = upd.get("message") or upd.get("edited_message")
                if not msg:
                    continue

                chat_id = str(msg.get("chat", {}).get("id", ""))
                if allowed_chat_id and chat_id != allowed_chat_id:
                    continue

                line = format_message(msg)
                print(line, flush=True)
                notify_macos("Telegram Mesaj", line[:180])

        except urllib.error.HTTPError as e:
            print(f"HTTP hata: {e.code} {e.reason}", file=sys.stderr)
            time.sleep(3)
        except urllib.error.URLError as e:
            print(f"Ağ hatası: {e.reason}", file=sys.stderr)
            time.sleep(3)
        except KeyboardInterrupt:
            print("\nKapatılıyor...")
            break
        except Exception as e:
            print(f"Beklenmeyen hata: {e}", file=sys.stderr)
            time.sleep(3)


if __name__ == "__main__":
    main()
