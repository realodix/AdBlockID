## Panduan Menulis Filter

Panduan ini dirancang untuk membantu Anda menulis dan mengelola filter.

- **Adblock Plus**: [How to write filters](https://help.eyeo.com/en/adblockplus/how-to-write-filters)
- **Adblock Plus**: [Adblock Plus filters explained](https://adblockplus.org/filter-cheatsheet)
- **AdGuard**: [How to create your own ad filters](https://adguard.com/kb/general/ad-filtering/create-own-filters/)
- **uBlock Origin**: [Static filter syntax](https://github.com/gorhill/uBlock/wiki/Static-filter-syntax)
- [Syntax meanings that are actually human readable](https://github.com/DandelionSprout/adfilt/blob/master/Wiki/SyntaxMeaningsThatAreActuallyHumanReadable.md)



## Struktur Direktori

Agar mudah di-maintain, daftar filter dipecah dan dikelompokkan ke dalam beberapa file.

```
/src
 ├─ /modules
 │   ├─ adult.adfl                [S] ...
 │   ├─ adult-block.adfl          [G] Blokir iklan berkonten dewasa.
 │   ├─ adult-hide.adfl           [G] Sembunyikan iklan berkonten dewasa.
 │   ├─ annoyance.adfl            [G/S] Menghilangkan elemen yang mengganggu.
 │   ├─ annoyance_limitation.adfl [G/S] Menangani beberapa limitasi.
 │   ├─ annoyance_safelink.adfl   [G/S] Menampilkan link asli yang ditutupi oleh safelink.
 │   ├─ comic.adfl                [All] Situs komik ilegal.
 │   ├─ international.adfl        [All] Situs internasional.
 │   ├─ movie.adfl                [All] Situs nonton ilegal.
 │   └─ safelink.adfl             [All] Situs berjenis safelink/shortlink.
 ├─ /packages               AdBlockID+
 │   └─ ...
 ├─ adservers.adfl          [G] Daftar domain/IP penyedia layanan iklan pihak ketiga.
 ├─ anti-adblock.adfl       [G/S] Melumpuhkan ad block detection.
 ├─ extended.adfl           [S] Perbaiki tampilan situs setelah iklannya dihilangkan.
 ├─ general_block.adfl      [G] Blokir iklan.
 ├─ general_hide.adfl       [G] Sembunyikan iklan.
 ├─ specific_block.adfl     [S] Blokir iklan.
 ├─ specific_hide.adfl      [S] Sembunyikan iklan.
 ├─ specific-hide_2.adfl    [S] ...
 ├─ thirdparty.adfl         [G] Mirip seperti filter di adservers.adfl, namun layanan utama
 │                          dari domain/IP situs tersebut bukan untuk menyediakan iklan.
 └─ whitelist.adfl          [G/S] Mengembalikan sesuatu yang seharusnya ada, namun hilang
                            karena tidak sengaja terblokir/disembunyikan.
```

<sup>
* Penjelasan lengkap ada di masing-masing file. <br>
* [All]: Menangani berbagai hal seperti iklan, ad block detection, hingga annoyance. Filter bersifat spesifi dan general. <br>
* [G]: Filter bersifat general, tidak mengarah secara spesifik ke situs tertentu. <br>
* [S]: Filter bersifat spesifik, mengarah secara spesifik ke situs tertentu.
</sup>


## Development Tools
### Requirements

- [Python (2.7 atau 3.5+)](https://www.python.org/downloads/)
- [pip](https://pypi.org/project/pip/)

Setelah semua sudah terinstall di komputer Anda, lalu jalankan perintah ini:

`$ pip install -e tools/filter-combiner`

#### Terminal Command

- `./build.sh`

  Mengurutkan dan merapikan filter pada folder `src`, serta menggabungkannya ke dalam 1 file di folder `dist`.

  VSCode Task: **`Build`**

- `flcombine -i abid=. template/adblockid.template.txt dist/adblockid.adfl.txt`

  Menggabungkan semua filter AdBlockID pada folder `src` ke dalam 1 file (`dist/adblockid.adfl.txt`).

- `flcombine -i abid=. template/adblockid_plus.template.txt dist/adblockid_plus.adfl.txt`

  Menggabungkan semua filter AdBlockID Plus pada folder `src` ke dalam 1 file (`dist/adblockid_plus.adfl.txt`).

- `python tools/fop/fop.py -d src`

  Mengurutkan dan merapikan filter.

  VSCode Task: **`FOP`**

#### Web Service
- [ABP Redundancy check](https://adblockplus.org/redundancy_check)
- [ABPVN Redundancy check](https://abpvn.com/ruleChecker/redundantRuleChecker.html)
