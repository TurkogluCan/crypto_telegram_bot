# 🤖 Telegram Mac Mini Bot

Telefondaki Telegram'dan gönderdiğiniz mesajları Mac Mini ekranına yazdıran basit bir bot.

## 🚀 Nasıl Kurulur?

### 1. Telegram Bot Oluştur

1. Telegram'da **@BotFather** bul
2. `/newbot` komutunu gönder
3. Bot için bir isim belirle
4. Bot için kullanıcı adı belirle (örn: `benim_mac_botum`)
5. Verilen **token**'ı kopyala (örn: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Bot Token'ı Ayarla

Terminal'i aç ve şu komutu çalıştır:

```bash
export TELEGRAM_BOT_TOKEN='buraya-token-yapistir'
```

### 3. Bot'u Çalıştır

```bash
cd "/Users/enescanturkoglu/Documents/New project/antigravity"
python3 telegram_bot.py
```

### 4. Test Et

- Telegram'da oluşturduğun botu bul
- `/start` yazarak başlat
- Herhangi bir mesaj gönder
- Mac Mini ekranında mesajın görünmesi gerekiyor! 🎉

## 🛑 Nasıl Durdurulur?

Terminal'de **Ctrl + C** tuşlarına bas.

## 📝 Notlar

- Bot çalışırken Terminal açık kalmalı
- Telefondaki mesajlar anında Mac ekranına yansır
- Harici bağımlılık yok - sadece Python 3 yeterli

## 🔒 Güvenlik İpucu

Token'ı kimseyle paylaşma! Bu token ile botunuzu kontrol edebilirler.
