# Complete 14x14 MapChip Gate

Status: `PASS_MAPCHIP_FOUNDATION`

The final staged gate renders the full native 14x14 MapChip topology with MapChip direct-image commands only. Empty raw cells remain empty; the 81 nonempty cells produce exactly 81 commands. No ObjChip, wall, Staff, or V8 command is included.

## Acceptance results

- alpha comparison: PASS;
- cell count: 81;
- command count: 81;
- connected alpha components: 1;
- unexpected transparent pixels: 0;
- expected source-transparent overlap pixels: 752;
- enclosed transparent pixels in the expected alpha union: 5;
- repeated render pixel digest: identical;
- output artifact: 1200x700;
- nontransparent bounds: x=300, y=240, width=720, height=359.

The 752 overlap pixels are expected because neighboring source images contain transparent regions. The five enclosed pixels are part of the expected source-alpha topology, not missing tile rectangles or black replacement gaps. The actual failure predicate is zero alpha mismatch, one connected component, and zero unexpected transparent pixels; all three pass.

## Evidence

- Machine result: `knowledge/fixtures/accepted/visual-port/mapchip-forensic/mapchip-14x14-results.json`
- Selector overlay: `knowledge/fixtures/accepted/visual-port/mapchip-forensic/previews/mapchip_selector_map.png`
- Render: `knowledge/fixtures/accepted/visual-port/mapchip-forensic/previews/mapchip_14x14.png`
- Alpha mask: `knowledge/fixtures/accepted/visual-port/mapchip-forensic/previews/mapchip_14x14_alpha_mask.png`
- Contact sheet: `knowledge/fixtures/accepted/visual-port/mapchip-forensic/previews/MAPCHIP_FORENSIC_CONTACT_SHEET.png`

This gate clears the MapChip foundation only. It does not authorize full-room integration or V8.
