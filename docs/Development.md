## Persiapan
Untuk menyatukan semua file ke dalam sebuah file [adblockid.txt](/output/adblockid.txt), Anda membutuhkan:

- [Python (2.7 atau 3.5+)](https://www.python.org/downloads/).
- [pip](https://pypi.org/project/pip/).

Setelah semua sudah terinstall di komputer Anda, lalu jalankan perintah ini:

`$ pip install -e tools/filters-compiler`



## Panduan untuk menulis filter

Panduan ini dirancang untuk membantu Anda menulis dan mengelola filter.

- **Adblock Plus**: [How to write filters](https://help.eyeo.com/en/adblockplus/how-to-write-filters).
- **Adblock Plus**: [Adblock Plus filters explained](https://adblockplus.org/filter-cheatsheet).
- **AdGuard**: [How to create your own ad filters](https://kb.adguard.com/en/general/how-to-create-your-own-ad-filters).
- **uBlock Origin**: [Static filter syntax](https://github.com/gorhill/uBlock/wiki/Static-filter-syntax).
- [Syntax meanings that are actually human readable](https://github.com/DandelionSprout/adfilt/blob/master/Wiki/SyntaxMeaningsThatAreActuallyHumanReadable.md).



## Struktur Direktori

Agar mudah di-maintain, daftar filter dipecah dan dikelompokkan ke dalam beberapa file, seperti bagan di bawah ini:

```
/src
 ├─ /packages
 │   ├─ adult-block.adbl       (GBlock) Iklan berkonten dewasa.
 │   ├─ adult-hide.adbl        (GHide) Iklan berkonten dewasa.
 │   ├─ adult-hide-ip.adbl     (GHide) Iklan berkonten dewasa.
 │   ├─ annoyances.adbl        [All] khusus untuk menangani beberapa limitasi.
 │   ├─ comic.adbl             [All] Situs komik ilegal.
 │   ├─ international.adbl     [All] Situs internasional.
 │   ├─ movie.adbl             [All] Situs nonton ilegal.
 │   ├─ sl_anti-adblock.adbl   Melumpuhkan detektor ad blocker, khusus untuk situs berjenis
 |   |                         safelink/shortlink.
 │   ├─ sl_anti-safelink.adbl  Melumpuhkan pembuatan safelink secara otomatis.
 │   └─ sl_safelink.adbl       [All, except sl_anti-adblock.adbl & sl_anti-safelink.adbl),
 |                             khusus untuk situs berjenis safelink/shortlink.
 ├─ adservers.adbl          Daftar domain/IP penyedia layanan iklan pihak ketiga.
 ├─ anti-adblock.adbl       [All] khusus untuk melumpuhkan detektor ad blocker.
 ├─ extended.adbl           Perbaiki tampilan situs setelah iklannya dihilangkan.
 ├─ general_block.adbl      Filter general untuk blokir iklan
 ├─ general_hide.adbl       Filter general untuk sembunyikan iklan jika tidak dapat diblokir
 ├─ specific_block.adbl     Filter spesifik untuk blokir iklan
 ├─ specific_hide.adbl      Filter spesifik untuk sembunyikan iklan jika tidak dapat diblokir
 ├─ specific_hide_ext.adbl  Hampir mirip seperti specific_hide.adbl, namun prosedural.
 ├─ thirdparty.adbl         Hampir mirip seperti di adservers.adbl, namun layanan utama dari situs
 │                          tersebut bukan untuk menyediakan iklan.
 └─ whitelist.adbl          Dalam kasus tertentu, Kita perlu memasukkan domain/IP situs ke dalam
                            whitelist. Contoh: Fungsi utama dari situs tersebut tidak jalan karena
                            terdapat kesalahan blokir.
```

<sup>***All**: fsfs.</sup> <br>
<sup>***GBlock**: fsfs.</sup> <br>
<sup>***GHide**: fsfs.</sup> <br>


## Development Tools

Anda dapat menggunakannya dengan 2 cara:
#### Terminal

- `./build.sh`

  Mengurutkan, merapikan dan menggabungkan semua filter pada bagan di atas ke dalam 1 file bernama `adblockid.txt` di folder `output`.

- `python tools/fop/fop.py`

  Mengurutkan dan merapikan semua filter pada bagan di atas.

- `flrender -i abid=. template/adblockid.adbl output/adblockid.txt`

  Menggabungkan semua filter pada bagan di atas ke dalam 1 file bernama `adblockid.txt` di folder `output`.

#### Visual Studio Code Tasks

Klik `Ctrl+Shift+P`, lalu klik `Tasks: Run Task`, maka akan terdapat beberapa pilihan:

- **Build**: Mengurutkan, merapikan dan menggabungkan semua filter pada bagan di atas ke dalam 1 file bernama `adblockid.txt` di folder `output`.
- **FOP**: Mengurutkan dan merapikan semua filter pada bagan di atas.

#### Web Service
- [ABP Redundancy check](https://adblockplus.org/redundancy_check)
- [ABPVN Redundancy check](https://abpvn.com/ruleChecker/redundantRuleChecker.html)

## Format Pesan Commit

Spesifikasi untuk menambahkan makna yang dapat dibaca manusia dan mesin untuk membuat pesan. Untuk contoh penggunaannya, Anda dapat melihat [history commit](https://github.com/realodix/AdBlockID/commits).

| Type   | Deskripsi |
| ------ | --------- |
| `AA`   | Anti-Adblock. |
| `M`    | Maintain filter. |
| `P`    | Problem. Tandai dengan `P` untuk perbaikan masalah yang ditimbulkan oleh AdBlockID atau masalah yang disebabkan oleh filter utama (easylist, AdGuard base filter & uBlock filters) yang ingin dibenerin dengan AdBlockID.|
| `docs` | Edit file dokumentasi pada folder `docs`, termasuk `readme.md` dan dokumentasi pada file fragment AdBlockID (folder `src`) . |
| `chore(<scope>)` | Semua pengeditan pada folder (`/tools`, `/.vscode`, `/.github`) dan file (`.editorconfig`, `.gitignore` & `build.sh`). |
