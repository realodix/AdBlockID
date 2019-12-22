<p align="center"><img src="https://i.imgur.com/iQB1Uti.jpg" /></p>
<br />

![AdBlockID Version](https://img.shields.io/badge/Version-19.356.828-blue.svg?longCache=true&style=flat-square)
<img src="https://img.shields.io/badge/Updated-Dec 22, 2019 UTC-orange.svg?longCache=true&style=flat-square"
    alt="Dec 22, 2019 UTC" />

> <sup>Tertarik jadi **contributor**? Jangan ragu untuk membuat issue / pull request!
> <br>
> Tertarik jadi **[collaborator](https://help.github.com/en/github/setting-up-and-managing-your-github-user-account/permission-levels-for-a-user-account-repository#collaborator-access-on-a-repository-owned-by-a-user-account) / maintainer** pada AdBlockID? Jangan ragu untuk beritahu Saya 😃</sup>

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

**Tutorial spesifik cara memasang AdBlockID:**
- [uBlock](/docs/uBlock.md): uBlock Origin, Nano Adblocker, AdNauseam, uBlock Plus Adblocker.
- [AdGuard](/docs/Adguard.md): AdGuard Browser extension, AdGuard for Windows & AdGuard for Android.
- [AdBlock](/docs/Adblock-Plus.md): AdBlock, Adblock Plus, StopAll Ads.
- [Opera Ad Blocker](/docs/Opera-AdBlocker.md)
- [Adaware ad block](/docs/adaware-ad-block.md)


## Berkontribusi
Terima kasih banyak untuk Anda yang ingin berkontribusi. Saya sangat menghargai komitmen Anda. Menggunakan filter AdBlockID di Ad Blocker favorit Anda sudah merupakan dukungan besar, tetapi ada cara terbaik lainnya untuk berkontribusi:

- Beri AdBlockID bintang/star di GitHub. Karena jika Anda menggunakan dan menyukainya, Anda setidaknya bisa menjadi stargazer!
- [Membuat issue](https://github.com/realodix/AdBlockID/issues/new/choose). Bantu Kami mengetahui jika ada iklan yang masih mengganggu Anda di luar sana.
- Bantu Kami menjawab dan memecahkan masalah pada issue yang masih terbuka. Jawaban Anda sangat membantu.
- Buat `pull requests` di GitHub untuk memberikan perbaikan dan peningkatan. Otomatis terdaftar sebagai [kontributor](https://github.com/realodix/AdBlockID/graphs/contributors)!
- Beritahu orang terdekat Anda, agar makin banyak yang bisa merasakan manfaat dari AdBlockID.
- Mari kita kopdar jika Anda sedang berada di sekitar Jakarta!


## Development
### Persiapan
Untuk menyatukan semua file ke dalam sebuah file [adblockid.txt](/output/adblockid.txt), Anda membutuhkan:

- [Python (2.7 atau 3.5+)](https://www.python.org/downloads/).
- [pip](https://pypi.org/project/pip/).

Setelah semua sudah terinstall di komputer Anda, lalu jalankan perintah ini:

`$ pip install -e tools/python-abp`

atau

`$ pip install -t tools tools/python-abp`

### Panduan untuk menulis filter

Panduan ini dirancang untuk membantu Anda menulis dan mengelola filter.

- **Adblock Plus**: [How to write filters](https://help.eyeo.com/en/adblockplus/how-to-write-filters)
- **Adblock Plus**: [Adblock Plus filters explained](https://adblockplus.org/filter-cheatsheet)
- **AdGuard**: [How to create your own ad filters](https://kb.adguard.com/en/general/how-to-create-your-own-ad-filters)
- **uBlock Origin**: [Static filter syntax](https://github.com/gorhill/uBlock/wiki/Static-filter-syntax)
- [Syntax meanings that are actually human readable](https://github.com/DandelionSprout/adfilt/blob/master/Wiki/SyntaxMeaningsThatAreActuallyHumanReadable.md)


### Development Tools

| File              | Deskripsi                                 |
| ----------------- | ----------------------------------------- |
| `build.sh`        | Menggabungkan filter list ke dalam file `adblockid.txt`. Hasilnya ada di folder `output`. |
| `validatehost.sh` | Periksa apakah host sedang up / down berdasarkan header yang dikembalikan dari curl. |

Sebagian besar filter pada AdBlockID ditulis dengan [Visual Studio Code](https://code.visualstudio.com/) dan berbagai tools pendukung telah diintegrasikan ke dalam Visual Studio Code melalui Tasks.

#### Visual Studio Code Tasks

Anda dapat mengakses Visual Studio Code Tasks dengan menekan `Ctrl+Shift+P`, lalu tekan `Tasks: Run Task`.

- **Build**: Render _filter list fragments_ ke dalam file `adblockid.txt`. Hasilnya ada di folder `output`.
- **FOP**: Mengurutkan, menggabungkan dan memformat ulang beberapa  filter jika memungkinkan.
- **Build Readme**: Render file `readme.template` ke dalam `readme.md`.
- **Validate Host**: Memeriksa apakah host sedang up / down berdasarkan header yang dikembalikan dari curl.

### Format Pesan Commit

Spesifikasi untuk menambahkan makna yang dapat dibaca manusia dan mesin untuk membuat pesan. Untuk contoh penggunaannya, Anda dapat melihat [history commit](https://github.com/realodix/AdBlockID/commits).

| Type   | Deskripsi |
| ------ | --------- |
| `A`    | Semua jenis iklan, termasuk banner, pop-up, ad server, dll. |
| `AA`   | Anti-Adblock. |
| `M`    | Maintain filter. |
| `P`    | Problem. Tandai dengan `P` untuk perbaikan masalah yang ditimbulkan oleh AdBlockID atau masalah yang disebabkan oleh filter utama (easylist, AdGuard base filter & uBlock filters) yang ingin dibenerin dengan AdBlockID.|
| `docs` | Edit file dokumentasi pada folder `docs`, termasuk dokumentasi pada file fragment AdBlockID (folder `src`) dan file template untuk readme (`/tools/readme/readme.template`). |
| `chore(<scope>)` | Semua pengeditan pada folder (`/tools`, `/.vscode`, `/.github`) dan file (`.editorconfig`, `.gitignore`, `build.sh` & `validatehost.sh`). Tidak termasuk file template untuk readme (`/tools/readme/readme.template`). |

### Struktur Direktori

Semua file fragment AdBlockID ada di dalam folder `src`, seperti bagan di bawah ini:

<pre>
/src
 ├─ /addons
 │   ├─ adult-block.adbl
 │   ├─ adult-hide.adbl
 │   ├─ annoyances.adbl
 │   ├─ movie.adbl
 │   ├─ news.adbl
 │   ├─ scriptlet-ublock.adbl
 │   └─ shortlink.adbl
 ├─ /template
 │   └─ ...
 ├─ adservers.adbl
 ├─ anti-adblock.adbl
 ├─ general_block.adbl
 ├─ general_hide.adbl
 ├─ specific_block.adbl
 ├─ specific_hide.adbl
 ├─ thirdparty.adbl
 └─ whitelist.adbl
</pre>

- `adservers.adbl`: Domain penyedia layanan iklan pihak ketiga.
- `anti-adblock.adbl`: Filter khusus menangani web yang mendeteksi dan melarang Anda menggunakan Ad Blocker.
- `general_block.adbl`: Filter umum untuk blockir content pada halaman web.
- `general_hide.adbl`: Filter umum untuk menyembunyikan content pada halaman web.
- `specific_block.adbl`: Secara spesifik hanya memblokir content pada domain yang disebutkan.
- `specific_hide.adbl`: Secara spesifik hanya menyembunyikan content pada domain yang disebutkan.
- `thirdparty.adbl`: Domain yang fungsi utamanya bukan sebagai server, namun dalam beberapa kasus dijadikan tempat untuk host iklan.
- `whitelist.adbl`: Dalam kasus tertentu, Kita perlu memasukkan web ke dalam whitelist. Contoh: Fungsi utama dari web tersebut tidak jalan karena kesalahan blokir.
- `/addons/adult-block.adbl`: Filter umum untuk blockir iklan berkonten dewasa.
- `/addons/adult-hide.adbl`: Filter umum untuk menyembunyikan iklan berkonten dewasa.
- `/addons/annoyances.adbl`: Filter untuk menghilangkan element web yang cukup mengganggu. Contoh: notifikasi cookie.
- `/addons/movie.adbl`: Filter untuk menangani iklan pada situs nonton film online.
- `/addons/news.adbl`: Filter untuk menangani iklan pada situs berita.
- `/addons/scriptlet-ublock.adbl`: Filter umum untuk [uBlock Resources](https://github.com/gorhill/uBlock/wiki/Resources-Library).
- `/addons/shortlink.adbl`: Filter untuk menangani iklan pada situs safelink / shortlink.
