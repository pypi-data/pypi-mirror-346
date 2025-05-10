# Proje Açıklaması
cloudscraper
PyPI version License: MIT image Build Status Donate

A simple Python module to bypass Cloudflare's anti-bot page (also known as "I'm Under Attack Mode", or IUAM), implemented with Requests. Cloudflare changes their techniques periodically, so I will update this repo frequently.

# Kurulum
Simply run `pip install cloudscraper`. The PyPI package is at https://pypi.python.org/pypi/cloudscraper/

Alternatively, clone this repository and run `python setup.py install`.

# Gereksinimler
- Python 3.x
- Requests >= 2.9.2
- requests_toolbelt >= 0.9.1

`python setup.py install` will install the Python dependencies automatically. The javascript interpreters and/or engines you decide to use are the only things you need to install yourself, excluding js2py which is part of the requirements as the default.

# JavaScript Yorumlayıcıları ve Motorları
We support the following Javascript interpreters/engines:
- ChakraCore
- js2py: >=0.67
- native: Self made native python solver (Default)
- Node.js
- V8

# Kullanım
```python
import cloudscraper

scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
# Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
print(scraper.get("http://somesite.com").text)  # => "<!DOCTYPE html><html><head>..."
```

# Seçenekler

## Cloudflare V1'i Devre Dışı Bırakma
```python
scraper = cloudscraper.create_scraper(disableCloudflareV1=True)
```

## Brotli Sıkıştırma
```python
scraper = cloudscraper.create_scraper(allow_brotli=False)
```

## Tarayıcı / Kullanıcı Ajanı Filtreleme
```python
scraper = cloudscraper.create_scraper(browser='chrome')

# Sadece Android'de mobil Chrome Kullanıcı Ajanları
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'android',
        'desktop': False
    }
)
```

## Hata Ayıklama
```python
scraper = cloudscraper.create_scraper(debug=True)
```

## Gecikmeler
```python
scraper = cloudscraper.create_scraper(delay=10)
```

## Mevcut Oturum Kullanımı
```python
session = requests.session()
scraper = cloudscraper.create_scraper(sess=session)
```

# Captcha Çözücüler
Desteklenen 3. parti Captcha çözücüler:
- 2captcha
- anticaptcha
- CapSolver
- CapMonster Cloud
- deathbycaptcha
- 9kw

## 2captcha Örneği
```python
scraper = cloudscraper.create_scraper(
  captcha={
    'provider': '2captcha',
    'api_key': 'your_2captcha_api_key'
  }
)
```

# Kriptografi
```python
# Daha karmaşık ecdh eğrisi kullanımı
scraper = cloudscraper.create_scraper(ecdhCurve='secp384r1')

# Sunucu ana bilgisayar adı manipülasyonu
scraper = cloudscraper.create_scraper(server_hostname='www.somesite.com')
scraper.get(
    'https://backend.hosting.com/',
    headers={'Host': 'www.somesite.com'}
)
``` 