# V4 Progress

## Final checkpoint status

| checkpoint | status | result |
| --- | --- | --- |
| V4.0 | PASS | V1/V2/V3 baseline and dependency inventory green |
| V4.1 | PASS | MapChip native surface recovered |
| V4.2 | PASS | MapChip projection, anchor, and floor culling closed |
| V4.3 | PASS | MapChip numeric resource, SEB, and extension semantics closed |
| V4.4 | PASS | ObjChip native surface and direction mapping closed |
| V4.5 | PASS | ObjChip wall, door, and selected object routes closed |
| V4.6 | PASS | FurnitureData selector binding and selected composition closed |
| V4.7 | PASS | Minimum Camera transform boundary closed |
| V4.8 | PASS | Local ordering and depth boundary closed |
| V4.9 | PASS | Isolated V4 compatibility adapter typechecks |
| V4.10 | PASS | Fixture matrix, command parity, and 20 focused tests green |
| V4.11 | PASS | Full regression/build/documentation gate green; stop before V5 |

## Deliverables

- Evidence: `knowledge/fixtures/accepted/visual-port/v4/`.
- Isolated adapter: `runtime/social-dev/src/v4/`.
- Focused tests: `runtime/social-dev/tests/v4-*.test.ts`.
- Reports: this directory's V4 recovery, fixture, parity, and boundary documents.

## Stop boundary

V4 remains static-only. The production renderer is unchanged, source roots remain read-only, and V5 has not started. The final handoff will stop after V4.11; it will not promote the isolated adapter or claim exact pixel parity.
