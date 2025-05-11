# Katsuo

Katsuo is a library of components and utilities for [Amaranth](https://amaranth-lang.org/).

## Policy

Katsuo intends to align with Amaranth conventions and best practices and will follow development of the Amaranth project.

Katsuo does not intend to duplicate functionality found in Amaranth, and will deprecate functionality if/when the equivalent is released in Amaranth.

## Subprojects

The `katsuo` package is a metapackage not containing any functionality by itself.
You can depend on `katsuo` to pull in the whole collection of subprojects, or only on the specific subprojects you need.

### [katsuo.stream](https://github.com/zyp/katsuo-stream/)

Stream components and utilities to complement `amaranth.lib.stream`.
