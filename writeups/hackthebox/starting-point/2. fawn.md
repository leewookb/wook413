# HTB - Fawn

#very-easy #linux

[TOC]

#### What does the 3-letter acronym FTP stand for?

File Transfer Protocol

#### Which port does the FTP service listen on usually?

21

#### FTP sends data in the clear, without any encryption. What acronym is used for a later protocol designed to provide similar functionality to FTP but securely, as an extension of the SSH protocol?

SFTP

#### What is the command we can use to send an ICMP echo request to test our connection to the target?

ping

#### From your scans, what version is FTP running on the target?

vsftpd 3.0.3

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ nmap 10.129.1.47 -Pn -n --open --min-rate 3000 -p- 
Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-06 18:58 UTC
Nmap scan report for 10.129.1.47
Host is up (0.046s latency).
Not shown: 61808 closed tcp ports (reset), 3726 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT   STATE SERVICE
21/tcp open  ftp

Nmap done: 1 IP address (1 host up) scanned in 19.05 seconds
```

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ nmap 10.129.1.47 -sC -sV -p 21                    
Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-06 18:59 UTC
Nmap scan report for 10.129.1.47
Host is up (0.045s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.14.63
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 1
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0              32 Jun 04  2021 flag.txt
Service Info: OS: Unix

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1.38 seconds
```

#### From your scans, what OS type is running on the target?

Unix

#### What is the command we need to run in order to display the 'ftp' client help menu?

`ftp -?`

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ ftp -?
usage: ftp [-46AadefginpRtVv] [-N NETRC] [-o OUTPUT] [-P PORT] [-q QUITTIME]
           [-r RETRY] [-s SRCADDR] [-T DIR,MAX[,INC]] [-x XFERSIZE]
           [[USER@]HOST [PORT]]
           [[USER@]HOST:[PATH][/]]
           [file:///PATH]
           [ftp://[USER[:PASSWORD]@]HOST[:PORT]/PATH[/][;type=TYPE]]
           [http://[USER[:PASSWORD]@]HOST[:PORT]/PATH]
           [https://[USER[:PASSWORD]@]HOST[:PORT]/PATH]
           ...
       ftp -u URL FILE ...
       ftp -?
  -4            Only use IPv4 addresses
  -6            Only use IPv6 addresses
  -A            Force active mode
  -a            Use anonymous login
  -d            Enable debugging
  -e            Disable command-line editing
  -f            Force cache reload for FTP or HTTP proxy transfers
  -g            Disable file name globbing
  -i            Disable interactive prompt during multiple file transfers
  -N NETRC      Use NETRC instead of ~/.netrc
  -n            Disable auto-login
  -o OUTPUT     Save auto-fetched files to OUTPUT
  -P PORT       Use port PORT
  -p            Force passive mode
  -q QUITTIME   Quit if connection stalls for QUITTIME seconds
  -R            Restart non-proxy auto-fetch
  -r RETRY      Retry failed connection attempts after RETRY seconds
  -s SRCADDR    Use source address SRCADDR
  -t            Enable packet tracing
  -T DIR,MAX[,INC]
                Set maximum transfer rate for direction DIR to MAX bytes/s,
                with optional increment INC bytes/s
  -u URL        URL to upload file arguments to
  -V            Disable verbose and progress
  -v            Enable verbose and progress
  -x XFERSIZE   Set socket send and receive size to XFERSIZE
  -?            Display this help and exit
```

#### What is the username that is used over FTP when you want to log in without having an account?

anonymous

#### What is the response code we get for the FTP message 'Login successful'?

230

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ ftp $IP
Connected to 10.129.1.47.
220 (vsFTPd 3.0.3)
Name (10.129.1.47:kali): anonymous
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
```

#### There are a couple of commands we can use to list the files and directories available on the FTP server. One is `dir`. What is the other that is a common way to list files on a Linux system?

`ls`

```bash
ftp> ls
229 Entering Extended Passive Mode (|||44128|)
150 Here comes the directory listing.
-rw-r--r--    1 0        0              32 Jun 04  2021 flag.txt
226 Directory send OK.
```

#### What is the command used to download the file we found of the FTP server?

`get`

```bash
ftp> get flag.txt
local: flag.txt remote: flag.txt
229 Entering Extended Passive Mode (|||57017|)
150 Opening BINARY mode data connection for flag.txt (32 bytes).
100% |*********************************************************************************************|    32       15.43 KiB/s    00:00 ETA
226 Transfer complete.
32 bytes received in 00:00 (0.67 KiB/s)
```

#### Submit root flag

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ cat flag.txt
035d...
```

