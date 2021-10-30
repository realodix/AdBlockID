## Panduan untuk menulis filter

Panduan ini dirancang untuk membantu Anda menulis dan mengelola filter.

- **Adblock Plus**: [How to write filters](https://help.eyeo.com/en/adblockplus/how-to-write-filters).
- **Adblock Plus**: [Adblock Plus filters explained](https://adblockplus.org/filter-cheatsheet).
- **AdGuard**: [How to create your own ad filters](https://kb.adguard.com/en/general/how-to-create-your-own-ad-filters).
- **uBlock Origin**: [Static filter syntax](https://github.com/gorhill/uBlock/wiki/Static-filter-syntax).
- [Syntax meanings that are actually human readable](https://github.com/DandelionSprout/adfilt/blob/master/Wiki/SyntaxMeaningsThatAreActuallyHumanReadable.md).



## Struktur Direktori

Agar mudah di-maintain, daftar filter dipecah dan dikelompokkan ke dalam beberapa file.

```
/src
 ├─ /packages
 │   ├─ adult-block.adbl          [G] Blokir iklan berkonten dewasa.
 │   ├─ adult-hide.adbl           [G] Sembunyikan iklan berkonten dewasa.
 │   ├─ adult-hide-ip.adbl        [G] Sembunyikan iklan berkonten dewasa.
 │   ├─ annoyance.adbl            [G/S] Menghilangkan elemen yang mengganggu.
 │   ├─ annoyance_limitation.adbl [G/S] Menangani beberapa limitasi.
 │   ├─ annoyance_safelink.adbl   [G/S] Menampilkan link asli yang ditutupi oleh safelink.
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
 ├─ specific_hide_ext.adbl  [S] Mirip seperti filter di specific_hide.adbl, namun prosedural.
 ├─ thirdparty.adbl         [G] Mirip seperti filter di adservers.adbl, namun layanan utama
 │                          dari domain/IP situs tersebut bukan untuk menyediakan iklan.
 └─ whitelist.adbl          [G/S] Mengembalikan sesuatu yang seharusnya ada, namun hilang
                            karena tidak sengaja terblokir/disembunyikan.
```

<sup>
* Penjelasan lengkap ada di masing-masing file. <br>
*[All]: Menangani berbagai hal seperti iklan, ad block detection, hingga annoyance. Filter bersifat spesifi dan general. <br>
*[G]: Filter bersifat general, tidak mengarah secara spesifik ke situs tertentu. <br>
*[S]: Filter bersifat spesifik, mengarah secara spesifik ke situs tertentu.
</sup>


## Development Tools
### Requirements

- [Python (2.7 atau 3.5+)](https://www.python.org/downloads/).
- [pip](https://pypi.org/project/pip/).

Setelah semua sudah terinstall di komputer Anda, lalu jalankan perintah ini:

`$ pip install -e tools/filters-compiler`

#### Terminal Command

- `./build.sh`

  Mengurutkan dan merapikan filter, serta menggabungkannya ke dalam 1 file (`adblockid.txt`) di folder `output`.

  VSCode Task: **`Build`**

- `flrender -i abid=. template/adblockid.adbl output/adblockid.txt`

  Menggabungkan semua filter ke dalam 1 file (`adblockid.txt`) di folder `output`.

  VSCode Task: **`FOP`**

- `python tools/fop/fop.py`

  Mengurutkan dan merapikan filter.

#### Web Service
- [ABP Redundancy check](https://adblockplus.org/redundancy_check)
- [ABPVN Redundancy check](https://abpvn.com/ruleChecker/redundantRuleChecker.html)
