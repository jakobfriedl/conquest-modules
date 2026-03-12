# Remote Operations Modules <!-- omit from toc -->

## Contents <!-- omit from toc -->

- [Overview](#overview)
  - [add-user](#add-user)
  - [add-groupmembership](#add-groupmembership)
  - [enable-user](#enable-user)
  - [unexpire-user](#unexpire-user)
  - [set-password](#set-password)
  - [reg-set](#reg-set)
  - [reg-delete](#reg-delete)
  - [reg-save](#reg-save)
  - [sc-config](#sc-config)
  - [sc-create](#sc-create)
  - [sc-delete](#sc-delete)
  - [sc-start](#sc-start)
  - [sc-stop](#sc-stop)
  - [schtasks-create](#schtasks-create)
  - [schtasks-delete](#schtasks-delete)
  - [schtasks-start](#schtasks-start)
  - [schtasks-stop](#schtasks-stop)
  - [shutdown](#shutdown)

## Overview

The remote operations modules provide commands for managing users, registry keys, services, scheduled tasks, and system state on local and remote systems. All commands are implemented as BOF wrappers for [CS-Remote-OPs-BOF](https://github.com/trustedsec/CS-Remote-OPs-BOF). The module contains the following commands:

```
 * add-user                 Add a user to a machine.
 * add-groupmembership      Add a specified user to a group.
 * enable-user              Enable a specified user account.
 * unexpire-user            Unexpire and enable a specified user account.
 * set-password             Set the password of a target user account.
 * reg-set                  Create or set a registry key/value on a target system.
 * reg-delete               Delete a registry key/value on a target system.
 * reg-save                 Save a specified registry key to a file on the target system.
 * sc-config                Configure an existing service on the target system.
 * sc-create                Create a service on the target system.
 * sc-delete                Delete a service on the target system.
 * sc-start                 Start a service on the target system.
 * sc-stop                  Stop a service on the target system.
 * schtasks-create          Create a scheduled task on the target system.
 * schtasks-delete          Delete a scheduled task or task folder on the target system.
 * schtasks-start           Run a scheduled task on the target system.
 * schtasks-stop            Stop a running scheduled task on the target system.
 * shutdown                 Shutdown or reboot a target system.
```

### add-user
Add a user to a machine.

```
Usage  : add-user <username> <password> [--server <server>]
Example: add-user backdoor Password123!

Required arguments:
  username                  STRING     Username of the new account.
  password                  STRING     Password of the new account.

Optional arguments:
  --server server           STRING     Specify target system (default: local computer).
```

### add-groupmembership
Add a specified user to a group.

```
Usage  : add-groupmembership <user> <group> [--server <server>]
Example: add-groupmembership conquest.local\backdoor "Domain Admins" --server dc01

Required arguments:
  user                      STRING     Target account in format domain.local\username.
                                       If the user is a local account, only specify the username.
  group                     STRING     Name of the target group.

Optional arguments:
  --server server           STRING     Specify target system (default: local computer).
```

### enable-user
Enable a specified user account.

```
Usage  : enable-user <user>
Example: enable-user conquest.local\user

Required arguments:
  user                      STRING     Target account in format domain.local\username.
                                       If the user is a local account, only specify the username.
```

### unexpire-user
Unexpire and enable a specified user account.

```
Usage  : unexpire-user <user>
Example: unexpire-user conquest.local\user

Required arguments:
  user                      STRING     Target account in format domain.local\username.
                                       If the user is a local account, only specify the username.
```

### set-password
Set the password of a target user account.

```
Usage  : set-password <user> <password>
Example: set-password conquest.local\user Password123!

Required arguments:
  user                      STRING     Target account in format domain.local\username.
                                       If the user is a local account, only specify the username.
  password                  STRING     New password.
```

### reg-set
Create or set a registry key/value on a target system.

```
Usage  : reg-set <hive> <path> <type> <data> [--key <key>] [--server <server>]
Example: reg-set HKCU "Software\TestApp" REG_SZ "Hello World" --key TestValue

Required arguments:
  hive                      STRING     Registry hive.
                                         - HKCR    HKEY_CLASSES_ROOT
                                         - HKCU    HKEY_CURRENT_USER
                                         - HKLM    HKEY_LOCAL_MACHINE
                                         - HKU     HKEY_USERS
  path                      STRING     Path to the registry key to modify.
  type                      STRING     Type of the registry value.
  data                      STRING     Data to store in the registry value.
                                       For REG_BINARY, provide a file path.

Optional arguments:
  --key key                 STRING     Name of the registry value (default: "").
  --server server           STRING     Target server for remote registry (default: local computer).
```

Available registry types:

| Type | Description |
| --- | --- |
| `REG_SZ` | String value |
| `REG_EXPAND_SZ` | Expandable string |
| `REG_BINARY` | Binary data (provide file path as data) |
| `REG_DWORD` | 32-bit integer |
| `REG_MULTI_SZ` | Multiple strings |
| `REG_QWORD` | 64-bit integer |

### reg-delete
Delete a registry key/value on a target system.

```
Usage  : reg-delete <hive> <path> [--key <key>] [--delete-key] [--server <server>]
Example: reg-delete HKCU "Software\TestApp" --key myValue

Required arguments:
  hive                      STRING     Registry hive.
                                         - HKCR    HKEY_CLASSES_ROOT
                                         - HKCU    HKEY_CURRENT_USER
                                         - HKLM    HKEY_LOCAL_MACHINE
                                         - HKU     HKEY_USERS
  path                      STRING     Path to the registry key to delete.

Optional arguments:
  --key key                 STRING     Name of the registry value to delete (default: "").
  --delete-key              BOOL       Delete the entire registry key.
  --server server           STRING     Target server for remote registry (default: local computer).
```

### reg-save
Save a specified registry key to a file on the target system. Automatically enables `SeBackupPrivilege` before execution.

```
Usage  : reg-save <hive> <path> <output-file>
Example: reg-save HKLM SAM C:\Windows\Tasks\sam.txt

Required arguments:
  hive                      STRING     Registry hive.
                                         - HKCR    HKEY_CLASSES_ROOT
                                         - HKCU    HKEY_CURRENT_USER
                                         - HKLM    HKEY_LOCAL_MACHINE
                                         - HKU     HKEY_USERS
  path                      STRING     Path to the registry key to save.
  output-file               STRING     Output file path on the target system.
```

### sc-config
Configure an existing service on the target system.

```
Usage  : sc-config <service> [binPath] [--error-mode <mode>] [--start-mode <mode>] [--server <server>]
Example: sc-config ConquestSvc C:\Temp\malware.exe

Required arguments:
  service                   STRING     Service to configure.

Optional arguments:
  binPath                   STRING     Binary path to set on the service.
  --error-mode mode         INT        Error mode (default: 1).
                                         - 0: ignore errors
                                         - 1: normal logging
                                         - 2: log severe errors
                                         - 3: log critical errors
  --start-mode mode         INT        Start mode (default: 2).
                                         - 2: auto start
                                         - 3: on demand start
                                         - 4: disabled
  --server server           STRING     Hostname or IP address of the target system (default: local computer).
```

### sc-create
Create a service on the target system.

```
Usage  : sc-create <service> <display-name> <binPath> [--description <desc>] [--error-mode <mode>] [--start-mode <mode>] [--sc-type <type>] [--server <server>]
Example: sc-create ConquestSvc "Conquest Service" C:\Windows\System32\calc.exe --description "Conquest service description."

Required arguments:
  service                   STRING     Service name.
  display-name              STRING     Display name of the service.
  binPath                   STRING     Binary path of the service.

Optional arguments:
  --description desc        STRING     Description of the service (default: "").
  --error-mode mode         INT        Error mode (default: 1).
                                         - 0: ignore errors
                                         - 1: normal logging
                                         - 2: log severe errors
                                         - 3: log critical errors
  --start-mode mode         INT        Start mode (default: 2).
                                         - 2: auto start
                                         - 3: on demand start
                                         - 4: disabled
  --sc-type type            STRING     Service type (default: SERVICE_WIN32_OWN_PROCESS).
                                         - SERVICE_FILE_SYSTEM_DRIVER
                                         - SERVICE_KERNEL_DRIVER
                                         - SERVICE_WIN32_OWN_PROCESS
                                         - SERVICE_WIN32_SHARE_PROCESS
  --server server           STRING     Hostname or IP address of the target system (default: local computer).
```

### sc-delete
Delete a service on the target system.

```
Usage  : sc-delete <service> [--server <server>]
Example: sc-delete ConquestSvc --server dc01

Required arguments:
  service                   STRING     Name of the service to delete.

Optional arguments:
  --server server           STRING     Hostname or IP address of the target system (default: local computer).
```

### sc-start
Start a service on the target system.

```
Usage  : sc-start <service> [--server <server>]
Example: sc-start ConquestSvc --server dc01

Required arguments:
  service                   STRING     Name of the service to start.

Optional arguments:
  --server server           STRING     Hostname or IP address of the target system (default: local computer).
```

### sc-stop
Stop a service on the target system.

```
Usage  : sc-stop <service> [--server <server>]
Example: sc-stop ConquestSvc --server dc01

Required arguments:
  service                   STRING     Name of the service to stop.

Optional arguments:
  --server server           STRING     Hostname or IP address of the target system (default: local computer).
```

### schtasks-create
Create a scheduled task on the target system using an XML task definition.

```
Usage  : schtasks-create <task> <xml> [--user-mode <mode>] [--user <user>] [--password <password>] [--update] [--server <server>]
Example: schtasks-create "\MyTasks\TestTask" /local/path/to/task.xml --user-mode SYSTEM --update

Required arguments:
  task                      STRING     Path for the scheduled task to create.
  xml                       FILE       File containing the XML task definition.
                                       Export from existing task: schtasks /query /tn "\Task" /xml > task.xml

Optional arguments:
  --user-mode mode          STRING     User context for the task (default: USER).
                                         - USER:     current user context
                                         - XML:      user from XML task definition
                                         - SYSTEM:   local system service
                                         - PASSWORD: credentials via --user and --password
  --user user               STRING     Username the task will run as (default: current user).
  --password password       STRING     Password of the user the task will run as (default: current user).
  --update                  BOOL       Update the task if it already exists.
  --server server           STRING     Hostname or IP address of the target system (default: local computer).
```

### schtasks-delete
Delete a scheduled task or task folder on the target system. Exactly one of `--task` or `--folder` must be specified.

```
Usage  : schtasks-delete [--task <task>] [--folder <folder>] [--server <server>]
Example: schtasks-delete --folder \MyTasks

Optional arguments:
  --task task               STRING     Path of the scheduled task to delete.
  --folder folder           STRING     Path of the folder to delete (must be empty).
  --server server           STRING     Hostname or IP address of the target system (default: local computer).
```

### schtasks-start
Run a scheduled task on the target system.

```
Usage  : schtasks-start <task> [--server <server>]
Example: schtasks-start \MyTasks\ConquestTask

Required arguments:
  task                      STRING     Path of the scheduled task to run.

Optional arguments:
  --server server           STRING     Hostname or IP address of the target system (default: local computer).
```

### schtasks-stop
Stop a running scheduled task on the target system.

```
Usage  : schtasks-stop <task> [--server <server>]
Example: schtasks-stop \MyTasks\ConquestTask

Required arguments:
  task                      STRING     Path of the scheduled task to stop.

Optional arguments:
  --server server           STRING     Hostname or IP address of the target system (default: local computer).
```

### shutdown
Shutdown or reboot a target system. The `--confirm` flag is required as a safety net to prevent accidental execution.

```
Usage  : shutdown [target] [--message <message>] [--in <seconds>] [--close-apps] [--reboot] [--confirm]
Example: shutdown --message "Goodbye from Conquest" --in 20 --reboot --confirm

Optional arguments:
  target                    STRING     Target system (default: local computer).
  --message message         STRING     Message to display before shutdown (default: none).
  --in seconds              INT        Seconds before shutdown/reboot (default: 0).
  --close-apps              BOOL       Close all running applications without saving.
  --reboot                  BOOL       Reboot system after shutdown.
  --confirm                 BOOL       Confirm shutdown. Required to proceed.
```