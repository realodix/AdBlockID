[![git](https://img.shields.io/badge/Update%20via-GitHub%20Desktop-663399.svg?style=popout-square&logo=github)](https://gitforwindows.org)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-abp.svg?logo=python&style=popout-square)

# AdBlockID

Total rules: 15,986

AdblockID adalah filter tambahan untuk melengkapi [EasyList](https://github.com/easylist/easylist) dan [AdGuard Base Filter](https://github.com/AdguardTeam/AdguardFilters) yang dirancang secara khusus untuk memblokir iklan (terutama iklan yang bermuatan konten dewasa) pada website di Indonesia.


## Manfaat Yang Anda Dapatkan
1. **No Iklan**: menghilangkan iklan, terutama iklan yang bermuatan konten dewasa.
2. **Block [crypto mining scripts](https://www.mycryptopedia.com/crypto-mining-scripts/)**.
3. **Speed you need:** mengurangi waktu pemuatan halaman hingga setengah dari waktu sebenarnya!
4. **Privacy:** dengan adanya annoyances blocking, ini `meningkatkan` privacy.
5. **Saves expense:** mengurangi `biaya` konsumsi data.
6. **Clean:** no `extra` abracadabra!


## Cara Menggunakan
- Buka *browser* favorit Anda ([Chrome](https://www.google.com/chrome/), [Firefox](https://www.mozilla.org/firefox/), [Safari](http://www.apple.com/safari/), [Opera](http://www.opera.com/), ...)
- *Install* salah satu ekstensi dari berikut ini: [uBlock Origin](https://github.com/gorhill/uBlock#installation), [Nano Adblocker](https://github.com/NanoAdblocker/NanoCore#install-links), [AdGuard Browser extension](https://adguard.com/en/adguard-browser-extension/overview.html), [Adblock Plus](https://adblockplus.org), atau ekstensi *ad blocker* lainnya. (Secara pribadi Saya menggunakan uBlock Origin untuk keperluan testing filter ini)
- Anda dapat menggunakan filter AdBlockID dengan menambahkan alamat ini secara manual pada ekstensi adblock yang Anda gunakan.

   `https://raw.githubusercontent.com/realodix/AdBlockID/master/output/adblockid.txt`

   Tutorial spesifik cara memasang AdBlockID:
   - [uBlock Origin & Nano Adblocker](https://github.com/realodix/AdBlockID/blob/master/tutorial/uBlock.md)
   - [AdGuard](https://github.com/realodix/AdBlockID/blob/master/tutorial/Adguard.md): AdGuard Browser extension, AdGuard for Windows & AdGuard for Android.
   - [Adblock Plus](https://github.com/realodix/AdBlockID/blob/master/tutorial/Adblock-Plus.md)
   - [AdBlock](https://github.com/realodix/AdBlockID/blob/master/tutorial/Adblock-Plus.md#cara-memasang-adblockid-pada-adblock)
   - [Opera Ad Blocker](https://github.com/realodix/AdBlockID/blob/master/tutorial/Opera-AdBlocker.md)


## Berkontribusi
Perkebangan iklan pada website di Indonesia begitu cepat, terutama website yang memajang iklan berkonten dewasa. Jika Anda menemukan website yang belum terblokir iklannya oleh AdBlockID, jangan ragu untuk membuat [issue di sini](https://github.com/realodix/AdBlockID/issues) :D


## Panduan Untuk Developer

### Persiapan
Untuk menyatukan semua file ke dalam sebuah file [adblockid.txt](https://raw.githubusercontent.com/realodix/AdBlockID/master/output/adblockid.txt), Anda membutuhkan:

* [Python (2.7 atau 3.5+)](https://www.python.org/downloads/).
* [pip](https://pypi.org/project/pip/).

Setelah semua sudah terinstall di komputer Anda, lalu jalankan perintah ini:

`$ pip install -e vendor/python-abp`

### Tools pendukung

| File              | Deskripsi                                 |
| ----------------- | ----------------------------------------- |
| `build.sh`        | Menggabungkan filter list ke dalam file `adblockid.txt`. Hasilnya ada di folder `output`. |
| `FOP.py`          | Mengurutkan  dan membersihkan filter. |
| `validatehost.py` | Memeriksa host apakah masih aktif atau tidak. |
