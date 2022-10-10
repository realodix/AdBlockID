> Reviewing:
> https://raw.githubusercontent.com/realodix/AdBlockID/master/output/adblockid_plus.txt
>
>   *= being a wildcard filter, it is an inherit slow filter. And should limited as much as possible. Would drag down performance of the browser.
>    Has a few english filters already covered in Easylist (which we use)

Sayangnya, filter [AdBlockID Plus](https://raw.githubusercontent.com/realodix/AdBlockID/master/output/adblockid_plus.txt) adalah filter yang tidak stabil dan bisa memberatkan browser. Ini cocok digunakan hanya di situs2 tertentu saja, lalu kembali dimatikan ketika membuka situs2 umum.

Setiap filter yang sudah teruji stabil, akan dimasukkan ke dalam [AdBlockID](https://raw.githubusercontent.com/realodix/AdBlockID/master/output/adblockid.txt).


> Reviewing: https://raw.githubusercontent.com/realodix/AdBlockID/master/output/adblockid.txt (not sure why they can’t be combined with both lists)
>
>    - Needs further optimizations; /*120x280*.gif$image /*betawitoto*.$image … etc (isn’t optimized, and considered slow filters)
>    - Remove as many generic filters as possible, and target just the regional sites. This would avoid redundancy with Easylist. Testing/ and using the list with Easylist/Easyprivacy. Remove any double ups/unneeded filters etc.
>    - Remove English/non Indonesia/Malaysian sites.
>    - Blocking various ##[href="https://bit.ly/3ybGTcA"] Not sure how related to Indonesia & Malaysia, having hardcoded blocks can be out of date quicky. I would for example use: domain.com,domain2.com##[href^="https://bit.ly/"] as a better example.
>
> Seems its been combined with other lists? (anti-adblock etc). The list needs to be cleaned up before being considered imo.
