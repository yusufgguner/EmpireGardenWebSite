# Empire Garden — Web Sitesi

Beylikdüzü'ndeki **Empire Garden Cafe & Restaurant** için hazırlanmış tek sayfalık (one-page) tanıtım ve rezervasyon sitesi.

Serpme kahvaltı, gurme lezzetler, soğuk içecekler, tatlılar ve nargile sunumunu; bahçe atmosferi fotoğraflarıyla birlikte tanıtır. Ziyaretçi tek sayfadan rezervasyon talebi gönderebilir, yol tarifi alabilir ve WhatsApp'tan yazabilir.

**Geliştiren:** [LineraSoft](https://www.linerasoft.com/)

---

## İçindekiler

- [Hızlı Başlangıç](#hızlı-başlangıç)
- [Yayına Alma (Build)](#yayına-alma-build)
- [Klasör Yapısı](#klasör-yapısı)
- [Alan Adı Ayarı](#alan-adı-ayarı-önemli)
- [Site Bölümleri](#site-bölümleri)
- [İçerik Güncelleme](#i̇çerik-güncelleme)
- [SEO](#seo)
- [Teknik Notlar](#teknik-notlar)
- [Bilinen Sınırlar](#bilinen-sınırlar)

---

## Hızlı Başlangıç

Site **saf HTML/CSS/JavaScript** ile yazılmıştır. Derleme aracı, paket yöneticisi veya çerçeve (framework) gerektirmez.

### Yerelde açmak

```bash
py -m http.server 5500
```

Ardından tarayıcıdan: `http://localhost:5500/index.html`

> `index.html` dosyasına çift tıklayarak da açabilirsiniz; ancak gömülü harita ve videoların düzgün çalışması için yukarıdaki gibi bir yerel sunucu üzerinden açmanız önerilir.

### Gereksinimler

| Ne için | Gereken |
|---|---|
| Siteyi görüntülemek | Sadece modern bir tarayıcı |
| Yerel sunucu / build almak | Python 3 |

---

## Yayına Alma (Build)

Yayına hazır dosyalar `build.py` ile üretilir:

```bash
py build.py
```

Bu komut `dist/` klasörünü sıfırdan oluşturur ve içine şunları koyar:

- **Sadeleştirilmiş `index.html`** — HTML/CSS yorumları ve fazla boşluklar temizlenir (yaklaşık **%32 küçülme**). Görünüm birebir aynı kalır.
- **Yalnızca kullanılan varlıklar** — sitenin gerçekten referans verdiği görsel, logo ve videolar kopyalanır. Orijinal fotoğraf arşivi ve ham logo kaynakları `dist/` içine **alınmaz**.
- `robots.txt` ve `sitemap.xml`

Komut çıktısında kaç dosyanın kopyalandığı ve eksik dosya olup olmadığı raporlanır. **Eksik dosya varsa build hata koduyla biter** — yayınlamadan önce mutlaka düzeltin.

### Sunucuya yükleme

`dist/` klasörünün **içindeki** her şeyi hosting'in kök dizinine (`public_html`, `www` vb.) yükleyin.

Site tamamen statiktir: PHP, veritabanı veya Node.js gerekmez. Herhangi bir paylaşımlı hosting, Netlify, Vercel, Cloudflare Pages veya GitHub Pages üzerinde çalışır.

---

## Klasör Yapısı

```
EmpireGardenWebSite/
├── index.html              # Sitenin tamamı (HTML + CSS + JS tek dosyada)
├── build.py                # Yayın derleyicisi → dist/ üretir
├── robots.txt              # Arama motoru yönergeleri
├── sitemap.xml             # Site haritası
├── README.md               # Bu dosya
│
├── assets/
│   ├── web/                # ✅ SİTENİN KULLANDIĞI görseller (optimize, ~1400px)
│   │   ├── IMG_5478.jpg …  # Galeri fotoğrafları
│   │   └── logos/          # Marka logosu, favicon, basın logoları, LineraSoft
│   ├── video/              # ✅ Instagram reels videoları
│   │
│   ├── edited photos/      # 📦 KAYNAK: fotoğrafların yüksek çözünürlüklü halleri
│   ├── haber/              # 📦 KAYNAK: basın logolarının ham dosyaları
│   ├── logo/               # 📦 KAYNAK: markanın orijinal logosu
│   └── hero_real_venue.jpg # 📦 KAYNAK: logolu tanıtım görseli
│
└── dist/                   # 🚀 build.py çıktısı — sunucuya yüklenecek klasör
```

**✅ = yayında kullanılır · 📦 = yalnızca kaynak/arşiv, yayına çıkmaz · 🚀 = yayın çıktısı**

Kaynak klasörleri (`edited photos`, `haber`, `logo`) siteyi çalıştırmak için gerekli **değildir**, ancak ileride farklı boyutta görsel üretmek gerekirse lazım olur. Bu yüzden depoda tutulur, `dist/` içine kopyalanmaz.

---

## Alan Adı

Sitenin resmî adresi: **`https://www.empiregarden.com.tr/`**

Bu adres 13 yerde tanımlıdır ve hepsi güncellenmiştir:

| Dosya | Nerede | Adet |
|---|---|---|
| `index.html` | `canonical`, `og:url`, `og:image`, `twitter:image` ve JSON-LD bloğu (`@id`, `url`, 3 görsel, `logo`, rezervasyon linki) | 11 |
| `robots.txt` | `Sitemap:` satırı | 1 |
| `sitemap.xml` | `<loc>` satırı | 1 |

### ⚠️ Hosting'de yapılması gereken yönlendirme

Site **www'li** adrese göre yapılandırıldı. Hosting panelinden **www'siz adresi www'li adrese 301 ile yönlendirin**:

```
empiregarden.com.tr  →  www.empiregarden.com.tr   (301 kalıcı yönlendirme)
```

Bu yapılmazsa Google aynı sayfayı iki ayrı adres olarak görür, SEO puanı ikiye bölünür.

Ayrıca **HTTPS sertifikası** (çoğu hosting'de ücretsiz Let's Encrypt) kurulu olmalı ve `http://` adresleri `https://`'e yönlendirilmelidir — sitedeki tüm adresler `https://` ile tanımlıdır.

### Alan adı ileride değişirse

Metin editöründe `www.empiregarden.com.tr` ifadesini toplu olarak yeni adresle değiştirin, ardından `py build.py` çalıştırıp `dist/` klasörünü yeniden üretin.

---

## Site Bölümleri

| Bölüm | Açıklama |
|---|---|
| **Hero** | Otomatik geçişli tanıtım görselleri, rezervasyon ve yol tarifi butonları |
| **Öne çıkanlar** | Serpme kahvaltı, vale hizmeti, bahçe terası, çalışma günleri |
| **Hakkımızda** | İşletme hikâyesi ve sayısal göstergeler |
| **Galeri** | 89 fotoğraf, 7 kategoriye ayrılmış filtreli vitrin |
| **Basında Biz** | 8 haber kaynağının logoları, sürekli kayan şerit |
| **Instagram Reels** | İki tanıtım videosu, sesi açma düğmesiyle |
| **Rezervasyon** | 3 adımlı form → WhatsApp mesajı olarak iletilir |
| **Dilek & Şikayet** | Geri bildirim formu → WhatsApp mesajı olarak iletilir |
| **İletişim** | Adres, telefon, çalışma saatleri, gömülü Google harita |

Ek olarak: sol altta **WhatsApp** butonu, sağ altta **Google'da puan ver** kutusu, mobilde alt sabit çubuk (Hemen Ara / Rezervasyon Yap).

---

## İçerik Güncelleme

Tüm içerik `index.html` içindedir. Sık gereken değişiklikler:

### Telefon numarası

`index.html` içinde `905304279404` ifadesini arayıp yeni numarayla değiştirin (telefon linkleri, WhatsApp linkleri ve JSON-LD'de geçer). Ekranda görünen `0530 427 94 04` metinlerini de güncellemeyi unutmayın.

### Adres ve çalışma saatleri

Footer bölümündeki `İletişim & Adres` ve `Çalışma Saatleri` alanlarını düzenleyin. Aynı bilgiler `<head>` içindeki JSON-LD bloğunda da geçtiği için **orayı da güncelleyin** (Google'ın gösterdiği bilgi oradan okunur).

### Galeriye fotoğraf eklemek

1. Fotoğrafı `assets/web/` klasörüne `IMG_XXXX.jpg` adıyla koyun (uzun kenar ~1400 piksel, ~150 KB önerilir).
2. `index.html` içinde `const GALLERY_PHOTOS` bloğunu bulun.
3. Numarayı uygun kategori dizisine ekleyin:

```js
const GALLERY_PHOTOS = {
    mekan:     [5915, 5916, ...],   // Mekan & Bahçe
    kahvalti:  [5480, 5486, ...],   // Serpme Kahvaltı
    yemekler:  [5894, 5882, ...],   // Yemekler
    icecekler: [5880, 5560, ...],   // Soğuk İçecekler
    tatlilar:  [5906, 5547, ...],   // Tatlılar
    nargile:   [5559]               // Nargile
};
```

### Galerinin ilk ekranını değiştirmek

Galeri açılışta 7 fotoğraf + bulanık "tümünü gör" karesi gösterir. İlk gösterilecek kareler `const FEATURED` dizisinde belirlenir:

```js
const FEATURED = [5915, 5480, 5916, 5894, 5560, 5906, 5559];
```

### Basına haber eklemek

`initPressMarquee` fonksiyonundaki diziye `['Kaynak Adı', 'logo yolu', 'haber linki']` biçiminde yeni satır ekleyin. Logoyu `assets/web/logos/` içine koyun (arka planı şeffaf PNG, yüksekliği ~60 piksel).

---

## SEO

Site arama motorları için hazır durumdadır:

- **Anahtar kelime odaklı başlık ve açıklama** (Beylikdüzü kahvaltı / cafe / nargile)
- **JSON-LD yapısal veri** (`CafeOrCoffeeShop`) — adres, telefon, çalışma saatleri, sunulan mutfak, olanaklar ve rezervasyon aksiyonu. Google'ın yerel arama ve harita kartlarını beslemesi için gerekli.
- **Open Graph + Twitter Card** — link paylaşıldığında önizleme görseli çıkar
- `canonical` adresi, `robots` yönergeleri, `theme-color`, konum meta etiketleri
- **Favicon** ve Apple dokunmatik simgesi
- `robots.txt` + `sitemap.xml`
- Tek `<h1>`, düzenli başlık hiyerarşisi, **tüm görsellerde `alt` metni**
- Görsellerde gecikmeli yükleme (lazy loading), tanıtım görselinde öncelikli yükleme

### Yayına aldıktan sonra yapılacaklar

1. [Google Search Console](https://search.google.com/search-console)'a alan adını ekleyin, `sitemap.xml` adresini gönderin.
2. **Google Business Profile** (İşletme Profili) kaydını açın/güncelleyin — yerel aramada en büyük etkiyi bu yapar. Sitedeki adres, telefon ve çalışma saatleriyle **birebir aynı** olmalıdır.
3. Sosyal medya hesaplarına site linkini ekleyin.

---

## Teknik Notlar

- **Bağımlılık yok.** Harici JavaScript kütüphanesi kullanılmaz. Dışarıdan yalnızca Google Fonts ve gömülü Google Harita yüklenir.
- **Mobil öncelikli (mobile-first) CSS.** Kırılma noktaları: 600 piksel, 900 piksel, 1180 piksel.
- **Erişilebilirlik:** klavyeyle gezinme, görünür odak halkaları, ARIA etiketleri, en az 44×44 piksel dokunma hedefleri, `prefers-reduced-motion` desteği (hareket azaltma tercihi olan kullanıcılarda animasyonlar kapanır).
- **Performans:** görseller ~150 KB'a optimize edilmiştir; videolar yalnızca ekranda görünürken oynar; sekme arka plandayken tanıtım geçişi durur.
- **Videolar web için sıkıştırılmıştır** — kamera çıkışı 1080×1920 / 21 Mbps (toplam 142 MB) idi, ffmpeg ile 720×1280 / CRF 28'e indirildi (toplam **10,7 MB**). Sitede video kartı en fazla ~400 piksel genişlikte göründüğü için kalite farkı gözle ayırt edilemiyor. Videolarda `faststart` etkin — dosya tamamen inmeden oynamaya başlar.

  Yeni video eklerken aynı ayarı kullanın:

  ```bash
  ffmpeg -i kaynak.mp4 -c:v libx264 -crf 28 -preset slow -profile:v high \
    -pix_fmt yuv420p -vf "scale=720:1280:flags=lanczos" \
    -c:a aac -b:a 96k -ac 2 -movflags +faststart cikti.mp4
  ```
- **Formlar sunucu gerektirmez.** Rezervasyon ve geri bildirim formları, girilen bilgileri hazır bir WhatsApp mesajına dönüştürüp `wa.me` üzerinden açar.

---

## Bilinen Sınırlar

Bunlar bilinçli tercihlerdir; ileride geliştirilmek istenirse buradan başlanabilir.

| Konu | Durum |
|---|---|
| **Marka logosu çözünürlüğü** | Kaynak logo 150×150 piksel JPEG. Site boyutunda sorunsuz görünür, ancak afiş/tabela gibi büyük kullanımlar için vektör (SVG/AI/PDF) dosya gerekir. |
| **Formlar** | E-posta veya veritabanına kayıt yapmaz; WhatsApp'a yönlendirir. Kayıt tutulması istenirse sunucu tarafı gerekir. |
| **Instagram akışı** | Canlı bağlantı yoktur. Videolar sitede yerel olarak durur; yeni paylaşımlar otomatik düşmez. |
| **Görsel koruması** | Sağ tık, sürükleme ve `F12`/`Ctrl+U` kısayolları engellenir. Bu **caydırıcı** bir önlemdir; kesin koruma sağlamaz (tarayıcı görselleri göstermek için indirmek zorundadır). Kesin çözüm filigran (watermark) eklemektir. |
| **Müşteri puanı** | Sitede belirtilen puan bilgisi JSON-LD yapısal verisine **bilerek eklenmemiştir.** Gerçek Google yorumlarına dayanmayan puan verisi Google politikalarına aykırıdır ve yaptırım riski taşır. |

---

© Empire Garden Beylikdüzü. Web sitesi hakları [LineraSoft](https://www.linerasoft.com/)'a saklıdır.
