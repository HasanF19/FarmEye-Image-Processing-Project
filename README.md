#Sentinel Hub API Kullanımı için Python Scripti

Bu proje, Sentinel Hub API'sini kullanarak uydu görüntülerini indirmenize ve bulut örtüsü analizi yapmanıza olanak tanır. Python diliyle hazırlanmış bu script, belirli koordinatlar ve tarih aralıkları için Sentinel-2 uydu verilerini işlemektedir.

##Özellikler

OAuth2 kimlik doğrulama desteği ile Sentinel Hub API'ye bağlanma.

Belirli bir koordinat ve tarih aralığı için uydu görüntülerini indirme.

Görüntülerin bulut örtüsünü analiz ederek uygun şartlarda indirme işlemi gerçekleştirme.

Özelleştirilebilir Evalscript ile görüntü işleme.

##Gereksinimler

Python 3.7 veya daha üstü

Gerekli Python kütüphaneleri:

requests

requests_oauthlib

oauthlib

#Kurulum için aşağıdaki komutu çalıştırabilirsiniz:

pip install requests requests_oauthlib oauthlib

Kullanım

#Kimlik Bilgileri Tanımlama:Kodun başlangıcında yer alan client_id ve client_secret değişkenlerine kendi Sentinel Hub kimlik bilgilerinizi girin:

client_id = 'Client ID'nizi buraya girin'
client_secret = 'Client Secret'ınızı buraya girin'

#Koordinatlar ve Tarih Aralıklarını Ayarlama:Aşağıdaki değişkenleri ihtiyacınıza göre düzenleyin:

start_date = datetime(2024,1, 1)
end_date = datetime(2024, 12, 30)
bbox = [23.88033, 38.24560, 23.97268, 38.18506]

#Çalıştırma:Python scriptinizi çalıştırarak uydu görüntülerinin indirilmesini sağlayabilirsiniz:

python App.py

#Fonksiyonlar

download_image(bounds, date_range, evalscript, index)

Belirtilen koordinatlar ve tarih aralığı için görüntü indirir.

get_cloud_coverage(bounds, date_range)

Belirtilen tarih aralığında bulut örtüsünü kontrol eder. Bulut oranı %10'dan düşükse görüntü indirilir.

Çıkış Dosyaları

İndirilen görüntüler, Yunanistan_Canlı_Test adlı klasöre kaydedilir. Dosya adları tarih aralıklarını içerir.

#Örnek Senaryo

Bir alanın belirli tarihler arasındaki bulut oranlarını kontrol etmek ve düşük bulut oranına sahip görüntüleri indirmek için kullanılabilir. Script, her 5 günlük zaman aralığında kontrol yapar ve uygun görüntüleri indirir.
