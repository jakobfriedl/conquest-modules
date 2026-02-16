import conquest
import os.path 

# Windows Privilege Escalation checks using PrivKit BOFs by @merterpreter & @nickvourd

PRIVESC_CHECKS = {
    "always-install-elevated": "/privilege-escalation/PrivKit/AlwaysInstallElevatedCheck/AlwaysInstallElevatedCheck.x64.o",
    "autologon": "/privilege-escalation/PrivKit/AutoLogonCheck/AutoLogonCheck.x64.o",
    "cred-manager": "/privilege-escalation/PrivKit/CredentialManagerCheck/CredentialManagerCheck.x64.o",
    "hijack-path": "/privilege-escalation/PrivKit/HijackablePathCheck/HijackablePathCheck.x64.o",
    "modify-autorun": "/privilege-escalation/PrivKit/ModifiableAutorunCheck/ModifiableAutorunCheck.x64.o",
    "modify-svc": "/privilege-escalation/PrivKit/ModifiableSVCCheck/ModifiableSVCCheck.x64.o",
    "token-privs": "/privilege-escalation/PrivKit/TokenPrivilegesCheck/TokenPrivilegesCheck.x64.o",
    "unquoted-svc-path": "/privilege-escalation/PrivKit/UnquotedSVCPathCheck/UnquotedSVCPathCheck.x64.o",
    "ps-history": "/privilege-escalation/PrivKit/PowerShellHistoryCheck/PowerShellHistoryCheck.x64.o",
    "uac-status": "/privilege-escalation/PrivKit/UACStatusCheck/UACStatusCheck.x64.o"
}
def _privkit(agentId, cmdline, args): 
    check = conquest.get_string(args, 0).lower()
        
    if check == "all":
        # Execute all checks
        for name, path in PRIVESC_CHECKS.items():
            bof = conquest.modules_root() + path
            if os.path.exists(bof):
                conquest.execute_alias(agentId, f"privkit {name}", f"bof {bof}")
            else:
                conquest.error(agentId, "cmdline", f"Failed to open object file: {bof}")
    else:
        # Execute specific check
        path = PRIVESC_CHECKS.get(check)
        if path is None:
            conquest.error(agentId, cmdline, f"Invalid privilege escalation check: {check}")
            return
        
        bof = conquest.modules_root() + path
        if os.path.exists(bof):
            conquest.execute_alias(agentId, cmdline, f"bof {bof}")
        else:
            conquest.error(agentId, cmdline, f"Failed to open object file: {bof}")

cmd_privkit = (
    conquest.createCommand(name="privkit", description="Run Windows privilege escalation checks.", example="privkit unquoted-svc-path",
                           message="Tasked agent to run privilege escalation check.", mitre=[])
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
