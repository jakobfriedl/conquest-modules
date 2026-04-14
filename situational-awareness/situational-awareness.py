import conquest
import os.path
import base64
import uuid
try:
    from impacket.ldap.ldaptypes import SR_SECURITY_DESCRIPTOR
    IMPACKET_AVAILABLE = True
except ImportError:
    IMPACKET_AVAILABLE = False

cmd_cat = (
    conquest.createCommand(name="cat", description="Retrieve the contents of a file.", example="cat C:\\Users\\Desktop\\Administrator\\passwords.txt", 
                           message="Tasked agent to retrieve the contents of a file.", mitre=["T1083"])
            .addArgString("file", "Relative or absolute path to the file.", True)
            .setHandler(lambda agentId, cmdline, args: (
                file := conquest.get_string(args, 0),

                bof := conquest.modules_root() + "/situational-awareness/cobaltstrike-cat-bof/cat.x64.o",
                params := conquest.bof_pack("Z", [
                    file    # Z: File name
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("situational awareness")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_enumdrives = (
    conquest.createCommand(name="enum-drives", description="List local drive letters and types.", example="enum-drives",
                           message="Tasked agent to list local drives.", mitre=["T1082", "T1083"])
            .setHandler(lambda agentId, cmdline, args: (
                bof := conquest.modules_root() + "/situational-awareness/OperatorsKit/KIT/EnumDrives/enumdrives.o",
                conquest.execute_alias(agentId, cmdline, f"bof {bof}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("situational awareness")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_whoami = (
    conquest.createCommand(name="whoami", description="Get user and group information.", example="whoami", 
                           message="Tasked agent to retrieve user and group information.", mitre=["T1033"])
            .setHandler(lambda agentId, cmdline, args: (
                bof := conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/whoami/whoami.x64.o",
                conquest.execute_alias(agentId, cmdline, f"bof {bof}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("situational awareness")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_env = ( 
    conquest.createCommand(name="env", description="List environment variables.", example="env", 
                           message="Tasked agent to list environment variables.")
            .setHandler(lambda agentId, cmdline, args: (
                bof := conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/env/env.x64.o",
                conquest.execute_alias(agentId, cmdline, f"bof {bof}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("situational awareness")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_dir = (
    conquest.createCommand(name="dir", description="List files and directories using BOF.", example="ls C:\\Users\\Administrator\\Desktop --recursive", 
                           message="Tasked agent to list files and directories using BOF.", mitre=["T1083"])
            .addArgString("directory", "Relative or absolute path. (default: current working directory)", False, ".")
            .addFlagBool("--recursive", "recursive", "Search all sub-directories recursively. Use with caution!")
            .setHandler(lambda agentId, cmdline, args: (
                directory := conquest.get_string(args, 0),
                recurse := conquest.get_bool(args, 1),

                bof := conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/dir/dir.x64.o",
                params := conquest.bof_pack("zs", [
                    directory,          # z: Directory
                    int(recurse)        # s: Search sub-directories
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("situational awareness")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


cmd_cacls = (
    conquest.createCommand(name="cacls", description="List user permissions for the specified file, wildcards supported.", example="cacls C:\\Services\\service.exe",
                           message="Tasked agent to list file permissions.", mitre=["T1222"])
            .addArgString("file", "Relative or absolute path to the file.", True)
            .setHandler(lambda agentId, cmdline, args: (
                file := conquest.get_string(args, 0),

                bof := conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/cacls/cacls.x64.o",
                params := conquest.bof_pack("Z", [
                    file    # Z: File name
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("situational awareness")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_arp = (
    conquest.createCommand(name="arp", description="List ARP table.", example="arp", 
                           message="Tasked agent to retrieve ARP table.", mitre=["T1018", "T1049"])
            .setHandler(lambda agentId, cmdline, args: (
                bof := conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/arp/arp.x64.o",
                conquest.execute_alias(agentId, cmdline, f"bof {bof}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("situational awareness")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_ipconfig = ( 
    conquest.createCommand(name="ipconfig", description="List IPv4 address, hostname, and DNS server.", example="ipconfig", 
                           message="Tasked agent to list network configuration.", mitre=["T1016"])
            .setHandler(lambda agentId, cmdline, args: (
                bof := conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/ipconfig/ipconfig.x64.o",
                conquest.execute_alias(agentId, cmdline, f"bof {bof}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("situational awareness")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

DNS_RECORD_TYPES = {
    "A": 0x1,           # IPv4 address
    "NS": 0x2,          # Name server
    "MD": 0x3,          # Mail destination (obsolete)
    "MF": 0x4,          # Mail forwarder (obsolete)
    "CNAME": 0x5,       # Canonical name
    "SOA": 0x6,         # Start of authority
    "MB": 0x7,          # Mailbox domain name
    "MG": 0x8,          # Mail group member
    "MR": 0x9,          # Mail rename domain
    "WKS": 0xb,         # Well-known service
    "PTR": 0xc,         # Pointer record (reverse DNS)
    "HINFO": 0xd,       # Host information
    "MINFO": 0xe,       # Mailbox information
    "MX": 0xf,          # Mail exchange
    "TXT": 0x10,        # Text record
    "RP": 0x11,         # Responsible person
    "AFSDB": 0x12,      # AFS database
    "X25": 0x13,        # X.25 address
    "ISDN": 0x14,       # ISDN address
    "RT": 0x15,         # Route through
    "AAAA": 0x1c,       # IPv6 address
    "SRV": 0x21,        # Service locator
    "DNSKEY": 0x19,     # DNS key record
    "NBSTAT": 0xff02,   # Windows name server
    "ANY": 0xff         # Query all record types
}
cmd_nslookup = (
    conquest.createCommand(name="nslookup", description="Perform a DNS query.", example="nslookup jump01 --server 10.0.0.10 --type A",
                           message="Tasked agent to perform a DNS query.", mitre=["T1018", "T1590.002"])
            .addArgString("hostname", "Hostname to look up.", True)
            .addFlagString("--server", "server", "DNS server.")
            .addFlagString("--type", "type", """DNS Record type (default: ANY).
Supported record types: ANY, A, NS, MD, MF, CNAME, SOA, MB, MG, MR, WKS, PTR, HINFO, MINFO, MX, TXT, RP, AFSDB, X25, ISDN, RT, AAAA, SRV, DNSKEY, NBSTAT""", False, "ANY")
            .setHandler(lambda agentId, cmdline, args: (
                hostname := conquest.get_string(args, 0),
                server := conquest.get_string(args, 1),
                type := conquest.get_string(args, 2).upper(),

                recordType := DNS_RECORD_TYPES.get(type, DNS_RECORD_TYPES["ANY"]),

                bof := conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/nslookup/nslookup.x64.o",
                params := conquest.bof_pack("zzs", [
                    hostname,       # z: Hostname
                    server,         # z: DNS Server
                    recordType      # s: DNS Record Type
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("situational awareness")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_listdns = (
    conquest.createCommand(name="list-dns", description="List DNS cache entries.", example="list-dns", 
                        message="Tasked agent to list DNS cache entries.", mitre=["T1016", "T1049"])
        .setHandler(lambda agentId, cmdline, args: (
            bof := conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/listdns/listdns.x64.o",
            conquest.execute_alias(agentId, cmdline, f"bof {bof}") if os.path.exists(bof)
            else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
        ))
).registerToGroup("situational awareness")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_netstat = (
    conquest.createCommand(name="netstat", description="List network connections.", example="netstat", 
                        message="Tasked agent to list network connections.", mitre=["T1049"])
        .setHandler(lambda agentId, cmdline, args: (
            bof := conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/netstat/netstat.x64.o",
            conquest.execute_alias(agentId, cmdline, f"bof {bof}") if os.path.exists(bof)
            else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
        ))
).registerToGroup("situational awareness")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_listroute = (
    conquest.createCommand(name="list-routes", description="List IPv4 routing table.", example="list-routes", 
                        message="Tasked agent to list routing table.", mitre=["T1016"])
        .setHandler(lambda agentId, cmdline, args: (
            bof := conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/routeprint/routeprint.x64.o",
            conquest.execute_alias(agentId, cmdline, f"bof {bof}") if os.path.exists(bof)
            else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
        ))
).registerToGroup("situational awareness")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_listpipes = (
    conquest.createCommand(name="list-pipes", description="List named pipes.", example="list-pipes", 
                        message="Tasked agent to list named pipes.", mitre=["T1135"])
        .setHandler(lambda agentId, cmdline, args: (
            conquest.execute_alias(agentId, cmdline, f"ls //./pipe/")
        ))
).registerToGroup("situational awareness")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_checkport = (
    conquest.createCommand(name="check-port", description="Check if a specific port is open on a remote machine.", example="check-port web01 80",
                           message="Tasked agent to check if a port is open on a remote machine.", mitre=["T1046"])
            .addArgString("target", "Hostname/IP address of the target system.", True)
            .addArgInt("port", "Port to check.", True)
            .setHandler(lambda agentId, cmdline, args: (
                target := conquest.get_string(args, 0),
                port := conquest.get_int(args, 1),

                bof := conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/probe/probe.x64.o",
                params := conquest.bof_pack("zi", [
                    target,         # z: Target hostname or IP 
                    port            # i: Port
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("situational awareness")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_pingsweep = (
    conquest.createCommand(name="pingsweep", description="Scan an IP range for live hosts.", example="pingsweep 10.10.15.0/24",
                           message="Tasked agent to perform a pingscan.", mitre=["T1018", "T1046"])
            .addArgString("targets", "Comma separated list of hosts to scan. Hostnames, IPs and IP ranges supported (eg. 192.168.1.128-192.168.2.240,192.168.1.0/24).", True)
            .setHandler(lambda agentId, cmdline, args: (
                targets := conquest.get_string(args, 0),

                bof := conquest.modules_root() + "/situational-awareness/portscanbof/bin/pingscanner.bof.o",
                params := conquest.bof_pack("z", [
                    targets         # z: Target list
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("situational awareness")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_netDomainGroup = (
    conquest.createCommand(name="net-group", description="List domain groups or members of a specified domain group.", example="net-group \"Domain Admins\" --domain domain.local",
                           message="Tasked agent to enumerate domain groups / domain group-memberships.", mitre=["T1069.002"])
            .addArgString("group", "Specify domain group name to view group memberships.")
            .addFlagString("--domain", "domain", "Domain (default: current domain).")
            .setHandler(lambda agentId, cmdline, args: (
                group := conquest.get_string(args, 0),
                domain := conquest.get_string(args, 1),

                bof := conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/netgroup/netgroup.x64.o",
                params := conquest.bof_pack("sZZ", [
                    int(group != ""),               # s: Type (0: list groups, 1: list group-memberships)
                    domain,                         # Z: Domain name
                    group                           # Z: Group name
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("situational awareness")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_netLocalGroup = (
    conquest.createCommand(name="net-localgroup", description="List local groups or members of a specified local group.", example="net-localgroup \"Administrators\" --domain domain.local",
                           message="Tasked agent to enumerate local groups / local group-memberships.", mitre=["T1069.001"])
            .addArgString("group", "Specify local group name to view group memberships.")
            .addFlagString("--server", "server", "Server (default: local machine).")
            .setHandler(lambda agentId, cmdline, args: (
                group := conquest.get_string(args, 0),
                server := conquest.get_string(args, 1),

                bof := conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/netlocalgroup/netlocalgroup.x64.o",
                params := conquest.bof_pack("sZZ", [
                    int(group != ""),               # s: Type (0: list groups, 1: list group-memberships)
                    server,                         # Z: Server
                    group                           # Z: Group name
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("situational awareness")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def _netUser(agentId, cmdline, args): 
    user = conquest.get_string(args, 0)
    domain = conquest.get_string(args, 1)

    if user != "": 
        # List user information if a username is specified
        bof = conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/netuser/netuser.x64.o"
        params = conquest.bof_pack("ZZ", [
            user,       # Z: Username 
            domain      # Z: Domain name
        ])
    else: 
        # List users
        bof = conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/netuserenum/netuserenum.x64.o"
        params = conquest.bof_pack("ii", [
            int(domain != ""),          # i: Use domain (0: local users, 1: domain users)
            1                           # i: Filter (1: all users, 2: locked-out users, 3: disabled users, 4: neither disabled and not locked-out users)
        ])

    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)

def _netUserOutput(agentId, output):
    lines = output.strip().split('\n')
    result = []

    for line in lines:
        line = line.rstrip()

        if not line:
            result.append('')
            continue

        if line.startswith(' ') or line.startswith('\t'):
            result.append(f' * {line.strip()}')
            continue

        if ':' in line:
            colon = line.index(':')
            key   = line[:colon].strip()
            value = line[colon + 1:].strip()
            result.append(f'{(key + ":") :<32} {value}' if value else f'{key}:')
        else:
            result.append(line)

    conquest.output(agentId, '\n'.join(result))

cmd_netUser = (
    conquest.createCommand(name="net-user", description="List user information.", example="net-user svc_sql --domain domain.local",
                           message="Tasked agent to list user information.", mitre=["T1087.001", "T1087.002"])
            .addArgString("user", "Specify username to retrieve user information. If no username is provided, this command enumerates and lists all users instead.")
            .addFlagString("--domain", "domain", "Specify domain to list domain users rather than local users.")
            .setHandler(_netUser)
            .setOutputHandler(_netUserOutput)    # Properly format user information
).registerToGroup("situational awareness")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_netShares = (
    conquest.createCommand(name="net-shares", description="List shares on a target system.", example="net-shares dc01 --admin",
                        message="Tasked agent to list shares.", mitre=["T1135"])
        .addArgString("host", "Hostname of the target system (default: local computer).")
        .addFlagBool("--admin", "admin", "List shares as admin (requires admin privileges).")
        .setHandler(lambda agentId, cmdline, args: (
            host := conquest.get_string(args, 0),
            admin := conquest.get_bool(args, 1),

            bof := conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/netshares/netshares.x64.o",
            params := conquest.bof_pack("Zi", [
                host,           # Z: Host 
                int(admin)      # i: List shares as admin
            ]),

            conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
            else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
        ))
).registerToGroup("situational awareness")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

LDAP_SCOPE = {
    "base": 1,
    "level": 2,
    "subtree": 3
}
def _ldapSearch(agentId, cmdline, args):
    query = conquest.get_string(args, 0)
    attributes = conquest.get_string(args, 1)
    count = conquest.get_int(args, 2)
    scope = conquest.get_string(args, 3)
    hostname = conquest.get_string(args, 4)
    dn = conquest.get_string(args, 5)
    ldaps = conquest.get_bool(args, 6)
    
    ldapScope = LDAP_SCOPE.get(scope, LDAP_SCOPE["subtree"])
    
    bof = conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/ldapsearch/ldapsearch.x64.o"
    params = conquest.bof_pack("zziizzi", [
        query,                      # z: LDAP filter query
        attributes,                 # z: Attributes (comma-separated or "*")
        count,                      # i: Max results (0 = unlimited)
        ldapScope,                  # i: Scope (1=base, 2=level, 3=subtree)
        hostname,                   # z: DC hostname (auto-discover if empty)
        dn,                         # z: Domain DN (auto-detect if empty)
        int(ldaps)                  # i: Use LDAPS
    ])
    
    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)

# LDAPSearch output handler: 
# - Converts ntSecurityDescriptor base64 value into a human-readable string using impacket.
# - Replaces well-known SIDs with group/user names. Only custom permissions show up as raw SID string.
# - Replaces access masks with Bloodhound-like DACL descriptions.

# Well-known local SIDs
WELL_KNOWN_SIDS = {
    "S-1-1-0": "Everyone",
    "S-1-3-0": "Creator Owner",
    "S-1-5-9": "Enterprise Domain Controllers",
    "S-1-5-10": "Self",
    "S-1-5-11": "Authenticated Users",
    "S-1-5-18": "SYSTEM",
    "S-1-5-32-544": "BUILTIN\\Administrators",
    "S-1-5-32-548": "BUILTIN\\Account Operators",
    "S-1-5-32-550": "BUILTIN\\Print Operators",
    "S-1-5-32-554": "BUILTIN\\Pre-Windows 2000 Compatible Access",
    "S-1-5-32-560": "BUILTIN\\Windows Authorization Access Group",
    "S-1-5-32-561": "BUILTIN\\Terminal Server License Servers",
}

# Well-known Domain RIDs
WELL_KNOWN_RIDS = {
    500: "Administrator",
    501: "Guest",
    502: "krbtgt",
    512: "Domain Admins",
    513: "Domain Users",
    514: "Domain Guests",
    515: "Domain Computers",
    516: "Domain Controllers",
    517: "Cert Publishers",
    518: "Schema Admins",
    519: "Enterprise Admins",
    520: "Group Policy Creator Owners",
    521: "Read-only Domain Controllers",
    522: "Cloneable Domain Controllers",
    525: "Protected Users",
    526: "Key Admins",
    527: "Enterprise Key Admins",
    553: "RAS and IAS Servers"
}

# Standard access rights
# https://learn.microsoft.com/en-us/windows/win32/api/iads/ne-iads-ads_rights_enum
ACCESS_RIGHTS = {
    0x10000000: "GenericAll",
    0x40000000: "GenericWrite",
    0x80000000: "GenericRead",
    0x20000000: "GenericExecute",
    0x00080000: "WriteOwner",
    0x00040000: "WriteDacl",
    0x01000000: "AccessSystemSecurity",
    0x00100000: "Synchronize",
    0x00020000: "ReadControl",
    0x00010000: "Delete",
    0x00000080: "ListObject",
    0x00000040: "DeleteTree",
    0x00000008: "Self",
    0x00000004: "ListChildren",
    0x00000002: "DeleteChild",
    0x00000001: "CreateChild",
}

ACE_OBJECT_TYPE_PRESENT = 0x01
GENERIC_ALL = 0x10000000
CONTROL_ACCESS = 0x00000100
WRITE_PROP = 0x00000020
READ_PROP = 0x00000010

# Bloodhound edge mapping
EXTENDED_RIGHT_EDGES = {
    "00299570-246d-11d0-a768-00aa006e0529": "ForceChangePassword",
    "ab721a53-1e2f-11d0-9819-00aa0040529b": "UserChangePassword",
    "1131f6aa-9c07-11d1-f79f-00c04fc2dcd2": "GetChanges",                   # DCSync (needs GetChangesAll too)
    "1131f6ad-9c07-11d1-f79f-00c04fc2dcd2": "GetChangesAll",                # DCSync (needs GetChanges too)
    "1131f6ab-9c07-11d1-f79f-00c04fc2dcd2": "SyncReplication",
    "1131f6ac-9c07-11d1-f79f-00c04fc2dcd2": "ManageReplicationTopology",
    "0e10c968-78fb-11d2-90d4-00c04f79dc55": "Enroll",
    "a05b8cc2-17bc-4802-a710-e7c15ab866a2": "AutoEnroll",
}

WRITE_PROPERTY_EDGES = {
    "bf9679c0-0de6-11d0-a285-00aa003049e2": "AddMember",                    # member attribute
    "5b47d60f-6090-40b2-9f37-2a4de88f3063": "AddKeyCredentialLink",         # msDS-KeyCredentialLink
    "3f78c3e5-f79a-46bd-a0b8-9d18116ddc79": "WriteAccountRestrictions"      # msDS-AllowedToActOnBehalfOfOtherIdentity
}

READ_PROPERTY_EDGES = {
    "d0bbf0b6-af77-4244-a7e9-9c5b08c20e7a": "ReadLAPSPassword",             # ms-Mcs-AdmPwd (LAPS v1)
    "e6fbb6ef-c39b-49b6-8512-c1e2d4a6aa80": "ReadLAPSPassword",             # msLAPS-Password (LAPS v2)
    "aee7307d-2b4e-4f26-8bc6-6498b5b5dcdd": "ReadLAPSPassword",             # msLAPS-EncryptedPassword (LAPS v2)
}

# Helper functions
def _resolve_sid(sid_str):
    if sid_str in WELL_KNOWN_SIDS:
        return WELL_KNOWN_SIDS[sid_str]
    parts = sid_str.split('-')
    if len(parts) >= 3:
        try:
            rid = int(parts[-1])
            if rid in WELL_KNOWN_RIDS:
                return WELL_KNOWN_RIDS[rid]
        except ValueError:
            pass
    return sid_str

def _get_ace_guid(ace):
    try:
        if ace['Flags'] & ACE_OBJECT_TYPE_PRESENT:  
            return str(uuid.UUID(bytes_le=bytes(ace['ObjectType'])))
    except (KeyError, AttributeError, ValueError):
        pass
    return None

def _resolve_ace_edges(mask, guid=None):
    if mask & GENERIC_ALL:
        return ["GenericAll"]

    edges = [name for bit, name in ACCESS_RIGHTS.items() if bit != 0x10000000 and mask & bit]

    if mask & CONTROL_ACCESS:
        edges.append(EXTENDED_RIGHT_EDGES.get(guid, "AllExtendedRights") if guid else "AllExtendedRights")

    if mask & WRITE_PROP: 
        edges.append(WRITE_PROPERTY_EDGES.get(guid, "WriteProperty") if guid else "WriteProperty")

    if mask & READ_PROP:
       edges.append(READ_PROPERTY_EDGES.get(guid, "ReadProperty") if guid else "ReadProperty")

    if "WriteDacl" in edges and "WriteOwner" in edges:
        return ["GenericAll"]

    return edges or [f"0x{mask:08X}"]

def _format_sid(sid):
    try:
        return sid.formatCanonical()
    except:
        return sid.getData().hex()

def _decode_security_descriptor(sd_string):
    try:
        sd = SR_SECURITY_DESCRIPTOR()
        sd.fromString(base64.b64decode(sd_string))
        lines = []
        if sd['OwnerSid']:
            lines.append(f"  Owner: {_resolve_sid(_format_sid(sd['OwnerSid']))}")
        if sd['GroupSid']:
            lines.append(f"  Group: {_resolve_sid(_format_sid(sd['GroupSid']))}")
        if sd['Dacl']:
            lines.append("  DACL:")
            for ace in sd['Dacl']['Data']:
                sid_str = _resolve_sid(_format_sid(ace['Ace']['Sid']))
                mask    = ace['Ace']['Mask']['Mask']
                aceType = ace['TypeName'].split("_")[1].capitalize()
                guid    = _get_ace_guid(ace['Ace'])
                edges   = _resolve_ace_edges(mask, guid)
                
                lines.append(f"    [{aceType}]".ljust(9) + f" {sid_str}: {', '.join(edges)}")
        return '\n'.join(lines)
    
    except Exception as e:
        return f"  [!] Failed to decode nTSecurityDescriptor: {e}"

# Output handler
def _ldapSearchOutput(agentId, output):
    if not IMPACKET_AVAILABLE:
        conquest.warn(agentId, "Missing pip dependency: impacket. Install impacket to convert ntSecurityDescriptor into human-readable output.")

    result = []
    for line in output.split('\n'):        
        # Process group memberships
        if line.lower().startswith('memberof:'):
            key, _, groups = line.partition(':')
            result.append(key + ':')
            for group in groups.strip().split(', '):
                result.append('  ' + group)
        
        # Process ntSecurityDescriptor if python3-impacket is installed
        elif IMPACKET_AVAILABLE and line.lower().startswith('ntsecuritydescriptor:'):
            key, _, sd_b64 = line.partition(':')
            result.append(key + ':')
            result.append(_decode_security_descriptor(sd_b64.strip()))
        
        else:
            result.append(line)

    conquest.output(agentId, '\n'.join(result))

cmd_ldapsearch = (
    conquest.createCommand(name="ldapsearch", description="Execute a LDAP query.", example="ldapsearch \"(objectClass=user)\" --attributes *,ntsecuritydescriptor --dn DC=conquest,DC=local --dc dc01.conquest.local",
                           message="Tasked agent to execute a LDAP query.", mitre=["T1087.002", "T1069.002", "T1482", "T1018"])
            .addArgString("query", "LDAP filter query.", True)
            .addFlagString("--attributes", "attributes", "Attributes to retrieve, comma-separated (default: *).", False, "*")
            .addFlagInt("--count", "count", "Maximum number of results (default: 0 = unlimited).")
            .addFlagString("--scope", "scope", """Search scope.
Available options:
  - base 
  - level 
  - subtree (default)""", False, "subtree")
            .addFlagString("--dc", "hostname", "Hostname or IP of domain controller (default: default domain controller).")
            .addFlagString("--dn", "dn", "LDAP query base DN (default: current domain).")
            .addFlagBool("--ldaps", "ldaps", "Use LDAPS on port 636 instead of LDAP on port 389.")
            .setHandler(_ldapSearch)
            .setOutputHandler(_ldapSearchOutput)
).registerToGroup("situational awareness")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

LDAP_QUERIES = {
    "unconstrained": (
        "(&(userAccountControl:1.2.840.113556.1.4.803:=524288)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))",
        "samAccountName,dnshostname"
    ),
    "constrained": (
        "(&(msDS-AllowedToDelegateTo=*)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))",
        "samAccountName,msDS-AllowedToDelegateTo"
    ),
    "constrained-protocol-transition": (
        "(&(userAccountControl:1.2.840.113556.1.4.803:=16777216)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))",
        "samAccountName,msDS-AllowedToDelegateTo"
    ),
    "rbcd": (
        "(&(msDS-AllowedToActOnBehalfOfOtherIdentity=*)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))",
        "samAccountName,msDS-AllowedToActOnBehalfOfOtherIdentity"
    ),
    "spn": (
        "(&(samAccountType=805306368)(!samAccountName=krbtgt)(serviceprincipalname=*)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))",
        "samAccountName,servicePrincipalName"
    ),
    "no-preauth": (
        "(&(userAccountControl:1.2.840.113556.1.4.803:=4194304)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))",
        "samAccountName"
    ),
    "users": (
        "(objectClass=user)",
        "samAccountName,distinguishedName,userPrincipalName,memberOf"
    ),
    "computers": (
        "(objectCategory=computer)",
        "samAccountName,dnshostname,operatingSystem,operatingSystemVersion,distinguishedName"
    ),
    "groups": (
        "(objectClass=group)",
        "samAccountName,distinguishedName,member,memberOf"
    ),
    "gpos": (
        "(objectClass=groupPolicyContainer)",
        "displayName,gPCFileSysPath,gPCMachineExtensionNames,gPCUserExtensionNames,distinguishedName,whenCreated,whenChanged"
    ),
    "ous": (
        "(objectClass=organizationalUnit)",
        "name,distinguishedName,gPLink,description"
    ),
    "trusts": (
        "(objectClass=trustedDomain)",
        "trustPartner,trustDirection,trustType,trustAttributes,flatName"
    ),
    "pre2k": (
        "(&(objectCategory=computer)(userAccountControl:1.2.840.113549.1.9.15.30.1:=4096)(logonCount=0))",
        "samAccountName"
    )
}

def _ldapQuery(agentId, cmdline, args): 
    type = conquest.get_string(args, 0).lower()
    dc = conquest.get_string(args, 1)
    dn = conquest.get_string(args, 2)
    ldaps = conquest.get_bool(args, 3)
    
    query_data = LDAP_QUERIES.get(type)
    if query_data is None: 
        conquest.error(agentId, f"Invalid LDAP query: {type}. Use \"help ldapquery\" to list available options.", cmdline)
        return
    
    (query, attributes) = query_data
    
    bof = conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/ldapsearch/ldapsearch.x64.o"
    params = conquest.bof_pack("zziizzi", [
        query,                      # z: LDAP filter query
        attributes,                 # z: Attributes (comma-separated or "*")
        0,                          # i: 0 -> Return all results
        3,                          # i: 3 -> Subtree
        dc,                         # z: DC hostname (auto-discover if empty)
        dn,                         # z: Domain DN (auto-detect if empty)
        int(ldaps)                  # i: Use LDAPS
    ])
    
    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)

cmd_ldapQuery = (
    conquest.createCommand(name="ldapquery", description="Execute a pre-configured LDAP query.", example="ldapquery rbcd",
                           message="Tasked agent to execute a pre-configured LDAP query.", mitre=[])
            .addArgString("query", """Pre-configured query to execute.
Available options:
- unconstrained: Enumerate AD objects configured for unconstrained delegation.
- constrained: Enumerate AD objects configured for constrained delegation.
- constrained-protocol-transition: Enumerate AD objects configured for constrained delegation with protocol transition.
- rbcd: Enumerate AD objects configured for resource-based constrained delegation.
- spn: Enumerate accounts that have an SPN set (Kerberoasting).
- no-preauth: Enumerate users that do not require Kerberos pre-authentication (ASREP-Roasting).
- users: Enumerate enabled domain users.
- computers: Enumerate enabled domain computers.
- groups: Enumerate domain groups.
- gpos: Enumerate group policies.
- ous: Enumerate organizational units.
- trusts: Enumerate domain trusts.
- pre2k: Enumerate pre-Windows 2000 Computers.""", True)
            .addFlagString("--dc", "hostname", "Hostname or IP of domain controller (default: default domain controller).")
            .addFlagString("--dn", "dn", "LDAP query base DN (default: current domain).")
            .addFlagBool("--ldaps", "ldaps", "Use LDAPS on port 636 instead of LDAP on port 389.")
            .setHandler(_ldapQuery)                        
).registerToGroup("situational awareness")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# Extract msDS-PrincipalName from ldapsearch output
def _convertFromSidOutput(agentId, output): 
    for line in output.splitlines():
        if line.strip().lower().startswith("msds-principalname:"):
            conquest.output(agentId, line.split(":", 1)[1].strip())
            return
    conquest.error(agentId, "Could not resolve SID.")

cmd_convertFromSid = (
    conquest.createCommand(name="convertfrom-sid", description="Convert a SID to a group/user name.", example="convertfrom-sid S-1-5-21-2062779629-1118245407-2952427100-1105",
                           message="Tasked agent to convert SID to group/user name.", mitre=[])
            .addArgString("sid", "Security identifier to convert.", True)
            .addFlagString("--dc", "hostname", "Hostname or IP of domain controller (default: default domain controller).")
            .addFlagString("--dn", "dn", "LDAP query base DN (default: current domain).")
            .addFlagBool("--ldaps", "ldaps", "Use LDAPS on port 636 instead of LDAP on port 389.")
            .setHandler(lambda agentId, cmdline, args: (
                sid := conquest.get_string(args, 0),
                dc := conquest.get_string(args, 1),
                dn := conquest.get_string(args, 2),
                ldaps := conquest.get_bool(args, 3),

                bof := conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/ldapsearch/ldapsearch.x64.o",
                params := conquest.bof_pack("zziizzi", [
                    f"(objectSid={sid})",       # z: LDAP filter Query
                    "msDS-PrincipalName",       # z: Username in format DOMAIN\sAMAccountName
                    0,                          # i: 0 -> Return all results
                    3,                          # i: 3 -> Subtree
                    dc,                         # z: DC hostname (auto-discover if empty)
                    dn,                         # z: Domain DN (auto-detect if empty)
                    int(ldaps)                  # i: Use LDAPS
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
            .setOutputHandler(_convertFromSidOutput)
).registerToGroup("situational awareness")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def _scEnum(agentId, cmdline, args): 
    service = conquest.get_string(args, 0)
    server = conquest.get_string(args, 1)

    if service != "": 
        # Get information about a specific service (sc_qc)
        bof = conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/sc_qc/sc_qc.x64.o"
        params = conquest.bof_pack("zz", [
            server,         # z: Target server 
            service,        # z: Target service
        ])
    else: 
        # List all services (sc_enum)
        bof = conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/sc_enum/sc_enum.x64.o"
        params = conquest.bof_pack("z", [
            server          # z: Target server 
        ])

    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)

cmd_scEnum = (
    conquest.createCommand(name="sc-enum", description="Get service information.", example="sc-enum --server dc01",
                           message="Tasked agent to enumerate services.", mitre=["T1007"])
            .addArgString("service", "Name of the target service. If not is provided, this command will list all services on the target system.")
            .addFlagString("--server", "server", "Hostname or IP address of the target system (default: local computer).")
            .setHandler(_scEnum)
).registerToGroup("windows services")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_scQuery = (
    conquest.createCommand(name="sc-query", description="Query service status status.", example="sc-qc UpdaterSvc",
                           message="Tasked agent to query service status.", mitre=["T1007"])
            .addArgString("service", "Name of the target service. If not provided, this command will list the status of all services running on the target system.")
            .addFlagString("--server", "server", "Hostname or IP address of the target system (default: local computer).")
            .setHandler(lambda agentId, cmdline, args: (
                service := conquest.get_string(args, 0),
                server := conquest.get_string(args, 1),

                bof := conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/sc_query/sc_query.x64.o",
                params := conquest.bof_pack("zz", [
                    server,         # z: Target server 
                    service,        # z: Target service
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("windows services")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def _schtasksEnum(agentId, cmdline, args): 
    task = conquest.get_string(args, 0)
    server = conquest.get_string(args, 1)

    if task != "": 
        # Get information about a specific scheduled task
        bof = conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/schtasksquery/schtasksquery.x64.o"
        params = conquest.bof_pack("ZZ", [
            server,         # Z: Target server 
            task,           # Z: Target scheduled task
        ])
    else: 
        # List all scheduled tasks
        bof = conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/schtasksenum/schtasksenum.x64.o"
        params = conquest.bof_pack("Z", [
            server          # Z: Target server 
        ])

    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)

cmd_schtasksEnum = (
    conquest.createCommand(name="schtasks-enum", description="Get information about scheduled task.", example="schtasks-enum \"\\Microsoft\\Office\\Office Background Push Maintenance\"",
                           message="Tasked agent to enumerate scheduled tasks.", mitre=["T1053.005"])
            .addArgString("path", "Path to the target scheduled task. If not provided, this command will list all scheduled tasks on the target system.")
            .addFlagString("--server", "server", "Hostname or IP address of the target system (default: local computer).")
            .setHandler(_schtasksEnum)
).registerToGroup("scheduled tasks")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

REGISTRY_HIVES = {
    "HKCR": 0,  # HKEY_CLASSES_ROOT
    "HKCU": 1,  # HKEY_CURRENT_USER
    "HKLM": 2,  # HKEY_LOCAL_MACHINE
    "HKU": 3    # HKEY_USERS
}
def _regQuery(agentId, cmdline, args): 
    hive = conquest.get_string(args, 0).upper()
    path = conquest.get_string(args, 1)
    key = conquest.get_string(args, 2)
    server = conquest.get_string(args, 3)
    recursive = conquest.get_bool(args, 4)
    
    regHive = REGISTRY_HIVES.get(hive)
    if regHive is None:
        conquest.error(agentId, f"Invalid registry hive: {hive}.", cmdline)
        return
    
    bof = conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/reg_query/reg_query.x64.o"
    params = conquest.bof_pack("zizzi", [
        server,                     # z: Hostname 
        regHive,                    # i: Hive (0=HKCR, 1=HKCU, 2=HKLM, 3=HKU)
        path,                       # z: Registry path
        key,                        # z: Key 
        int(recursive)              # i: Recursive enumeration
    ])
    
    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)

cmd_regQuery = (
    conquest.createCommand(name="reg-query", description="Query the registry.", example="reg-query HKLM \"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\" ProgramFilesDir",
                           message="Tasked agent to query the registry.", mitre=["T1012"])
            .addArgString("hive", """Registry hive.
Available options:
  - HKCR
  - HKCU
  - HKLM
  - HKC""", True)
            .addArgString("path", "Registry path.", True)
            .addArgString("key", "Specific key/value name to query. If not provided, enumerates all subkeys and values.")
            .addFlagString("--server", "server", "Target server for remote registry (default: local computer).")
            .addFlagBool("--recursive", "recursive", "Recursively enumerate all subkeys.")
            .setHandler(_regQuery)
).registerToGroup("windows registry")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_windowList = (
    conquest.createCommand(name="list-windows", description="List visible windows in the current user session.", example="list-windows --all",
                           message="Tasked agent to list windows.", mitre=["T1010"])
            .addFlagBool("--all", "all", "Include hidden windows in window list.")
            .setHandler(lambda agentId, cmdline, args: (
                all := conquest.get_bool(args, 0),

                bof := conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/windowlist/windowlist.x64.o",
                params := conquest.bof_pack("i", [
                    int(all),         # i: List all windows 
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("situational awareness")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_wmiQuery = ( 
    conquest.createCommand(name="wmi-query", description="Run a WMI query on a local or remote system.", example="wmi-query \"Select * From Win32_Process Where ProcessId = 33380\"",
                           message="Tasked agent to run a WMI query.", mitre=["T1047"])
            .addArgString("query", "Query to run (WQL format).", True)
            .addFlagString("--server", "server", "Specify remote target system (default: local computer).", False, ".")
            .addFlagString("--namespace", "namespace", "Specify namespace to connect to (default: root\\cimv2).", False, "root\\cimv2")
            .setHandler(lambda agentId, cmdline, args: (
                query := conquest.get_string(args, 0),
                server := conquest.get_string(args, 1),
                namespace := conquest.get_string(args, 2),

                bof := conquest.modules_root() + "/situational-awareness/CS-Situational-Awareness-BOF/SA/wmi_query/wmi_query.x64.o",
                params := conquest.bof_pack("ZZZZ", [
                    server,                             # Z: Target system
                    namespace,                          # Z: Target namespace
                    query,                              # Z: WMI Query
                    f"\\\\{server}\\{namespace}"        # Z: Resource
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("situational awareness")