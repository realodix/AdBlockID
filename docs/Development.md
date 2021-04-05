### Persiapan
Untuk menyatukan semua file ke dalam sebuah file [adblockid.txt](/output/adblockid.txt), Anda membutuhkan:

- [Python (2.7 atau 3.5+)](https://www.python.org/downloads/).
- [pip](https://pypi.org/project/pip/).

Setelah semua sudah terinstall di komputer Anda, lalu jalankan perintah ini:

`$ pip install -e tools/python-abp_AdBlockID`

### Panduan untuk menulis filter

Panduan ini dirancang untuk membantu Anda menulis dan mengelola filter.

- **Adblock Plus**: [How to write filters](https://help.eyeo.com/en/adblockplus/how-to-write-filters).
- **Adblock Plus**: [Adblock Plus filters explained](https://adblockplus.org/filter-cheatsheet).
- **AdGuard**: [How to create your own ad filters](https://kb.adguard.com/en/general/how-to-create-your-own-ad-filters).
- **uBlock Origin**: [Static filter syntax](https://github.com/gorhill/uBlock/wiki/Static-filter-syntax).
- [Syntax meanings that are actually human readable](https://github.com/DandelionSprout/adfilt/blob/master/Wiki/SyntaxMeaningsThatAreActuallyHumanReadable.md).


### Development Tools

| File              | Deskripsi                                 |
| ----------------- | ----------------------------------------- |
| `build.sh`        | Menggabungkan filter list ke dalam file `adblockid.txt`. Hasilnya ada di folder `output`. |


#### Visual Studio Code Tasks

Sebagian besar filter pada AdBlockID ditulis dengan [Visual Studio Code](https://code.visualstudio.com/) dan berbagai tools pendukung telah diintegrasikan ke dalam Visual Studio Code melalui Tasks.

Anda dapat mengakses Visual Studio Code Tasks dengan menekan `Ctrl+Shift+P`, lalu tekan `Tasks: Run Task`.

- **Build**: Render _filter list fragments_ ke dalam file `adblockid.txt`. Hasilnya ada di folder `output`.
- **FOP**: Mengurutkan, menggabungkan dan memformat ulang beberapa  filter jika memungkinkan.


### Format Pesan Commit

Spesifikasi untuk menambahkan makna yang dapat dibaca manusia dan mesin untuk membuat pesan. Untuk contoh penggunaannya, Anda dapat melihat [history commit](https://github.com/realodix/AdBlockID/commits).

| Type   | Deskripsi |
| ------ | --------- |
| `AA`   | Anti-Adblock. |
| `M`    | Maintain filter. |
| `P`    | Problem. Tandai dengan `P` untuk perbaikan masalah yang ditimbulkan oleh AdBlockID atau masalah yang disebabkan oleh filter utama (easylist, AdGuard base filter & uBlock filters) yang ingin dibenerin dengan AdBlockID.|
| `docs` | Edit file dokumentasi pada folder `docs`, termasuk `readme.md` dan dokumentasi pada file fragment AdBlockID (folder `src`) . |
| `chore(<scope>)` | Semua pengeditan pada folder (`/tools`, `/.vscode`, `/.github`) dan file (`.editorconfig`, `.gitignore` & `build.sh`). |

### Struktur Direktori

Semua file fragment AdBlockID ada di dalam folder `src`, seperti bagan di bawah ini:

```
/src
 ├─ /packages
 │   ├─ adult-block.adbl       Filter umum untuk blockir iklan berkonten dewasa.
 │   ├─ adult-hide.adbl        Filter umum untuk menyembunyikan iklan berkonten dewasa.
 │   ├─ annoyances.adbl
 │   ├─ comic.adbl
 │   ├─ international.adbl
 │   ├─ movie.adbl
 │   ├─ sl_anti-adblock.adbl
 │   ├─ sl_anti-safelink.adbl
 │   └─ sl_safelink.adbl       Filter untuk menangani iklan pada situs safelink / shortlink.
 ├─ /template
 │   └─ ...
 ├─ adservers.adbl          Domain penyedia layanan iklan pihak ketiga.
 ├─ anti-adblock.adbl       Filter khusus menangani web yang mendeteksi dan melarang Anda
 │                          menggunakan Ad Blocker.
 ├─ extended.adbl           Extended CSS selectors dan lainnya.
 ├─ general_block.adbl      Filter umum untuk blockir content pada halaman web.
 ├─ general_hide.adbl       Filter umum untuk menyembunyikan content pada halaman web.
 ├─ specific_block.adbl     Secara spesifik hanya menyembunyikan content pada domain yang
 │                          disebutkan.
 ├─ specific_hide.adbl      Secara spesifik hanya blockir content pada domain yang
 │                          disebutkan.
 ├─ thirdparty.adbl         Domain yang fungsi utamanya bukan sebagai server, namun dalam
 │                          beberapa kasus dijadikan tempat untuk host iklan.
 └─ whitelist.adbl          Dalam kasus tertentu, Kita perlu memasukkan web ke dalam
                            whitelist. Contoh: Fungsi utama dari web tersebut tidak jalan
                            karena kesalahan blokir.
```
