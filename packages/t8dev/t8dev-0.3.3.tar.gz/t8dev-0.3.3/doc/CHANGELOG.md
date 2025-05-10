Changelog
=========

This file follows most, but not all, of the conventions described at
[keepachangelog.com]. Especially we always use [ISO dates]. Subsections or
notations for changes may include Added, Changed, Deprecated, Fixed,
Removed, and Security.

Release version numbers follow the [Python packaging
specifications][pyver], which are generally consistent with [semantic
versioning][semver]: are _major.minor.patch_ Development versions use the
version number of the _next_ release with _.devN_ appended; `1.2.3.dev4` is
considered to be earlier than `1.2.3`.

On any change to the programs or libraries (not, generally, the tests), the
previous release version number is bumped and `.devN` is appended to it, if
this hasn't already been done. A `.devN` suffix will stay until the next
release, though its _N_ need not be bumped unless the developer feels the
need. Notes marked "API" indicate breaking API changes.

Releases are usually tagged with `vN.N.N`. Potentially not all releases
will be tagged, but specific releases can also be fetched via the Git
commit ID.

For release instructions, see [cynic-net/pypi-release] on GitHub.

### dev

### 0.3.3 (2025-05-10)
- Fixed: Syntax error in `cmpasl`.

### 0.3.2 (2025-05-10)
- Fixed: Add some missing dependency checks for `toolset` modules.
- Changed: Symbols now case-sensitive in `cmpasl` assembly.
- Changed: `z80dasm-clean` improved and renamed to `intel-disassm-clean`.

### 0.3.1 (2025-04-28)
- Fixed: Updated `pactivate` to 0.5.7 for zsh support when sourced standalone.
- Added: `MBytesIO` object in `testmc.generic` with additional API
  convenience methods that improve how our tests read.
- Added: ROM sources for CSCP Sharp MZ-700 emulators.
- Fixed: `p2a2bin` now handles files that load above $7FFF.
- Fixed: `t8dev pytest` now tests everything under $T8_PROJDIR when given
  no file/dir args, and better checks for file/dir args.
- Fixed: minor fixes to `cmpasl`.
- Added: `z80dasm-clean` stand-alone script extracted from `cmpasl`.
- Added: `disx` disassembler toolset

### 0.3.0 (2025-02-16)
- Added: `t8dev buildtoolset ctools` for Commodore 64/128 CP/M disk images.
- Changed: `t8setup.bash` now leaves the first `--` option in `$@` so that
  the caller can see it, if it needs the separator for its own purposes.
- Changed: new toolset.bm2 download location
- Added: `t8dev emulate runcpm` now copies files to the "disks" and can
  optionally auto-run the first file given.
- Added: In `testmc.generic.machine`, `stepto()` now has an optional `addr`
  (start address) parameter, and `stepto()` and `call()` have an optional
  `nstop` (number of times to see a stop point before returning) parameter.
- API: tmc BIOS docs now clarify that `prchar` may destroy A, and the
  implementation deliberately changes A to aid in detecting client bugs.
- API: t8dev subcommands reworked (use `-h` to see new formats)
- Fixed: Path specified with `-P`/`--project-dir` option now exported to
  environment as `T8_PROJDIR`.
- Added: `Test` script to run pytest tests for this repo, using a "parent"
  T8_PROJDIR or as a stand-alone test. This needs further development.
- Added: VirtualT (Tandy Model 100 and family) emulator.
- Fixed: Two instances of Python 3.9 incompatibility in t8dev and testmc.
- Fixed: t8dev.toolset.asl now uses `main` branch Makefile.def, which
  has been fixed to work on ARM (Mac) CPUs.
- Fixed: Various fixes for better Bash 3/MacOS compatibility.

### 0.2.0 (2024-11-04)
- API: `testmc.*.Machine.call()` now executes return instructions, rather
  stopping on them. This should not affect most users, but it can be a
  breaking API change for certain kinds of tests.
