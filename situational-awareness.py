import conquest
import os.path
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#                                          Situational Awareness                                          #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
cmd_whoami = (
    conquest.createCommand(name="whoami", description="Get user and group information.", example="whoami", 
                           message="Tasked agent to retrieve user and group information.", mitre=["T1033"])
            .setHandler(lambda agentId, cmdline, args: (
                bof := conquest.modules_root() + "/CS-Situational-Awareness-BOF/SA/whoami/whoami.x64.o",
                conquest.execute_alias(agentId, cmdline, f"bof {bof}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}")
            )))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
cmd_cat = (
    conquest.createCommand(name="cat", description="Retrieve the contents of a file.", example="cat C:\\Users\\Desktop\\Administrator\\passwords.txt", 
                           message="Tasked agent to retrieve the contents of a file.", mitre=["T1083"])
            .addArgString("file", "Relative or absolute path to the file.", True)
            .setHandler(lambda agentId, cmdline, args: (
                file := conquest.get_string(args, 0),

                bof := conquest.modules_root() + "/cobaltstrike-cat-bof/cat.x64.o",
                params := conquest.bof_pack("Z", [
                    file    # Z: File name
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}")
            )))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
cmd_cacls = (
    conquest.createCommand(name="cacls", description="List user permissions for the specified file, wildcards supported.", example="cacls C:\\Services\\service.exe",
                           message="Tasked agent to list file permissions.")
            .addArgString("file", "Relative or absolute path to the file.", True)
            .setHandler(lambda agentId, cmdline, args: (
                file := conquest.get_string(args, 0),

                bof := conquest.modules_root() + "/CS-Situational-Awareness-BOF/SA/cacls/cacls.x64.o",
                params := conquest.bof_pack("Z", [
                    file    # Z: File name
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}")
            )))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
cmd_enumdrives = (
    conquest.createCommand(name="enum-drives", description="List local drive letters and types.", example="enum-drives",
                           message="Tasked agent to list local drives.")
            .setHandler(lambda agentId, cmdline, args: (
                bof := conquest.modules_root() + "/OperatorsKit/KIT/EnumDrives/enumdrives.o",
                conquest.execute_alias(agentId, cmdline, f"bof {bof}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}")
            )))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
cmd_arp = (
    conquest.createCommand(name="arp", description="List ARP table.", example="arp", 
                           message="Tasked agent to retrieve ARP table.")
            .setHandler(lambda agentId, cmdline, args: (
                bof := conquest.modules_root() + "/CS-Situational-Awareness-BOF/SA/arp/arp.x64.o",
                conquest.execute_alias(agentId, cmdline, f"bof {bof}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}")
            )))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
cmd_ipconfig = ( 
    conquest.createCommand(name="ipconfig", description="List IPv4 address, hostname, and DNS server.", example="ipconfig", 
                           message="Tasked agent to list network configuration.")
            .setHandler(lambda agentId, cmdline, args: (
                bof := conquest.modules_root() + "/CS-Situational-Awareness-BOF/SA/ipconfig/ipconfig.x64.o",
                conquest.execute_alias(agentId, cmdline, f"bof {bof}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}")
            )))
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
                           message="Tasked agent to perform a DNS query.")
            .addArgString("hostname", "Hostname to look up.", True)
            .addFlagString("--server", "server", "DNS server.")
            .addFlagString("--type", "type", """DNS Record type (default: ANY).
Supported record types: ANY, A, NS, MD, MF, CNAME, SOA, MB, MG, MR, WKS, PTR, HINFO, MINFO, MX, TXT, RP, AFSDB, X25, ISDN, RT, AAAA, SRV, DNSKEY, NBSTAT""")
            .setHandler(lambda agentId, cmdline, args: (
                hostname := conquest.get_string(args, 0),
                server := conquest.get_string(args, 1),
                type := conquest.get_string(args, 2, "ANY").upper(),

                recordType := DNS_RECORD_TYPES.get(type, DNS_RECORD_TYPES["ANY"]),

                bof := conquest.modules_root() + "/CS-Situational-Awareness-BOF/SA/nslookup/nslookup.x64.o",
                params := conquest.bof_pack("zzs", [
                    hostname,       # z: Hostname
                    server,         # z: DNS Server
                    recordType      # s: DNS Record Type
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}")
            )))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
cmd_listdns = (
    conquest.createCommand(name="listdns", description="List DNS cache entries.", example="listdns", 
                        message="Tasked agent to list DNS cache entries.")
        .setHandler(lambda agentId, cmdline, args: (
            bof := conquest.modules_root() + "/CS-Situational-Awareness-BOF/SA/listdns/listdns.x64.o",
            conquest.execute_alias(agentId, cmdline, f"bof {bof}") if os.path.exists(bof)
            else conquest.error(agentId, f"Failed to open object file: {bof}")
        )))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
cmd_checkport = (
    conquest.createCommand(name="check-port", description="Check if a specific port is open on a remote machine.", example="check-port web01 80",
                           message="Tasked agent to check if a port is open on a remote machine.")
            .addArgString("target", "Hostname/IP address of the target system.", True)
            .addArgInt("port", "Port to check.", True)
            .setHandler(lambda agentId, cmdline, args: (
                target := conquest.get_string(args, 0),
                port := conquest.get_int(args, 1),

                bof := conquest.modules_root() + "/CS-Situational-Awareness-BOF/SA/probe/probe.x64.o",
                params := conquest.bof_pack("zi", [
                    target,         # z: Target hostname or IP 
                    port            # i: Port
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}")
            )))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
cmd_pingsweep = (
    conquest.createCommand(name="pingsweep", description="Scan an IP range for live hosts.", example="pingsweep 10.10.15.0/24",
                           message="Tasked agent to perform a pingscan.")
            .addArgString("targets", "Comma separated list of hosts to scan. Hostnames, IPs and IP ranges supported (eg. 192.168.1.128-192.168.2.240,192.168.1.0/24).", True)
            .setHandler(lambda agentId, cmdline, args: (
                targets := conquest.get_string(args, 0),

                bof := conquest.modules_root() + "/portscanbof/bin/pingscanner.bof.o",
                params := conquest.bof_pack("z", [
                    targets         # z: Target list
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}")
            )))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
cmd_netDomainGroup = (
    conquest.createCommand(name="net-group", description="List domain groups or members of a specified domain group.", example="net-group \"Domain Admins\" --domain domain.local",
                           message="Tasked agent to enumerate domain groups / domain group-memberships.")
            .addArgString("group", "Specify domain group name to view group memberships.")
            .addFlagString("--domain", "domain", "Domain (default: current domain).")
            .setHandler(lambda agentId, cmdline, args: (
                group := conquest.get_string(args, 0),
                domain := conquest.get_string(args, 1),

                bof := conquest.modules_root() + "/CS-Situational-Awareness-BOF/SA/netgroup/netgroup.x64.o",
                params := conquest.bof_pack("sZZ", [
                    1 if group != "" else 0,        # s: Type (0: list groups, 1: list group-memberships)
                    domain,                         # Z: Domain name
                    group                           # Z: Group name
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}")
            )))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
cmd_netLocalGroup = (
    conquest.createCommand(name="net-localgroup", description="List local groups or members of a specified local group.", example="net-localgroup \"Administrators\" --domain domain.local",
                           message="Tasked agent to enumerate local groups / local group-memberships.")
            .addArgString("group", "Specify local group name to view group memberships.")
            .addFlagString("--server", "server", "Server (default: local machine).")
            .setHandler(lambda agentId, cmdline, args: (
                group := conquest.get_string(args, 0),
                server := conquest.get_string(args, 1),

                bof := conquest.modules_root() + "/CS-Situational-Awareness-BOF/SA/netlocalgroup/netlocalgroup.x64.o",
                params := conquest.bof_pack("sZZ", [
                    1 if group != "" else 0,        # s: Type (0: list groups, 1: list group-memberships)
                    server,                         # Z: Server
                    group                           # Z: Group name
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}")
            )))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def handler_netUser(agentId, cmdline, args): 
    user = conquest.get_string(args, 0)
    domain = conquest.get_string(args, 1)

    if user != "": 
        # List user information if a username is specified
        bof = conquest.modules_root() + "/CS-Situational-Awareness-BOF/SA/netuser/netuser.x64.o"
        params = conquest.bof_pack("ZZ", [
            user,       # Z: Username 
            domain      # Z: Domain name
        ])
    else: 
        # List users
        bof = conquest.modules_root() + "/CS-Situational-Awareness-BOF/SA/netuserenum/netuserenum.x64.o"
        params = conquest.bof_pack("ii", [
            1 if domain != "" else 0,   # i: Use domain (0: local users, 1: domain users)
            1                           # i: Filter (1: all users, 2: locked-out users, 3: disabled users, 4: neither disabled and not locked-out users)
        ])

    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, f"Failed to open object file: {bof}")

cmd_netUser = (
    conquest.createCommand(name="net-user", description="List user information.", example="net-user svc_sql --domain domain.local",
                           message="Tasked agent to list user information.")
            .addArgString("user", "Specify username to retrieve user information. If no username is provided, this command enumerates and lists all users instead.")
            .addFlagString("--domain", "domain", "Specify domain to list domain users rather than local users.")
            .setHandler(handler_netUser))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
cmd_netShares = (
    conquest.createCommand(name="net-shares", description="List shares on a target system.", example="net-shares dc01 --admin",
                        message="Tasked agent to list shares.")
        .addArgString("host", "Hostname of the target system (default: local computer).")
        .addFlagBool("--admin", "admin", "List shares as admin (requires admin privileges).")
        .setHandler(lambda agentId, cmdline, args: (
            host := conquest.get_string(args, 0),
            admin := 1 if conquest.get_bool(args, 1) else 0,

            bof := conquest.modules_root() + "/CS-Situational-Awareness-BOF/SA/netshares/netshares.x64.o",
            params := conquest.bof_pack("Zi", [
                host,       # Z: Host 
                admin,      # i: List shares as admin
            ]),

            conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
            else conquest.error(agentId, f"Failed to open object file: {bof}")
        )))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
LDAP_SCOPE = {
    "base": 1,
    "level": 2,
    "subtree": 3
}
def ldapsearch_handler(agentId, cmdline, args):
    query = conquest.get_string(args, 0)
    attributes = conquest.get_string(args, 1, "*")
    count = conquest.get_int(args, 2)
    scope = conquest.get_string(args, 3, "subtree").lower()
    hostname = conquest.get_string(args, 4)
    dn = conquest.get_string(args, 5)
    ldaps = conquest.get_bool(args, 6)
    
    ldapScope = LDAP_SCOPE.get(scope, LDAP_SCOPE["subtree"])
    
    bof = conquest.modules_root() + "/CS-Situational-Awareness-BOF/SA/ldapsearch/ldapsearch.x64.o"
    params = conquest.bof_pack("zziizzi", [
        query,                      # z: LDAP filter query
        attributes,                 # z: Attributes (comma-separated or "*")
        count,                      # i: Max results (0 = unlimited)
        ldapScope,                  # i: Scope (1=base, 2=level, 3=subtree)
        hostname,                   # z: DC hostname (auto-discover if empty)
        dn,                         # z: Domain DN (auto-detect if empty)
        1 if ldaps else 0           # i: Use LDAPS
    ])
    
    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, f"Failed to open object file: {bof}")

cmd_ldapsearch = (
    conquest.createCommand(name="ldapsearch", description="Execute a LDAP query.", example="ldapsearch \"(objectClass=user)\" --attributes *,ntsecuritydescriptor --dn DC=conquest,DC=local --dc dc01.conquest.local",
                           message="Tasked agent to execute a LDAP query.")
            .addArgString("query", "LDAP filter query.", True)
            .addFlagString("--attributes", "attributes", "Attributes to retrieve, comma-separated (default: *).")
            .addFlagInt("--count", "count", "Maximum number of results (default: 0 = unlimited).")
            .addFlagString("--scope", "scope", """Search scope.
Available options:
  - base 
  - level 
  - subtree (default)""")
            .addFlagString("--dc", "hostname", "Hostname or IP of domain controller (default: default domain controller).")
            .addFlagString("--dn", "dn", "LDAP query base DN (default: current domain).")
            .addFlagBool("--ldaps", "ldaps", "Use LDAPS on port 636 instead of LDAP on port 389.")
            .setHandler(ldapsearch_handler))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def handler_scEnum(agentId, cmdline, args): 
    service = conquest.get_string(args, 0)
    server = conquest.get_string(args, 1)

    if service != "": 
        # Get information about a specific service (sc_qc)
        bof = conquest.modules_root() + "/CS-Situational-Awareness-BOF/SA/sc_qc/sc_qc.x64.o"
        params = conquest.bof_pack("zz", [
            server,         # z: Target server 
            service,        # z: Target service
        ])
    else: 
        # List all services (sc_enum)
        bof = conquest.modules_root() + "/CS-Situational-Awareness-BOF/SA/sc_enum/sc_enum.x64.o"
        params = conquest.bof_pack("z", [
            server          # z: Target server 
        ])

    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, f"Failed to open object file: {bof}")

cmd_scEnum = (
    conquest.createCommand(name="sc-enum", description="Get service information.", example="sc-enum --server dc01",
                           message="Tasked agent to enumerate services.")
            .addArgString("service", "Name of the target service. If not is provided, this command will list all services on the target system.")
            .addFlagString("--server", "server", "Hostname or IP address of the target system.")
            .setHandler(handler_scEnum))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
cmd_scQuery = (
    conquest.createCommand(name="sc-query", description="Query service status status.", example="sc-qc UpdaterSvc",
                           message="Tasked agent to query service status.")
            .addArgString("service", "Name of the target service. If not provided, this command will list the status of all services running on the target system.")
            .addFlagString("--server", "server", "Hostname or IP address of the target system.")
            .setHandler(lambda agentId, cmdline, args: (
                service := conquest.get_string(args, 0),
                server := conquest.get_string(args, 1),

                bof := conquest.modules_root() + "/CS-Situational-Awareness-BOF/SA/sc_query/sc_query.x64.o",
                params := conquest.bof_pack("zz", [
                    server,         # z: Target server 
                    service,        # z: Target service
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}")
            )))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def handler_schtasksEnum(agentId, cmdline, args): 
    task = conquest.get_string(args, 0)
    server = conquest.get_string(args, 1)

    if task != "": 
        # Get information about a specific scheduled task
        bof = conquest.modules_root() + "/CS-Situational-Awareness-BOF/SA/schtasksquery/schtasksquery.x64.o"
        params = conquest.bof_pack("ZZ", [
            server,         # Z: Target server 
            task,           # Z: Target scheduled task
        ])
    else: 
        # List all scheduled tasks
        bof = conquest.modules_root() + "/CS-Situational-Awareness-BOF/SA/schtasksenum/schtasksenum.x64.o"
        params = conquest.bof_pack("Z", [
            server          # Z: Target server 
        ])

    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, f"Failed to open object file: {bof}")

cmd_schtasksEnum = (
    conquest.createCommand(name="schtasks-enum", description="Get information about scheduled task.", example="schtasks-enum \"\\Microsoft\\Office\\Office Background Push Maintenance\"",
                           message="Tasked agent to enumerate scheduled tasks.")
            .addArgString("path", "Path to the target scheduled task. If not provided, this command will list all scheduled tasks on the target system.")
            .addFlagString("--server", "server", "Hostname or IP address of the target system.")
            .setHandler(handler_schtasksEnum))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
REGISTRY_HIVES = {
    "HKCR": 0,  # HKEY_CLASSES_ROOT
    "HKCU": 1,  # HKEY_CURRENT_USER
    "HKLM": 2,  # HKEY_LOCAL_MACHINE
    "HKU": 3    # HKEY_USERS
}
def handler_regQuery(agentId, cmdline, args): 
    hive = conquest.get_string(args, 0).upper()
    path = conquest.get_string(args, 1)
    key = conquest.get_string(args, 2)
    hostname = conquest.get_string(args, 3)
    recursive = conquest.get_bool(args, 4)
    
    regHive = REGISTRY_HIVES.get(hive)
    if regHive is None:
        conquest.log_command(agentId, cmdline)
        conquest.error(agentId, f"Invalid registry hive: {hive}.")
        return
    
    bof = conquest.modules_root() + "/CS-Situational-Awareness-BOF/SA/reg_query/reg_query.x64.o"
    params = conquest.bof_pack("zizzi", [
        hostname,                   # z: Hostname 
        regHive,                    # i: Hive (0=HKCR, 1=HKCU, 2=HKLM, 3=HKU)
        path,                       # z: Registry path
        key,                        # z: Key 
        1 if recursive else 0       # i: Recursive enumeration
    ])
    
    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, f"Failed to open object file: {bof}")

cmd_regQuery = (
    conquest.createCommand(name="reg-query", description="Query the registry.", example="reg-query HKLM \"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\" ProgramFilesDir",
                           message="Tasked agent to query the registry.")
            .addArgString("hive", """Registry hive.
Available options:
  - HKCR
  - HKCU
  - HKLM
  - HKC""", True)
            .addArgString("path", "Registry path.", True)
            .addArgString("key", "Specific key/value name to query. If not provided, enumerates all subkeys and values.")
            .addFlagString("--hostname", "hostname", "Target hostname for remote registry (default: local computer).")
            .addFlagBool("--recursive", "recursive", "Recursively enumerate all subkeys.")
            .setHandler(handler_regQuery))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

conquest.registerModule(
    name="situational-awareness", 
    description="Local and remote reconnaissance capabilities.", 
    group="situational-awareness", 
    commands=[cmd_whoami, 
              cmd_cat, cmd_cacls, cmd_enumdrives,
              cmd_arp, cmd_ipconfig, cmd_nslookup, cmd_listdns, cmd_checkport, cmd_pingsweep,
              cmd_netDomainGroup, cmd_netLocalGroup, cmd_netUser, cmd_netShares,
              cmd_scEnum, cmd_scQuery, cmd_schtasksEnum, cmd_regQuery,
              cmd_ldapsearch
    ])