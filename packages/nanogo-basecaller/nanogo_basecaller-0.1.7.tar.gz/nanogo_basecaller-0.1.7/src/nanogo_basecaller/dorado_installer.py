#!/usr/bin/env python3
"""
Dorado Installer for NanoGO Basecaller

This script handles downloading and installing the latest version of Oxford Nanopore's
Dorado basecaller tool. It can be run as a standalone script after package installation.
"""

import os
import sys
import hashlib
import tarfile
import urllib.request
import shutil
import tempfile
import re
import subprocess
import platform
import argparse

# Fallback version info if we can't fetch the latest
FALLBACK_DORADO_URL = (
    "https://cdn.oxfordnanoportal.com/software/analysis/dorado-0.9.2-linux-x64.tar.gz"
)
FALLBACK_DORADO_SHA256 = (
    "ddb125dc562cb3fb8ed9fe63ff0958def5dfb567270bd421b5662d8cddfc7ad1"
)

# Known stable version to try as another fallback
STABLE_DORADO_VERSION = "0.9.2"


def get_install_dirs(user_install=False):
    """
    Determine the appropriate directories for installing Dorado.
    Returns a tuple of (bin_dir, lib_dir, can_write)
    """
    # Try to determine if this is a user install or not
    venv_path = os.environ.get("VIRTUAL_ENV")

    # If in a virtual environment, install there
    if venv_path:
        bin_dir = os.path.join(venv_path, "bin")
        lib_dir = os.path.join(venv_path, "lib")
        print(f"Installing Dorado to virtual environment: {venv_path}")
        return bin_dir, lib_dir, True

    # If user install, use user's local bin directory
    if user_install:
        import site

        user_base = site.USER_BASE
        bin_dir = os.path.join(user_base, "bin")
        lib_dir = os.path.join(user_base, "lib")
        # Create the directories if they don't exist
        os.makedirs(bin_dir, exist_ok=True)
        os.makedirs(lib_dir, exist_ok=True)
        print(f"Installing Dorado to user directories: {bin_dir} and {lib_dir}")
        return bin_dir, lib_dir, True

    # For system installs, check if we have write permission to sys.prefix
    bin_dir = os.path.join(sys.prefix, "bin")
    lib_dir = os.path.join(sys.prefix, "lib")

    # Check if we have write permission
    can_write = os.access(os.path.dirname(bin_dir), os.W_OK) and os.access(
        os.path.dirname(lib_dir), os.W_OK
    )

    if not can_write:
        print(f"Warning: No write permission to {bin_dir} and {lib_dir}.")
        print("Consider using --user flag or a virtual environment.")

    return bin_dir, lib_dir, can_write


def check_version_exists(version):
    """
    Check if a specific Dorado version exists by sending a HEAD request.

    Args:
        version: Version string to check (e.g., "0.9.5")

    Returns:
        Tuple of (exists, url) where exists is a boolean and url is the download URL
    """
    url = f"https://cdn.oxfordnanoportal.com/software/analysis/dorado-{version}-linux-x64.tar.gz"
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status == 200, url
    except Exception:
        return False, url


def get_known_working_versions():
    """Return a list of known working Dorado versions to try."""
    # List of versions that have been confirmed to work
    # (in order from newest to oldest)
    return ["0.9.6", "0.9.5", "0.9.2", "0.9.1", "0.9.0"]


