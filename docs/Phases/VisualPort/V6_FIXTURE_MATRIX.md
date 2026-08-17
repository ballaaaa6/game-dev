# V6 Staff fixture matrix

The focused matrix covers StaffData 0 as the command fixture, StaffData 1 and 2 as room actors, StaffData 3 as an additional normal catalog record, and StaffData 100 as a source-backed variant metadata record.

Required directional coverage is closed for:

- wait: right, left, up, down;
- move: right, left, up, down;
- typing: right, left, up, down;
- unsupported `fly_away` with an explicit no-selector result;
- alpha-zero spawn and visible alpha-255 preview;
- default and non-zero integer camera offsets.

Each command fixture records the StaffData image selector, SEB selector, frame, TexId, crop rectangle, destination offset, reverse flags, blend boundary, world/screen position, and Room pass. The machine-readable rows are in `staff-fixture-manifest.json` and `staff-command-parity-results.json`.
