# Catalog contract

`collections.json` conforms to `collections.schema.json`. Schema version 1 has:

- a unique kebab-case collection `name`;
- a non-empty `description`;
- optional unique direct `skills`;
- optional unique collection `includes`.

At least one of `skills` or `includes` is required. All references must exist,
include graphs must be acyclic, expanded skills must be unique, and expansion
preserves declaration order. Aggregate collections such as `game-dev` have no
runtime meaning. The README command block is a deterministic rendering of the
expanded catalog.

`skills.json` schema version 2 distinguishes frozen Geremmyas migrations from
Storehouse-owned skills. It preserves the Geremmyas source commit, license
evidence, per-skill hashes, security classification, compatibility, and
migration dispositions. Storehouse-owned skills have no external origin record:
their current files and Git history are authoritative.
