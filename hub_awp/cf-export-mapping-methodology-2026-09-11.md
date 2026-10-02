# CF_Export agreement and invoice map: methodology

*Built 2026-09-11. Source: `/Volumes/SSD/CF_Export`, read only; nothing on the SSD was written, moved or
renamed. Reference data: a same-day snapshot of `[Engineering]` and `[Data-Warehouse]` (TheHub) taken
over the 1434 tunnel with the portal's read-only connection.*

The export holds the **Contract Administration division's consultant files**: construction engineering
inspection (CEI), QAM, coatings, materials, signals and district inspection agreements from 2015 to 2026.
It also covers their procurement (advertisements, letters of interest, short lists, interviews), the
executed agreements, letter agreements, supplements, invoices and consultant evaluations. This document
explains how every file was read, classified, grouped into agreements and linked to the Engineering
database. The companion workbook holds the results.

## 1. Deliverables and headline numbers

| File | What it is |
|---|---|
| `cf-export-agreement-invoice-map-2026-09-11.xlsx` | The mapping: 13 sheets, one row per agreement unit, agreement instrument, invoice, document, folder, DB agreement/invoice/supplement, consultant and project (§16) |
| `cf-export-mapping-methodology-2026-09-11.md` | This document |
| `research/cf-export-2026-09-11/` | The eight scripts that produced the workbook (`extract_pdf.py`, `extract_other.py`, `ocr.py`, `snapshot_db.py`, `cfmap.py`, `cfextract.py`, `cfbuild.py`) and `summary.json` with every count quoted here |

| Measure | Result |
|---|---|
| Documents mapped | **14,321**: 12,924 files + 625 zip members + 772 e-mail attachments |
| Document types | 53 (§7); 180 left unclassified |
| Agreement units | **825**: 442 statewide assignments, 203 firm-level master agreements, 93 district agreements, 79 project agreements, 8 D12 construction contracts |
| Units with a consultant | 821 (708 from the folder name, 104 by document vote, 3 from the DB, 6 construction contractors) |
| Agreement instruments | 4,293 (agreements, master and letter agreements, supplements, their approval memos, PMDs, selection memos) |
| Invoices | 1,593 (1,142 on the WVDOT BF-2 voucher, 451 on vendor layouts) |
| Units linked to an Engineering-DB agreement | **364**: 120 High, 244 Medium confidence |
| `AgreementsCA` rows found in the export | **127 of 130** |
| `AgreementsM` rows found | 40 of 58 (the 18 missing are 2022 MCS&T masters and two 2025 firms with no folder) |
| `SupplementsCA` supplement numbers seen in the matching folder | 56 of 78 |
| `InvoicesCA` rows matched to an invoice document | 46 of 68 (38 by invoice number, 8 by amount and date) |
| TheHub project keys found in the documents | 602 |

## 2. The source

### 2.1 Size and content

* 40 top-level folders, 1,983 sub-folders, 12,924 files, 19.2 GB of file content (23 GB on disk). Files
  sit 2 to 10 levels deep; 72% sit at depth 4 or 5.
* No hidden or system files.

| Extension | Files | Extension | Files |
|---|---|---|---|
| pdf | 10,091 | xls | 87 |
| doc | 815 | tif / tiff | 67 |
| dgn | 483 | jpg / png | 60 |
| msg | 479 | xlsm | 27 |
| docx | 280 | dat, xml, eml, csv | 27 |
| xlsx | 268 | pset, mp4, wav, vsdx, vsd, txt, mcb, cc | 10 |
| zip | 230 | | |

* **PDFs:** 10,091 files and 115,981 pages. 7,373 have a text layer; the rest are scans, mostly from the
  division's Konica Minolta bizhub copiers. 8 are encrypted but readable.
* **Zip files:** 230, holding 625 members (622 PDF, 2 DOC, 1 JPG). 166 of them are in
  *2023-2024 Statewide CEI & QAM* and 27 in *2023-2024 Statewide Coatings*. Almost all are DocuSign
  "Complete with DocuSign" packages: executed letter agreement or supplement, approval memo, fee
  proposal, selection memo, FHWA notice and the DocuSign `Summary.pdf`.
* **E-mails:** 479 Outlook `.msg` and 5 `.eml`, carrying 772 attachments (338 PNG, 267 PDF, 80 DOCX,
  79 JPG, 5 XLSX, 3 other).
* **DGN files:** all 483 are MicroStation drawings from the Wellsburg Bridge design-build stipend
  submissions (`QAM-Project Specific/Wellsburg Bridge/Stipend/American Bridge|Walsh Construction`).

### 2.2 How the export is organised

The folder conventions changed over the years. Each top folder was assigned one **layout**, and the
layout decides which folder level is an agreement (§6).

