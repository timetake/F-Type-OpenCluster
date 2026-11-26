# What the first-generation cluster can display

## 2015 US F-TYPE S Coupé

The MY2015 US order guide lists two analog gauges and a 5-inch color display across the range, including the S Coupé. This fixes the physical target for the project. The guide gives no pixel dimensions. [Order guide, Equipment, page 6](https://www.jaguarforums.com/forum/attachments/f-type-x152-72/f-type-how-guides-information-101906/f-type_order_guide-87390d1402346864)

Jaguar's MY2014 training book describes driver information on the central display, including basic audio details and navigation. The left steering-wheel control opens its menus. The trip-computer section describes trip memories A and B, distance, mean speed and the available unit systems. These observations support an original PC model of those interactions. Their visual layout and exact behavior on the 2015 car remain to be checked against the car. [NP14-FT, Electrical Systems, pages 3.36–3.37](https://studylib.net/doc/25233709/np14-ft-course-book-05-10-2013)

## What the identifiers establish

| Evidence | Observation | What it identifies |
| --- | --- | --- |
| Jaguar SSM65737, June 2013 | For production sequence K00001–K00734, revision EX53-14C026-AG or later corrected a date-format retention issue. The date appears in the touchscreen settings. | A software revision used in an early X152 cluster. The bulletin does not identify software installed in a 2015 Coupé. [Bulletin, page 1](https://static.nhtsa.gov/odi/tsbs/2013/MC-10227110-9999.pdf) |
| MY2015 US parts catalog | Among the 3.0L chrome-surround assemblies from K10249, T2R22446 is listed for the 190 mph dial and T2R22444 for the 200 mph dial. | Service assembly numbers. The speedometer's highest printed speed can narrow the hardware search. Installed software still needs its own identifier. [Parts catalog, Cluster Assembly](https://jaguar.oempartsonline.com/v-2015-jaguar-f-type--s--3-0l-v6-gas/electrical--navigation-system) |
| Third-party VBF catalog | Seven EX53-14C026 entries have seven distinct SHA-256 digests. All seven pages report VBF 2.2 and 738,441 bytes. | Reference fingerprints transcribed from individual listings. Each row links its source in the [catalog](firmware-catalog.csv). Vehicle fitment is unknown. |

An exact digest match identifies a file against the third-party listing. The OEM bulletin supports the AG software number independently. It does not publish the corresponding hash. A block's declared address describes its position in the container's target address space. Processor type, display resolution and the location of graphics assets are still unknown.

## USB and the two original displays

The vehicle milestone is a repeatable visible change in the factory interface using an ordinary flash drive. For example, two builds could supply different titles or layouts for the same page. Record the display and software version, how the page was opened, and what remained visible after removing the drive. Persistence after removal is an observation to make during testing.

| Interface | Evidence for the early X152 | Relevance to a flash-drive build |
| --- | --- | --- |
| Center touchscreen and phone apps | InControl Apps was option **H57A** on the US 2015 S Coupé. An equipped car presents approved apps running on a connected smartphone. [MY2015 order guide, Optional Equipment](https://www.jaguarforums.com/forum/attachments/f-type-x152-72/f-type-how-guides-information-101906/f-type_order_guide-87390d1402346864) · [Jaguar USA connection guide](https://www.jaguar.com/en-us/jdx/incontrol/incontrol-user-guide/incontrol-apps.html) | A labeled USB port or an InControl Apps menu identifies a phone integration feature. This documentation provides no installer format for a standalone flash drive. |
| Center touchscreen software | Jaguar identifies the Gen 2.1 touchscreen as the FCDIM, also called TSD or HLDF. Its service software download and recovery use the SDD diagnostic system. [Jaguar SSM71803](https://static.nhtsa.gov/odi/tsbs/2014/MC-10231223-9999.pdf) | Use these names to match a module report to the touchscreen. The bulletin describes dealer servicing and gives no owner-facing page-loading interface. |
| Instrument cluster software | Jaguar's early-X152 service message identifies a separate cluster software revision and an SDD service workflow. [Jaguar SSM65737](https://static.nhtsa.gov/odi/tsbs/2013/MC-10227110-9999.pdf) | The IPC software number identifies the cluster build. It does not establish that the console USB port can load a page there. |

**Current result.** The sources above document USB phone integration and identify the two display modules. None specifies an ordinary USB package that can add an owner-authored screen to either factory interface. A matching module identification record would narrow the hardware/software search. Demonstrating installability also requires an interface supported by that build and an observed result on the physical display.

## Next observation

An existing Jaguar SDD **module identification** report for the relevant vehicle would answer which instrument cluster it has. Record the IPC hardware/assembly identifier, application software number and calibration number under their original labels. Leave an unavailable field blank. A separate IAM or FCDIM row helps distinguish the infotainment unit and central dashboard screen from the instrument cluster. A cropped report showing the module rows is sufficient. Keep the full report local.

With the installed application number and a corresponding authorized local VBF, run the inventory command and retain its digest and block report. Compare that result to the cited catalog. Record an unlisted revision as a new observation. A parked photo of the trip display and the dial scale provides a separate visual reference for the desktop model.
