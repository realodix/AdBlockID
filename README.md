# AdBlockID

Total rules: 12,722

AdblockID adalah filter tambahan untuk [EasyList](https://github.com/easylist/easylist) dan [AdguardFilters](https://github.com/AdguardTeam/AdguardFilters) yang dirancang secara khusus untuk menghilangkan iklan (terutama iklan yang bermuatan konten dewasa) pada website di Indonesia.


## Fitur Yang Tersedia
1. Block iklan.
2. Block popups.
3. Block miner.
4. Menghilangkan elemen website yang dirasa cukup menggangu.


## Cara Menggunakan
Anda dapat menggunakannya secara manual dengan menambahkan alamat ini `https://raw.githubusercontent.com/realodix/AdBlockID/master/output/adblockid.txt` pada plugin adblock Anda.


## Berkontribusi
Perkebangan web di Indonesia begitu cepat, terutama web yang memajang iklan berkonten dewasa. Jika Anda menemukan web yang tidak terfilter oleh AdBlockID, jangan ragu untuk membuat issue di sini :D


## Generate File

### Persiapan
Untuk menyatukan semua file ke dalam sebuah file [adblockid.txt](https://raw.githubusercontent.com/realodix/AdBlockID/master/output/adblockid.txt), Anda membutuhkan:

* [Python (2.7 atau 3.5+)](https://www.python.org/downloads/),
* pip.

Setelah semua sudah terinstall di komputer Anda, lalu jalankan perintah ini:

`$ pip install -e vendor/python-abp`

### Perintah Untuk generate
* Klik file `FOP.py` untuk mengurutkan.
* Klik file `generate.py` untuk menyatukan.
