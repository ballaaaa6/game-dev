# V7 pixel diff report

## Status

`PASS_STATIC`

Diffs are computed only between deterministic V7 surfaces. Historical screenshots are not used to derive geometry, tune pixels, or establish acceptance.

## Results

| Comparison | Changed pixels | Max channel error | Mean channel error | Classification |
| --- | ---: | ---: | ---: | --- |
| repeated room:0 structural render | 0 | 0 | 0 | `PROVEN` deterministic repeat |
| repeated room:0 + Staff render | 0 | 0 | 0 | `PROVEN` deterministic repeat |
| structural vs room:0 + Staff | 830 | 255 | 169.96897590361445 | `C_COMPATIBILITY_BACKEND_DIFFERENCE` / expected selected content delta |

The structural-to-Staff difference is bounded to `x=426, y=99, width=30, height=30`, matching the selected Staff content region. Its diff PNG SHA-256 is `b8aba8d9e4375ea534493eec6d567193d7a62c7e735ee1478190e81d786152f2`.

## Interpretation

The two repeat comparisons prove deterministic serialization, raster traversal, sampling, compositing, and PNG output for the same command stream. The room-to-Staff difference is expected content addition, not a failed repeat. Native compositor/shader difference remains explicitly classified as `COMPATIBILITY_REIMPLEMENTATION`, not silently upgraded to native pixel proof.

Machine evidence is in [pixel-diff-results.json](../../../knowledge/fixtures/accepted/visual-port/v7/pixel-diff-results.json).
