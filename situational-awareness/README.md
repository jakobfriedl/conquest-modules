# Situational Awareness Modules <!-- omit from toc -->

## Contents <!-- omit from toc -->

- [Overview](#overview)
  - [cat](#cat)
  - [dir](#dir)
  - [cacls](#cacls)
  - [enum-drives](#enum-drives)
  - [whoami](#whoami)
  - [env](#env)
  - [list-windows](#list-windows)
  - [wmi-query](#wmi-query)
  - [arp](#arp)
  - [ipconfig](#ipconfig)
  - [nslookup](#nslookup)
  - [list-dns](#list-dns)
  - [netstat](#netstat)
  - [list-routes](#list-routes)
  - [list-pipes](#list-pipes)
  - [check-port](#check-port)
  - [pingsweep](#pingsweep)
  - [net-group](#net-group)
  - [net-localgroup](#net-localgroup)
  - [net-user](#net-user)
  - [net-shares](#net-shares)
  - [ldapsearch](#ldapsearch)
  - [ldapquery](#ldapquery)
  - [sc-enum](#sc-enum)
  - [sc-query](#sc-query)
  - [schtasks-enum](#schtasks-enum)
  - [reg-query](#reg-query)

## Overview

The situational awareness modules provide commands for enumerating the local system, Active Directory, network topology, and Windows internals. All commands are implemented as BOF wrappers for [CS-Situational-Awareness-BOF](https://github.com/trustedsec/CS-Situational-Awareness-BOF) and other open-source object file collections. The module contains the following commands: 

```
 * cat                      Retrieve the contents of a file.
 * dir                      List files and directories using BOF.
 * cacls                    List user permissions for the specified file, wildcards supported.
 * enum-drives              List local drive letters and types.
 * whoami                   Get user and group information.
 * env                      List environment variables.
 * list-windows             List visible windows in the current user session.
 * wmi-query                Run a WMI query on a local or remote system.
 * arp                      List ARP table.
 * ipconfig                 List IPv4 address, hostname, and DNS server.
 * nslookup                 Perform a DNS query.
 * list-dns                 List DNS cache entries.
 * netstat                  List network connections.
 * list-routes              List IPv4 routing table.
 * list-pipes               List named pipes.
 * check-port               Check if a specific port is open on a remote machine.
 * pingsweep                Scan an IP range for live hosts.
 * net-group                List domain groups or members of a specified domain group.
 * net-localgroup           List local groups or members of a specified local group.
 * net-user                 List user information.
 * net-shares               List shares on a target system.
 * ldapsearch               Execute a LDAP query.
 * ldapquery                Execute a pre-configured LDAP query.
 * sc-enum                  Get service information.
 * sc-query                 Query service status.
 * schtasks-enum            Get information about scheduled tasks.
 * reg-query                Query the registry.
```

### cat
Retrieve the contents of a file.

```
Usage  : cat <file>
Example: cat C:\Users\Desktop\Administrator\passwords.txt

Required arguments:
  file                      STRING     Relative or absolute path to the file.
```

### dir
List files and directories using BOF. Supports recursive directory traversal.

```
Usage  : dir [directory] [--recursive]
Example: dir C:\Users\Administrator\Desktop --recursive

Optional arguments:
  directory                 STRING     Relative or absolute path. Default: current working directory.
  --recursive               BOOL       Search all sub-directories recursively. Use with caution!
```

### cacls
List user permissions for the specified file, wildcards supported.

```
Usage  : cacls <file>
Example: cacls C:\Services\service.exe

Required arguments:
  file                      STRING     Relative or absolute path to the file.
```

### enum-drives
List local drive letters and types.

```
Usage  : enum-drives
Example: enum-drives
```

### whoami
Get user and group information.

```
Usage  : whoami
Example: whoami
```

### env
List environment variables.

```
Usage  : env
Example: env
```

### list-windows
List visible windows in the current user session.

```
Usage  : list-windows [--all]
Example: list-windows --all

Optional arguments:
  --all                     BOOL       Include hidden windows in window list.
```

### wmi-query
Run a WMI query on a local or remote system.

```
Usage  : wmi-query <query> [--server <server>] [--namespace <namespace>]
Example: wmi-query "Select * From Win32_Process Where ProcessId = 33380"

Required arguments:
  query                     STRING     Query to run (WQL format).

Optional arguments:
  --server server           STRING     Specify remote target system (default: local computer).
  --namespace namespace     STRING     Specify namespace to connect to (default: root\cimv2).
```

### arp
List ARP table.

```
Usage  : arp
Example: arp
```

### ipconfig
List IPv4 address, hostname, and DNS server.

```
Usage  : ipconfig
Example: ipconfig
```

### nslookup
Perform a DNS query.

```
Usage  : nslookup <hostname> [--server <server>] [--type <type>]
Example: nslookup jump01 --server 10.0.0.10 --type A

Required arguments:
  hostname                  STRING     Hostname to look up.

Optional arguments:
  --server server           STRING     DNS server.
  --type type               STRING     DNS record type (default: ANY).
                                         Supported: ANY, A, NS, MD, MF, CNAME, SOA, MB, MG, MR,
                                         WKS, PTR, HINFO, MINFO, MX, TXT, RP, AFSDB, X25, ISDN,
                                         RT, AAAA, SRV, DNSKEY, NBSTAT
```

### list-dns
List DNS cache entries.

```
Usage  : list-dns
Example: list-dns
```

### netstat
List network connections.

```
Usage  : netstat
Example: netstat
```

### list-routes
List IPv4 routing table.

```
Usage  : list-routes
Example: list-routes
```

### list-pipes
List named pipes.

```
Usage  : list-pipes
Example: list-pipes
```

### check-port
Check if a specific port is open on a remote machine.

```
Usage  : check-port <target> <port>
Example: check-port web01 80

Required arguments:
  target                    STRING     Hostname or IP address of the target system.
  port                      INT        Port to check.
```

### pingsweep
Scan an IP range for live hosts.

```
Usage  : pingsweep <targets>
Example: pingsweep 10.10.15.0/24

Required arguments:
  targets                   STRING     Comma-separated list of hosts to scan.
                                       Hostnames, IPs, and IP ranges supported.
                                       Example: 192.168.1.128-192.168.2.240,192.168.1.0/24
```

### net-group
List domain groups or members of a specified domain group. If no target group is provided, this command lists all domain groups instead.

```
Usage  : net-group [group] [--domain <domain>]
Example: net-group "Domain Admins" --domain domain.local

Optional arguments:
  group                     STRING     Domain group name to view memberships.
                                       If not provided, lists all domain groups.
  --domain domain           STRING     Domain (default: current domain).
```

### net-localgroup
List local groups or members of a specified local group. If no target group is provided, this command lists all local groups instead.

```
Usage  : net-localgroup [group] [--server <server>]
Example: net-localgroup "Administrators" --server dc01

Optional arguments:
  group                     STRING     Local group name to view memberships.
                                       If not provided, lists all local groups.
  --server server           STRING     Server (default: local machine).
```

### net-user
List user information. If no target user is provided, this command lists all users instead. If a domain is provided to the command, domain users are enumerated instead of local accounts. 

```
Usage  : net-user [user] [--domain <domain>]
Example: net-user svc_sql --domain domain.local

Optional arguments:
  user                      STRING     Username to retrieve information for.
                                       If not provided, lists all users.
  --domain domain           STRING     Specify domain to list domain users rather than local users.
```

### net-shares
List shares on a target system.

```
Usage  : net-shares [host] [--admin]
Example: net-shares dc01 --admin

Optional arguments:
  host                      STRING     Hostname of the target system (default: local computer).
  --admin                   BOOL       List shares as admin (requires admin privileges).
```

### ldapsearch
Execute a LDAP query.

```
Usage  : ldapsearch <query> [--attributes <attributes>] [--count <count>] [--scope <scope>] [--dc <dc>] [--dn <dn>] [--ldaps]
Example: ldapsearch "(objectClass=user)" --attributes *,ntsecuritydescriptor --dn DC=conquest,DC=local --dc dc01.conquest.local

Required arguments:
  query                     STRING     LDAP filter query.

Optional arguments:
  --attributes attributes   STRING     Attributes to retrieve, comma-separated (default: *).
  --count count             INT        Maximum number of results (default: 0 = unlimited).
  --scope scope             STRING     Search scope (default: subtree).
                                         - base
                                         - level
                                         - subtree
  --dc dc                   STRING     Hostname or IP of domain controller (default: default domain controller).
  --dn dn                   STRING     LDAP query base DN (default: current domain).
  --ldaps                   BOOL       Use LDAPS on port 636 instead of LDAP on port 389.
```

### ldapquery
Execute a pre-configured LDAP query.

```
Usage  : ldapquery <query> [--dc <dc>] [--dn <dn>] [--ldaps]
Example: ldapquery rbcd

Required arguments:
  query                     STRING     Pre-configured query to execute (See table below).

Optional arguments:
  --dc dc                   STRING     Hostname or IP of domain controller (default: default domain controller).
  --dn dn                   STRING     LDAP query base DN (default: current domain).
  --ldaps                   BOOL       Use LDAPS on port 636 instead of LDAP on port 389.
```

The following pre-configured queries are available:
| Query | LDAP Filter | Fields |
| --- | --- | --- |
| `unconstrained` | `(&(userAccountControl:1.2.840.113556.1.4.803:=524288)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))` | `samAccountName`, `dnshostname` |
| `constrained` | `(&(msDS-AllowedToDelegateTo=*)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))` | `samAccountName`, `msDS-AllowedToDelegateTo` |
| `constrained-protocol-transition` | `(&(userAccountControl:1.2.840.113556.1.4.803:=16777216)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))` | `samAccountName`, `msDS-AllowedToDelegateTo` |
| `rbcd` | `(&(msDS-AllowedToActOnBehalfOfOtherIdentity=*)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))` | `samAccountName`, `msDS-AllowedToActOnBehalfOfOtherIdentity` |
| `spn` | `(&(samAccountType=805306368)(!samAccountName=krbtgt)(serviceprincipalname=*)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))` | `samAccountName`, `servicePrincipalName` |
| `no-preauth` | `(&(userAccountControl:1.2.840.113556.1.4.803:=4194304)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))` | `samAccountName` |
| `users` | `(objectClass=user)` | `samAccountName`, `distinguishedName`, `userPrincipalName`, `memberOf` |
| `computers` | `(objectCategory=computer)` | `samAccountName`, `dnshostname`, `operatingSystem`, `operatingSystemVersion`, `distinguishedName` |
| `groups` | `(objectClass=group)` | `samAccountName`, `distinguishedName`, `member`, `memberOf` |
| `gpos` | `(objectClass=groupPolicyContainer)` | `displayName`, `gPCFileSysPath`, `gPCMachineExtensionNames`, `gPCUserExtensionNames`, `distinguishedName`, `whenCreated`, `whenChanged` |
| `ous` | `(objectClass=organizationalUnit)` | `name`, `distinguishedName`, `gPLink`, `description` |
| `trusts` | `(objectClass=trustedDomain)` | `trustPartner`, `trustDirection`, `trustType`, `trustAttributes`, `flatName` |
| `pre2k` | `(&(objectCategory=computer)(userAccountControl:1.2.840.113549.1.9.15.30.1:=4096)(logonCount=0))` | `samAccountName` |


### sc-enum
Get service information. If no service name is provided, lists all services on the target system.

```
Usage  : sc-enum [service] [--server <server>]
Example: sc-enum --server dc01

Optional arguments:
  service                   STRING     Name of the target service.
                                       If not provided, lists all services on the target system.
  --server server           STRING     Hostname or IP address of the target system (default: local computer).
```

### sc-query
Query service status.

```
Usage  : sc-query [service] [--server <server>]
Example: sc-query UpdaterSvc

Optional arguments:
  service                   STRING     Name of the target service.
                                       If not provided, lists the status of all running services.
  --server server           STRING     Hostname or IP address of the target system (default: local computer).
```

### schtasks-enum
Get information about scheduled tasks. If no task path is provided, lists all scheduled tasks on the target system.

```
Usage  : schtasks-enum [path] [--server <server>]
Example: schtasks-enum "\Microsoft\Office\Office Background Push Maintenance"

Optional arguments:
  path                      STRING     Path to the target scheduled task.
                                       If not provided, lists all scheduled tasks on the target system.
  --server server           STRING     Hostname or IP address of the target system (default: local computer).
```

### reg-query
Query the registry.

```
Usage  : reg-query <hive> <path> [key] [--server <server>] [--recursive]
Example: reg-query HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion" ProgramFilesDir

Required arguments:
  hive                      STRING     Registry hive.
                                         - HKCR
                                         - HKCU
                                         - HKLM
                                         - HKU
  path                      STRING     Registry path.

Optional arguments:
  key                       STRING     Specific key/value name to query.
                                       If not provided, enumerates all subkeys and values.
  --server server           STRING     Target server for remote registry (default: local computer).
  --recursive               BOOL       Recursively enumerate all subkeys.
```