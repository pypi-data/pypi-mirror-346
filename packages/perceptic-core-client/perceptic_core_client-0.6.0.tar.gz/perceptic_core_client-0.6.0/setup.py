import os
import subprocess
import sys
from pathlib import Path

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from setuptools.command.egg_info import egg_info
from setuptools.command.sdist import sdist

# --- Configuration ---
PROJECT_ROOT = Path(__file__).parent.resolve()
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "generate_client.py"
SPEC_ENV_VAR = "OPENAPI_SPEC_PATH"
VERSION_ENV_VAR = "PACKAGE_VERSION"
DEFAULT_SPEC_PATH = "specs/openapi.yaml"
DEFAULT_VERSION = "0.0.0.dev0"
# ---

def run_generation_script():
    """Runs the client generation script, getting config from env vars."""
    spec_path = Path(os.environ.get(SPEC_ENV_VAR, DEFAULT_SPEC_PATH)).resolve()
    version = os.environ.get(VERSION_ENV_VAR, DEFAULT_VERSION)

    print("--- Running Pre-Build Client Generation ---", flush=True)
    print(f"Using Spec Path: {spec_path} (Source: {'Env Var' if SPEC_ENV_VAR in os.environ else 'Default'})")
    print(f"Using Version:   {version} (Source: {'Env Var' if VERSION_ENV_VAR in os.environ else 'Default'})")

    if not SCRIPT_PATH.is_file():
        print(f"Error: Generation script not found at {SCRIPT_PATH}", file=sys.stderr, flush=True)
        sys.exit(1)

    if not spec_path.is_file() and SPEC_ENV_VAR not in os.environ:
         # Only error if the *default* path doesn't exist AND the env var wasn't set
         # If env var *was* set but file doesn't exist, generate_client.py will error out
        print(f"Warning: Default spec file '{DEFAULT_SPEC_PATH}' not found and '{SPEC_ENV_VAR}' env var not set.", file=sys.stderr, flush=True)
        print("Attempting build without generation. This might fail or use stale code.", file=sys.stderr, flush=True)
        # Decide if you want to fail hard here instead:
        # sys.exit(1)
        return # Allow build to proceed, potentially failing later or using old code

    if not spec_path.is_file() and SPEC_ENV_VAR in os.environ:
         print(f"Warning: Spec file specified via {SPEC_ENV_VAR} ('{spec_path}') not found.", file=sys.stderr, flush=True)
         print("Attempting build without generation. This might fail or use stale code.", file=sys.stderr, flush=True)
         # Decide if you want to fail hard here instead:
         # sys.exit(1)
         return # Allow build to proceed, potentially failing later or using old code


    command = [
        sys.executable, # Use the same python interpreter that's running setup.py
        str(SCRIPT_PATH),
        "--spec-path", str(spec_path),
        "--version", version
    ]

    try:
        print(f"Executing: {' '.join(command)}", flush=True)
        # Use check=True to raise CalledProcessError on failure
        subprocess.run(command, check=True, text=True) #, capture_output=True) # capture can hide useful interactive output/errors
        print("--- Client Generation Script Finished Successfully ---", flush=True)
    except subprocess.CalledProcessError as e:
        print("\n--- Client Generation Script Failed ---", file=sys.stderr, flush=True)
        print(f"Command failed with exit code {e.returncode}", file=sys.stderr, flush=True)
        # print("STDOUT:", file=sys.stderr, flush=True)
        # print(e.stdout, file=sys.stderr, flush=True) # Often empty if text=True not fully compatible or error happens early
        # print("STDERR:", file=sys.stderr, flush=True)
        # print(e.stderr, file=sys.stderr, flush=True) # stderr might have more info
        sys.exit(1) # Exit the build process if generation fails
    except FileNotFoundError:
         print(f"Error: Could not execute Python interpreter at '{sys.executable}' or script at '{SCRIPT_PATH}'.", file=sys.stderr, flush=True)
         sys.exit(1)


# Custom command classes to ensure generation runs before standard commands
class CustomBuildPy(build_py):
    def run(self):
        run_generation_script()
        super().run()

class CustomEggInfo(egg_info):
    def run(self):
        run_generation_script()
        super().run()

class CustomSdist(sdist):
     def run(self):
        run_generation_script()
        super().run()

setup(
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    cmdclass={
        'build_py': CustomBuildPy,
        'egg_info': CustomEggInfo,
        'sdist': CustomSdist,
    },
    include_package_data=True,
    package_data={
        "perceptic_core_client": ["**/*"],
    },
)