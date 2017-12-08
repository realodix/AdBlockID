import subprocess
subprocess.call("flrender -i abid=. adblockid.template adblockid.txt")
subprocess.call("flrender -i abid=. template/adblockid.template output/adblockid.txt")
subprocess.call("flrender -i abid=. template/adblockid_ultimate.template output/adblockid_ultimate.txt")