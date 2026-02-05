import conquest
import os.path

# Situational awarness BOF wrappers
sa_root = "/situational-awareness/"

cmd_whoami = (
    conquest.createCommand(name="whoami", description="Get user and group information.", example="whoami", 
                           message="Tasked agent to retrieve user and group information.", mitre=["T1033"])
            .setHandler(lambda agentId, cmdline, args: (
                bof := conquest.modules_root() + sa_root + "sa/SA/whoami/whoami.x64.o",
                conquest.execute_alias(agentId, cmdline, f"bof {bof}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}")
            )))

cmd_cat = (
    conquest.createCommand(name="cat", description="Retrieve the contents of a file.", example="cat C:\\Users\\Desktop\\Administrator\\passwords.txt", 
                           message="Tasked agent to retrieve the contents of a file.", mitre=["T1083"])
            .addArgString("file", "Relative or absolute path to the file.", True)
            .setHandler(lambda agentId, cmdline, args: (
                file := conquest.get_string(args, 0),

                bof := conquest.modules_root() + sa_root + "cat/cat.x64.o",
                params := conquest.bof_pack("Z", [
                    file    # Z: File name
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}")
            )))

cmd_arp = (
    conquest.createCommand(name="arp", description="List ARP table.", example="arp", 
                           message="Tasked agent to retrieve ARP table.")
            .setHandler(lambda agentId, cmdline, args: (
                bof := conquest.modules_root() + sa_root + "sa/SA/arp/arp.x64.o",
                conquest.execute_alias(agentId, cmdline, f"bof {bof}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}")
            )))

cmd_cacls = (
    conquest.createCommand(name="cacls", description="List user permissions for the specified file, wildcards supported.", example="cacls C:\\Services\\service.exe",
                           message="Tasked agent to list file permissions.")
            .addArgString("file", "Relative or absolute path to the file.", True)
            .setHandler(lambda agentId, cmdline, args: (
                file := conquest.get_string(args, 0),

                bof := conquest.modules_root() + sa_root + "sa/SA/cacls/cacls.x64.o",
                params := conquest.bof_pack("Z", [
                    file    # Z: File name
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}")
            )))

cmd_ipconfig = ( 
    conquest.createCommand(name="ipconfig", description="List IPv4 address, hostname, and DNS server.", example="ipconfig", 
                           message="Tasked agent to list network configuration.")
            .setHandler(lambda agentId, cmdline, args: (
                bof := conquest.modules_root() + sa_root + "sa/SA/ipconfig/ipconfig.x64.o",
                conquest.execute_alias(agentId, cmdline, f"bof {bof}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}")
            )))

cmd_netDomainGroup = (
    conquest.createCommand(name="net-group", description="List domain groups or members of a specified domain group.", example="net-group \"Domain Admins\" --domain domain.local",
                           message="Tasked agent to enumerate domain groups / domain group-memberships.")
            .addArgString("group", "Specify domain group name to view group memberships.")
            .addFlagString("--domain", "domain", "Domain (Default: current domain).")
            .setHandler(lambda agentId, cmdline, args: (
                group := conquest.get_string(args, 0),
                domain := conquest.get_string(args, 1),

                type := 1 if group != "" else 0, # List group members if group is provided as an argument

                bof := conquest.modules_root() + sa_root + "sa/SA/netgroup/netgroup.x64.o",
                params := conquest.bof_pack("sZZ", [
                    type,           # s: Type (0: list groups, 1: list group-memberships)
                    domain,         # Z: Domain name
                    group           # Z: Group name
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}")
            )))

cmd_netLocalGroup = (
    conquest.createCommand(name="net-localgroup", description="List local groups or members of a specified local group.", example="net-localgroup \"Administrators\" --domain domain.local",
                           message="Tasked agent to enumerate local groups / local group-memberships.")
            .addArgString("group", "Specify local group name to view group memberships.")
            .addFlagString("--server", "server", "Server (Default: local machine).")
            .setHandler(lambda agentId, cmdline, args: (
                group := conquest.get_string(args, 0),
                server := conquest.get_string(args, 1),

                type := 1 if group != "" else 0, # List group members if group is provided as an argument

                bof := conquest.modules_root() + sa_root + "sa/SA/netlocalgroup/netlocalgroup.x64.o",
                params := conquest.bof_pack("sZZ", [
                    type,           # s: Type (0: list groups, 1: list group-memberships)
                    server,         # Z: Server
                    group           # Z: Group name
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}")
            )))

def handler_netUser(agentId, cmdline, args): 
    user = conquest.get_string(args, 0)
    domain = conquest.get_string(args, 1)

    if user != "": 
        # List user information if a username is specified
        bof = conquest.modules_root() + sa_root + "sa/SA/netuser/netuser.x64.o"
        params = conquest.bof_pack("ZZ", [
            user,       # Z: Username 
            domain      # Z: Domain name
        ])
    else: 
        # List users
        bof = conquest.modules_root() + sa_root + "sa/SA/netuserenum/netuserenum.x64.o"
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
            .addArgString("user", "Specify username to retrieve information.")
            .addFlagString("--domain", "domain", "Specify domain to list domain users rather than local users.")
            .setHandler(handler_netUser))




conquest.registerModule(
    name="situational-awareness", 
    description="Local and remote reconnaissance capabilities.", 
    group="situational-awareness", 
    commands=[cmd_whoami, cmd_cat, cmd_arp, cmd_cacls, cmd_ipconfig, cmd_netDomainGroup, cmd_netLocalGroup, cmd_netUser])