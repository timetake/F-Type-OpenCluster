"""Package an OpenCluster page config for the project's native renderer."""

import argparse
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from zipfile import ZipFile, ZipInfo


def build(config, output, renderer):
    if config.resolve() == output.resolve():
        raise ValueError("the config and output must be different files")
    entry = ZipInfo("OPENCLUSTER/PAGE.CFG", (1980, 1, 1, 0, 0, 0))
    entry.create_system = 3
    entry.external_attr = 0o100644 << 16
    with TemporaryDirectory(dir=output.parent) as folder:
        snapshot = Path(folder) / "PAGE.CFG"
        contents = config.read_bytes().replace(b"\r\n", b"\n")
        snapshot.write_bytes(contents)
        subprocess.run([renderer, "--check", snapshot], check=True)
        package = Path(folder) / "page.zip"
        with ZipFile(package, "w") as archive:
            archive.writestr(entry, contents)
        package.replace(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--renderer", type=Path, required=True, help="compiled render_page host")
    args = parser.parse_args()
    build(args.config, args.output, args.renderer.resolve())
