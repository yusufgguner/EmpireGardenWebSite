# -*- coding: utf-8 -*-
"""Empire Garden — yayın (production) derleyicisi.

Kaynak dosyalardan yayına hazır 'dist/' klasörü üretir:
  * index.html içindeki HTML/CSS/JS yorumları temizlenir, boşluklar sadeleştirilir
  * yalnızca siteden referans verilen görsel/video/logo dosyaları kopyalanır
  * kaynak arşivleri (orijinal fotoğraflar, ham logolar) dışarıda bırakılır

Kullanım:  py build.py
"""
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
SRC_HTML = os.path.join(ROOT, "index.html")

NL = chr(10)
CR = chr(13)
BACKSLASH = chr(92)


# ---------------------------------------------------------------- yardımcılar
def human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return "%.1f %s" % (n, unit)
        n /= 1024.0
    return "%.1f TB" % n


def dir_size(path):
    total = 0
    for base, _dirs, files in os.walk(path):
        for f in files:
            total += os.path.getsize(os.path.join(base, f))
    return total


def protect(html):
    """<script>/<style>/<textarea>/<pre> bloklarını yer tutucuya al.

    Böylece HTML yorum temizliği ve boşluk daraltma bu blokların içini bozmaz.
    """
    blocks = []

    def stash(m):
        blocks.append(m.group(0))
        return "\x00BLOCK%d\x00" % (len(blocks) - 1)

    html = re.sub(r"<script\b[^>]*>.*?</script>", stash, html, flags=re.S | re.I)
    html = re.sub(r"<style\b[^>]*>.*?</style>", stash, html, flags=re.S | re.I)
    html = re.sub(r"<textarea\b[^>]*>.*?</textarea>", stash, html, flags=re.S | re.I)
    html = re.sub(r"<pre\b[^>]*>.*?</pre>", stash, html, flags=re.S | re.I)
    return html, blocks


def restore(html, blocks):
    for i, b in enumerate(blocks):
        html = html.replace("\x00BLOCK%d\x00" % i, b)
    return html


def strip_js_comments(js):
    """JavaScript'teki // ve /* */ yorumlarını sil.

    Düz bir "//.*" regexi URL'lerdeki "https://" kısmını da keserdi. Bu yüzden
    karakter karakter tarayıp string / template literal içinde olup olmadığımızı
    takip ediyoruz; yalnızca kod bağlamındaki işaretler yorum sayılır.
    """
    line_breaks = CR + NL
    out = []
    i = 0
    n = len(js)
    quote = None                      # açık string tırnağı (' " veya `)

    while i < n:
        c = js[i]
        nxt = js[i + 1] if i + 1 < n else ""

        if quote:                     # string içindeyiz: aynen kopyala
            out.append(c)
            if c == BACKSLASH and i + 1 < n:
                out.append(js[i + 1])
                i += 2
                continue
            if c == quote:
                quote = None
            i += 1
            continue

        if c in "\"'`":               # string başlıyor
            quote = c
            out.append(c)
            i += 1
            continue

        if c == "/" and nxt == "/":   # satır yorumu -> at
            while i < n and js[i] not in line_breaks:
                i += 1
            continue

        if c == "/" and nxt == "*":   # blok yorumu -> at
            i += 2
            while i + 1 < n and not (js[i] == "*" and js[i + 1] == "/"):
                i += 1
            i += 2
            continue

        out.append(c)
        i += 1

    kept = "".join(out).splitlines()
    kept = [ln.rstrip() for ln in kept]
    return NL.join(ln for ln in kept if ln.strip())


def minify_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)           # yorumlar
    css = re.sub(r"\s+", " ", css)                            # boşluk daralt
    css = re.sub(r"\s*([{}:;,>~+])\s*", r"\1", css)           # noktalama etrafı
    css = re.sub(r";}", "}", css)                             # gereksiz son ;
    return css.strip()


def build_html():
    with open(SRC_HTML, encoding="utf-8") as f:
        html = f.read()
    before = len(html)

    # 1) script/style/textarea/pre bloklarını koru
    html, blocks = protect(html)

    # 2) HTML yorumlarını sil (koşullu yorumlar hariç)
    html = re.sub(r"<!--(?!\[if).*?-->", "", html, flags=re.S)

    # 3) Tüm boşluk dizilerini TEK boşluğa indir.
    #    Tarayıcı zaten böyle davrandığı için görünüm birebir aynı kalır.
    #    ">\s+<" ile tamamen silmek etiketler arası anlamlı boşluğu yok ederdi
    #    (ör. "hakları <a>LineraSoft</a>" -> "haklarıLineraSoft").
    html = re.sub(r"\s+", " ", html)

    # 4) blokları geri koy
    html = restore(html, blocks)

    # 5) CSS'i küçült
    def shrink_style(m):
        return "<style>" + minify_css(m.group(1)) + "</style>"

    html = re.sub(r"<style\b[^>]*>(.*?)</style>", shrink_style, html, flags=re.S | re.I)

    # 6) JS yorumları BİLEREK korunuyor.
    #    strip_js_comments() denendi; regex literalleri ve iç içe template
    #    literal'lerde ("${...}" içinde tırnak) tarayıcıyı yanıltıp
    #    "Invalid or unexpected token" hatası ürettiği için devre dışı.
    #    Kazanç ~3 KB / 88 KB (%3) — siteyi kırma riskine değmez.
    #    Gerçek bir JS küçültücü (terser vb.) eklenirse burada çağrılmalı.

    after = len(html)
    return html, before, after


def collect_assets(html):
    """index.html'in gerçekten kullandığı varlıkları topla."""
    needed = set(re.findall(r'(?:src|href|poster|content)="(assets/[^"]+)"', html))
    needed |= set(re.findall(r"'(assets/[^']+\.(?:jpg|png|mp4|webp|svg))'", html))

    # JS'te 'assets/web/IMG_' + numara şeklinde kurulan galeri yolları
    for const in ("GALLERY_PHOTOS", "FEATURED"):
        m = re.search(r"const %s\s*=\s*[\[{](.*?)[\]}];" % const, html, re.S)
        if m:
            for num in re.findall(r"\b(\d{4})\b", m.group(1)):
                needed.add("assets/web/IMG_%s.jpg" % num)

    return sorted(needed)


def main():
    if not os.path.exists(SRC_HTML):
        sys.exit("index.html bulunamadı")

    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)

    html, before, after = build_html()
    assets = collect_assets(html)

    missing = []
    copied = 0
    for rel in assets:
        src = os.path.join(ROOT, rel.replace("/", os.sep))
        if not os.path.exists(src):
            missing.append(rel)
            continue
        dst = os.path.join(DIST, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        copied += 1

    with open(os.path.join(DIST, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

    for extra in ("robots.txt", "sitemap.xml"):
        p = os.path.join(ROOT, extra)
        if os.path.exists(p):
            shutil.copy2(p, os.path.join(DIST, extra))

    print("index.html : %s -> %s  (%%%.0f kucuduk)"
          % (human(before), human(after), (1 - after / before) * 100))
    print("varlik     : %d dosya kopyalandi" % copied)
    if missing:
        print("EKSIK      : %d dosya bulunamadi!" % len(missing))
        for m in missing:
            print("   -", m)
    print("dist boyutu: %s" % human(dir_size(DIST)))
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
