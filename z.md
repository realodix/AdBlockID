Waduh pembahasan di [community.brave.com/t/reque...28329](https://community.brave.com/t/request-add-new-regional-list-filter/428329) cukup teknis ya. Saya akan menjelaskannya secara singkat di sini, tetapi jika membutuhkan jawaban panjang, Sayang bersedia menjelaskannya.

----

Saat ini AdBlockID sudah dioptimalkan dan dibersihkan, jumlah filter dari yang sebelumnya 8,322 sekarang menjadi 8,303.

> - Remove as many generic filters as possible, and target just the regional sites. This would avoid redundancy with Easylist. Testing/ and using the list with Easylist/Easyprivacy. Remove any double ups/unneeded filters etc.

`##.home-banner-big-ads`

----

> Reviewing:
> https://raw.githubusercontent.com/realodix/AdBlockID/master/output/adblockid_plus.txt
>
>   *= being a wildcard filter, it is an inherit slow filter. And should limited as much as possible. Would drag down performance of the browser.
>    Has a few english filters already covered in Easylist (which we use)

Seperti yang di deskripsikan di [halaman depan](https://github.com/realodix/AdBlockID#readme) *"Patahkan berbagai batasan cakupan yang ada di AdBlockID"* dan deskripsi di [file filternya](https://raw.githubusercontent.com/realodix/AdBlockID/master/output/adblockid_plus.txt) *"Ekstensi untuk menambah cakupan situs yang tidak dapat dijangkau oleh AdBlockID"*. Jadi memang filter yang tidak dapat dimasukkan ke dalam AdBlockID akan dimasukkan ke dalam AdBlockID Plus, seperti personal filter (yang isinya sebagian situs luar) dan filter2 yang secara teori dapat memberatkan browser, walaupun dalam prakteknya hanya sebagian kecil situs saja (situs berbahasa Indonesia).


> Reviewing: https://raw.githubusercontent.com/realodix/AdBlockID/master/output/adblockid.txt (not sure why they can’t be combined with both lists)

Mengacu jawaban di atas, karena AdBlockID Plus diisi dengan filter yang tidak dapat dimasukkan ke dalam AdBlockID, jadi tidak mungkin disatukan.

>    - Needs further optimizations; `/*120x280*`.gif$image `/*betawitoto*`.$image … etc (isn’t optimized, and considered slow filters)

Sudah dioptimalkan

>    - Remove as many generic filters as possible, and target just the regional sites. This would avoid redundancy with Easylist. Testing/ and using the list with Easylist/Easyprivacy. Remove any double ups/unneeded filters etc.

Semua generic filter yang ada didapatkan dari situs berbahasa Indonesia, termasuk generic filter seperti `##.home-banner-big-ads` yang terlihat seperti filter untuk situs berbahasa Inggris. Setiap sebulan sekali, Saya selalu memeriksa apakah filter seperti `##.home-banner-big-ads` sudah ada di easylist. Caranya dengan memasukkan [AdBlockID/src/general-hide.adfl](https://raw.githubusercontent.com/realodix/AdBlockID/master/src/general-hide.adfl) dan [easylist/easylist_general_hide.txt](https://raw.githubusercontent.com/easylist/easylist/master/easylist/easylist_general_hide.txt) ke https://adblockplus.org/redundancy_check

>    - Remove English/non Indonesia/Malaysian sites.
>    - Blocking various `##[href="https://bit.ly/3ybGTcA"]` Not sure how related to Indonesia & Malaysia, having hardcoded blocks can be out of date quicky. I would for example use: `domain.com,domain2.com##[href^="https://bit.ly/"]` as a better example.
>
> Seems its been combined with other lists? (anti-adblock etc). The list needs to be cleaned up before being considered imo.
