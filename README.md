# F-Type-OpenCluster

Offline research into the five-inch center display between the analog dials on a US-market 2015 Jaguar F-TYPE S Coupé (X152). The first milestone identifies what the original display can show, catalogs software references and models a small part of its behavior on a computer.

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

- [Evidence and next observation](docs/research.md) covers the 2015 display, two cataloged hardware variants, and the production range of Jaguar's 2013 software bulletin.
- [Firmware catalog](docs/firmware-catalog.csv) records seven published EX53-14C026 fingerprints with source URLs. The test suite uses synthetic containers. No matching vehicle file has been examined for this release.
- [Project instructions](AGENTS.md) and the project-local Codex configuration select Astra xhigh for the lead and leave the choice of supporting models to the lead.

Keep locally obtained OEM files under firmware/ and vehicle-specific exports under private/. Both directories are ignored by Git. Original project code and documentation are released under the [MIT license](LICENSE).
