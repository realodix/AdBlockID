# AdBlockID

Total rules: 13,270

AdblockID adalah filter tambahan untuk melengkapi [EasyList](https://github.com/easylist/easylist) dan [AdguardFilters](https://github.com/AdguardTeam/AdguardFilters) yang dirancang secara khusus untuk menghilangkan iklan (terutama iklan yang bermuatan konten dewasa) pada website di Indonesia.


## Fitur Yang Tersedia
1. Block iklan.
2. Block popups.
3. Block [crypto mining scripts](https://www.mycryptopedia.com/crypto-mining-scripts/).
4. Menghilangkan element website yang dirasa cukup menggangu.


## Cara Menggunakan
- Buka browser favorit Anda ([Chrome](https://www.google.com/chrome/), [Firefox](https://www.mozilla.org/firefox/), [Safari](http://www.apple.com/safari/), [Opera](http://www.opera.com/), ...)
- Install ekstensi [uBlock Origin](https://github.com/gorhill/uBlock#installation), [AdGuard Browser extension](https://adguard.com/en/adguard-browser-extension/overview.html), [Adblock Plus](https://adblockplus.org), atau ekstensi ad blocker lainnya. (Secara pribadi Saya menggunakan uBlock Origin untuk keperluan testing filter ini)
- Anda dapat menggunakannya secara manual dengan menambahkan alamat ini `https://raw.githubusercontent.com/realodix/AdBlockID/master/output/adblockid.txt` pada plugin adblock yang Anda gunakan.


## Berkontribusi
Perkebangan web di Indonesia begitu cepat, terutama web yang memajang iklan berkonten dewasa. Jika Anda menemukan web yang tidak terfilter oleh AdBlockID, jangan ragu untuk membuat issue di sini :D


## Generate File

### Persiapan
Untuk menyatukan semua file ke dalam sebuah file [adblockid.txt](https://raw.githubusercontent.com/realodix/AdBlockID/master/output/adblockid.txt), Anda membutuhkan:

* [Python (2.7 atau 3.5+)](https://www.python.org/downloads/),
* [pip](https://pypi.org/project/pip/).

Setelah semua sudah terinstall di komputer Anda, lalu jalankan perintah ini:

`$ pip install -e vendor/python-abp`

### Perintah untuk generate
* Klik file `FOP.py` untuk mengurutkan.
* Klik file `generate.py` untuk menyatukan.
