#!/usr/bin/env python3
"""
Telegram Bot - Telefondaki mesajları Mac Mini ekranına yazdırır
"""
import os
import sys
import time
import json
import urllib.request
import urllib.parse
import urllib.error


def telegram_api(token, method, data=None):
    """Telegram API'ye istek gönderir"""
    url = f"https://api.telegram.org/bot{token}/{method}"
    
    if data:
        data = urllib.parse.urlencode(data).encode('utf-8')
    
    req = urllib.request.Request(url, data=data)
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"❌ API Hatası: {e}")
        return None


def mesaji_ekrana_yazdir(mesaj):
    """Gelen mesajı ekrana yazdırır"""
    if 'text' in mesaj:
        text = mesaj['text']
        from_user = mesaj.get('from', {})
        first_name = from_user.get('first_name', 'Bilinmeyen')
        
        print(f"\n📱 {first_name}: {text}")
        print("-" * 50)


def bot_calistir(token):
    """Bot'u çalıştırır ve mesajları dinler"""
    print("🤖 Telegram Bot başlatıldı!")
    print("📲 Telefondaki Telegram'dan mesaj gönderebilirsiniz.")
    print("⏹️  Durdurmak için Ctrl+C basın\n")
    print("=" * 50)
    
    son_update_id = 0
    
    while True:
        try:
            # Yeni mesajları al
            params = {
                'offset': son_update_id + 1,
                'timeout': 30
            }
            
            result = telegram_api(token, 'getUpdates', params)
            
            if result and result.get('ok'):
                updates = result.get('result', [])
                
                for update in updates:
                    son_update_id = update['update_id']
                    
                    if 'message' in update:
                        mesaji_ekrana_yazdir(update['message'])
            
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\n\n👋 Bot durduruluyor...")
            break
        except Exception as e:
            print(f"⚠️  Hata: {e}")
            time.sleep(3)


def main():
    """Ana fonksiyon"""
    # Bot token'ı kontrol et
    token = os.environ.get('TELEGRAM_BOT_TOKEN_ect_crypto_bot')
    
    if not token:
        print("❌ HATA: TELEGRAM_BOT_TOKEN bulunamadı!")
        print("\n📝 Kullanım:")
        print("   export TELEGRAM_BOT_TOKEN='buraya-bot-token-girin'")
        print("   python3 telegram_bot.py")
        sys.exit(1)
    
    bot_calistir(token)


if __name__ == '__main__':
    main()
