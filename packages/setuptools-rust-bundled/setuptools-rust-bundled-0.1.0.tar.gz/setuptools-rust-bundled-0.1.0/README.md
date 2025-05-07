# setuptools-rust-bundled ![rustc] ![cargo] [![Packaging and test]][Packaging and test url] [![PyPI]][PyPI url]

[rustc]: https://img.shields.io/badge/rustc-1.86-green.svg
[cargo]: https://img.shields.io/badge/cargo-0.87-green.svg
[Packaging and test]: https://github.com/QunaSys/setuptools-rust-bundled/actions/workflows/package.yml/badge.svg
[Packaging and test url]: https://github.com/QunaSys/setuptools-rust-bundled/actions/workflows/package.yml
[PyPI]: https://img.shields.io/pypi/pyversions/setuptools-rust-bundled
[PyPI url]: https://pypi.org/project/setuptools-rust-bundled/

A zero-setup build helper that lets you ship Python wheels or source distributions backed by Rust—even on machines that have no Rust tool-chain installed.
It transparently wraps either setuptools-rust or maturin, downloading rustc, cargo, and the target standard libraries on-demand so the underlying backend “just works”.

## ✨ Key features

- The wheel packages of setuptools-rust-bundled are shipped with toolchain binaries, so you can skip downloading or installing toolchain in build process.
- setuptools-rust-bundled provides sdist, and wheels for many underlying environments, so you can support many systems just using this library.


## 😊 Distribution

- sdist package is distributed via [PyPI](https://pypi.org/project/setuptools-rust-bundled/).
- wheel packages are available at [releases page](https://github.com/QunaSys/setuptools-rust-bundled/releases/)

## 🚀 Quick start
Below are minimal pyproject.toml snippets for the two supported backends.

### 1. using setuptools-rust (recommended)

```pyproject.toml
[build-system]
requires = ["setuptools>=64", "setuptools-rust", "setuptools-rust-bundled"]
build-backend = "setuptools_rust_bundled.setuptools"

[project]
name = "example"
version = "0.1.0"

[[tool.setuptools-rust.ext-modules]]
target = "example.example"

[tool.setuptools.packages]
find = { where = ["."] }
```

### 2. using maturin

> Because maturin itself is written in Rust, it cannot run on systems where the Rust toolchain is not installed and a pre-built maturin wheel is unavailable.

```pyproject.toml
[build-system]
requires = ["setuptools-rust-bundled", "maturin>=1.0,<2.0"]
build-backend = "setuptools_rust_bundled.maturin"

[project]
name = "example"
version = "0.1.0"

[tool.maturin]
python-source = "."
module-name = "example.example"
```

## 📝 Developing setuptools-rust-bundled

### Build setuptools-rust-bundled

Use these commands to build development version of setuptools-rust-bundled:

```shell
# Build sdist in `dist/`
python setup.py sdist
# Build wheel in `dist/`
python setup.py bdist_wheel -p <platform>
```

### Build example packages with setuptools-rust-bundled

```shell
# Install dependencies for setuptools-rust-bundled
pip install setuptools wheel requests tomli
# Install setuptools-rust-bundled from source
pip install .
# Or install from package
pip install dist/*
# Install examples
cd examples/setuptools
pip install --no-build-isolation -v .
```

# 🛠️ Available toolchain

| Tool     | Version |
|----------|----------|
| rustc    | 1.86.0   |
| cargo    | 0.87.0   |
| rust-std    | 1.86.0   |

# 💻 Supported systems

| Python platform tag | Rust platform tag | sdist install tested | maturin supported | setuptools supported |
|------|------|-----|-----|-----|
| manylinux_2_17_i686    | i686-unknown-linux-gnu | | | YES |
| manylinux_2_17_x86_64  | x86_64-unknown-linux-gnu | YES | YES | YES |
| manylinux_2_17_aarch64 | aarch64-unknown-linux-gnu | YES | YES | YES |
| manylinux_2_17_riscv64 | aarch64-unknown-linux-gnu | | | YES |
| manylinux_2_17_armv7l  | armv7-unknown-linux-gnueabihf | | | YES |
| manylinux_2_17_ppc64le | powerpc64le-unknown-linux-gnu | | | YES |
| manylinux_2_17_s390x   | s390x-unknown-linux-gnu | | | YES |
| win_amd64 | x86_64-pc-windows-msvc | YES | YES | YES |
| win_arm64 | aarch64-pc-windows-msvc | YES | YES | YES |
| macosx_11_0_arm64 | aarch64-apple-darwin | YES | YES | YES |
| macosx_10_12_x86_64 | x86_64-apple-darwin | YES | YES | YES |
| freebsd_14_2_release_amd64 | x86_64-unknown-freebsd | | | YES |
| netbsd_10_1_amd64 | x86_64-unknown-netbsd | | | YES |

# 📒 Notes

## For FreeBSD

This library supports freebsd_12_0_release or upper. Rename the distributed wheel package of setuptools-rust-bundled to the system's correct version.

## For NetBSD

This library supports netbsd_9_0 or upper. Rename the distributed wheel package of setuptools-rust-bundled to the system's correct version.
