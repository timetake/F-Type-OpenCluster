import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from zipfile import ZipFile

from tools.build_page import build


ROOT = Path(__file__).resolve().parents[1]
PPM_HEADER = b"P6\n400 224\n255\n"


class UsbPageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cc = os.environ.get("CC") or shutil.which("cc") or shutil.which("gcc")
        if not cc:
            raise unittest.SkipTest("set CC to a C99 compiler to run native page tests")
        cls.workspace = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.workspace.cleanup)
        name = "render_page.exe" if os.name == "nt" else "render_page"
        cls.host = Path(cls.workspace.name) / name
        subprocess.run([cc, "-std=c99", "-Wall", "-Wextra", "-Werror",
                        ROOT / "page/page.c", ROOT / "tools/render_page.c", "-o", cls.host],
                       check=True)

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.config = self.root / "OPENCLUSTER/PAGE.CFG"

    def render(self, *readings):
        frame = self.root / "frame.ppm"
        subprocess.run([self.host, self.root, frame, *readings], check=True)
        data = frame.read_bytes()
        self.assertTrue(data.startswith(PPM_HEADER))
        pixels = data[len(PPM_HEADER):]
        self.assertEqual(len(pixels), 400 * 224 * 3)
        return pixels

    @staticmethod
    def pixel(pixels, x, y):
        i = (y * 400 + x) * 3
        return pixels[i:i + 3].hex().upper()

    def test_distributed_pages_load_and_select_the_correct_readings(self):
        for theme, accent in (("road", "61D4BE"), ("sport", "FF9858")):
            archive = ROOT / "packages" / (theme + "-page.zip")
            rebuilt = self.root / "rebuilt.zip"
            build(ROOT / "pages" / (theme + ".cfg"), rebuilt, self.host)
            self.assertEqual(rebuilt.read_bytes(), archive.read_bytes())
            with ZipFile(archive) as package:
                self.assertEqual(package.namelist(), ["OPENCLUSTER/PAGE.CFG"])
                package.extractall(self.root)
            pixels = self.render()
            self.assertEqual(self.pixel(pixels, 15, 45), accent)
            if theme == "road":
                self.assertEqual(self.pixel(pixels, 204, 56), accent)
                self.assertEqual(self.render("rpm=3200"), pixels)
                self.assertNotEqual(self.render("oil_f=210"), pixels)
            else:
                self.assertEqual(self.pixel(pixels, 12, 138), accent)
                self.assertEqual(self.render("oil_f=210"), pixels)
                self.assertNotEqual(self.render("rpm=3200"), pixels)

    def test_edited_title_changes_only_the_header(self):
        self.config.parent.mkdir()
        source = (ROOT / "pages/road.cfg").read_text()
        self.config.write_text(source)
        a = self.render("oil_f=-15")
        self.config.write_text(source.replace("title=ROAD", "title=F-TYPE S"))
        b = self.render("oil_f=-15")
        boundary = 400 * 44 * 3
        self.assertNotEqual(a[:boundary], b[:boundary])
        self.assertEqual(a[boundary:], b[boundary:])

    def test_invalid_rebuild_preserves_last_package(self):
        cfg = self.root / "source.cfg"
        package = self.root / "page.zip"
        source = (ROOT / "pages/road.cfg").read_bytes()
        cfg.write_bytes(source)
        build(cfg, package, self.host)
        good = package.read_bytes()
        for bad in (source + b"\ntitle=DUPLICATE", source.replace(b"oil_f", b"unknown"),
                    source.replace(b"61D4BE", b"FFFFX0"), source + b"\x00",
                    b"title=ROAD\n", b"X" * 513):
            cfg.write_bytes(bad)
            with self.assertRaises(subprocess.CalledProcessError):
                build(cfg, package, self.host)
            self.assertEqual(package.read_bytes(), good)
