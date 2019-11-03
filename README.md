![AdBlockID Version](https://img.shields.io/badge/Version-19.307.1237-blue.svg?longCache=true&style=flat-square)
<img src="https://img.shields.io/badge/Updated-Nov 03, 2019 UTC-orange.svg?longCache=true&style=flat-square"
    alt="Nov 03, 2019 UTC" />

# AdBlockID

Total rules: 16K+

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

#### Tutorial spesifik cara memasang AdBlockID:
   - [uBlock Origin & Nano Adblocker](/doc/uBlock.md)
   - [AdGuard](/doc/Adguard.md): AdGuard Browser extension, AdGuard for Windows & AdGuard for Android.
   - [Adblock Plus](/doc/Adblock-Plus.md)
   - [AdBlock](/doc/Adblock-Plus.md#cara-memasang-adblockid-pada-adblock)
   - [Opera Ad Blocker](/doc/Opera-AdBlocker.md)
   - [Adaware ad block](/doc/adaware-ad-block.md)


## Berkontribusi
Perkebangan iklan pada website di Indonesia begitu cepat, terutama website yang memajang iklan berkonten dewasa. Jika Anda menemukan website yang belum terblokir iklannya oleh AdBlockID, jangan ragu untuk membuat [issue di sini](https://github.com/realodix/AdBlockID/issues) :D


## Panduan Untuk Developer

### Persiapan
Untuk menyatukan semua file ke dalam sebuah file [adblockid.txt](/output/adblockid.txt), Anda membutuhkan:

* [Python (2.7 atau 3.5+)](https://www.python.org/downloads/).
* [pip](https://pypi.org/project/pip/).

Setelah semua sudah terinstall di komputer Anda, lalu jalankan perintah ini:

`$ pip install -e tools/python-abp`

atau

`$ pip install -t tools tools/python-abp`

### Tools pendukung

| File              | Deskripsi                                 |
| ----------------- | ----------------------------------------- |
| `build.sh`        | Menggabungkan filter list ke dalam file `adblockid.txt`. Hasilnya ada di folder `output`. |
| `validatehost.sh` | Periksa apakah host sedang up / down berdasarkan header yang dikembalikan dari curl. |
