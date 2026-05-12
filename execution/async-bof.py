import conquest 
import os.path

ASYNC_DLL = conquest.resources_root() + "/async-bof-loader/dist/async-bof.dll"
EXPORT_FUNC = "Run"

# Only register async commands if the DLL exists
if not os.path.exists(ASYNC_DLL):
    raise FileNotFoundError(f"Async BOF DLL not found: {ASYNC_DLL}")

cmd_bofAsync = (
    conquest.createCommand(name="bof-async", description="Execute an object file asynchronously in the background.", example="bof-async /path/to/process-notify.x64.o <packed-args>",
                            message="Tasked agent to execute an object file asynchronously.", mitre=["T1055", "T1620"])
            .addArgFile("object-file", "Path to the object file to execute.", True)
            .addArgString("arguments", "Arguments to be passed to the object file, packed as a HEX string according to beacon_generate.py.")
            .setHandler(lambda agentId, cmdline, args: (
                bof := conquest.get_file(args, 0)[1],
                args := conquest.get_string(args, 1),
                conquest.execute_alias(agentId, cmdline, f"dll {ASYNC_DLL} {EXPORT_FUNC} {conquest.async_bof_pack(bof, args)}")
            ))
).registerToGroup("execution")
