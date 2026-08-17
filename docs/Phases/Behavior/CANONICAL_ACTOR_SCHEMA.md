# Canonical Actor Schema

Status: `PASS_DATA_DEPENDENCY_FORENSIC_WITH_SOURCE_LIMITS`

This report is static/offline evidence only. No decompiled C# was executed and no runtime, renderer, MapChip, V8, emulator, server, network, or browser work was started.

The canonical actor schema keeps StaffData source fields, saved Staff fields, transient Staff fields, and derived formula outputs in separate namespaces. `instance_id` and dashboard task references are explicitly `PRODUCT_POLICY`; they are not original game fields.

The schema forbids fabricating source values or adding raw x/y/HP fields to the dashboard adapter.
