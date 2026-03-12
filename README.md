# Conquest Modules

This is the offical modules repository for the [Conquest](https://github.com/jakobfriedl/conquest/) post-exploitation framework. It contains a collection of Python modules that allow operators to use battle-tested BOFs with the Conquest framework. Among others, commands are created for post-exploitation capabilities from the famous repositories ([CS-Situational-Awareness-BOF](https://github.com/trustedsec/CS-Situational-Awareness-BOF), [CS-Remote-OPs-BOF](https://github.com/trustedsec/CS-Remote-OPs-BOF), ...) 

## Modules 

Refer to the following modules for more information about the included commands.

- [Situational Awareness](./situational-awareness/README.md)
- [Remote Operations](./remote-operations/README.md)
- [Kerberos Abuse](./kerbeus/README.md)
- [Privilege Escalation](./privilege/escalation/README.md)
- [Credential Dumping](./credential-dumping/README.md)
- [Lateral Movement](./lateral-movement/README.md)
- [Execution](./execution/README.md)

```
CORE
 * exit                     Exit the agent.
 * self-destruct            Exit the agent and delete the executable from disk.
 * sleep                    Update sleep delay settings.
 * jitter                   Update jitter settings.
 * sleepmask                Retrieve or update sleepmask settings. Executing without arguments retrieves the current sleepmask settings.
 * link                     Create a link to a SMB agent.
 * unlink                   Remove a link to a SMB agent.

EXECUTION
 * shell                    Execute a shell command and retrieve the output.
 * bof                      Execute an object file in memory and retrieve the output.
 * dotnet                   Execute a .NET assembly in memory and retrieve the output.
 * no-consolation           Execute an unmanaged PE in memory.

POST-EXPLOITATION
 * download                 Download a file.
 * upload                   Upload a file.
 * regdump                  Dump SAM, SYSTEM and SECURITY from the Windows registry.

SITUATIONAL AWARENESS
 * ps                       Display running processes.
 * pwd                      Retrieve current working directory.
 * cd                       Change current working directory.
 * ls                       List files and directories.
 * rm                       Remove a file.
 * rmdir                    Remove a directory.
 * move                     Move a file or directory.
 * copy                     Copy a file or directory.
 * screenshot               Take and retrieve a screenshot of the target desktop.
 * cat                      Retrieve the contents of a file.
 * enum-drives              List local drive letters and types.
 * whoami                   Get user and group information.
 * env                      List environment variables.
 * dir                      List files and directories using BOF.
 * cacls                    List user permissions for the specified file, wildcards supported.
 * arp                      List ARP table.
 * ipconfig                 List IPv4 address, hostname, and DNS server.
 * nslookup                 Perform a DNS query.
 * list-dns                 List DNS cache entries.
 * netstat                  List network connections.
 * list-routes              List IPv4 routing table.
 * list-pipes               List named pipes.
 * check-port               Check if a specific port is open on a remote machine.
 * pingsweep                Scan an IP range for live hosts.
 * net-group                List domain groups or members of a specified domain group.
 * net-localgroup           List local groups or members of a specified local group.
 * net-user                 List user information.
 * net-shares               List shares on a target system.
 * ldapsearch               Execute a LDAP query.
 * ldapquery                Execute a pre-configured LDAP query.
 * list-windows             List visible windows in the current user session.
 * wmi-query                Run a WMI query on a local or remote system.

USER IMPERSONATION
 * make-token               Create an access token from username and password.
 * steal-token              Steal the primary access token of a remote process.
 * rev2self                 Revert to original access token.
 * token-info               Retrieve information about the current access token.
 * enable-privilege         Enable a token privilege.
 * disable-privilege        Disable a token privilege.

REMOTE OPERATIONS
 * add-user                 Add a user to a machine.
 * add-groupmembership      Add a specified user to a group.
 * enable-user              Enable a specified user account.
 * unexpire-user            Unexpire and enable a specified user account.
 * set-password             Set the password of a target user account.
 * shutdown                 Shutdown or reboot a target system.

WINDOWS REGISTRY
 * reg-set                  Create or set a registry key/value on a target system.
 * reg-delete               Delete a registry key/key on a target system.
 * reg-save                 Save a specified registry key to a file on the target system.
 * reg-query                Query the registry.

WINDOWS SERVICES
 * sc-config                Configure an existing service on the target system
 * sc-create                Create a service on the target system
 * sc-delete                Delete a service on the target system
 * sc-start                 Start a service on the target system
 * sc-stop                  Stop a service on the target system
 * sc-enum                  Get service information.
 * sc-query                 Query service status status.

SCHEDULED TASKS
 * schtasks-create          Create a scheduled task on the target system
 * schtasks-delete          Delete a scheduled task or task folder on the target system
 * schtasks-start           Run a scheduled task on the target system
 * schtasks-stop            Stop a running scheduled task on the target system
 * schtasks-enum            Get information about scheduled task.

LATERAL MOVEMENT
 * scshell                  Perform fileless lateral movment by modifying an existing remote service's binary path (SCShell tool).

KERBEROS ABUSE
 * asktgt                   Retrieve a TGT for a user using username and password/hash.
 * asktgs                   Retrieve a service ticket using a TGT.
 * renew                    Renew a TGT.
 * s4u                      Perform S4U constrained delegation abuse.
 * cross-s4u                Perform S4U constrained delegation abuse across domains.
 * ptt                      Inject a Kerberos ticket into a logon session via Pass-the-Ticket.
 * purge                    Purge tickets from a logon session.
 * describe                 Parse and describe a ticket.
 * klist                    List tickets in the current user's logon session. If the agent runs in an elevated context, this command will display tickets from all logon sessions.
 * dump                     Extract current TGTs and service tickets for the current user. If the agent runs in an elevated context, all current TGTs and service tickets are extracted.
 * triage                   List current user tickets. If the agent runs in an elevated context, all Kerberos tickets on the system are displayed.
 * tgtdeleg                 Retrieve a usable TGT for the current user without elevation by abusing the Kerberos GSS-API.
 * kerberoast               Perform Kerberoasting.
 * asreproast               Perform AS-REP roasting.
 * hash                     Calculate rc4_hmac, aes128_cts_hmac_sha1, aes256_cts_hmac_sha1 hashes.
 * changepw                 Reset a user's password from a supplied TGT.

PRIVILEGE ESCALATION
 * privkit                  Run Windows privilege escalation checks.
```

## Creating Modules

Check out the [Conquest documentation](https://github.com/jakobfriedl/conquest/blob/main/docs/8-SCRIPTING.md) to learn how to use the Python Scripting API to create your own modules. 