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
 │   ├─ adult-block.adbl          [G] Blokir iklan berkonten dewasa.
 │   ├─ adult-hide.adbl           [G] Sembunyikan iklan berkonten dewasa.
 │   ├─ adult-hide-ip.adbl        [G] Sembunyikan iklan berkonten dewasa.
 │   ├─ annoyance.adbl            [G/S] Menghilangkan elemen yang mengganggu.
 │   ├─ annoyance_limitation.adbl [G/S] Menangani beberapa limitasi.
 │   ├─ annoyance_safelink.adbl   [G/S] Menampilkan link aslinya.
 │   ├─ comic.adbl                [All] Situs komik ilegal.
 │   ├─ international.adbl        [All] Situs internasional.
 │   ├─ movie.adbl                [All] Situs nonton ilegal.
 │   └─ safelink.adbl             [All] Situs berjenis safelink/shortlink.
 ├─ adservers.adbl          [G] Daftar domain/IP penyedia layanan iklan pihak ketiga.
 ├─ anti-adblock.adbl       [G/S] Melumpuhkan ad block detection.
 ├─ extended.adbl           [S] Perbaiki tampilan situs setelah iklannya dihilangkan.
 ├─ general_block.adbl      [G] Blokir iklan.
 ├─ general_hide.adbl       [G] Sembunyikan iklan.
 ├─ specific_block.adbl     [S] Blokir iklan.
 ├─ specific_hide.adbl      [S] Sembunyikan iklan.
 ├─ specific_hide_ext.adbl  [S] Mirip seperti filter pada specific_hide.adbl, namun prosedural.
 ├─ thirdparty.adbl         [G] Mirip seperti filter pada adservers.adbl, namun layanan utama
 │                          dari domain/IP situs tersebut bukan untuk menyediakan iklan.
 └─ whitelist.adbl          [G/S] Mengembalikan sesuatu yang seharusnya ada, namun hilang
                            karena tidak sengaja terblokir/disembunyikan.
```

<sup>
* Penjelasan lengkap ada di masing-masing file. <br>
*[All]: Menangani berbagai hal seperti iklan, ad block detection, hingga annoyance. Filter bersifat spesifi dan general. <br>
*[G]: Filter bersifat general, tidak terbatas pada situs tertentu. <br>
*[S]: Filter bersifat spesifik, terbatas pada situs tertentu.
</sup>


## Development Tools

Tools pendukung sudah Kami sediakan, tetapi jika ini pertama kalinya bagi Anda, Anda perlu melakukan beberapa instalasi di komputer Anda.

- [Python (2.7 atau 3.5+)](https://www.python.org/downloads/).
- [pip](https://pypi.org/project/pip/).

Setelah semua sudah terinstall di komputer Anda, lalu jalankan perintah ini:

`$ pip install -e tools/filters-compiler`

#### Terminal

- `./build.sh`

  Mengurutkan, merapikan dan menggabungkan semua filter pada bagan di atas ke dalam 1 file bernama `adblockid.txt` di folder `output`.

  VS Code Task: **`Build`**

- `python tools/fop/fop.py`

  Mengurutkan dan merapikan semua filter pada bagan di atas.

- `flrender -i abid=. template/adblockid.adbl output/adblockid.txt`

  Menggabungkan semua filter pada bagan di atas ke dalam 1 file bernama `adblockid.txt` di folder `output`.

  VS Code Task: **`FOP`**

#### Visual Studio Code Tasks

Klik `Ctrl+Shift+P`, lalu klik `Tasks: Run Task`, maka akan terdapat beberapa pilihan:

- **Build**: Mengurutkan, merapikan dan menggabungkan semua filter pada bagan di atas ke dalam 1 file bernama `adblockid.txt` di folder `output`.
- **FOP**: Mengurutkan dan merapikan semua filter pada bagan di atas.

#### Web Service
- [ABP Redundancy check](https://adblockplus.org/redundancy_check)
- [ABPVN Redundancy check](https://abpvn.com/ruleChecker/redundantRuleChecker.html)

## Format Pesan Commit

Spesifikasi untuk menambahkan makna yang dapat dibaca manusia dan mesin untuk membuat pesan. Untuk contoh penggunaannya, Anda dapat melihat [history commit](https://github.com/realodix/AdBlockID/commits).

| Kode   | Cakupan         |
| ------ | --------------- |
| `AA`   | Anti-Adblock    |
| `M`    | Maintain filter |
| `P`    | Perbaikan masalah yang disebabkan oleh AdBlockID dan/atau oleh filter utama (easylist, AdGuard base filter & uBlock filters).|
| `docs` | Semuanya pada folder `docs`, termasuk file `readme.md` dan dokumentasi di setiap file filter AdBlockID (folder `src`) . |
| `chore(<scope>)` | Semua pengeditan pada repository AdBlockID, kecuali yang masuk dalam cakupan kode `docs`. |
