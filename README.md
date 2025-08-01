<p align="center"><img src="https://i.imgur.com/iQB1Uti.jpg" /></p>
<br />

<p align="right">
<a href="https://github.com/realodix/AdBlockID/commits/main"><img src="https://img.shields.io/github/commit-activity/m/realodix/AdBlockID?label=Commits&style=flat-square"></a>
<a href="https://github.com/realodix/AdBlockID/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed/realodix/AdBlockID?label=Issues&style=flat-square"></a>
<a href="https://www.jsdelivr.com/package/gh/realodix/AdBlockID"><img src="https://data.jsdelivr.com/v1/package/gh/realodix/AdBlockID/badge"></a>
</p>

> <sup>Tertarik jadi **contributor**? Jangan ragu untuk membuat issue / pull request!
> <br>
> Tertarik jadi **[collaborator](https://help.github.com/en/github/setting-up-and-managing-your-github-user-account/permission-levels-for-a-user-account-repository#collaborator-access-on-a-repository-owned-by-a-user-account) / maintainer** di AdBlockID? Jangan ragu untuk beritahu Saya 😃</sup>

AdblockID adalah filter pemblokir/penghilang iklan di situs berbahasa Indonesia dan Malaysia, sebagai pelengkap filter Internasional seperti [EasyList](https://github.com/easylist/easylist), [uBlock filters](https://github.com/uBlockOrigin/uAssets) dan [AdGuard Base Filter](https://github.com/AdguardTeam/AdguardFilters). Dirancang khusus untuk membuat Anda lebih nyaman dalam berselancar di internet.

## Manfaat Yang Anda Dapatkan
1. Menghilangkan iklan di **ribuan** situs web portal berita online dari berbagai jaringan besar seperti detik Network, Kompas Gramedia Group, MNC Portal, Tempo, Jaringan Media Siber Indonesia, Asosiasi Media Siber Indonesia, ProMedia Teknologi dan hingga ke portal berita online daerah.
2. Menghilangkan iklan di **ribuan** situs web nonton seperti LK21, situs web manga berbahasa indonesia, hingga situs dewasa.
3. **Faster, More Enjoyable Browsing**: Ucapkan selamat tinggal kepada iklan (terutama iklan yang bermuatan konten dewasa), PopAds dan banyak lagi.
4. **Anti-blocker-defusing**: Melumpuhkan detektor adblock untuk memungkinkan Anda terus menggunakan adblocker.
5. **Clean:** Halaman web jadi bersih dan nyaman. No `extra` abracadabra!

<sup>* Perlu diperhatikan, walaupun manfaatnya terlihat sangat menggiurkan, tetapi walau bagaimanapun tidak ada produk yang sempurna.</sup>


## Subscription

> [!TIP]
> AdBlockID sudah tersedia di AdGuard, Anda tidak perlu melakukan subscribe manual.

| Name           | Subscription | Raw File | Description |
| -------------- | --------- | -------- | ----------- |
| AdBlockID      | [Subscribe][ABID_Subs] | [jsdelivr.net/gh/realodix/.../adblockid.adfl.txt][ABID_Raw] | Main filter |
| AdBlockID Plus | [Subscribe][ABID-Plus_Subs] | [jsdelivr.net/gh/realodix/.../adblockid_plus.adfl.txt][ABID-Plus_Raw] | Extension |

[ABID_Subs]: https://subscribe.adblockplus.org/?location=https://cdn.jsdelivr.net/gh/realodix/AdBlockID@master/dist/adblockid.adfl.txt&title=AdBlockID
[ABID_Raw]: https://cdn.jsdelivr.net/gh/realodix/AdBlockID@master/dist/adblockid.adfl.txt
[ABID-Plus_Subs]: https://subscribe.adblockplus.org/?location=https://cdn.jsdelivr.net/gh/realodix/AdBlockID@master/dist/adblockid_plus.adfl.txt&title=AdBlockID%20Plus
[ABID-Plus_Raw]: https://cdn.jsdelivr.net/gh/realodix/AdBlockID@master/dist/adblockid_plus.adfl.txt

<!-- #### Developer

> ⚠️ Link `adblockid.pages.dev` dapat berisi filter yang masih dalam tahap uji coba dan mungkin dapat merusak di sebagian situs. Pastikan Anda sadar dengan peringatan ini saat menggunakannya.

| Name           | Subscription | Raw File | Description |
| -------------- | --------- | -------- | ----------- |
| AdBlockID      | [Subscribe][ABID_Subs_cf] | [adblockid.pages.dev/adblockid.adfl.txt][ABID_Raw_cf] | Main filter |
| AdBlockID Plus | [Subscribe][ABID-Plus_Subs_cf] | [adblockid.pages.dev/adblockid_plus.adfl.txt][ABID-Plus_Raw_cf] | Extension | -->

[ABID_Subs_cf]: https://subscribe.adblockplus.org/?location=https://adblockid.pages.dev/adblockid.adfl.txt&title=AdBlockID
[ABID_Raw_cf]: https://adblockid.pages.dev/adblockid.adfl.txt
[ABID-Plus_Subs_cf]: https://subscribe.adblockplus.org/?location=https://adblockid.pages.dev/adblockid_plus.adfl.txt&title=AdBlockID%20Plus
[ABID-Plus_Raw_cf]: https://adblockid.pages.dev/adblockid_plus.adfl.txt


#### FAQ
- **Q**: Apa bedanya antara AdBlockID dan AdBlockID Plus? <br>
  **A**: AdBlockID berfokus hanya pada website Indonesia; dan AdBlockID Plus pada dasarnya adalah personal filter yang Saya bagikan untuk melengkapi AdBlockID.


## Cara Menggunakan

> [!IMPORTANT]
> Pastikan Anda hanya menggunakan AdBlockID di AdGuard dan uBlock Origin ya guys. Alasannya cukup sepele, karena saat ini sebagian besar fitur ajaib yang ada di dalam AdBlockID, hanya dapat dijalankan oleh AdGuard dan uBlock Origin saja 😃

#### Desktop
1. Buka *browser* favorit Anda ([Chrome](https://www.google.com/chrome/), [Firefox](https://www.mozilla.org/firefox/), [Microsoft Edge](https://www.microsoft.com/edge), etc)
2. *Install* salah satu ekstensi dari berikut ini: [AdGuard Browser extension](https://adguard.com/en/adguard-browser-extension/overview.html) atau [uBlock Origin](https://github.com/gorhill/uBlock#installation).
3. Install AdBlockID
   - **AdGuard**: Cukup aktifkan AdBlockID di bagian *language-specific*.
   - **uBlock Origin**: Pada table di atas, klik `Subscribe` atau tambahkan `Raw link` di kotak import. Lebih lanjut lihat [`Import 3rd-party filter lists`](https://github.com/gorhill/uBlock/wiki/Filter-lists-from-around-the-web#import-3rd-party-filter-lists).

#### Mobile
- **Browser (Android)**: Anda dapat menggunakan [AdGuard Browser extension](https://adguard.com/en/adguard-browser-extension/overview.html) atau [uBlock Origin](https://github.com/gorhill/uBlock) pada browser yang mendukung extensi, seperti [Firefox](https://play.google.com/store/apps/details?id=org.mozilla.firefox) dan [Microsoft Edge](https://play.google.com/store/apps/details?id=com.microsoft.emmx). Cara install AdBlockID mirip seperti di desktop.
- **Android**: [AdGuard for Android](https://adguard.com/en/adguard-android/overview.html), aktifkan AdBlockID di bagian *language-specific*.
- **iOS**: [AdGuard for iOS](https://adguard.com/en/adguard-ios/overview.html), aktifkan AdBlockID.

#### Tutorial spesifik cara memasang AdBlockID:
- [AdGuard](/docs/Adguard.md)
- [uBlock Origin](/docs/uBlock_Origin.md)


## Berkontribusi
Terima kasih telah mempertimbangkan untuk berkontribusi, Saya sangat menghargai komitmen Anda. Menggunakan filter AdBlockID di ad blocker favorit Anda sudah merupakan dukungan besar, tetapi ada cara terbaik lainnya untuk berkontribusi:

- ⭐ Berikan AdBlockID bintang/star di GitHub. Karena jika Anda tidak menggunakan AdBlockID tetapi menyukainya, Anda setidaknya bisa menjadi stargazer!
- ✍️ [Membuat issue][GHIssuesNew]. Bantu Kami mengetahui jika ada iklan yang masih mengganggu Anda di luar sana.
- 💬 Bantu Kami menjawab dan memecahkan masalah di halaman [issues][GHIssuesPage] dan [diskusi][GHDiscussionsPage]. Jawaban Anda sangat membantu.
- ✍️ Buat [`pull requests`][GHGlossaryPullReq] di GitHub untuk memberikan perbaikan dan peningkatan. Otomatis terdaftar sebagai [kontributor][GHContributorsPage]!
- 📢 Beritahu orang terdekat Anda, agar makin banyak yang bisa merasakan manfaat dari AdBlockID.
- 🍔 Mari kita kopdar jika Anda sedang berada di sekitar Jakarta!

[GHIssuesNew]: https://github.com/realodix/AdBlockID/issues/new/choose
[GHIssuesPage]: https://github.com/realodix/AdBlockID/issues
[GHDiscussionsPage]: https://github.com/realodix/AdBlockID/discussions
[GHContributorsPage]: https://github.com/realodix/AdBlockID/graphs/contributors
[GHGlossaryPullReq]: https://docs.github.com/en/get-started/quickstart/github-glossary#pull-request


## Development
Lihat [/docs/Development.md](/docs/Development.md)
