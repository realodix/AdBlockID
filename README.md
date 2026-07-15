<p align="center"><img width="200" height="200" alt="Logo" src="https://raw.githubusercontent.com/realodix/AdBlockID-src/refs/heads/main/art/logo.png" /></p>

<h1 align="center">AdBlockID Filters</h1>

<p align="right">
<a href="https://github.com/realodix/AdBlockID/commits/main"><img src="https://img.shields.io/github/commit-activity/m/realodix/AdBlockID?label=Commits&style=flat-square"></a>
<a href="https://github.com/realodix/AdBlockID/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed/realodix/AdBlockID?label=Issues&style=flat-square"></a>
<a href="https://www.jsdelivr.com/package/gh/realodix/AdBlockID"><img src="https://data.jsdelivr.com/v1/package/gh/realodix/AdBlockID/badge"></a>
</p>


Filter pemblokir iklan untuk situs berbahasa Indonesia dan Malaysia.

AdBlockID dibuat untuk pengguna yang menuntut pengalaman berselancar yang bersih dari iklan, cepat, dan tanpa interupsi. Melenyapkan gangguan, menembus dinding anti-adblock, dan mengembalikan fokus Anda pada konten.

<!-- ### Satu filter, banyak gangguan hilang

#### 01/Block - Iklan
Hilangkan iklan di ribuan situs berita, forum, streaming, manga, dan situs populer lainnya.

#### 02/Clean - Halaman web
Singkirkan elemen pengganggu, placeholder kosong, dan sisa-sisa iklan yang membuat halaman terlihat berantakan.

#### 03/Anti-Adblock Immunity
Berhenti berdebat dengan peringatan "matikan adblock Anda". Filter ini menetralkan skrip deteksi secara otomatis, memastikan Anda tetap tidak terdeteksi dan konten tetap terbuka. -->

<br>

| Name           | Subscription | Raw File |
| -------------- | --------- | -------- |
| AdBlockID      | [Subscribe][ABID_Subs] | [jsdelivr.net/gh/realodix/.../adblockid.adfl.txt][ABID_Raw] |
| AdBlockID Plus | [Subscribe][ABID-Plus_Subs] | [jsdelivr.net/gh/realodix/.../adblockid_plus.adfl.txt][ABID-Plus_Raw] |
| Annoyances | [Subscribe][ABID-ANY_Subs] | [jsdelivr.net/gh/realodix/.../annoyance.txt][ABID-ANY_Raw] |

#### # AdBlockID

Filter utama AdBlockID untuk menghilangkan iklan di situs berbahasa Indonesia. Gunakan bersamaan dengan EasyList sebagai dasarnya.

#### # AdBlockID Plus

- Self-promotion banner, search ads, campaign banner, fake button.
- Mendukung style fixer untuk menata ulang tata letak halaman yang berantakan setelah iklan dihilangkan.
- Website Internasional yang memiliki pilihan bahasa Indonesia.

Gunakan AdBlockID sebagai dasarnya.

#### # Annoyances

- Remove: Cookie warning, pop-up banner, autoplay pop-up video, download app bar, subscription offers, AI suggestion.
- Defuse: Automated safelink, automated link attribution, right-click protection, copy-paste protection.

Gunakan filter annoyances dari AdGuard atau Easylist sebagai dasarnya.


[ABID_Subs]: https://subscribe.adblockplus.org/?location=https://cdn.jsdelivr.net/gh/realodix/AdBlockID@master/dist/adblockid.adfl.txt&title=AdBlockID
[ABID_Raw]: https://cdn.jsdelivr.net/gh/realodix/AdBlockID@master/dist/adblockid.adfl.txt
[ABID-Plus_Subs]: https://subscribe.adblockplus.org/?location=https://cdn.jsdelivr.net/gh/realodix/AdBlockID@master/dist/adblockid_plus.adfl.txt&title=AdBlockID%20Plus
[ABID-Plus_Raw]: https://cdn.jsdelivr.net/gh/realodix/AdBlockID@master/dist/adblockid_plus.adfl.txt
[ABID-ANY_Subs]: https://subscribe.adblockplus.org/?location=https://cdn.jsdelivr.net/gh/realodix/AdBlockID@master/dist/annoyance.txt&title=AdBlockID%20-%20Annoyances
[ABID-ANY_Raw]: https://cdn.jsdelivr.net/gh/realodix/AdBlockID@master/dist/annoyance.txt


