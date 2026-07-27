import conquest
import os.path

scripts = [
    "situational-awareness/situational-awareness.py",
    "remote-operations/remote-ops.py",
    "privilege-escalation/privilege-escalation.py",
    "lateral-movement/scshell.py",
    "credential-dumping/credential-dumping.py",
    "kerbeus/kerbeus.py",
    "mssql/SQL.py",
    "execution/no-consolation.py",
    "execution/async-bof.py"
]

for script in scripts:
    conquest.load_script(os.path.join(conquest.modules_root(), script))

conquest.unload_script(__file__)