def get_latest_dorado_version():
    """
    Check ONT's CDN for the latest version of Dorado.
    First tries to parse the index page, then falls back to checking specific versions.
    Returns a tuple of (version, url, sha256) or None if unable to determine.
    """
    print("Checking for available Dorado versions...")
    base_url = "https://cdn.oxfordnanoportal.com/software/analysis/"

    # First approach: Try to parse the index page for all versions
    try:
        print("Trying to parse the ONT CDN index page...")
        with urllib.request.urlopen(base_url, timeout=10) as response:
            html = response.read().decode("utf-8")

            # Look for dorado release tarballs in the HTML
            pattern = r'href="(dorado-(\d+\.\d+\.\d+)-linux-x64\.tar\.gz)"'
            matches = re.findall(pattern, html)

            if matches:
                # Sort by version number to find the latest
                sorted_versions = sorted(
                    matches,
                    key=lambda x: [int(n) for n in x[1].split(".")],
                    reverse=True,
                )

                # Try each version from newest to oldest
                for match in sorted_versions:
                    filename = match[0]
                    version = match[1]
                    version_url = f"{base_url}{filename}"

                    # Check if this specific version exists
                    exists, _ = check_version_exists(version)
                    if exists:
                        print(f"Found available Dorado version: {version}")
                        # Try to get the SHA256 hash
                        try:
                            hash_url = f"{version_url}.sha256"
                            with urllib.request.urlopen(
                                hash_url, timeout=5
                            ) as hash_response:
                                sha256 = (
                                    hash_response.read()
                                    .decode("utf-8")
                                    .strip()
                                    .split()[0]
                                )
                                return (version, version_url, sha256)
                        except Exception:
                            print(
                                f"SHA256 file not found for {filename}. Will verify after download."
                            )
                            return (version, version_url, None)
                    else:
                        print(
                            f"Version {version} is not accessible. Trying next version..."
                        )

    except Exception as e:
        print(f"Error parsing ONT CDN index: {e}")

    # Second approach: Try specific versions directly (newest to oldest)
    print("Trying specific Dorado versions directly...")

    # First try newer major versions that might exist
    versions_to_try = [
        "1.0.0",
        "0.9.9",
        "0.9.8",
        "0.9.7",
    ] + get_known_working_versions()

    for version in versions_to_try:
        print(f"Checking if Dorado version {version} is available...")
        exists, url = check_version_exists(version)

        if exists:
            print(f"Found available Dorado version: {version}")
            # Try to get the SHA256 hash
            try:
                hash_url = f"{url}.sha256"
                with urllib.request.urlopen(hash_url, timeout=5) as hash_response:
                    sha256 = hash_response.read().decode("utf-8").strip().split()[0]
                    return (version, url, sha256)
            except Exception:
                print(
                    f"SHA256 file not found for version {version}. Will verify after download."
                )
                return (version, url, None)

    print("Could not find any accessible Dorado versions.")
    return None


