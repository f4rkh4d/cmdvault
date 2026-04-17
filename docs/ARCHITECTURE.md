# Architecture

## Overview

cmdvault is organized as a small, focused Python package. Core logic lives in
`src/cmdvault/`; CLI glue is kept thin and delegates to pure functions that are
easy to test in isolation.

## Modules

See `src/cmdvault/` for the current module layout. Each module has a single
responsibility and a public API surface that the CLI depends on.

## Testing

Tests mirror the source layout under `tests/`. Fixtures live near the tests
that use them. Integration tests exercise the CLI end-to-end via `CliRunner`.
