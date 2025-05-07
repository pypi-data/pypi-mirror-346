import subprocess
from pathlib import Path
from hatchling.builders.hooks.plugin.interface import BuildHookInterface

PACKAGE_NAME = "compas_lcmtypes"

class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        """Initialize the build hook by generating Python code from LCM files."""
        # Check if we're doing a pure Python build, and skip generation if so
        if build_data.get("pure_python", False):
            return

        # Get the root directory of the project
        root_dir = Path(self.root)

        # Find all .lcm files in the root directory
        lcm_files = list(root_dir.glob("*.lcm"))

        # Run lcm-gen for Python on all LCM files
        lcm_gen_cmd = [
            "lcm-gen",
            "--python",
            "--package-prefix", PACKAGE_NAME,
            *[str(f) for f in lcm_files]
        ]

        self.app.display_info(f"Running: {' '.join(lcm_gen_cmd)}")
        try:
            subprocess.run(
                lcm_gen_cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.app.display_success("Successfully generated Python code from LCM files")
        except subprocess.CalledProcessError as e:
            self.app.display_error(f"Error running lcm-gen: {e}")
            self.app.display_error(f"stdout: {e.stdout.decode() if e.stdout else ''}")
            self.app.display_error(f"stderr: {e.stderr.decode() if e.stderr else ''}")
            raise