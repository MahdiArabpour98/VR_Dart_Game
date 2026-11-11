# VR Dart Stage 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Steps use checkbox syntax.

**Goal:** Produce a minimal saved dart lab and establish actual Android build readiness without requiring a connected headset.

**Architecture:** Preserve the XR template and author only new DartLab content. Stage 1 has static dart geometry; throwing and the native simulation belong to subsequent stages. Use an Unreal Python commandlet against the same project so the user's unsaved editor state is preserved.

**Tech Stack:** UE 5.8.3, existing OpenXR/Enhanced Input Blueprint template, Unreal Python, Android SDK tools.

**Spec:** 2026-11-11-vr-dart-design.fa.md

## Global Constraints

- Standalone Meta Quest 2, Touch controllers; Android packaging is the headset deliverable, no phone edition.
- One map, one dart, one board; no scoring, menus, multiplayer or aiming assistance.
- Preserve existing assets and unrelated staged changes.
- User selected work in the same open project, without a worktree.
- No headset currently available: installation, tracking, performance and feel acceptance remain pending.
- Build, C++ Compile, Blueprint Compile, desktop checks and headset checks are reported separately.

## Review Focus

- Unsaved editor work must survive scene authoring: use a separate commandlet and never save all dirty assets.
- Re-running scene creation must not overwrite existing DartLab work: fail if destination already exists.
- Static placeholders must not be reported as working grab/throw interactions.
- Missing Android SDK components must not be mistaken for a game-code build failure.
- No device must not prevent authoring and desktop verification or be reported as device success.

## Task 1: Establish Android readiness

Files: logs under interaction/dart/stage1; no global environment changes.
Interfaces: consumes Engine/Config/Android/Android_SDK.json; produces installed-package inventory and actual SDK validation result.

- [x] Read project state, engine requirements, Java and installed packages; run adb devices.
- [x] Attempt installing the exact missing SDK packages with the existing sdkmanager.
- [ ] Diagnose and record download failures; run Turnkey VerifySdk without installing or changing versions implicitly.
- [x] Keep build/installation incomplete if prerequisites remain missing; continue Task 2 independently.

## Task 2: Author and verify the static lab

Files: tools/dart/create_stage1_lab.py; target Content/DartLab/Maps/L_DartLab.umap; report interaction/dart/stage1/map-report.json.
Interfaces: Python main() creates the new map, validates authored dimensions/actors/collision/game mode, and writes a structured report. It does not implement throwing.

- [x] Check existing asset, dirty editor state and template availability before mutation.
- [x] Create a simple floor, lighting, player start, fixed board and one composite static dart; keep existing XR GameMode.
- [x] Validate map name, board diameter, board distance/height, disabled simulation and collision, floor support and template references. Dart overall dimensions still need detailed geometry acceptance in stage 2.
- [x] Save only the new map. Reopen it in a fresh commandlet to verify persistence independently.
- [x] Read actual output and report verified geometry separately from play testing.

## Task 3: Handoff and evidence

- [ ] Record commands, outcomes, limitations and next headset checks in the ledger.
- [ ] Report stage as partial until Android build/device acceptance is possible; do not continue to throw implementation in this stage.

## Execution ledger

- Ruling: execute inline in the user's existing project as explicitly requested; no worktree.
- Ruling: separate commandlet authoring protects the open editor's two unsaved packages; do not switch its map or save its state.
- Ruling: no native module in stage 1; the approved C++ simulation begins in stage 2, after the static baseline. No C++ compilation claim will be made.
- Android attempt: sdkmanager failed to fetch official Google manifests; verbose trace reports FileNotFoundException for repository2-2.xml. SDK36/NDK27c not installed by that attempt.
- SDK validation: Unreal's actual ValidatePlatforms startup reports `Win64 VALID 10.0.22621.0` and `Android INVALID r27c`. A separate Turnkey VerifySdk has not run; no Android Build or package is claimed.
- Test RED: valid forward-slash commandlet invocation failed with `Dart lab map does not exist` before asset creation. Earlier backslash invocations failed at script loading and do not count as test execution.
- Persistence regression: initial saved dart loaded with BlockAll despite setting CollisionEnabled; diagnostic confirmed its profile. Fixed by persisting NoCollision profile, including a narrow migration script for the newly authored map.
- Test GREEN: fresh commandlet `test_stage1_lab.py`, exit 0, `DART_LAB_VERIFY PASS`; geometry/configuration assertions passed. NullRHI verification does not prove rendering or playability.
- User instruction: no physical headset is currently available; proceed with independent work and defer device acceptance.
- User instruction: GitHub Desktop, VR_Dart_Game repository, main branch. Desktop confirmed main and clean state before changes. No Git CLI mutations for this stage.
- Independent review: no critical static-baseline issue; missing project guard in repair was important. Added project and commandlet guards to protect matching maps in other projects and unsaved interactive editor state.