| Layout | Programs | Organisation |
|---|---|---|
| `legacy` | 2015–2017 statewide Coatings / Construction Inspection / QAM | One folder per construction job: `<7-digit AASHTOWare contract> <name> D-n` with `Emails/` and `Invoices/`. Program folders `Consultant Contracts/<firm>` (the firm's statewide agreement), `Executed Contracts`, `Fee Proposals`, `LOI`, `Audits`, `Supplemental Contracts`. 2016 QAM adds `Bridge Deck Scanning/<bridge>`; 2015 QAM Corridor H adds `Assignment #1 (RFP)`, `Assignment #2 (Surveying Services)`, `Stipend`. 2017 is mostly letters of interest (and one withdrawn advertisement). |
| `contract` | 2015 and 2016 D12 Statewide Contracts | **Construction contracts, not consultant agreements.** Statewide striping, sealing and RPM contracts by AASHTOWare contract number, holding the contractor's NTP, pre-construction minutes, bonds, insurance, starting notices and overrun/underrun letters. |
| `district2018` | 2018 District Specific Contracts | `Consultant.Agreements.Records/<firm>/<Dn Agreements \| Dn Executed>/(Supplemental)`, plus procurement folders by service (`Materials`, `Resurfacing`, `Slide repair`, `Small Structures` → `LOIs`). 816 of its 921 PDFs are scans. |
| `assign2018` | 2018 statewide CEI / QAM / Coatings | One folder per assignment named `<district project> - <firm>` (or `<firm> - <district> <project>`), with `Invoices/` and `Supplemental n/`. Program folders `Executed Agreements`, `MEMOs`, `Approval letter to consultant`. |
| `signals2018` | 2018 Statewide Signals | `Lighting/<Dn Assignment - WRA>`, `Lighting/Consultants/Fee proposals/<firm>`, `Consultant Letters`, `Executed Agreement`, `LOIs`. |
| `firm` | 2019, 2021, 2023-2024 statewide CEI / QAM / Coatings; 2025 Statewide CEI (new firms) | `<firm>/` holds the firm's master agreement. Annual master supplements sit in `SUPPLEMENTAL #1 (2025)` and `#2 (2026)`, and in `Supplemental 1` for 2019. `<firm>/<Dn_assignment>/` holds one letter agreement with `Letter Agreement/`, `Supplemental #n/` and `Invoices/`. Program folders: `z LOQ's`, `z FEE PROPOSALS`, `Advertisements`, `LOIs`, `Interviews`, `2025 SUPPLEMENTAL (GENERAL INFO)`. |
| `district2020` | 2020 District Specific Contracts | `Consultant Agreements/<firm>/<Dn>/(Supplemental 1)`; program folders `CEI Services/LOIs`, `Material Services/LOIs`, `Consultant Rankings`. |
| `project` | 2018–2026 Project Specific | `<Dn - project>/` with `Advertisement`, `LOQ`/`LOI`, `Short List`, `Interview`, `Agreement`, `Supplemental #n` and `Invoices`. Sub-projects occur (`QA`/`QC`, `Interchange CEI`, `Brooks IC`, `40th to 58th`). `Miller Road O/P D-2` became two folders because the name contains a slash. |
| `materials` | 2025-2026 Statewide Materials | `<MCS&T category>/<firm>/(<assignment>)`. Categories are AMT, AST, CAP, ENG, ENV, LAB, MAT, PAV and SAM (Appendix A). |
| `qamproj` | QAM-Project Specific | `<corridor or bridge>/<section or phase>/Supplemental n/Invoices`: Corridor H sections 1–4, I-64, I-70, US 35, Beckley Widening, Coalfield Express, Wellsburg Bridge. |
| `evals` | zEvaluations | `<year> Services/(<year>/)<firm>/(Signed Evaluations \| With consultant response)`. |
| `fin` | Consultant Financial Statements | `<firm>/`. |

Per-program counts come from the workbook's Summary sheet. In this table:
- **Units w/ DB** counts units with a linked DB agreement.
- **Instr.** counts agreement instruments.
- **Inv. matched** counts invoices matched to `InvoicesCA`.

| Program | Layout | Documents | No text | OCR'd | Units | Units w/ DB | Instr. | Invoices | Inv. matched |
|---|---|---|---|---|---|---|---|---|---|
| 2015 D12 Statewide Contracts | contract | 35 | 0 | 24 | 5 | 0 | 0 | 0 | 0 |
| 2015 Statewide Coatings Inspection | legacy | 125 | 22 | 60 | 7 | 0 | 16 | 32 | 0 |
| 2015 Statewide Construction Inspection | legacy | 51 | 0 | 40 | 4 | 0 | 9 | 20 | 0 |
| 2015 Statewide QAM | legacy | 63 | 0 | 48 | 15 | 0 | 24 | 8 | 0 |
| 2016 D12 Statewide Contracts | contract | 19 | 0 | 17 | 3 | 0 | 0 | 0 | 0 |
| 2016 Statewide Coatings Inspection | legacy | 19 | 0 | 14 | 3 | 0 | 9 | 0 | 0 |
| 2016 Statewide Construction | legacy | 14 | 0 | 11 | 2 | 0 | 7 | 0 | 0 |
| 2016 Statewide QAM | legacy | 35 | 0 | 27 | 6 | 1 | 12 | 5 | 0 |
| 2017 Statewide Coatings Inspection | legacy | 12 | 0 | 6 | 1 | 0 | 1 | 0 | 0 |
| 2017 Statewide Construction Inspection | legacy | 19 | 0 | 3 | 1 | 0 | 0 | 0 | 0 |
| 2017 Statewide Construction Inspection Withdrew | legacy | 17 | 0 | 4 | 0 | 0 | 0 | 0 | 0 |
| 2017 Statewide QAM | legacy | 26 | 0 | 9 | 0 | 0 | 4 | 0 | 0 |
| 2018 District Specific Contracts | district2018 | 1,020 | 55 | 816 | 60 | 0 | 780 | 0 | 0 |
| 2018 Project Specific Contracts | project | 120 | 5 | 75 | 3 | 0 | 25 | 17 | 0 |
| 2018 Statewide Coatings Inspection | assign2018 | 41 | 4 | 26 | 5 | 0 | 20 | 0 | 0 |
| 2018 Statewide Construction Inspection | assign2018 | 166 | 18 | 118 | 22 | 0 | 53 | 62 | 0 |
| 2018 Statewide QAM | assign2018 | 47 | 3 | 25 | 2 | 0 | 19 | 13 | 0 |
| 2018 Statewide Signals | signals2018 | 86 | 3 | 35 | 2 | 0 | 16 | 31 | 0 |
| 2019 Project Specific Contracts | project | 148 | 2 | 52 | 3 | 2 | 51 | 0 | 0 |
| 2019 Statewide Coatings Services | firm | 143 | 22 | 48 | 22 | 0 | 37 | 3 | 0 |
| 2019 Statewide Construciton Services | firm | 420 | 17 | 153 | 55 | 0 | 134 | 69 | 0 |
| 2019 Statewide QAM | firm | 259 | 10 | 116 | 24 | 0 | 101 | 30 | 0 |
| 2020 District Specific Contracts | district2020 | 558 | 94 | 25 | 76 | 0 | 239 | 0 | 0 |
| 2020 Project Specific Contracts | project | 659 | 64 | 53 | 12 | 10 | 173 | 0 | 0 |
| 2021 Project Specific | project | 255 | 2 | 22 | 7 | 6 | 44 | 0 | 0 |
| 2021 Statewide CEI | firm | 446 | 70 | 11 | 59 | 41 | 96 | 28 | 0 |
| 2021 Statewide Coatings | firm | 133 | 20 | 5 | 16 | 7 | 16 | 0 | 0 |
| 2021 Statewide QAM | firm | 82 | 7 | 4 | 5 | 3 | 17 | 2 | 0 |
| 2022 Project Specific Contracts | project | 59 | 0 | 4 | 2 | 2 | 9 | 0 | 0 |
| 2023 Project Specific Contracts | project | 245 | 0 | 29 | 8 | 7 | 37 | 0 | 0 |
| 2023-2024 Statewide CEI & QAM | firm | 4,051 | 174 | 168 | 247 | 201 | 1,554 | 930 | 35 |
| 2023-2024 Statewide Coatings | firm | 604 | 27 | 24 | 38 | 21 | 216 | 104 | 11 |
| 2024 Project Specific Contracts | project | 451 | 19 | 38 | 7 | 2 | 67 | 8 | 0 |
| 2025 Project Specific Contracts | project | 520 | 10 | 52 | 13 | 0 | 91 | 0 | 0 |
| 2025 Statewide CEI (new firms) | firm | 200 | 7 | 6 | 16 | 2 | 123 | 0 | 0 |
| 2025-2026 Statewide Materials | materials | 92 | 0 | 2 | 50 | 44 | 70 | 0 | 0 |
| 2026 Project Specific Contracts | project | 190 | 0 | 17 | 4 | 0 | 42 | 1 | 0 |
| Consultant Financial Statements | fin | 5 | 1 | 3 | 0 | 0 | 0 | 0 | 0 |
| QAM-Project Specific | qamproj | 1,903 | 873 | 189 | 20 | 15 | 181 | 230 | 0 |
| zEvaluations | evals | 983 | 5 | 201 | 0 | 0 | 0 | 0 | 0 |

"No text" in QAM-Project Specific is almost entirely the Wellsburg stipend design files (DGN, TIFF boring
logs). Those were deliberately not read (§5.4).

## 3. Reference data

Snapshot taken 2026-09-11 by `snapshot_db.py`, SELECT only.

| Table | Rows | Used for |
|---|---|---|
| `[Engineering].AgreementsCA` | 130 | Contract Administration agreements, the main link target |
| `SupplementsCA` / `InvoicesCA` / `Invoices_SubSupCA` | 78 / 68 / 11 | Supplements and invoices on those agreements |
| `AgreementsM` / `InvoicesM` / `SupplementsM` | 58 / 211 / 0 | MCS&T (Materials) statewide masters and invoices |
| `AgreementsTO/IT/PM/OD` + invoices | 12 / 4 / 1 / 1 | Other divisions (one TO agreement links) |
| `Agreements` / `Supplements` / `Invoices` (EN) | 1,344 / 552 / 9,425 | Engineering Division agreements, shown for information only (§11.4) |
| `Consultants` (+ 237-row division copies) | 263 | Consultant numbers and names |
| `Statewide_Agreement_Tracking`, `Prequal_Agreement_Tracking` | 453 / 170 | Checked; they hold Engineering master agreements, none for CEI |
| `PTSData` | 15,241 | Checked; `CONT_NO` is empty on every row, so it cannot join construction contract numbers |
| `[Data-Warehouse].Project` (TheHub) | 15,241 | Project keys, names, state project numbers, districts |
| `ProjectPhase` | 18,714 | Federal project numbers |
| `AWP_HUBDates` / `AWP_Dates` / `AWP_ChangeOrders` | 5,494 / 9,558 / 2,725 | AASHTOWare contract numbers (7-digit and 10-digit) |

What the Contract Administration tables actually contain:

* **`AgreementsCA` is recent and coarse.** 124 of 130 rows say *"Agreement loaded from initial data
  dump"*. 92 are Selection Type MA (master) and 37 EA. Distribution dates run from 2016 to 2025, with 46
  in 2023 and 46 in 2024. There are **no 2015–2020 statewide, district or 2019 master agreements**.
* **Statewide assignments are recorded as one *umbrella* row per firm per district.** The row's project
  key is the district-level Hub project, e.g. `2024840014` = *D4 – Statewide Construction Engineering
  Inspection* (Appendix A). 58 `AgreementsCA` rows sit on these umbrella and program keys. 64 rows are
  flagged `Invoiced_Under_Separate_Project_ID = YES`; 3 say NO and 63 are blank.
* **The export holds several letter agreements per firm per district.** Where the umbrella row has an
  amount, it equals the maximum payable of one specific letter agreement. For example, CDM Smith's D4
  umbrella `2024840014-155-A` has $283,761.14, the D4 Office Manager assignment. The rest of that firm's
  D4 letter agreements are not individually represented.
* **`AgreementsM` holds the 2022 and 2025 MCS&T statewide masters.** There is one row per firm per
  category, all Lump Sum, MA, at $7,500,000, on the category keys `2024990286`–`2024990301`.
* **The consultant number inside `AgreementNumberGenerated` (`<key>-<consultant #>-A`) is the reliable
  join.** `Consultant_id` points at the Engineering `Consultants` table for 128 of the 130 CA rows, not
  at the CA copy.

## 4. Pipeline

```
/Volumes/SSD/CF_Export (read only)
  └─ find → files.txt (12,924), dirs.txt (1,983)
       ├─ pass 1  extract_pdf.py    pdfinfo + first-3-page pdftotext for every PDF        397 s
       ├─ pass 2  extract_other.py  msg/eml/doc/docx/xls(x)/txt + zip members + attachments 117 s
       └─ pass 3  ocr.py            tesseract on every text-less PDF / zip member / image  560 s
  snapshot_db.py → db.json (Engineering + TheHub + AWP tables)
  stage 1  cfmap.py      folder-layout parsing + document classification → docs.jsonl
  stage 2  cfextract.py  identifiers and fields from each document's text
  stage 3  cfbuild.py    agreement units, consultant resolution, DB linking, invoice matching
           → cf-export-agreement-invoice-map-2026-09-11.xlsx + summary.json            ≈ 60 s
```

Every stage reads only the previous stage's output, so any stage can be rerun alone. Text is cached
under `text/<id>.txt` (and `<id>.ocr.txt`), where `id = sha1(relative path)[:16]`. A zip member's or
attachment's path is `<container>!<member>`.

## 5. Getting text out of every document

### 5.1 PDFs

`pdfinfo` gives the page count, producer, creator, title and dates. `pdftotext -layout -l 3` extracts the
text of the **first three pages**. Every identifying block sits on those pages: the BF-2 cover sheet,
the agreement header with `STATE:` / `FEDERAL:` / `CID:`, the memo `SUBJECT:` and the DocuSign stamp.
Eight worker threads processed 10,091 PDFs in 6.6 minutes. A PDF with fewer than 100 characters of text
on those pages counts as a scan and goes to OCR.

### 5.2 Other formats

| Format | Tool | Captured |
|---|---|---|
| `.msg` | `extract-msg` | Subject, sender, to, cc, date, attachment names, body; PDF/DOC(X) attachments become documents in their own right |
| `.eml` | Python `email` | Same |
| `.doc` | `antiword`, falling back to macOS `textutil` | Text |
| `.docx` | `python-docx` | Paragraphs and table cells |
| `.xlsx` / `.xlsm` | `openpyxl` (values, first 3,000 rows per sheet) | Cell text by sheet |
| `.xls` | `xlrd` | Same |
| `.txt` `.csv` `.xml` | Read as text | First 400 kB |
| `.zip` | Python `zipfile` | Every member listed; PDF members through pdfinfo/pdftotext, DOC(X) members through antiword/python-docx |
| `.dgn` `.vsd(x)` `.mcb` `.cc` `.pset` `.dat` `.mp4` `.wav` | Not read | Classified by extension |

Two `.xlsx` files are not valid zip containers and could not be read.

### 5.3 OCR

* **What was OCR'd:** every file PDF and zip-member PDF under 100 characters, plus every TIFF, JPEG and PNG
  outside the Wellsburg stipend design deliverables.
* **Pages:** page 1 always. Page 2 as well when the path mentions an agreement, supplement, invoice,
  letter, memo, "executed" or "contract".
* **Settings:** `pdftoppm -r 200 -gray` then `tesseract --psm 1 -l eng`, one tesseract thread per worker,
  8 workers.
* **Result:** 2,585 jobs, 3,709 pages, 0 errors. 2,577 produced 100 or more characters. The median was
  1.5 s per job, and the whole pass took 560 s wall-clock (4,470 CPU-seconds).
* **Not OCR'd:** e-mail attachments that are scans, and inline e-mail images.

### 5.4 Resulting text coverage

| Text came from | Documents |
|---|---|
| PDF text layer | 8,165 |
| OCR | 2,580 |
| Word `.doc` / `.docx` | 817 / 348 |
| Outlook / `.eml` | 479 / 5 |
| Excel `.xlsx` / `.xls` / `.xlsm` | 266 / 87 / 27 |
| Plain text / csv / xml | 13 |
| Too short to use | 18 |
| None | 1,516, of which 774 design deliverables, 412 e-mail inline images, 229 DocuSign zip containers and 101 other documents |

## 6. Parsing the folder layout (`cfmap.parse_path`)

### 6.1 Program attributes

Each top folder carries a program year, service line, layout and kind. The kind is **consultant**,
**construction_contract** (the D12 folders) or **reference** (evaluations, financial statements). The
full table is `P` in `cfmap.py`.

### 6.2 Agreement units

A **unit** is the folder that stands for one agreement or assignment. Every document below it belongs to
it. Documents above unit level are **program-level** (730 of them: shared procurement files and program
memos) or **reference** (evaluations and financial statements).

| Layout | Unit folder | Unit kind |
|---|---|---|
| `firm` | `<program>/<firm>/<assignment>`, or `<program>/<firm>/<Supplemental n>/<assignment>` when an assignment was filed under the firm's supplement (e.g. 2019 Baker `Supplemental 1/D7 Gerald R Freeman Br`) | assignment |
| `firm` | `<program>/<firm>` (documents directly in it or in its master supplement folders) | master |
| `materials` | `<program>/<category>/<firm>/<assignment>`, else `<program>/<category>/<firm>` | assignment / master |
| `district2020` | `…/Consultant Agreements/<firm>/<Dn>` | district_agreement; `<firm>` alone is master |
| `district2018` | `…/Consultant.Agreements.Records/<firm>/<folder naming a district>` | district_agreement; `<firm>` alone is master |
| `assign2018`, `signals2018` | `<program>/<assignment folder>` | assignment |
| `legacy` | `<program>/<job folder>` (with `Bridge Deck Scanning/<bridge>` and Corridor H `Assignment #n` / `Stipend` as sub-units); `<program>/Consultant Contracts/<firm>` | assignment / master |
| `project` | `<program>/<project>` or, when the next folder is not a role folder, `<program>/<project>/<sub-project>` | project_agreement |
| `qamproj` | `<program>/<corridor>/<section>` when the section is not a role folder, else `<program>/<corridor>` | project_agreement |
| `contract` | `<program>/<contract folder>` | construction_contract |

### 6.3 Role folders

Folder names below a unit are matched against these patterns (case-insensitive) to label a document's
role and stop the unit descent:

| Role | Pattern examples |
|---|---|
| invoices | `Invoice`, `Invoices`, `Invocie`, `Engineer Invoice` |
| emails | `Email`, `Emails` |
| supplement | `Supplemental 1`, `Supplemental #3 - extension`, `Supp #1`, `Supp. Letter Agreement #1`, `SUPPLEMENTAL #1 (2025)`, `2025 SUPPLEMENTAL #1`, `Supplementals`, `Completed Supp Agg #1` |
| letter_agreement | `Letter Agreement`, `Complete Ltr Agg`, `Completed letter agreement`, `Approved letter agreement`, `Previous letter agreement` |
| agreement | `Agreement`, `AGREEMENT`, `Executed agreement(s)`, `Executed Contracts`, `Consultant Contracts`, `Final executed agreement`, `Completed agreement`, `D4 Agreements`, `D8 Executed` |
| advertisement | `Advertisement(s)`, `Advetisement` |
| loq_loi | `LOI`, `LOIs`, `LOI's`, `LOQ`, `LOQs`, `z LOQ's`, `LOIs and responses` |
| shortlist / interview | `Short List`, `Shortlist & Interview`, `Selection Criteria Form`, `Proposed Personnel`, `Workload`, `Updated Org Charts`, `Dear John Letters`, `Consultant Rankings`, `Interview(s)` |
| fee_proposal, scope, approval, audit | `Fee Proposal(s)`, `z FEE PROPOSALS`, `Scope of Work`, `Approval Memo`, `MEMOs`, `Audits` |
| evaluation, project_info, insurance, stipend, general_info | `Signed Evaluations`, `With consultant response`, `Project Info`, `Plans & Documents`, `FOIA`, `Misc`, `Insurance`, `Stipend`, `2025 SUPPLEMENTAL (GENERAL INFO)` |

* **District** is read from the unit name, then the file name, then inner folder names with
  `D-6 | D6 | D 5 | D10_ | District 1` (1–12).
* **Supplement number and year** are read from supplement folder names, e.g. `SUPPLEMENTAL #1 (2025)` gives
  supplement 1 for 2025.

## 7. Classifying documents (`cfmap.classify`)

### 7.1 Rule order

The first matching rule wins. Filename rules come first wherever a quoted phrase in the text could
mislead. Selection memos, for example, quote "Master Agreement".

1. **Paths and extensions.** Wellsburg stipend folders and design extensions give design_deliverable or
   media; inline images in e-mails give email_image.
2. **DocuSign certificate.** `Summary.pdf`, or text starting "Certificate Of Completion". Zip containers
   give docusign_package.
3. **E-mail.** `.msg` or `.eml`, or a printed e-mail filename (`State of West Virginia Mail - …`,
   `_External_`, `RE_`, `FW_`).
4. **Reference and construction programs.** The evaluations and financial-statements programs. In D12
   construction contract folders, NTP, pre-construction, insurance, bond, starting notice and
   overrun/underrun by filename.
5. **Invoice.** BF-2 wording in the text ("FORM BF-2", "CONSULTANT VOUCHER", "PROGRESS REPORT OF WORK
   PERFORMED"). Otherwise an invoice word in the filename, a file in an `Invoices` folder that isn't a
   proposal, memo, agreement or letter, or an invoice header plus money in the first page of text.
6. **Strong filename signals.** Selection or interview approval memo; interview, short list, scoring or
   invite; LOI/LOQ or prospectus; PMD (Project Modification Document); fee or price proposal;
   disclosure form.
7. **Agreement instruments,** from the filename together with the text:
   * **Supplement.** A supplement word, or "SUPPLEMENTAL AGREEMENT", "SUPPLEMENTING THAT CERTAIN" or
     "SUPPLEMENTAL #n". It becomes a **supplement memo** if the document is a memorandum with no
     agreement text, a **supplemental letter agreement** if it's a letter agreement, otherwise a
     **supplemental agreement**.
   * **Letter agreement.** "LETTER AGREEMENT", or `letter agreement` / `SW letter` in the name. Memos
     become **letter agreement memos**.
   * **Agreement.** "THIS AGREEMENT", "WITNESSETH", or an agreement word in the filename. "MASTER
     AGREEMENT" in the text or `master` in the name makes it a **master agreement**.
8. **Everything else.**
   * Selection memo: "Selected:", "recommendations were made" or "selection report".
   * Advertisement, district request (including the Google Forms request printouts and DE concurrence),
     consultant response, FHWA notice, agreement attachment (`Attachment B/C` in an agreement folder),
     contract detail sheet.
   * Fee proposal (including the text phrases "SPECIFIC RATE OF PAY" and "PROJECT MODIFICATION DOCUMENT"),
     cost estimate, staffing, project info / CPM update, audit, rates and overhead, insurance, NTP,
     scope, approval or acceptance letter, expense regulations.
   * Generic memo, letter or spreadsheet.
   * A zip member or attachment that still matched nothing takes the kind its container's name implies
     (e.g. an attachment of an `Ad Confirmation.msg` is an advertisement).
   * Otherwise **other**.

### 7.2 Document types

| Type | Count | What it is |
|---|---|---|
| invoice | 1,593 | Consultant invoice, BF-2 voucher or invoice package |
| fee_proposal | 1,465 | Fee or price proposal, specific-rate-of-pay proposal, supplement fee proposal |
| supplemental_agreement | 1,190 | Executed supplemental agreement: the firm's annual master supplement (rates and term) or an assignment supplement |
| email | 1,142 | Outlook message or printed e-mail |
| design_deliverable | 1,110 | Wellsburg design-build stipend deliverables |
| evaluation | 1,002 | Consultant evaluation form |
| selection_memo | 842 | Selection / interview-scoring approval memo, selection letter |
| supplement_memo | 671 | Memo requesting or approving a supplement |
| loq_loi | 658 | Letter of interest or qualifications, unpriced prospectus |
| shortlist_interview | 641 | Short-list scoring, interview invite, score sheet, vote summary, selection criteria form |
| agreement | 516 | Executed agreement (project-specific, district, 2015–2018 statewide) or its transmittal letter |
| docusign_certificate | 421 | DocuSign certificate of completion (`Summary.pdf`) |
| email_image | 412 | Inline image inside an e-mail |
| letter_agreement | 279 | Executed statewide letter agreement (the assignment under a master) |
| master_agreement | 266 | Statewide or district master agreement |
| district_request | 234 | District request for consultant services, request form, DE concurrence |
| advertisement | 230 | Legal advertisement, notice for consulting services, ad confirmation |
| docusign_package | 229 | DocuSign zip container (its members are classified individually) |
| pmd | 191 | Project Modification Document (hours/fee change supporting a supplement) |
| letter_agreement_memo | 179 | Approval memo for a letter agreement |
| supplemental_letter_agreement | 143 | Supplement to a letter agreement |
| disclosure_form | 97 | Disclosure of interested parties |
| letter_other / memo_other | 96 / 24 | Other correspondence |
| project_info | 91 | Plans, cross-sections, CPM schedule updates |
| scope_of_work | 89 | Scope-of-work notes |
| approval_memo_letter | 57 | Approval letter to the consultant, acceptance letter |
| fhwa_notice | 40 | FHWA notice of consultant use |
| consultant_response | 36 | Consultant's availability response to a district request |
| rates_overhead / audit | 26 / 25 | Rate schedules, overhead memos / audit reports |
| construction_contract_* | 54 | D12 contract paperwork: NTP 8, pre-con 10, insurance 7, starting notice 6, overrun/underrun 4, bond 3, other 16 |
| cost_estimate, spreadsheet, agreement_attachment, ntp, staffing, reference_regulations | 15 / 14 / 13 / 11 / 7 / 7 | As named |
| image, financial_statement, contract_detail, media, insurance, agreement_memo, document_other, zip_package | 5 / 5 / 4 / 4 / 3 / 3 / 2 / 1 | As named |
| other | 178 | No rule matched (listed on the Exceptions sheet) |

### 7.3 Known weaknesses

* Scanned documents with uninformative names (`SC458 ID12721102909490.pdf`) are typed only as well as
  their OCR allows.
* The 2018 district "EXECUTED_Agree_…" scans are split between agreement and supplemental_agreement,
  depending on whether the OCR'd first pages contain "SUPPLEMENTAL".
* Some project-folder interview invitations read like selection memos; the filename rule catches most.

## 8. Reading fields (`cfextract.py`)

### 8.1 Identifiers (every document, first 20,000 characters plus the file name)

| Identifier | Pattern | Validation |
|---|---|---|
| **Project key** (10 digits, `YYYYNNNNNN`) | Not preceded by `$ . , / -`. "Labelled" when `CID`, `Contract ID`, `Contract No`, `Project ID/No/Key` precedes it within 30 characters | Kept only if it is a TheHub `Project.ProjectId`. Other 10-digit numbers are vendor project numbers (Stantec's `2026251912`, `2026252102`, …) and are reported but never used |
| **State project number** | `S350-37-20.58 00`, `X328-52-11.16`, `S313-60/34-9.01 00` | Normalised to `prefix\|route\|milepost×100` (`S350\|37\|2058`). TheHub stores `StateProjectNo` fixed-width (`X328  52   111611`: prefix X328, route 52, last field = milepost 1116 + suffix 11) or dashed (`S345- 064/00 138.01 00`); both parse to the same key. If the exact key misses, prefix+milepost is accepted when it identifies exactly one project |
| **Federal project number** | `STBG-0020(400)D`, `NHPP-0641(413)`, `NFA-0037(051)D` and 40 program prefixes | Punctuation removed and matched to `ProjectPhase.FederalProjectNo`; weight 0.5 because one federal number can cover several phases |
| **AASHTOWare contract number** (7 digits, optional `R#`) | Only from a legacy job-folder name (`1003227 East Huntington Bridge D-2`) or text labelled `Contract ID/No`, `Call No`, `CID` | Checked against `AWP_HUBDates` / `AWP_Dates`. **The 2015–2016 numbers are not in either table**, so they are shown but not joined to TheHub |

* 2,535 documents carry at least one validated project identifier: 1,339 through a project key, 1,703
  through a state project number and 1,006 through a federal number.
* 602 distinct Hub projects appear.

### 8.2 Invoices

**BF-2 voucher (1,142 documents).** Both the 10/2023 revision and the older layout used on the QAM
projects ("Letter Assignment", "Amount due this invoice") are read. The fields are:

* vendor name, vendor number, remit address ID;
* vendor invoice # and invoice date;
* work period from/to;
* agreement date;
* original agreement (or letter assignment), supplementals and total (the maximum payable);
* % funds expended;
* state project, federal project, project name;
* the INVOICE AMOUNT row as previous / current / to date, with "Amount due consultant" / "Amount due this
  invoice" as a fallback for current and "Less previous payment" for previous.

The vendor detail after `COMMENTS:` supplies the vendor project number.

**Vendor layout (451).**
* **Invoice #** from `INVOICE NO/NUMBER/#`, `INV #` or a line reading `INVOICE: …`.
* **Invoice date** from `INVOICE DATE`, `DATE OF INVOICE` or `DATE:`.
* **Period** from `PERIOD` / `SERVICES FROM … TO …`.
* **Current amount** from the first of these that matches: *invoice #n in the amount of*, *amount due
  (this invoice / period / consultant)*, *total amount due*, *this invoice*, *current amount/billing*,
  *invoice total*, *total due*, *balance due*.
* **Previous and to-date** from *previously billed* and *billed to date*.
* **Maximum** from *not-to-exceed* / *maximum payable* / *contract amount*.
* **Vendor project #** from `Project No`.

**Filename.** `Invoice #2`, `Inv #2090332-01` and `#2211167` are kept as separate invoice references and
used in matching.

| Field | Invoices with it |
|---|---|
| Current amount | 1,397 (88%) |
| Invoice date | 1,393 (87%) |
| Invoice number | 1,303 (82%) |
| Maximum payable | 1,096 (69%) |
| Period end | 891 (56%) |
| BF-2 project name | 698 |
| BF-2 vendor name | 623 |

The 196 invoices without a current amount are mostly vendor layouts without a labelled total and OCR'd
2015–2019 scans. They are listed on the Exceptions sheet.

### 8.3 Agreements, letter agreements, supplements and memos

* **Consultant named in the agreement clause.** "*and* NAME*, hereinafter called "Consultant"*",
  allowing "a corporation," and similar.
* **Header block** `STATE:` / `FEDERAL:` / `CID:`.
* **Agreement title.** The line(s) after "DIVISION OF HIGHWAYS FOR".
* **Executed date.** The DocuSign-stamped date printed immediately before "THIS AGREEMENT", else "entered
  into … <date>".
* **Original agreement date** ("*agreement dated* February 13, 2023").
* **Supplement number** ("SUPPLEMENTAL AGREEMENT 1", "SUPPLEMENTAL #2").
* **Master agreement name** ("2023-2024 STATEWIDE CEI & QAM MASTER AGREEMENT", "DISTRICT MATERIALS
  INSPECTION SERVICES").
* **Amounts:**
  * maximum payable ("*new max amount payable for the assignment will be* $572,460.46", "*maximum
    payable amount of* $283,761.14");
  * amount added ("*will add* $288,699.32");
  * not-to-exceed;
  * fee total.
* **Memo fields:**
  * memo date (first long-form date);
  * the `SUBJECT:` block, e.g. *CDM SMITH, INC. SUPPLEMENTAL #1 DISTRICT 4 – OFFICE MANAGER & FINALIZATION
    STATEWIDE CEI & QAM MASTER AGREEMENT*;
  * firm and assignment ("*Letter Agreement with* FIRM*, for the* ASSIGNMENT*…*", "*The consulting firm*
    FIRM *submitted*");
  * selection memos' `Selected:` and `1st/2nd Alternate:`.

| Type | n | Consultant in text | Executed date | Memo date | CID | Max payable | Supp # | Subject | Master name |
|---|---|---|---|---|---|---|---|---|---|
| agreement | 516 | 125 | 81 | – | 92 | 25 | 17 | – | 191 |
| master_agreement | 266 | 175 | 175 | – | 5 | – | – | – | 122 |
| letter_agreement | 279 | 153 | – | 254 | 26 | 82 | 145 | 93 | 84 |
| letter_agreement_memo | 179 | 8 | – | 156 | 13 | 135 | 4 | 179 | 132 |
| supplemental_agreement | 1,190 | 771 | 217 | – | 14 | 207 | 840 | – | 358 |
| supplemental_letter_agreement | 143 | 100 | 22 | 128 | – | 42 | 114 | 42 | 13 |
| supplement_memo | 671 | 84 | – | 545 | 32 | 12 | 565 | 659 | 259 |
| selection_memo | 842 | 5 | – | 637 | 26 | – | – | 765 | 484 |

The low maximum-payable rate on executed agreements is expected. Their compensation article sits after
page 3, which was not extracted. The approval memos and letter agreements carry the amount instead.

### 8.4 DocuSign certificates, e-mails and dates

* **DocuSign certificates.** Envelope ID (91%), envelope subject (100%) and completion date (95%). The
  subject names the documents in the envelope, e.g. "*Please DocuSign: MEMO DC thru HD to Statewide CEI.
  RKK.docx, 2021.CEI.Master.agreeement.SW.RKK.pdf*".
* **E-mails.** Subject, sender and date from the `.msg`/`.eml` headers. For printed e-mails the subject
  comes from the "Subject:" line, or failing that from the filename after "State of West Virginia Mail -".
* **Best date for a document.** The first of: invoice date, executed date, memo date, e-mail date,
  DocuSign completion date, filename date. Filename dates are read in `YYYY MM DD`, `YYYY-MM-DD`,
  `YYYYMMDD`, `M.D.YYYY` and `MMDDYY` forms.
* **Money** is parsed into `Decimal` strings and never converted to float. The workbook writes numbers
  only at the cell.

## 9. Resolving consultants

### 9.1 Canonical firms

`FIRMS` in `cfmap.py` lists 55 canonical firms. Each has an alias pattern (case-sensitive for short
acronyms such as `ICE`, `CEC`, `GAI`, `TRC`, `EXP`) and its Engineering consultant number(s). Appendix B
has the list. Points to note:

* **Two numbers for one firm.** CTL Engineering is `740` in `Consultants` but `60` in the CA agreements.
  KTA-Tator is `630` (Materials) and `62` (CA). Superior Services is `84` and `79`. All numbers are
  accepted.
* **No consultant number in the Engineering tables.** **Quinn Consulting** (10 units), **L.R. Kimball**
  (4 units) and **Advanced Asphalt Technologies** have no consultant row at all, so nothing of theirs
  can be linked.
* **Aliases seen in folder names.** "Summit" and "Summitt"; "Mead & Hunt" and "Mead and Hunt"; "Mannik
  Smith", "Mannick & Smith" and "MSG"; "ELR", "EL ROBINSON" and "E.L. Robinson"; "S&ME" and "S & ME";
  "Baker", "MBI" and "Michael Baker"; "GPI", "G-P" and the misspelling "GRENNMAN".
* **Construction contractors are tagged `[contractor]`.** American Bridge and Walsh (the Wellsburg
  stipend), A&A Safety and Scodeller (the D12 contracts) are never treated as consultants.

### 9.2 A unit's consultant

1. **Folder name** (708 units) whenever the layout puts the firm in the path.
2. **Document vote** (104 units). Letters of interest, short lists, interviews, advertisements and
   evaluations are excluded, since those come from every competing firm. From the remaining documents:

   | Source | Weight |
   |---|---|
   | Consultant clause of an agreement or letter agreement | 6 |
   | Master or supplemental agreement | 5 |
   | Letter agreement memo | 5 |
   | Supplement or agreement memo, BF-2 vendor name | 4 |
   | Selection memo's `Selected:` line | 3 |
   | Fee proposal, PMD, e-mail, district request | 2–3 |
   | Firm named in any other file name | 1 |
3. **DB consultant** (3 units). A project folder holding only procurement files takes the consultant on
   the DB agreement it matches by project key or name (§11).
4. **Contractor** (6 D12 units).

Two units end with no consultant: `2015 Statewide QAM/1322506R1 Corridor H/Stipend` and the
`2016 Statewide QAM/Bridge Deck Scanning` parent folder.

### 9.3 Largest consultants in the export

| Consultant | # | Units | Documents | Invoices | Instruments | `AgreementsCA` rows | Units linked |
|---|---|---|---|---|---|---|---|
| Greenman-Pedersen (GPI) | 200 | 104 | 1,492 | 307 | 411 | 16 | 46 |
| Whitman, Requardt & Associates (WRA) | 405 | 63 | 1,034 | 164 | 301 | 11 | 38 |
| Michael Baker International | 275 | 59 | 1,044 | 164 | 333 | 14 | 26 |
| CDM Smith | 155 | 57 | 983 | 196 | 309 | 8 | 33 |
| A. Morton Thomas (AMT) | 100 | 53 | 816 | 73 | 277 | 10 | 26 |
| Stantec | 350 | 50 | 1,981 | 190 | 261 | 8 | 22 |
| TRC Engineers | 390 | 47 | 741 | 117 | 230 | 10 | 24 |
| Mead & Hunt | 270 | 41 | 737 | 87 | 227 | 10 | 22 |
| HNTB | 225 | 39 | 694 | 49 | 233 | 7 | 14 |
| E.L. Robinson | 175 | 26 | 338 | 13 | 137 | 2 | 4 |
| S&ME | 545 | 26 | 380 | 42 | 102 | 3 | 13 |
| The Thrasher Group | 385 | 23 | 381 | 5 | 133 | 4 | 9 |
| RK&K | 330 | 18 | 257 | 53 | 90 | 1 | 9 |
| Terradon | 370 | 18 | 170 | 20 | 95 | 1 | 6 |
| Mannik & Smith Group | 375 | 16 | 290 | 16 | 80 | 4 | 6 |

The Consultants sheet has all 57 rows, including the folder aliases seen and the DB names.

## 10. Building agreement units (`cfbuild.py`)

For each of the 825 units:

* **District.** The most common folder district, else the most common district named in the unit's
  agreement or invoice text.
* **Project key.** A weighted vote over the unit's documents:
  * each validated key scores its document type's weight (the same weights as §9.2; invoices 4);
  * a key that is labelled (`CID:` etc.) scores double;
  * a key reached through a state project number scores the weight once, through a federal number half;
  * evaluations are ignored;
  * umbrella and program keys (Appendix A) are set aside in their own column;
  * the top remaining key is the unit's project key.

  317 units have one: 240 statewide assignments, 75 project agreements and 2 masters. Statewide
  "Various Projects" assignments usually name no single project.
* **Supplements.** Supplement numbers come from folder names and from supplement documents, and years
  from the `(2025)`/`(2026)` master-supplement folders.
* **Amounts and dates:**
  * first and last instrument dates;
  * the latest maximum payable (by document date) and the document it came from;
  * first and last invoice dates;
  * the sum of current amounts over **unique** invoice numbers (the same invoice filed twice is counted
    once);
  * the highest "billed to date".

## 11. Linking units to the Engineering database

### 11.1 Candidates

Every agreement row in the CA, M, TO, IT, PM and OD tables is a candidate. Engineering Division rows are
handled in §11.4. Each candidate gets a rank (lower is better) and a confidence.

| Method | Condition | Rank | Confidence |
|---|---|---|---|
| **Project key + consultant** | The agreement's project key is one of the unit's top six keys and its consultant number is the unit's. Kept at rank 1 if it's the top key, holds ≥ 30% of the key vote, or its Hub name resembles the folder name (≥ 70); otherwise rank 6 (not linked) | 1 | High when it's the top key with ≥ 30% of the vote or name similarity ≥ 60, else Medium |
| **MCS&T category master + consultant** | Materials units: the category's 2025 MCS&T key (Appendix A) + consultant | 1 | High |
| **Folder name ≈ Hub project name + consultant** | The consultant's own non-umbrella agreements whose Hub project name scores ≥ 85 against the folder name (§11.3) | 2 | High at ≥ 92, else Medium |
| **Project key only / folder name only, consultant taken from DB** | Project and assignment units with no consultant or only weak evidence: the top key's agreement, or a name score ≥ 88 | 3 | Medium |
| **District umbrella + consultant** | Statewide assignments in the 2021, 2023-2024 and 2025 programs: the district's CEI or Coatings umbrella key (Appendix A) + consultant | 4 | Medium |
| **Master → CA program key** | 2023-2024 CEI masters: `2024990229` / `2024990230` + consultant | 4 | Medium |
| **Master → district umbrellas** | A firm's master unit links to that firm's umbrella rows in every district | 5 | Medium |
| **Program key named in documents + consultant** | An umbrella or program key appears in the unit's text | 5 | Medium |

### 11.2 Corroboration and demotion

* **Promotion.** If a candidate's DB amount equals any amount printed in the unit's documents (maximum
  payable, original agreement, not-to-exceed, fee total, amount added), its rank drops by 0.6, its
  confidence becomes High, and the method notes "DB amount equals an amount in the documents". **47 of
  the 364 primary links are corroborated this way.**
* **Demotion.** A project-key match is demoted by 3.5 ranks, below the district umbrella, when both of
  these hold:
  * the key was not printed as the agreement's own `CID:`;
  * either the key's Hub project is in a different district from the unit, or the folder names a
    specific project whose Hub name scores under 40.

  Vendors copy BF-2 project blocks between assignments; for example, GAI's D8 Greenawalt Gap invoices
  print the Armilda Bridge state project. Four key matches were demoted.
* **Primary and linked matches.** The best-ranked candidate is the **primary** match. Every candidate
  ranked 5 or better is **linked**. Rank 6 and worse are listed as weak candidates only.

### 11.3 Name similarity

Both names are upper-cased and normalised:

* **Abbreviations and spelling fixes.** BRIDGE→BR, MEMORIAL→MEM, ROAD→RD, STREET→ST, I/C→IC, O/P→OP,
  O/H→OH, CONNECTOR→CONN, CREEK→CR, MOUNTAIN→MTN, &→AND, and the misspellings RANDOPLH→RANDOLPH and
  GREENAWALT→GREENWALT.
* **Words removed.** District tags, "Various", "Projects", "CEI", "QAM", "SW", "Statewide",
  "Inspection", "Construction", "Coatings", years and single digits.

A match needs at least one **shared distinctive word**; Materials, Finalization, Office, Area, Engineer,
Support, Resurfacing, BR, RD, IC and similar generic words don't count. Only then is rapidfuzz
`token_set_ratio` applied. For a sub-project folder (`…/QA`, `…/Brooks IC`) the last segment is used when
it is at least 4 characters after cleaning.

### 11.4 Engineering Division agreements

Engineering Division (`[Engineering].Agreements`) rows are never linked. Where the same consultant holds
an Engineering Division agreement on the unit's project key, the row is shown in its own column. Sixteen
units have one, typically the firm's **design** agreement for the project, e.g. Stantec's I-70 Bridges
design agreement `2016001061-350-A` beside its I-70 QAM inspection. An earlier draft that linked them
produced false positives: a key mentioned in passing linked Superior Bridge to Mannik & Smith's
*Mowish Property Drainage* design agreement.

### 11.5 Supplements and invoices

* **Supplements.** For every linked agreement, its `SupplementsCA` rows are listed. A supplement counts
  as found when its `Supp_Num` is among the unit's supplement numbers.
* **Invoices.** Each invoice document is compared with the `InvoicesCA` / `InvoicesM` / other-division
  invoices of the unit's linked agreements:
  1. **By number.** The vendor invoice #, the `#…` filename reference or the `Invoice #n` filename
     reference equals the DB `Invoice_Number` after removing punctuation and leading zeros (at least 2
     characters).
  2. **By amount and date.** The current amount equals `Invoice_Amount` exactly, with the invoice date
     within 20 days where both dates are known.

## 12. Results

### 12.1 Units linked to the database

| Unit kind | Units | Linked | Why the rest are not |
|---|---|---|---|
| Statewide assignment | 442 | 237 | 2015–2019 statewide programs have no DB rows; 2021+ assignments without a firm umbrella row in the DB |
| Firm master | 203 | 83 | 2015–2019 and 2020 masters are not in the DB; 2023-2024 masters link to their district umbrellas |
| District agreement (2018, 2020) | 93 | **0** | The DB has no district-specific agreements |
| Project agreement | 79 | 44 | Older (2018–2020) and newest (2025–2026) projects are missing from `AgreementsCA`; some folders hold procurement only |
| D12 construction contract | 8 | 0 | Construction contracts are not consultant agreements |

| Primary method | Units |
|---|---|
| District umbrella + consultant | 184 (+ 4 amount-corroborated) |
| Project key + consultant | 32 (+ 39 amount-corroborated, + 3 demoted but still primary) |
| Master → district umbrella | 42 |
| MCS&T category master + consultant | 44 |
| Folder name ≈ Hub name + consultant | 6 (+ 4 amount-corroborated) |
| Folder name ≈ Hub name, consultant from DB | 5 |
| Master → CA program key | 1 |
| **Total** | **364** (High 120, Medium 244) |

### 12.2 Database coverage

* **`AgreementsCA`: 127 of 130 found.** Three rows have no folder in the export:
  * `2017001275-100-A` AMT, Parkersburg–St Marys Rd;
  * `2024990304-860-A` 2LMN, CA statewide CEI;
  * `2024170018-1-A` GFT, Clarksburg Hub rail-trail.
* **`AgreementsM`: 40 of 58.** The 18 missing are the 16 **2022** MCS&T masters (`2024990286`–`292`),
  since the export's Materials folder is 2025-2026 only, and two 2025 masters with no folder (Baker
  pavement testing, Ascent materials facility).
* **`SupplementsCA`:** the supplement number is visible in the linked unit's folders for 56 of 78. For
  the other 22 the agreement is found but that supplement number isn't filed under it.
* **`InvoicesCA`: 46 of 68 matched to an export invoice.** Of the 22 unmatched:
  * 14 belong to agreements whose export units hold **no invoice documents at all** (project-specific
    invoices are evidently filed elsewhere);
  * 7 are on units with invoices, but not those invoices;
  * 1 is on the GFT agreement, which isn't in the export.
* **`InvoicesM`: 0 of 211.** The Materials folder contains no invoices.

### 12.3 In the export but not in the database

* All **2015–2020** statewide, district (93 units) and project agreements before the 2016–2019
  `AgreementsCA` rows, with their invoices. Every invoice before 2023 is here and not in `InvoicesCA`.
* Individual **letter agreements** under the 2023-2024 statewide masters. The DB keeps one umbrella row
  per firm per district, carrying one letter agreement's amount (§3).
* **GPI's 2025-2026 CEI Materials Facility Testing & Sampling master** (`MAT/GPI`), which has no
  `AgreementsM` row.
* Every agreement of **Quinn Consulting**, **L.R. Kimball** and **Advanced Asphalt Technologies**, which
  have no consultant number.
* 1,002 consultant evaluations. 559 of them are tied to a likely unit of the same firm by filename
  similarity (token_set_ratio ≥ 70); this link is informational.

### 12.4 Exceptions sheet

820 rows:

| Exception | Rows |
|---|---|
| Unit without a DB agreement (with the reason: no project key; key under another consultant; no DB agreement on the key) | 333 |
| Invoice without a current amount | 196 |
| Unclassified document | 180 |
| Document with no readable text (excluding design files, images and zip containers) | 109 |
| Unit without a consultant | 2 |

## 13. Validation

### 13.1 Spot checks

| Unit | Evidence in the documents | Linked DB agreement | Result |
|---|---|---|---|
| 2023-2024 CEI & QAM / CDM Smith / D4_Office Manager | Supplement memo: prior maximum payable $283,761.14 | `AgreementsCA#250 2024840014-155-A` (D4 umbrella), $283,761.14 | Correct; High through amount |
| 2023-2024 CEI & QAM / GAI / D8_Greenawalt Gap Bridge | BF-2 original agreement $252,424.06, but the state project printed is Armilda's | `#322 2021000428-195-A` Greenwalt Gap, $252,424.06 | Correct after demotion of the copied key; High |
| 2023-2024 CEI & QAM / GAI / D1_Various Projects | A D2 Armilda key in one document | `#219 2024810014-195-A` D1 umbrella; Armilda kept as a secondary (cross-district) | Correct |
| 2023 Project Specific / D10 – Princeton Overhead Bridge | Agreement header `CID: 2017001624`, WRA, DocuSign 10/21/2023 | `#345 2017001624-405-A`, distributed 2023-10-21 | Correct; High |
| 2023-2024 CEI & QAM / Mead & Hunt / D1_SW Jill Micah Hess Memorial Bridge | Letter-agreement memo maximum payable $396,037.60 | `#222 2020000550-270-A` Jill Micah Hess Mem Br, $396,037.60 | Correct; High (an invoice in the folder carries the Airport Rd key, which was demoted) |
| 2023-2024 CEI & QAM / HNTB / D4_Hutchinson Truss Project | Selection memo 2024-05-04, HNTB selected | `#263 2020000595-225-A`, distributed 2024-05-15 | Correct; High |
| 2023-2024 CEI & QAM / Stantec / D6_Monument Place Bridge | Maximum payable $439,878.69 | `#302 2000001398-350-A`, $439,878.69 | Correct; High |
| 2023-2024 CEI & QAM / TRC / D9_Hico Bridge | Project key, TRC | `#328 2020000590-390-A`; 2 of its 23 DB invoices matched | Correct; High |
| 2023 Project Specific / D4 – Bristol Bridges EB & WB | Maximum payable $3,551,907; ICE selected | `#252 2020000589-61-A`, $3,551,907 | Correct; High |
| 2021 Project Specific / D2 – Mountain View to Gilbert | Procurement files only | `#231 2018000238-275-A` Mtn View to Gilbert (Baker), by name | Correct; Medium, consultant from DB |
| 2021 Project Specific / D1 Carter / Brooks IC | Procurement files only | `#209 2014000011-200-A` Carter Br – Brooks St I/C (GPI), by name | Correct; High |
| 2023-2024 CEI & QAM / Michael Baker / D2_Area Engineer | Folder firm and district | `#233 2024820014-275-A` D2 umbrella | Correct; Medium (umbrella) |

### 13.2 Amount agreement

For the 75 units that have both a maximum payable in their documents and an amount on the primary DB
agreement, the two are equal in 40.

* **Most of the 35 differences are umbrella rows.** The umbrella's single amount belongs to a sibling
  letter agreement. CDM Smith's D4 umbrella equals the Office Manager assignment, so its other D4
  assignments differ.
* **The rest are project agreements whose latest amount in the export precedes or follows a
  supplement.** For example, John Nash Blvd's documents show $2,656,820 against the DB's $3,943,360.

### 13.3 Iterations

Three draft builds were audited before this one; each change is in the scripts:

* Engineering Division matches moved to information only.
* Name matching added; it recovered 8 `AgreementsCA` rows.
* Amount corroboration and district/name demotion added.
* The BF-2 amount pattern widened for the older layout and for `$` followed by several spaces. Current
  amount coverage went from 73% to 88%.
* "I/C" normalised before slashes are split.
* The program-kind field renamed so it no longer overwrote the document kind.

## 14. Limitations

* **Text depth.** PDFs are read to page 3 and scans to page 2. Anything later (compensation articles,
  rate tables, invoice detail) is not read.
* **OCR quality.** 200 dpi greyscale is adequate for typed forms and weak for faint copies and
  handwriting. OCR'd amounts and dates can be wrong: always check the linked PDF before relying on an
  OCR'd value.
* **Attachments and images.** E-mail attachments that are scans were not OCR'd, and inline images were
  ignored.
* **Classification is rule-based.** 180 documents are "other", and scanned agreement/supplement pairs can
  swap types (§7.3).
* **Firm aliases are regular expressions.** A firm word inside a project name can add a false vote, e.g.
  "Martin" in *Clarence Martin Jr Memorial Bridge*. It never overrides a folder-name firm, but it can
  appear in the documents' "Firms named" column.
* **Umbrella links are coarse.** "District umbrella + consultant" (Medium) says the assignment was
  administered under that firm's district umbrella row; it does not mean the DB holds this assignment on
  its own.
* **Name matching can confuse similarly named bridges.** It requires a shared distinctive word and a
  score of at least 85, and stays Medium unless an amount corroborates it.
* **Invoice matching needs the invoice filed in the export.** Most DB invoices on project-specific
  agreements are not (§12.2). Duplicate copies of one invoice are counted once per unit only when their
  numbers normalise alike.
* **2015–2016 AASHTOWare contract numbers** are not in the AWP tables, so those job folders reach TheHub
  only through state project numbers or names in their documents.
* **Hyperlinks** are `file:///Volumes/SSD/CF_Export/…` and open only where the SSD is mounted at that
  path. Zip members and attachments link to their container.
* **Snapshot date.** Database rows are as of 2026-09-11. Rerun `snapshot_db.py` and `cfbuild.py` to
  refresh the links without re-reading the export.

## 15. Reproducing the run

```bash
W=/path/to/workdir; ROOT=/Volumes/SSD/CF_Export; R=research/cf-export-2026-09-11
( cd "$ROOT" && find . -type f | sed 's|^\./||' | sort ) > "$W/files.txt"
( cd "$ROOT" && find . -type d | sed 's|^\./||' | sort ) > "$W/dirs.txt"

python3 -m venv "$W/venv"
"$W/venv/bin/pip" install openpyxl extract-msg xlrd rapidfuzz python-docx
# system tools: poppler (pdfinfo, pdftotext, pdftoppm), tesseract, antiword; macOS textutil

python3 "$R/extract_pdf.py" "$W"                     # pass 1
"$W/venv/bin/python" "$R/extract_other.py" "$W"      # pass 2
python3 "$R/ocr.py" "$W"                             # pass 3
( cd backend && .venv/bin/python "../$R/snapshot_db.py" "$W" )   # needs the 1434 tunnel

cp "$R"/cf*.py "$W/"
"$W/venv/bin/python" "$W/cfmap.py" "$W"              # stage 1 → docs.jsonl
"$W/venv/bin/python" "$W/cfbuild.py" "$W" cf-export-agreement-invoice-map-YYYY-MM-DD.xlsx "$R/summary.json"
```

## 16. Workbook guide

| Sheet | Rows | One row per | Key columns |
|---|---|---|---|
| README | – | – | What each sheet is |
| Summary | 40 | Program | Documents, files, no-text, OCR'd, units, units with firm, units with DB agreement, instruments, invoices, invoices matched, fee proposals, selection memos, procurement documents, e-mails, evaluations |
| **Agreements** | 825 | Agreement unit | Unit folder (hyperlink); program; kind; assignment; district; materials category; consultant (+ source, #); document / instrument / invoice / supplement counts; supplement #s and years; project key and Hub name and state project; state/federal project numbers in the documents; AASHTOWare contract; first/last instrument; latest maximum payable; first/last invoice; invoiced (unique); billed to date; **primary DB agreement, method, confidence, DB consultant, DB project, DB amount, DB distributed**; other linked DB agreements; weak candidates; DB supplement #s; DB invoices on linked agreements / matched; same key under another consultant; Engineering Division agreements (info); consultant votes |
| Instruments | 4,293 | Agreement-type document | Type and basis; unit; consultant; consultant named in text; agreement title; master agreement; memo subject; supplement #; executed / memo / original agreement / filename dates; maximum payable; amount added; not-to-exceed; CID; Hub keys; state/federal project; selected; alternates; text source; pages |
| Invoices | 1,593 | Invoice document | Format (BF-2 / vendor); vendor; invoice # (text and filename); invoice / filename dates; period; previous / current / to-date; original agreement; supplementals; maximum payable; % expended; BF-2 project name; state / federal project; vendor number; remit ID; vendor project #; Hub keys; unit project key; **matched DB invoice** (table, agreement, #, date, amount, paid) and how |
| Documents | 14,321 | Document | Path (hyperlink); program; kind (file / zip member / attachment); extension; bytes; pages; text source; type and basis; level; unit; consultant; district; folder roles; supplement #; best date; Hub keys; state / federal project; AASHTOWare contract; firms named; e-mail or DocuSign subject; evaluation → likely unit and score |
| Folders | 1,983 | Folder | Depth; name; role; program; unit; consultant; district; files here; files below; top document types below |
| DB_Agreements | 189 | DB agreement (all CA and M, plus any other division row linked) | Table; SQL_id; agreement #; project key and Hub name; consultant # and name; amount; distributed; org date; selection; fee type; prequal; separate-project flag; closed; PAG; DB invoice / supplement counts; **in export?**; export units; how |
| DB_Invoices | 279 | DB invoice (all CA and M, plus invoices of any linked agreement) | Agreement; invoice #; date; amount; work period; keyed; paid; PAG; agreement status; invoice documents in linked units; **matched export document**; how; why unmatched |
| DB_Supplements | 78 | `SupplementsCA` row | Supplement #; master; amount; date; export units; status |
| Consultants | 57 | Canonical firm | Engineering consultant #(s); DB names; folder aliases (file counts); units; documents; invoices; instruments; `AgreementsCA` / `AgreementsM` rows; units linked |
| Projects | 602 | TheHub project found in the documents | Name; district; county; state project; umbrella flag; documents; units; DB agreements on the key |
| Exceptions | 820 | Issue | Issue; item (hyperlink); program; detail |

## Appendix A: program and umbrella keys

| Key | TheHub project | Used for |
|---|---|---|
| `2024810014` `2024820014` `2024830012` `2024840014` `2024850014` `2024860017` `2024870013` `2024880016` `2024890016` `2024900010` | D1 … D10 – Statewide Construction Engineering Inspection | CEI/QAM statewide assignments, by district |
| `2024810015` `2024820015` `2024830013` `2024840015` `2024850015` `2024860018` `2024870014` `2024880017` `2024890017` `2024900011` | D1 … D10 – Statewide Coatings | Coatings statewide assignments, by district |
| `2024990229` / `2024990230` | Contract Administration 2023 / 2024 Statewide CEI & QAM | CA program-level agreements (Baker CPM / program support) |
| `2024990304` | CA – Statewide Construction Engineering Inspection | 2LMN |
| `2024990293` AMT, `…294` CAP, `…295` ENG, `…296` ENV, `…297` LAB, `…298` MAT, `…299` PAV, `…300` SAM, `…301` AST | MCS&T 2025 statewide masters by category (asphalt materials testing, cathodic protection, engineering services, environmental assessment & remediation, environmental lab testing, CEI materials facility testing & sampling, pavement testing, sampling & inspection, UST/AST) | Materials units |
| `2024990286`–`2024990292` | MCS&T 2022 statewide masters | Not in the export |
| `2018000692`, `2019000041` / `2018001047`, `2019000052` / `2018001122`, `2018001330` / `2019000694` | QAM Services 2018/2019 · Statewide Const Insp Services · Bridge Coating Assessment · Resurfacing Inspection Services (D1) | Recognised as program keys; no DB agreements on them |

## Appendix B: canonical consultants

Engineering consultant numbers are in parentheses.

* **Inspection and CEI firms:**
  * 2LMN (860);
  * A. Morton Thomas / AMT (100);
  * AECOM (105);
  * Alpha Associates (115);
  * CDM Smith (155);
  * Civil & Environmental Consultants / CEC (165);
  * CTL Engineering (740, 60);
  * E.L. Robinson / ELR (175);
  * EXP (945);
  * GAI (195);
  * Gannett Fleming (59);
  * Greenman-Pedersen / GPI (200);
  * GFT Infrastructure (960);
  * HNTB (225);
  * ICE (61);
  * J.B. Turman (230);
  * KTA-Tator (630, 62);
  * L.R. Kimball (none);
  * Mannik & Smith Group (375);
  * Martin Engineering (265);
  * Mead & Hunt (270);
  * Michael Baker International (275);
  * Monaloh Basin Engineers / MBE (595);
  * Potesta (315);
  * Quinn Consulting (none);
  * RK&K (330);
  * S&ME (545);
  * Specialized Engineering (63);
  * Stantec (350);
  * Summit Design and Engineering (775);
  * Terracon (560);
  * Terradon (370);
  * The Thrasher Group (385);
  * TRC Engineers (390);
  * Triad Engineering (570);
  * Volkert (820);
  * Whitman, Requardt & Associates / WRA (405).
* **Materials and laboratory firms:**
  * Advanced Asphalt Technologies (none);
  * ALS Group (67);
  * Applied Research Associates (68);
  * Ascent (69);
  * Bureau Veritas (71);
  * Elzly Technology (72);
  * EnviroProbe (183);
  * Greenbrier Environmental Group (620);
  * HRV Conformance Verification (73);
  * Infrasense (74);
  * Kemron (75);
  * Pace Analytical (300);
  * Pennoni (530);
  * Quality Engineering Solutions / QES (76);
  * Resource International (77);
  * Superior Services (84, 79).
* **Construction contractors,** tagged and never linked: American Bridge, Walsh Construction, A&A Safety,
  Scodeller.
