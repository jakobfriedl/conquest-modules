import conquest
import os.path

cmd_bofAsync = (
    conquest.createCommand(name="bof-async", description="Execute an object file asynchronously in the background.", example="bof-async /path/to/process-notify.x64.o <packed-args>",
                            message="Tasked agent to execute an object file asynchronously.", mitre=["T1055", "T1620"])
            .addArgString("object-file", "Path to the object file to execute.", True)
            .addArgString("arguments", "Arguments to be passed to the object file, packed as a HEX string according to beacon_generate.py.")
            .setHandler(lambda agentId, cmdline, args: (
                bof := conquest.get_string(args, 0),
                args := conquest.get_string(args, 1),
                
                dll := conquest.resources_root() + f"/async-bof-loader/dist/async-bof.{conquest.arch(agentId)}.dll",
                conquest.execute_alias(agentId, cmdline, f"dll {dll} Run {conquest.async_bof_pack(bof, args)}") if os.path.exists(bof) and os.path.exists(dll)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline) if not os.path.exists(bof)
                else conquest.error(agentId, f"Async BOF DLL not found: {dll}", cmdline)
            ))
).registerToGroup("execution")