def is_dorado_installed(bin_dir):
    """
    Check if Dorado is already installed and working.

    Args:
        bin_dir: Directory where the dorado executable should be located

    Returns:
        Boolean indicating if Dorado is properly installed and working
    """
    dorado_bin = os.path.join(bin_dir, "dorado")

    # Check if the executable exists
    if not os.path.exists(dorado_bin):
        print(f"Dorado executable not found at {dorado_bin}")
        return False

    # Check if it's executable
    if not os.access(dorado_bin, os.X_OK):
        print(f"Dorado exists but is not executable at {dorado_bin}")
        return False

    # Try to run a basic command to verify it works
    try:
        result = subprocess.run(
            [dorado_bin, "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
            text=True,
        )
        if result.returncode == 0:
            version = result.stdout.strip() or result.stderr.strip()
            print(f"Dorado is already installed: {version}")
            return True
        else:
            print(f"Dorado found but failed to run: {result.stderr.strip()}")
            return False
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        print(f"Error verifying Dorado: {e}")
        return False


def calculate_sha256(file_path):
    """Calculate SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def make_backup(bin_dir, lib_dir):
    """
    Create a backup of the existing Dorado installation.

    Args:
        bin_dir: Directory containing the Dorado executable
        lib_dir: Directory containing Dorado libraries

    Returns:
        Path to the backup directory, or None if no backup was created
    """
    dorado_bin = os.path.join(bin_dir, "dorado")
    if not os.path.exists(dorado_bin):
        return None  # Nothing to back up

    try:
        # Create a backup directory
        backup_dir = tempfile.mkdtemp()
        backup_bin = os.path.join(backup_dir, "bin")
        backup_lib = os.path.join(backup_dir, "lib")
        os.makedirs(backup_bin, exist_ok=True)
        os.makedirs(backup_lib, exist_ok=True)

        # Copy the current dorado executable
        shutil.copy2(dorado_bin, os.path.join(backup_bin, "dorado"))

        # Copy lib files if they exist
        dorado_libs = [
            "libdorado_torch_lib.so",
            "libdorado_cudnn_lib.so",
            # Add more library files if needed
        ]

        for lib_name in dorado_libs:
            lib_path = os.path.join(lib_dir, lib_name)
            if os.path.exists(lib_path):
                shutil.copy2(lib_path, os.path.join(backup_lib, lib_name))

        print("Created backup of existing Dorado installation.")
        return backup_dir

    except Exception as e:
        print(f"Warning: Could not create backup of existing Dorado: {e}")
        return None


def restore_backup(backup_dir, bin_dir, lib_dir):
    """
    Restore the backed up Dorado installation.

    Args:
        backup_dir: Directory containing the backup
        bin_dir: Target bin directory to restore to
        lib_dir: Target lib directory to restore to

    Returns:
        Boolean indicating if the restore was successful
    """
    if not backup_dir or not os.path.exists(backup_dir):
        print("No backup available to restore.")
        return False

    try:
        print("Restoring previous Dorado installation...")
        backup_bin = os.path.join(backup_dir, "bin")
        backup_lib = os.path.join(backup_dir, "lib")

        if not os.path.exists(backup_bin):
            print(f"Backup bin directory not found at {backup_bin}")
            return False

        # Restore bin files
        for filename in os.listdir(backup_bin):
            src = os.path.join(backup_bin, filename)
            dst = os.path.join(bin_dir, filename)
            if os.path.exists(dst):
                os.remove(dst)
            shutil.copy2(src, dst)
            os.chmod(dst, 0o755)  # Make executable

        # Restore lib files
        if os.path.exists(backup_lib):
            for filename in os.listdir(backup_lib):
                src = os.path.join(backup_lib, filename)
                dst = os.path.join(lib_dir, filename)
                if os.path.exists(dst):
                    if os.path.isdir(dst):
                        shutil.rmtree(dst)
                    else:
                        os.remove(dst)
                shutil.copy2(src, dst)

        print("Previous Dorado installation restored.")
        return True

    except Exception as e:
        print(f"Error restoring previous Dorado installation: {e}")
        return False


def try_install_version(version, url, sha256, bin_dir, lib_dir):
    """
    Attempt to install a specific version of Dorado.

    Args:
        version: The version string
        url: URL to download from
        sha256: Expected SHA256 hash (can be None)
        bin_dir: Target bin directory
        lib_dir: Target lib directory

    Returns:
        True if installation and verification succeeded, False otherwise
    """
    # Create a temporary directory for download and extraction
    tmp_dir = tempfile.mkdtemp()
    tarball_path = os.path.join(tmp_dir, "dorado.tar.gz")

    try:
        # Download Dorado
        print(f"Downloading Dorado {version} from {url}...")
        try:
            urllib.request.urlretrieve(url, tarball_path)
        except urllib.error.HTTPError as e:
            print(f"Error downloading Dorado {version}: {e}")
            if e.code == 403:
                print(
                    f"Access forbidden (403) for version {version}. This version may be unavailable."
                )
            return False
        except Exception as e:
            print(f"Error downloading Dorado {version}: {e}")
            return False

        # Verify download
        print("Verifying download...")
        if sha256:
            # Verify against provided hash
            calculated_hash = calculate_sha256(tarball_path)
            if calculated_hash != sha256:
                print(f"SHA256 hash verification failed for Dorado download.")
                print(f"Expected: {sha256}")
                print(f"Got: {calculated_hash}")
                return False
            print("✓ SHA256 verified.")
        else:
            # If we don't have a hash to verify against, just log the hash we calculated
            calculated_hash = calculate_sha256(tarball_path)
            print(f"Downloaded file SHA256: {calculated_hash}")

        # Extract the archive
        print("Extracting Dorado...")
        with tarfile.open(tarball_path, "r:gz") as tar:
            tar.extractall(path=tmp_dir)

        # Find the extracted directory
        extracted_dirs = [
            d
            for d in os.listdir(tmp_dir)
            if os.path.isdir(os.path.join(tmp_dir, d)) and d.startswith("dorado-")
        ]

        if not extracted_dirs:
            print(
                f"Could not find Dorado directory in extracted contents: {os.listdir(tmp_dir)}"
            )
            return False

        # Use the first directory that matches the pattern
        extracted_dir = os.path.join(tmp_dir, extracted_dirs[0])

        extracted_bin = os.path.join(extracted_dir, "bin")
        extracted_lib = os.path.join(extracted_dir, "lib")

        # Make sure target directories exist
        os.makedirs(bin_dir, exist_ok=True)
        os.makedirs(lib_dir, exist_ok=True)

        # Move all files from the extracted bin folder
        print(f"Moving files from {extracted_bin} to {bin_dir}...")
        for filename in os.listdir(extracted_bin):
            src = os.path.join(extracted_bin, filename)
            dst = os.path.join(bin_dir, filename)
            if os.path.exists(dst):
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                else:
                    os.remove(dst)
            shutil.copy2(src, dst)  # Use copy2 to preserve permissions
            os.chmod(dst, 0o755)  # Make executable

        # Move all files from the extracted lib folder
        print(f"Moving files from {extracted_lib} to {lib_dir}...")
        for filename in os.listdir(extracted_lib):
            src = os.path.join(extracted_lib, filename)
            dst = os.path.join(lib_dir, filename)
            if os.path.exists(dst):
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                else:
                    os.remove(dst)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)  # Use copy2 to preserve permissions

        # Verify the installation
        if is_dorado_installed(bin_dir):
            print(f"✓ Dorado {version} installed successfully.")
            return True
        else:
            print("Dorado was installed but verification failed.")

            # Check common reasons for verification failure
            check_dependencies()

            return False

    except Exception as e:
        print(f"Error installing Dorado version {version}: {e}")
        return False

    finally:
        # Cleanup the temporary directory
        try:
            shutil.rmtree(tmp_dir)
        except Exception as e:
            print(f"Warning: Could not clean up temporary directory: {e}")


def check_dependencies():
    """Check for common missing dependencies and print helpful information."""
    print("\nChecking system dependencies...")

    try:
        result = subprocess.run(
            ["ldd", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode == 0:
            output = result.stdout.strip() or result.stderr.strip()
            print(f"System libc version: {output}")

            # Extract the GLIBC version
            glibc_match = re.search(r"GLIBC\s+(\d+\.\d+)", output)
            if glibc_match:
                glibc_version = glibc_match.group(1)
                print(f"Detected GLIBC version: {glibc_version}")

                # Check if the GLIBC version is too old
                if float(glibc_version) < 2.25:
                    print(
                        "\nWarning: Your system's GLIBC version may be too old for newer Dorado versions."
                    )
                    print(
                        "Consider using an older Dorado version (e.g., 0.9.2) or upgrading your system."
                    )
    except Exception:
        print("Could not determine system GLIBC version.")

    print("\nCommon issues with Dorado:")
    print("1. Missing or incompatible GLIBC version (required: 2.25+)")
    print("2. Missing or incompatible GLIBCXX version")
    print("3. Missing or incompatible libstdc++")
    print("\nPossible solutions:")
    print("- Try an older version of Dorado (e.g., 0.9.2)")
    print("- Use a container (Docker/Singularity) with a newer OS")
    print("- Use a compute environment with a newer OS")


def install_dorado(user_install=False, force=False, specific_version=None):
    """
    Install Dorado if not already installed, trying to use the latest version.

    Args:
        user_install: Whether to install to user directories
        force: Whether to force installation even if Dorado is already installed
        specific_version: Specific version to install (e.g. "0.9.2")

    Returns:
        True if installation was successful or Dorado was already installed.
    """
    # Check if platform is supported
    if platform.system() != "Linux":
        print(
            f"Dorado auto-installation is only supported on Linux, not {platform.system()}."
        )
        print("Please manually install Dorado for your platform.")
        return False

    # Determine installation directories
    bin_dir, lib_dir, can_write = get_install_dirs(user_install)

    # Check if already installed
    if is_dorado_installed(bin_dir) and not force:
        print("Dorado is already installed and working. Skipping installation.")
        print("Use --force to reinstall.")
        return True

    # If we can't write to the target directories, we can't install
    if not can_write:
        print("Cannot install Dorado due to permission issues.")
        print("Please install Dorado manually or reinstall with --user flag.")
        return False

    # Create a backup of the existing installation
    backup_dir = make_backup(bin_dir, lib_dir)

    try:
        # If a specific version is requested, try only that version
        if specific_version:
            exists, url = check_version_exists(specific_version)
            if exists:
                print(f"Using specified Dorado version: {specific_version}")
                if try_install_version(specific_version, url, None, bin_dir, lib_dir):
                    return True
                else:
                    print(f"Failed to install specified version {specific_version}.")
                    restore_backup(backup_dir, bin_dir, lib_dir)
                    return False
            else:
                print(f"Specified version {specific_version} is not available.")
                print(
                    "Please specify a different version or let the installer choose automatically."
                )
                return False

        # Get the latest available version
        version_info = get_latest_dorado_version()

        if version_info:
            version, url, sha256 = version_info
            if try_install_version(version, url, sha256, bin_dir, lib_dir):
                return True

            # If the latest version fails, try known stable versions
            print(f"Installation of Dorado {version} failed. Trying stable versions...")

            # Try some known stable versions
            for stable_version in get_known_working_versions():
                # Skip the version we just tried
                if stable_version == version:
                    continue

                exists, stable_url = check_version_exists(stable_version)
                if exists:
                    print(f"Trying stable version {stable_version}...")
                    if try_install_version(
                        stable_version, stable_url, None, bin_dir, lib_dir
                    ):
                        return True

        # If we get here, all installation attempts failed
        print("All installation attempts failed.")

        # Restore backup if available
        if backup_dir:
            if restore_backup(backup_dir, bin_dir, lib_dir):
                # Check if the restored version works
                if is_dorado_installed(bin_dir):
                    print("Restored previous Dorado installation, which is working.")
                    return True
                else:
                    print(
                        "Restored previous Dorado installation, but it's also not working."
                    )

        print("\nDorado installation failed. Consider the following:")
        print("1. Try manually downloading a specific version with --version flag")
        print("2. Check system dependencies")
        print("3. Try an older version like 0.9.2 which has fewer dependencies")
        print("4. See https://github.com/nanoporetech/dorado for manual installation")

        return False

    except Exception as e:
        print(f"Error during Dorado installation: {e}")
        restore_backup(backup_dir, bin_dir, lib_dir)
        return False

    finally:
        # Clean up backup directory if needed
        if backup_dir and os.path.exists(backup_dir):
            try:
                shutil.rmtree(backup_dir)
            except Exception:
                pass


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Install Dorado for NanoGO Basecaller")
    parser.add_argument(
        "--user",
        action="store_true",
        help="Install to user directories instead of system directories",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force installation even if Dorado is already installed",
    )
    parser.add_argument(
        "--version",
        type=str,
        help="Specify a particular Dorado version to install (e.g., 0.9.2)",
    )
    parser.add_argument(
        "--list-versions",
        action="store_true",
        help="List known working versions and exit",
    )
    args = parser.parse_args()

    # Handle listing known versions
    if args.list_versions:
        print("\n=== Known Working Dorado Versions ===\n")
        for version in get_known_working_versions():
            exists, _ = check_version_exists(version)
            status = "Available" if exists else "Not Available"
            print(f"Dorado {version} - {status}")
        return 0

    print("\n=== Dorado Installer for NanoGO Basecaller ===\n")
    success = install_dorado(
        user_install=args.user, force=args.force, specific_version=args.version
    )

    if success:
        print("\nDorado installation completed successfully.")
        print("You can now use nanogo-basecaller with Dorado support.")
    else:
        print("\nDorado installation failed.")
        print("You may need to install Dorado manually.")
        print("See https://github.com/nanoporetech/dorado for instructions.")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