<!-- #### Developer

> ⚠️ Link `adblockid.pages.dev` dapat berisi filter yang masih dalam tahap uji coba dan mungkin dapat merusak di sebagian situs. Pastikan Anda sadar dengan peringatan ini saat menggunakannya.

| Name           | Subscription | Raw File | Description |
| -------------- | --------- | -------- | ----------- |
| AdBlockID      | [Subscribe][ABID_Subs_cf] | [adblockid.pages.dev/adblockid.adfl.txt][ABID_Raw_cf] | Main filter |
| AdBlockID Plus | [Subscribe][ABID-Plus_Subs_cf] | [adblockid.pages.dev/adblockid_plus.adfl.txt][ABID-Plus_Raw_cf] | Extension |

[ABID_Subs_cf]: https://subscribe.adblockplus.org/?location=https://adblockid.pages.dev/adblockid.adfl.txt&title=AdBlockID
[ABID_Raw_cf]: https://adblockid.pages.dev/adblockid.adfl.txt
[ABID-Plus_Subs_cf]: https://subscribe.adblockplus.org/?location=https://adblockid.pages.dev/adblockid_plus.adfl.txt&title=AdBlockID%20Plus
[ABID-Plus_Raw_cf]: https://adblockid.pages.dev/adblockid_plus.adfl.txt -->


## Cara Menggunakan

> [!IMPORTANT]
> Pastikan Anda hanya menggunakan AdBlockID di AdGuard dan uBlock Origin ya guys. Alasannya cukup sepele, karena saat ini sebagian besar fitur ajaib yang ada di dalam AdBlockID, hanya dapat dijalankan oleh AdGuard dan uBlock Origin saja 😃

#### Desktop
1. Buka *browser* favorit Anda ([Chrome](https://www.google.com/chrome/), [Firefox](https://www.mozilla.org/firefox/), [Microsoft Edge](https://www.microsoft.com/edge), etc)
2. *Install* salah satu ekstensi dari berikut ini: [AdGuard Browser extension](https://adguard.com/en/adguard-browser-extension/overview.html) atau [uBlock Origin](https://github.com/gorhill/uBlock#installation).
3. Install AdBlockID
   - **AdGuard**: Cukup aktifkan AdBlockID di bagian *language-specific*. Lebih lanjut lihat [/docs/Adguard.md](/docs/Adguard.md).
   - **uBlock Origin**: Pada table di atas, klik `Subscribe` atau tambahkan `Raw link` di kotak import. Lebih lanjut lihat [/docs/uBlock_Origin.md](/docs/uBlock_Origin.md).

#### Mobile
- **Browser (Android)**: Anda dapat menggunakan [AdGuard Browser extension](https://adguard.com/en/adguard-browser-extension/overview.html) atau [uBlock Origin](https://github.com/gorhill/uBlock) pada browser yang mendukung extensi, seperti [Firefox](https://play.google.com/store/apps/details?id=org.mozilla.firefox) dan [Microsoft Edge](https://play.google.com/store/apps/details?id=com.microsoft.emmx). Cara install AdBlockID mirip seperti di desktop.
- **Android**: [AdGuard for Android](https://adguard.com/en/adguard-android/overview.html), aktifkan AdBlockID di bagian *language-specific*.
- **iOS**: [AdGuard for iOS](https://adguard.com/en/adguard-ios/overview.html), aktifkan AdBlockID.


## Berkontribusi
Kunjungi [`realodix/AdBlockID-src`](https://github.com/realodix/AdBlockID-src).
