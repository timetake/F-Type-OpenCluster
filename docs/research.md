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

## What the VW and GR86/BRZ projects actually display

| Original project | What the driver sees | Where the page comes from |
| --- | --- | --- |
| MacsInSpace, MIB Cluster Map | A supported VW Group digital instrument cluster shows the phone's navigation view. The author's compatibility table distinguishes cars that can show a full image from those that only show turn instructions. | An SD card delivers software to a Harman MIB2 or MIB2.5 High head unit. During use the phone supplies a separate instrument video stream. The head unit passes it to the cluster over the same display path used for the built-in navigation view. [Author's README](https://github.com/MacsInSpace/mib-cluster-map/blob/4c717c220e58fa775aabaaad22858b21617f59f0/README.md) · [Compatibility and vehicle reports](https://github.com/MacsInSpace/mib-cluster-map/blob/4c717c220e58fa775aabaaad22858b21617f59f0/docs/FAQ.md) |
| jilleb, MQB Performance Monitor | The factory center screen shows configurable gauges. The app's own settings name left, center and right gauge positions, a graph view and peak markers. | An Android app supplies the interface via Android Auto. The maintainer's screenshots show several layouts on the infotainment screen. This project provides a working example of choosing which measurements to display. [Author's README and screenshots](https://github.com/jilleb/mqb-pm/blob/c47ca0ed3e277ac72fa525803f6c9c5b3aaeed5b/README.md) · [Gauge settings in source](https://github.com/jilleb/mqb-pm/blob/c47ca0ed3e277ac72fa525803f6c9c5b3aaeed5b/app/src/main/res/values/strings.xml) |
| Ranktec, Toyota GR86 / Subaru BRZ | The vendor shows a Gauges app with example data and a separate OEM Cluster app intended for the left information screen behind the steering wheel. The vendor marks both apps as in development. | Ranktec describes a dedicated USB installer device that connects to a network, binds to an account and downloads selected apps from its store. We found the vendor's product page but could not verify an author-published source repository or a released OEM Cluster build. [Product previews, device setup and release status](https://www.ranktec.net/) |

### Applying the comparison to the 2015 US F-TYPE S Coupé

Jaguar already offered an example of the intended result on the 8-inch touchscreen. On an S Coupé equipped with the optional Performance Pack, the Dynamic-i page can display G-force, lap timing and pedal inputs. A photo of that page on the target car would confirm which factory feature is present. Its presence alone gives no information about loading a second page from USB. [MY2015 Jaguar brochure, Dynamic Mode](https://cdn.dealereprocess.org/cdn/brochures/jaguar/2015-ftype.pdf) · [US order guide, Performance Pack S, page 8](https://www.jaguarforums.com/forum/attachments/f-type-x152-72/f-type-how-guides-information-101906/f-type_order_guide-87390d1402346864)

For the 5-inch instrument display, Jaguar documents audio and navigation information. Those functions can be drawn by the cluster from individual values. Their presence does not establish that the cluster accepts a complete image from the head unit as the VW cluster does. For the center touchscreen, the missing evidence is a user-content format accepted by this Jaguar build that can change a factory page from a flash drive. None of the three reference projects identifies such a format for the X152. A vehicle result would be the same custom element, changed between two USB builds, visible in the same factory page on this model.

## Next observation

### Identifying the center touchscreen

The US parts catalog for a 2015 F-TYPE S 3.0L lists display unit **T2R19384** for production sequences K10666 through K14061. A Swedish dismantler lists a 2015 F-TYPE donor, K12557, within that range. Its multifunction display record gives the label as **EX5310E889CF**, the article number as **T2R14233** and the original number as **T2R19384**. This identifies a center-screen assembly to study without access to the target car. The installed software revision and the donor's original sales market are unknown. [US catalog, Display Unit](https://parts.jaguarcary.com/v-2015-jaguar-f-type--s--3-0l-v6-gas/electrical--navigation-system) · [Donor G-L2858336](https://lagabasen.com/visa-produkter?CarBreaker=G&c=47985155&vehicle=0)

A second 2015 listing reports the same label with **T2R20045E**. Jaguar's own catalog identifies T2R20045E as a remanufactured single-view F-TYPE touchscreen. This explains why the lookup keeps both records. Sharing a label does not establish shared firmware. [Donor K-L797801](https://lagabasen.com/visa-produkter?articleno=EX5310E889CF&vehicle=0) · [Jaguar remanufactured parts catalog, Infotainment & Navigation](https://www.jaguar.com/content/dam/jdx/pdfs/US/JGUK_19B_CAM_RemanParts_Catalogue_Digi_TRADE.pdf)

Jaguar's US quick start guide describes the console USB flash drive under portable audio. Bosch demonstrated a different USB use in an F-TYPE Coupé with its mySPIN phone integration. The phone hosts the app. Jaguar's early X152 touchscreen update bulletin identifies the FCDIM as the recipient of the factory software update and describes an SDD session. Its specified 2014 production range ends at K09823, before the K12557 donor. None of these documents specifies a user-authored page format or verifies a USB build for this display. [US quick start guide, portable media](https://cariffy.com/wp-content/uploads/2024/10/2015-Jaguar-F-Type-Owners-Manual.pdf) · [Bosch F-TYPE demonstration](https://us.bosch-press.com/pressportal/us/en/press-release-593.html) · [Jaguar UPS6413-1bNAS1, pages 1–3](https://static.nhtsa.gov/odi/tsbs/2013/MC-10226630-9999.pdf)

### Which module handles the media USB port

Jaguar workshop manual, X152 section 415-01, *Information and Entertainment System*, in the 2013–2019 compilation, distinguishes the media reader, the center display and the instrument cluster. The chapter headers on PDF pages 5867 and 6016 explicitly say **2017.0 F-TYPE** and carry a March 2015 publication date. Its module descriptions are comparative evidence for the 2015 US car. The installed equipment and software on that car remain unverified.

| Documented equipment | What Jaguar describes | PDF pages |
| --- | --- | --- |
| InControl Touch Plus with Integrated Audio Module (IAM) | The console media USB feeds the IAM on both of the IAM variants shown. The center touchscreen provides the controls. | 5875–5879 |
| HDD navigation with IAM | The IAM sends an image to the center touchscreen. The instrument cluster receives turn instructions separately. This documents a center-screen image path and a more limited type of content on the instrument screen. | 6019–6021 |

The public TOPIx download labeled *SDD Manual Software Download* is the Windows diagnostic application. JLR assigns earlier X152 model years to SDD and requires an active programming subscription to use it for module programming. The SDD installer version cannot identify the application running on a vehicle module. For an offline study of this system, retain the IAM and FCDIM application software numbers under their respective module names when a matching identification report becomes available. No matching original module image or owner-page installer was obtained from the public materials reviewed. [JLR diagnostics coverage](https://topix.jlrext.com/topix/service/procedure/1694991/ODYSSEY_GENERIC/G3345251/en_US?uid=G3345249) · [JLR diagnostic download FAQ](https://topix.jlrext.com/topix/service/procedure/1700886/ODYSSEY_GENERIC/G4142441/en_US?uid=G4142440)

### Archived display software for offline comparison

The public SDD 160 calibration archive lists these three files under `160 Calibration Files/VBF/`. Its member sizes agree with the separate catalogs. The archive is a third-party copy. Its single-file extraction returned error 126 for all three entries during this review, so the bytes and headers have not been verified locally. The software identifiers installed on the project car are still unknown. [Archive directory](https://archive.org/download/jlr-sdd-dvd160.04/4_Calibration%20Files%20Collection/)

| File | Listed bytes | Evidence |
| --- | ---: | --- |
| EX53-14C060-CF.vbf | 89,351,515 | The catalog identifies this as X152 FCDIM application software. [File record](https://jlrvbf.com/vbf/EX53-14C060-CF) |
| EX53-14C061-CF.vbf | 30,361 | The catalog identifies this as FCDIM calibration data. [File record](https://obdbdm.com/jlr/EX53-14C061-CF.html) |
| EX53-14C026-AG.vbf | 738,441 | Jaguar names this IPC software in an early X152 bulletin covering K00001 through K00734. [Jaguar bulletin](https://static.nhtsa.gov/odi/tsbs/2013/MC-10227110-9999.pdf) |

### Identifying the instrument cluster

An existing Jaguar SDD **module identification** report for the relevant vehicle would answer which instrument cluster it has. Record the IPC hardware/assembly identifier, application software number and calibration number under their original labels. Leave an unavailable field blank. A separate IAM or FCDIM row helps distinguish the infotainment unit and central dashboard screen from the instrument cluster. A cropped report showing the module rows is sufficient. Keep the full report local.

With the installed application number and a corresponding authorized local VBF, run the inventory command and retain its digest and block report. Compare that result to the cited catalog. Record an unlisted revision as a new observation. A parked photo of the trip display and the dial scale provides a separate visual reference for the desktop model.
