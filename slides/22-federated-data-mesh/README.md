# Slide 22 · Federated data mesh

> **Revised deck.** The revised deck (2026-10-31) replaces the three placeholders (`c1`–`c3`, superseded) with an iRODS permission diagram (claims `c5`–`c10`).

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-22)

## Findings (checked 2026-10-31)

The iRODS mechanisms on the slide are real and documented. Two things need care: (1) MESA's public docs do not yet describe agents running under a separate read-only account (the hosted Formation connector acts *as the user* and can delete), so present the diagram as the design, not as what every MESA agent does today; (2) "audit log" and "no deleted datasets" depend on optional configuration, not iRODS defaults.

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| `c4` Notes: one namespace, rules on ingest, no deletes, data stays put | partially supported | Unified namespace and PEPs on every operation (f1, f4); `irm` moves to trash by default, `-f` bypasses (f9) | "iRODS gives one namespace over storage at different institutions, and a policy engine whose rules can fire on ingest and refuse deletes. Your data stays where it lives." |
| `c5` Agent has own read-only account; writes denied and logged | partially supported | `read_object` alone cannot delete/move/overwrite (f12); but Formation "acts as that user" with `delete_data` (f19, f20); mesa-sandbox untested on a cluster (f23, developer-reported) | "Give the AI agent its own iRODS account with read rights only. Deletes, overwrites and permission changes are refused, whatever its intent; turn on auditing to log them." |
| `c6` MESA gate: pre-check on every request | partially supported | PEPs checked before every operation; failing `_pre` stops it (f4–f6); delete has `pep_api_data_obj_unlink_pre` (f7); rule sees user and zone (f8). "MESA gate" not on the public site; MESA's deployment only checkable in code | "Policy gate: iRODS checks each request before it runs: who is asking, what rights they hold (own, modify, read), which zone and path." |
| `c7` Audit log; federated zones keep own catalogs and rules | partially supported | Federation: independent zones, one iCAT each (f16–f18). Audit: optional AMQP plugin, not on by default (f15) | "With iRODS auditing on, every call is recorded. Federated zones share data but keep their own catalogs and rules." |
| `c8` Rights: own, modify or read (new) | supported | iRODS 4.3 has 10 levels; own/modify_object/read_object are the common three (f10, f11) | — |
| `c9` Owner can edit, move, delete and share (new) | supported | Owner has full control and can grant access (f13, f14) | — |
| `c10` Footer NSF Award #2632685 (new) | supported | NSF Award API: MESA, UNM, PI Swetnam, 2026-07-15 to 2029-05-31 (f24) | — |

Small inconsistency in the notes: "one policy engine across storage at different institutions" vs "zones keep their own catalogs and rules". Both are true at different levels (one engine per zone; each federated zone has its own).

## Evidence

- `src/01_fetch.py` — fetches iRODS 4.3.4 docs, MESA public pages (Markdown twins) and the NSF award record into `data/raw/sources/` (gitignored, logged in `MANIFEST.yaml`).
- `src/02_facts.py` — writes [`data/raw/research/facts.csv`](data/raw/research/facts.csv) and checks every quote appears verbatim in the fetched text ([`data/processed/quote_check.csv`](data/processed/quote_check.csv): 25/25 found).
- Not checked: MESA source code (whether MESA zones deploy agent accounts, pre-PEPs or the audit plugin).