- API: `bios.*` files renamed to `biosdef.*`.
- API: `t8setup.bash` no longer installs Python packages in subdirs.
  Instead add them explicitly to your `requirements.txt`

### 0.1.3 (2024-11-04)
- Fixed: testmc.i8080 INC r/DEC r now correctly preserves CY flag instead
  of clearing it. (Only the logic ops, AND etc., should clear that flag.)
- Fixed: testmc.i8080: RST now pushes return address on stack.

### 0.1.2. (2024-10-24)
- Fixed: t8setup.bash no longer adds `[all]` to local `t8dev` install

### 0.1.1 (2024-10-24)
- Changed: No more need for `t8dev[all]`; all optional req's now standard.
- Added: iomem now throws an exception if an I/O function attached to a
  memory addess returns a bad value (not int or int out of range) on read.
- Fixed: tmc now returns exitvalue if exitport is read so that the
  command-line simulator doesn't die if you read that address.

### 0.1.0 (2024-10-20)
- Breaking API change: testmc.pytest.fixtures.loadbios() now does not
  require (though still can optionally accept) a BIOS name. See commit
  messge for full details.

### 0.0.6 (2024-10-20)
- Fixed: mos65 simulator throws ModuleNotFoundError for py65 only if it's
  actually used. (This fixes `t8dev[toolset]` and similar installs.)

### 0.0.5 (2024-10-20)
- Added: Simulator/unit test BIOS source code and `t8dev aslt8dev` command
- Added: `tmc` program for command line simulation of any CPU simulator,
  replacing `tmc6800` which did only mc6800 simulation.
- Changed: `tmc` simulator now uses output to a port to request exit.
- Updated: New version of `bm2` Basic Master Jr. emulator
  (old version no longer downloadable from that site).
- Added: Shell scripts from `bin/` added to distribution package.
- Added: bin/cmpasl script to assemble a disassembled binary and compare
  with the original

### 0.0.4 (2024-09-22)
- Fixed: `t8dev emu` no longer tries to use `wine` on Windows

### 0.0.3 (2024-08-28)
- Fixed: The locations whence to download TK-80BS ROM images have changed.
- Changed: The `pytest_pt` module is no longer included under `psrc/`;
  instead it's now a runtime dependency. (See `pyproject.toml` for an
  explanation of why it's a runtime instead of development dependency.)
- Changed: When building ASL from `asl-releases`, use branch `upstream`
  instead of `dev/cjs/master`; thus you now always get the latest version.
  (There is currently no facility to request an earlier version except to
  tweak the source code.)

### 0.0.2 (2024-07-30)
- Added: CSCP emulator suite `tk80bs` ROM configuration (BASIC SYSTEM) and
  `tk80` alternate ROM configuration (base system).
- Fixed: Various `t8dev emulator cscp` UI improvements.

### 0.0.1 (2024-07-21)
- Added: `t8setup.bash` can now be run without setting $T8_PROJDIR if the
  current or higher directory appears to have a virtualenv with t8dev
  installed.
- Changed: Use Python packaging dependency management so that the
  user no longer needs to put t8dev dependencies in `requirements.txt`.
- Added: Add [CSCP] emulators to toolsets.
- Added: `t8dev emulator` command.

### 0.0.0 (2024-04-23)
- Initial PyPI release for testing; proper documentation not available.



<!-------------------------------------------------------------------->
[ISO dates]: https://xkcd.com/1179/
[cynic-net/pypi-release]: https://github.com/cynic-net/pypi-release
[keepachangelog.com]: https://keepachangelog.com/
[pyver]: https://packaging.python.org/en/latest/specifications/version-specifiers/#version-specifiers
[semver]: https://en.wikipedia.org/wiki/Software_versioning#Semantic_versioning

[CSCP]: http://takeda-toshiya.my.coocan.jp/common/
