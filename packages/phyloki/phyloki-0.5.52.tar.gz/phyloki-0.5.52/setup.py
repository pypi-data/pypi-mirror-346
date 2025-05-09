import os
import stat
from setuptools import setup, find_packages
from setuptools.command.install import install

VERSION_FILE = "phyloki/version.py"


class CustomInstallCommand(install):
    """Custom installation to download scripts and set execution permissions."""

    def run(self):
        # Run standard installation
        install.run(self)

        # Define where to download the scripts
        install_dir = os.path.join(self.install_lib, "phyloki")
        os.makedirs(install_dir, exist_ok=True)

        # Ensure all local scripts in phyloki/ are executable
        self.set_executable_permissions(install_dir)

    def set_executable_permissions(self, directory):
        """Ensure all scripts in phyloki/ have execution permissions."""
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith((".py")):  # Adjust if needed
                    script_path = os.path.join(root, filename)
                    os.chmod(
                        script_path,
                        stat.S_IRUSR
                        | stat.S_IWUSR
                        | stat.S_IXUSR
                        | stat.S_IRGRP
                        | stat.S_IXGRP
                        | stat.S_IROTH
                        | stat.S_IXOTH,
                    )
                    print(f"Set executable permissions for {script_path}")


version = {}
with open(VERSION_FILE) as f:
    exec(f.read(), version)

setup(
    name="phyloki",
    version=version["__version__"],
    description="Annotate phylogenetic trees like never before",
    long_description=open("README_PyPi.md").read(),
    long_description_content_type="text/markdown",
    author="Ilia Popov",
    author_email="iljapopov17@gmail.com",
    url="https://github.com/iliapopov17/phyloki",
    packages=find_packages(),
    cmdclass={"install": CustomInstallCommand},
    entry_points={
        "console_scripts": [
            "Phyloki=phyloki:phyloki.main",  # Maps the command to the main function
        ],
    },
    install_requires=open("requirements.txt").read().splitlines(),
    python_requires=">=3.10",
)
