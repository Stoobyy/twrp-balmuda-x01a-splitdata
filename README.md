# X01A custom split-data TWRP

For this converted A101BM/X01A unit only. Separate local repository derived from the generic tree; no GitHub remote is configured. Decryption is intentionally disabled. This build is intended for selecting the correct partitions before a separately approved slot-B data reset.

| Partition | Physical node | Bytes |
|---|---|---:|
| metadata_a | sda6 | 16777216 |
| userdata_a | sda22 | 54224453632 |
| userdata_b | sda24 | 54223470592 |
| metadata_b | sda25 | 16777216 |

TWRP uses unsuffixed userdata and metadata paths with `slotselect` on both entries. Slot A selects the A pair; slot B selects the B pair. There is no partition named data_b: Android /data is backed by userdata_b on slot B. Do not switch slots while data or metadata is mounted; reboot into the intended slot and verify recovery.log and resolved block paths before a destructive operation.

## Validation and evidence

Read the supplied README-per-slot-data.md, both FLASHING-SLOT-B guides, the generic build README, device research README/FINDINGS, and dump manifest. Live read-only checks on 2026-11-06 confirmed slot A active, /metadata on metadata_a and /data on dm-13 backed by sda22. GPT primary/backup CRCs, matching entry arrays, ranges, and non-overlap passed. Live sysfs uses 512-byte units, while GPT LBAs use 4096-byte sectors.

Live GPT names, ranges, and sizes agree with the saved split layout. Attributes differ: metadata_a and userdata_a now have bit 50 set; the saved proposal had zero. No GPT changes were made or assumed necessary.

Kernel, DTB and recovery DTBO were extracted from the live recovery_b image. Their hashes are recorded in evidence/recovery-header.json; they differ from the generic prebuilts. Header v2, 4096-byte pages, offsets and command line match the device. Recovery header OS/patch is kept at the live B values, 11.0.0 / 2023-02-01, replacing the generic artificial 2099 patch date. The current A recovery reports a different patch date. This does not establish bootloader rollback policy.

Super size is 13958643712 bytes and the B dynamic group maximum is 6438256640 bytes. Both lpdump slots contain B COW entries, while active A snapshot directory is empty. Their lifecycle remains uncertain; do not delete or merge them without investigating before installing LineageOS.

Removed generic removable-media entries: sda1 is internal ssd, not USB storage; the MicroSD node was unverified. MTP remains disabled. Backlight max 255 was confirmed live. No crypto support is promised or required for the requested future B reset.

## Build

Run `python tools/validate.py` locally. After a separately approved push to a NEW GitHub repository, manually run the build workflow. It syncs twrp-12.1, builds twrp_X01A_splitdata-eng, checks output size and uploads an artifact. No workflow runs automatically and none flashes a phone. A full build has not been run locally; runner capacity, upstream changes, generated ramdisk contents, boot, fastbootd and wipe behavior still need validation. A/B/Virtual A/B build support is retained for compatibility, not authorization to install OTA zips.

The phone was on slot A during inspection. A wipe in that state would target main data. No flash, wipe, reboot, slot change or push was performed. Future slot-B formatting must verify BOTH userdata_b and metadata_b and obtain explicit approval. Do not use fastboot -w, flash whole super, install A/B OTA zips, or write firmware. Follow the supplied slot-B guides for a later LineageOS/GSI plan.

Upstream implementation checked: https://github.com/TeamWin/android_bootable_recovery/blob/android-12.1/partition.cpp and partitionmanager.cpp; build packing checked against TeamWin/android_build android-12.1 core/Makefile. Full successful compilation and device testing remain required.
