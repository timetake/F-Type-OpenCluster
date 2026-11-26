# F-Type-OpenCluster

The goal is to customize the factory interface of a US-market 2015 Jaguar F-TYPE S Coupé (X152) using an ordinary USB flash drive. The first vehicle milestone is an owner-authored screen element or page that can be changed in a second USB build and seen in the same place on the original center touchscreen or the five-inch instrument display.

**Vehicle status.** Original page content can now be packaged and rendered by the project's C99 code. The Jaguar-side loader, display connection, and vehicle data source are still unimplemented. The packages below contain page settings only. The [USB interface findings](docs/research.md#usb-and-the-two-original-displays) cover the factory interfaces examined so far.

## USB page content

| Package | Layout | Readings |
| --- | --- | --- |
| [Road](packages/road-page.zip) | Two side-by-side tiles | Oil temperature and coolant temperature in °F |
| [Sport](packages/sport-page.zip) | Two stacked rows | Engine RPM and throttle position in percent |

Each ZIP contains one plain-text file at `OPENCLUSTER/PAGE.CFG`. The native reader accepts a title of up to 18 uppercase letters, digits, spaces or hyphens, a six-digit RGB accent, a `rows` or `columns` layout, and two metric IDs. The IDs are `oil_f`, `coolant_f`, `rpm` and `throttle_pct`. The [Road config](pages/road.cfg) can be edited directly.

### Render a package and build an edited version

These commands exercise the real page reader in a local directory standing in for a mounted drive. They require a C99 compiler and Python 3.9 or later.

~~~sh
cc -std=c99 -O2 page/page.c tools/render_page.c -o render_page
python -m zipfile -e packages/road-page.zip test-drive
./render_page test-drive road.ppm oil_f=208 coolant_f=194
python tools/build_page.py pages/sport.cfg custom-page.zip --renderer ./render_page
python -m zipfile -e custom-page.zip test-drive
./render_page test-drive sport.ppm rpm=3200 throttle_pct=35
~~~

On Windows with GCC, use `gcc` and name the output `render_page.exe`. The numbers on these command lines are test inputs. Missing readings appear as two dashes. The PPM file contains the actual pixels drawn by the native renderer.

The [native API](page/page.h) accepts the config bytes, host-provided measurements and a caller-owned RGB888 frame. The 400 × 224 canvas is a logical page size chosen for this project. A factory integration would still need a supported way to start the renderer and present its frame. Tests compare the distributed ZIPs with fresh builds, exercise both layouts, and verify that changing only the title leaves the pixels below the header identical.

## Try the trip display

Open [ui/trip.html](ui/trip.html) in a browser from your local checkout. Select Trip A or Trip B and change between US and metric units. The page uses original graphics and fixed example trips. The layout is illustrative. Its behavior is based on Jaguar's early X152 training material. It runs entirely offline.

## Inspect a local VBF

Requires Python 3.9 or later, standard library only. From the project root, run the command below with the path to a local VBF 2.2 file. Add additional paths to inventory several files in order.

~~~sh
python tools/vbf_inventory.py path/to/local.vbf
~~~

The JSON report includes the software identifier declared in the header, whole-file SHA-256, and each block's declared address, stored byte count and payload SHA-256. A matching whole-file digest returns the software number reported by the catalog. File names do not determine identity. Missing matches appear as JSON null.

The reader implements VBF 2.2 text headers followed immediately by big-endian address/length records with two-byte checksum trailers. It reports stored bytes and skips the trailer without validating block CRCs, digital signatures or vehicle compatibility. [Container layout reference](https://github.com/esaulenka/vbf_parser)

~~~sh
python -m unittest discover -s tests -v
~~~

## Research record

- The [2015 center-display records](docs/research.md#identifying-the-center-touchscreen) pair a dismantler's reported display label with the US parts catalog. Run `python tools/display_lookup.py EX53-10E889-CF` to list every direct match and its source. Identifiers may be entered with or without hyphens. An unknown identifier returns an empty JSON array and exit status 1.
- [Evidence and next observation](docs/research.md) covers the 2015 display, two cataloged hardware variants, and the production range of Jaguar's 2013 software bulletin.
- [Firmware catalog](docs/firmware-catalog.csv) records seven published EX53-14C026 fingerprints with source URLs. The test suite uses synthetic containers. No matching vehicle file has been examined for this release.
- [Project instructions](AGENTS.md) and the project-local Codex configuration select Astra xhigh for the lead and leave the choice of supporting models to the lead.

Keep locally obtained OEM files under firmware/ and vehicle-specific exports under private/. Both directories are ignored by Git. Original project code and documentation are released under the [MIT license](LICENSE).
