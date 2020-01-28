#!/usr/bin/python3
''' ValidateHost
    Host Validator
    (r2c) 2016 Idx

    Simply check host state is up or down based on returned header from curl
    This app will parse and preload all host from: /host.txt
    Make sure FOP.py has been generated for any changes in unit filters

    By knowing down host, should come in handy adjusting obsolete filter

    Usage:
      python validatehost.py -h

      python validatehost.py -f host.txt -t 9050

      # run in background
      nohup python validatehost.py -t 9050 &


    Dependency (optional)
      Tor (Expert Bundle): https://www.torproject.org/download/download.html

      Running Tor as Service
      https://jeffchiu.wordpress.com/2013/06/27/kb-how-to-install-tor-as-a-windows-service/

    ---
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import os, sys, subprocess
import re, datetime, time, argparse

# host resources will be parsed from this file
filename='tools/validatehost/host.txt'

# down host will be writen to this file
log_downhost='tools/validatehost/downhost.log'

# list of exclude host being check
exclusions = [
  'bit.ly',
  'blogspot.com',
  'github.com',
  'rawgit.com',
  'raw.githubusercontent.com',
  'yourjavascript.com',
  'adservers.adbl',
  'adult-block.adbl',
  'adult-hide.adbl',
  'annoyances.adbl',
  'anti-adblock.adbl'
  'general_block.adbl',
  'general_hide.adbl',
  'movie.adbl',
  'news.adbl',
  'scriptlet-ublock.adbl',
  'specific_block.adbl',
  'specific_hide.adbl',
  'thirdparty.adbl',
  'whitelist.adbl',
  'plus_annoyance.adbl',
  'plus_anti-adblock.adbl',
  'plus_specific_block.adbl',
  'plus_specific_hide.adbl',
]

log_fh = False
curl_timeout = 60 # in seconds

# check tor proxy connectivity, must used with curl
def tor_OK(args):
  if not 'tor' in args:
    return False
  cmd = "curl -sL --socks4a localhost:"+args["tor"]+" http://check.torproject.org/ | egrep -iA 1 'congratulations' | head -n 1"
  ret = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  output, err = ret.communicate(b"input data that is passed to subprocess' stdin")
  return "browser is configured to use Tor" in str(output)
# endof:tor_OK


# Do ping/curl given host
def ping(host, args):
  """
  Returns True if host responds to a ping request
  """
  import platform

  is_windows = platform.system().lower()=="windows"

  # Ping parameters as function of OS
  ret = ""

  if 'curl' in args and args["curl"]:

    curl_opts = ""
    if 'tor' in args and args["tor"]:
      curl_opts = curl_opts +" --socks4a localhost:"+str(args["tor"])

    if 'timeout' in args and args["timeout"]:
      curl_opts = curl_opts +" --connect-timeout "+str(args["timeout"])

    cmd = "curl -sIL "+curl_opts+" http://"+host+" | egrep -iA 10 'HTTP/1.' | grep -iP '(?:\.\d\s+(?:4[0-2]\d{1}|30\d{1}|20\d{1}))|Location\:'"

    ret = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = ret.communicate(b"input data that is passed to subprocess' stdin")
    output = output.decode()
    output = output.strip()
    if not output:
      return False
    else:
      ret = "HTTP/1." in output or host in output

  else:
    ping_str = "-n 1" if is_windows else "-c 1"
    cmd = "ping " + ping_str + " " + host + " > nul" if is_windows else ""
    ret = os.system(cmd) == 0


  return ret
# endof:ping


# Write log of down host
def logdown(host, args):
  if 'log' in args and args["log"]:
    log_fh = open(log_downhost, 'a+')
    log_fh.write(host+"\n")
    log_fh.close()
# endof:logdown



# argument-parser
parser = argparse.ArgumentParser(prog="validatehost.py", usage='%(prog)s [options]', description='Validate host availability')
parser.add_argument('-t','--tor', help='Use Tor Proxy port (9050). Will switch to curl mode.', required=False)
parser.add_argument('-l','--log', help='Write log of down host, default: True', required=False, default=True)
parser.add_argument('-c','--curl', help='Use curl mode, default: True', required=False, default=True)
parser.add_argument('-f','--filter_filename', help='Path to subscription filter filename', required=False, default=filename)
parser.add_argument('-T','--timeout', help='Maximum time allowed for connection via curl', required=False)
args = vars(parser.parse_args())

if "filter_filename" in args and args["filter_filename"]:
  filename = args["filter_filename"]


if not os.path.exists(filename):
  print("Subscription File Not Found")
  print("> "+filename)
  print("")
  print("It should be generated by executing these commands:")
  print("$ ./build.sh")
  sys.exit()

else:

  print("Subscription found:")
  print("> "+filename)
  lastmod = os.path.getmtime(filename)
  tm = datetime.datetime.strptime(time.ctime(lastmod), "%a %b %d %H:%M:%S %Y")
  print("Last modified: " + str(tm))
  checksum = ""
  with open(filename, "r") as fo:
    content_string = fo.read()
    cucok = re.search('Checksum:\s*(\w+)', content_string)
    if cucok:
      checksum = cucok.group(0)
      print(checksum)
  print("")

  print("Downhost will be writen in this log file:")
  print("> "+log_downhost)
  if 'tor' in args and args["tor"]:
    print("")
    print("Using Tor Proxy on port: "+str(args["tor"]), end="")

    sys.stdout.flush()
    if not tor_OK(args):
      print("Unable connect with Tor Proxy")
      sys.exit()
    else:
      print(" [OK]")

    # force activate curl
    args["curl"] = True

  else:
    print("")
    print("[--Not using any proxy--]")



  # clearing log
  log_fh = open(log_downhost, 'w')
  tm = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  log_fh.write('[::Downhost:: Check: '+str(tm)+', Source: '+filename+(", "+checksum if checksum else "")+']'+"\n")
  log_fh.close()


lines = [line.rstrip('\n') for line in open(filename, "r")]
bulkhost = []
for line in lines:
  ValidIpAddressRegex = r"\b(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\b"

  ValidHostnameRegex = r"\b((?:[\da-z\.-]+)\.([a-z\.]{2,6}))\b"

  NonTLD = r"gif|png|jpg|jpeg|html|php|htm|js|css|ico|swf|asp"

  # parse valid hostname
  cucok = re.finditer(ValidHostnameRegex, line, re.IGNORECASE)
  if cucok:
    for match in cucok:
      host = match.group(0)

      if not re.search(NonTLD, host, re.IGNORECASE) and host not in bulkhost and host not in exclusions:
        bulkhost.append(host)


  # parse ip-address host
  cucok = re.finditer(ValidIpAddressRegex, line)
  if cucok:
    for match in cucok:
      host = match.group(0);

      # if ip host not in bulkhost:
      if host not in bulkhost and host not in exclusions:
        bulkhost.append(host)

# endfor:lines

# -------------------
nHost = len(bulkhost)
if nHost == 0:
  print("No Host not found in your subscription")
  print("> "+filename)

else:

  print("")
  print("Found " + str(nHost) + " host", end="")
  print("" if nHost <= 1 else "s")

  iStep = nHost
  baseLen = len( str(nHost) )

  for host in bulkhost:
    iStepStr = str(iStep)
    print("["+ iStepStr.zfill(baseLen) + "] " + host, end=" ")
    sys.stdout.flush()


    is_OK = ping(host, args)
    if 'tor' in args and args["tor"] and not is_OK:
      dummy_args = args.copy()
      dummy_args['tor'] = False
      print(" [2nd-step]", end="")
      is_OK = ping(host, dummy_args)


    if is_OK == True:
      print(" [OK]")
    else:
      print(" >>>> [DOWN] !! " + host + "")
      logdown(host, args)


    sys.stdout.flush()
    iStep = (iStep - 1)

logdown('[::eof::]', args)
#eof.
