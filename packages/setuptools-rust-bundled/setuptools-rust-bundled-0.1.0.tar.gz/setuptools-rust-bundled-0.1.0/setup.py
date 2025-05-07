import sysconfig
import setuptools
try:
    from setuptools.command.bdist_wheel import bdist_wheel as _bdist_wheel
except ModuleNotFoundError:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

from distutils.command.install_data import install_data as _install_data

plat_name = None


class bdist_wheel(_bdist_wheel):
    def run(self):
        global plat_name
        # self.root_is_pure = False
        self.python_tag = "py3"
        if not self.plat_name_supplied or not self.plat_name:
            self.plat_name = sysconfig.get_platform()
        plat_name = self.plat_name
        _bdist_wheel.run(self)


class install_data(_install_data):
    def run(self):
        global plat_name
        import os
        import platform
        import subprocess
        import hashlib
        import tarfile
        import tomli
        from pathlib import Path
        import requests
        import re
        from typing import Tuple, List


        def parse_platform_tag(tag: str) -> Tuple[str, str, str]:
            # match = re.match(r"([a-zA-Z]+)(?:_([0-9_]+))?_([a-zA-Z0-9]+)", tag)
            # if not match:
            #     raise RuntimeError(f"bad platform tag: '{tag}'")
            tokens = tag.split("-")
            os_name = tokens[0]
            version = "-".join(tokens[1:-1])
            arch = tokens[-1]
            return os_name, version, arch


        def gen_triple(platform_tag: str) -> List[str]:
            if platform_tag.upper() == "WIN32":
                return ["i686-pc-windows-msvc"]
            elif platform_tag.upper() == "WIN64":
                return ["x86_64-pc-windows-msvc"]
            elif platform_tag.lower() == "manylinux2014":
                return [
                    f"{a}-unknown-linux-gnu"
                    for a in ["aarch64", "x86_64", "i686", "armv7", "powerpc64", "powerpc64le", "s390x"]
                ]
            os_name, version, arch = parse_platform_tag(platform_tag)
            os_name = os_name.lower()
            arch = arch.lower()
            if os_name == "win":
                os_name = "windows"
            if arch == "arm64":
                arch = "aarch64"
            if arch == "ppc":
                arch = "powerpc"
            if arch == "ppc64":
                arch = "powerpc64"
            if arch == "ppc64le":
                arch = "powerpc64le"
            if arch == "amd64":
                arch = "x86_64"
            if arch == "armv7l":
                # 'l' means little endian, that is default.
                arch = "armv7"
            if arch == "riscv64":
                arch = "riscv64gc"
            if os_name == "manylinux":
                if version:
                    major, minor = version.split("_")
                    if int(major) < 2 or (int(major) == 2 and int(minor) < 17):
                        raise RuntimeError(f"Glibc version {major}.{minor} is not supported ({platform_tag=})")
                return [f"{arch}-unknown-linux-gnu{arch == 'armv7' and 'eabihf' or ''}"]

            if os_name == "musllinux":
                if version:
                    major, minor = version.split("_")
                    if int(major) == 1 and int(minor) < 2:
                        raise RuntimeError(f"Musl version {major}.{minor} is not supported ({platform_tag=})")
                return [f"{arch}-unknown-linux-musl{arch == 'armv7' and 'eabi' or ''}"]
            if os_name == "windows":
                return [f"{arch}-pc-windows-msvc"]
            if os_name == "macosx":
                arch_list = [arch]
                if arch == "universal2":
                    arch_list = ["aarch64", "x86_64"]
                elif arch == "universal":
                    arch_list = ["i386", "x86_64", "powerpc", "powerpc64"]
                elif arch == "intel":
                    arch_list = ["i386", "x86_64"]
                elif arch == "fat":
                    arch_list = ["i386", "powerpc"]
                elif arch == "fat3":
                    arch_list = ["i386", "powerpc", "x86_64"]
                elif arch == "fat64":
                    arch_list = ["powerpc64", "x86_64"]
                return [f"{a}-apple-darwin" for a in arch_list]
            # openbsd, freebsd, netbsd
            return [f"{arch}-unknown-{os_name}{os_name == 'linux' and '-gnu' or ''}"]


        def build_data_files(plat_name: str) -> List[tuple[str, List[str]]]:
            data_files = []
            print(f"📦 setup hook: plat_name = {plat_name}")
            host_triples = gen_triple(plat_name)
            print(f"Host triples = {host_triples}")

            # Load manifest
            script_dir = Path(__file__).resolve().parent
            manifest_file = script_dir / "channel-rust-stable.toml"
            print(f"Loading manifest {manifest_file}...")
            with open(manifest_file, "rb") as f:
                manifest_data = tomli.load(f)

            dest_dir = script_dir / "data"
            dest_dir.mkdir(exist_ok=True)
            temp_dir = script_dir / "temp"
            temp_dir.mkdir(exist_ok=True)

            profile = "minimal"
            profile_pkgs = manifest_data["profiles"][profile]

            for pkg in profile_pkgs:
                for host_triple in host_triples:
                    dest_dir_host = dest_dir / host_triple
                    dest_dir_host.mkdir(exist_ok=True)

                    record_pkg = manifest_data["pkg"][pkg]["target"]
                    if not host_triple in record_pkg:
                        if pkg == "rust-mingw":
                            continue
                        else:
                            raise RuntimeError(f"cannot find pkg.{pkg}.target.{host_triple} in {manifest_file}")
                    record = record_pkg[host_triple]
                    if not record["available"]:
                        raise RuntimeError(f"not available: pkg.{pkg}.target.{host_triple}")

                    fname = record["url"].split("/")[-1]
                    extracted_path = temp_dir / f"{fname.replace('.tar.gz', '')}"
                    if not extracted_path.is_dir():
                        archive_path = temp_dir / fname
                        if not archive_path.is_file():
                            print(f"Downloading {record['url']}")
                            response = requests.get(record['url'])
                            response.raise_for_status()
                            archive_path.write_bytes(response.content)
                        print(f"Checking sha256sum")
                        sha256 = hashlib.sha256()
                        with open(archive_path, "rb") as f:
                            for chunk in iter(lambda: f.read(8192), b""):
                                sha256.update(chunk)
                        if sha256.hexdigest() != record["hash"]:
                            raise RuntimeError(f"sha256sum mismatch for {archive_path}")
                        print(f"Extracting {archive_path}")
                        with tarfile.open(archive_path, "r:gz") as tar:
                            tar.extractall(path=temp_dir)
                        print("Finished extracting")

                    script_file = extracted_path / "install.sh"
                    args = ["bash", str(script_file), f"--prefix={str(dest_dir_host)}"]
                    if platform.system() == "Linux":
                        args.append("--disable-ldconfig")
                    print(f"Executing {args}")
                    subprocess.run(args)
                    print("Finished executing")
                    for file in dest_dir_host.glob("**/*"):
                        if file.is_file():
                            relpath = file.parent.relative_to(script_dir)
                            data_files.append(("setuptools_rust_bundled" / relpath, [str(file)]))
            return data_files

        self.data_files = build_data_files(plat_name)
        print(f"📦 install finished: data_files = {self.data_files}")
        return _install_data.run(self)


setuptools.setup(
    data_files=[("data", [])],  # dummy
    cmdclass={
        'bdist_wheel': bdist_wheel,
        "install_data": install_data,
    },
)
