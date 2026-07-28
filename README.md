# Conquest Modules

This is the offical module repository for the [Conquest](https://github.com/jakobfriedl/conquest/) post-exploitation framework. It contains a collection of Python modules that allow operators to use battle-tested BOFs with the Conquest framework. Among others, commands are created for post-exploitation capabilities from famous repositories, such as [CS-Situational-Awareness-BOF](https://github.com/trustedsec/CS-Situational-Awareness-BOF) and [CS-Remote-OPs-BOF](https://github.com/trustedsec/CS-Remote-OPs-BOF).

## Modules 

Refer to the following modules for more information about the included commands.

- [Core Modules](https://github.com/jakobfriedl/conquest/blob/main/docs/7-MODULES.md)
- [Execution](./execution/)
- [Situational Awareness](./situational-awareness/)
- [Remote Operations](./remote-operations/)
- [Privilege Escalation](./privilege-escalation/)
- [Kerberos Abuse](./kerbeus/)
- [MSSQL Abuse](./mssql/)
- [Credential Dumping](./credential-dumping/)
- [Lateral Movement](./lateral-movement/)

```
CORE
 * config                   Retrieve and update agent settings.
 * exit                     Exit the agent.
 * self-destruct            Exit the agent and delete the executable from disk.
 * link                     Create a link to a SMB agent.
 * unlink                   Remove a link to a SMB agent.
 * links                    List linked agents.
 * jobs                     List running jobs.
 * cancel                   Cancel a running job.

EXECUTION
 * shell                    Execute a shell command and retrieve the output.
 * bof                      Execute an object file in memory and retrieve the output.
 * dotnet                   Execute a .NET assembly in memory and retrieve the output.
 * dll                      Execute a DLL asynchronously in memory.
 * no-consolation           Execute an unmanaged PE in memory.
 * bof-async                Execute an object file asynchronously in the background.

POST-EXPLOITATION
 * download                 Download a file.
 * upload                   Upload a file.
 * regdump                  Dump SAM, SYSTEM and SECURITY from the Windows registry.
 * silentharvest            Gather SAM and SECURITY secrets using the SilentHarvest method of dumping registry values.
 * keelog                   Capture KeePass master password (async).

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
 * get-machineaccountquota  Retrieve MachineAccountQuota in the current domain.
 * asyncscan                Scan target systems for open ports (async).
 * asyncsweep               Scan for live hosts (async).
 * clipboard-monitor        Monitor and output clipboard changes to the agent console (async).
 * get-clipboard            Retrieve clipboard contents.
 * usb-monitor              Notify when a USB device is connected/disconnected (async).
 * logon-monitor            Notify when a user logs on to a target system (async).
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
 * net-group                List domain groups or members of a specified domain group.
 * net-localgroup           List local groups or members of a specified local group.
 * net-user                 List user information.
 * net-shares               List shares on a target system.
 * ldapsearch               Execute a LDAP query.
 * ldapquery                Execute a pre-configured LDAP query.
 * convertfrom-sid          Convert a SID to a group/user name.
 * list-windows             List visible windows in the current user session.
 * wmi-query                Run a WMI query on a local or remote system.

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
 * tgt-monitor              Monitor for new Kerberos TGTs and automatically extract them as they appear (async).
 * tgt-renew                Automatically renew Kerberos TGTs that are about to expire (async).

USER IMPERSONATION
 * make-token               Create an access token from username and password.
 * steal-token              Steal the primary access token of a remote process.
 * use-token                Use and impersonate access token from the vault.
 * remove-token             Remove access token from the vault.
 * rev2self                 Revert to original access token.
 * token-vault              List access tokens stored in the vault.
 * token-info               Retrieve information about the current access token.
 * enable-privilege         Enable a token privilege.
 * disable-privilege        Disable a token privilege.

REMOTE OPERATIONS
 * add-machineaccount       Add computer account to the Active Directory domain.
 * remove-machineaccount    Delete computer account from the Active Directory domain.
 * add-user                 Add a user to a machine.
 * add-groupmembership      Add a specified user to a group.
 * enable-user              Enable a specified user account.
 * unexpire-user            Unexpire and enable a specified user account.
 * set-password             Set the password of a target user account.
 * shutdown                 Shutdown or reboot a target system.

PRIVILEGE ESCALATION
 * privkit                  Run Windows privilege escalation checks.
 * godpotato                Escalate privileges to NT AUTHORITY\SYSTEM via SeImpersonatePrivilege (GodPotato).

LATERAL MOVEMENT
 * scshell                  Perform fileless lateral movement by modifying an existing remote service's binary path (SCShell tool).

MSSQL ABUSE
 * sql-1434udp              Enumerate SQL Server connection information.
 * sql-adsi                 Obtain ADSI credentials from a linked server.
 * sql-agentcmd             Execute a system command using agent jobs.
 * sql-agentstatus          Enumerate SQL Agent status and jobs.
 * sql-checkrpc             Enumerate RPC status of linked servers.
 * sql-clr                  Load and execute .NET assembly in a stored procedure.
 * sql-columns              Enumerate columns within a table.
 * sql-databases            Enumerate SQL databases.
 * sql-enable               Enable a SQL server module.
 * sql-disable              Disable a SQL server module.
 * sql-impersonate          Enumerate users that can be impersonated.
 * sql-info                 Gather information about the SQL server.
 * sql-links                Enumerate linked servers.
 * sql-olecmd               Execute a system command using OLE Automation Procedures.
 * sql-query                Execute a custom SQL query.
 * sql-rows                 Get the count of rows in a table.
 * sql-search               Search a table for a column name.
 * sql-smb                  Coerce NetNTLM auth via xp_dirtree.
 * sql-tables               Enumerate tables within a database.
 * sql-users                Enumerate users with database access.
 * sql-whoami               Gather logged in user, mapped user and roles.
 * sql-xpcmdshell           Execute a system command via xp_cmdshell.

LDAP OPERATIONS
 * get-users                List all users in the domain.
 * get-computers            List all computers in the domain.
 * get-groups               List all groups in the domain.
 * get-usergroups           List all groups a user is a member of.
 * get-groupmembers         List all members of a group.
 * get-object               Get all attributes of an object.
 * get-domaininfo           Get domain information from rootDSE.
 * get-maq                  Get machine account quota (ms-DS-MachineAccountQuota).
 * get-writable             Find objects you have write access to.
 * get-delegation           Get delegation configuration for an object.
 * get-uac                  Get UAC flags for an object.
 * get-attribute            Get specific attribute values.
 * get-spn                  Get SPNs for an object.
 * get-acl                  Get ACL/security descriptor for an object.
 * get-rbcd                 Get RBCD configuration for an object.
 * add-user                 Add a user to the domain.
 * add-computer             Add a computer to the domain.
 * add-group                Add a group to the domain.
 * add-groupmember          Add a member to a group.
 * add-ou                   Add an organizational unit.
 * add-sidhistory           Add a SID to an object's sidHistory attribute.
 * add-spn                  Add an SPN to an object.
 * add-attribute            Add a value to an attribute.
 * add-uac                  Add UAC flags to an object.
 * add-delegation           Add a delegation SPN to an object.
 * add-rbcd                 Add an RBCD delegation.
 * add-ace                  Add an ACE to an object's DACL.
 * add-genericall           Add a GenericAll ACE to an object's DACL.
 * add-genericwrite         Add a GenericWrite ACE to an object's DACL.
 * add-dcsync               Add a DCSync ACE to an object's DACL.
 * add-asreproastable       Make a user AS-REP roastable (set DONT_REQ_PREAUTH).
 * add-unconstrained        Enable unconstrained delegation on an object.
 * add-constrained          Set/replace delegation SPNs (constrained delegation).
 * set-password             Set/reset a user's password.
 * set-spn                  Set/replace all SPNs on an object.
 * set-delegation           Set/replace delegation SPNs.
 * set-attribute            Set/replace an attribute value.
 * set-uac                  Set UAC flags (replaces all).
 * set-owner                Set the owner of an object (requires WriteOwner).
 * move-object              Move an object to a different OU.
 * remove-groupmember       Remove a member from a group.
 * remove-object            Remove an object from the domain.
 * remove-spn               Remove an SPN from an object.
 * remove-delegation        Remove a delegation SPN.
 * remove-attribute         Remove an attribute or attribute value.
 * remove-uac               Remove UAC flags from an object.
 * remove-ace               Remove an ACE from an object's DACL.
 * remove-rbcd              Remove an RBCD delegation.
 * remove--dcsync           Remove a DCSync ACE from an object's DACL.
 * remove-genericwrite      Remove a GenericWrite ACE from an object's DACL.
 * remove-genericall        Remove a GenericAll ACE from an object's DACL.
```

## Creating Modules

Check out the [Conquest documentation](https://github.com/jakobfriedl/conquest/blob/main/docs/8-SCRIPTING.md) to learn how to use the Python Scripting API to create your own modules.