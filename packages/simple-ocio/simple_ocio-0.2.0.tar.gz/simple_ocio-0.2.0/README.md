# simple-ocio

Simplify OpenColorIO Usage for Tone-Mapping

## Examples

| AgX | Filmic | Khronos PBR Neutral | Standard |
|-----|--------|---------------------|-----------|
| ![AgX](examples/shader-ball-agx.png) | ![Filmic](examples/shader-ball-filmic.png) | ![PBR Neutral](examples/shader-ball-pbr-neutral.png) | ![Standard](examples/shader-ball-standard.png) |

All examples generated from the same HDR input image using different OCIO view transforms. See [example.py](example.py) for the code.

## Installation

```bash
pip install simple-ocio
```

## Usage

```python
tone_mapper = simple_ocio.ToneMapper()
ldr_img = tone_mapper.hdr_to_ldr(hdr_img)

# If you want to specify a tonemapper
tone_mapper.view = "AgX"
# Check the full list of available tonemappers
print(tone_mapper.available_views)
# Available ones: 'Standard', 'Khronos PBR Neutral', 'AgX', 'Filmic', 'Filmic Log', 'False Color', 'Raw'
```

## Third‑Party Licenses and Notices

This package redistributes the complete *Blender Color Management* (OpenColorIO) directory, including Filmic, AgX, and supporting LUTs. Each configuration keeps its original license. No functional changes have been made except relocating the files into the `simple_ocio/ocio_data` package directory. The full license text is available at `simple_ocio/ocio_data/ocio-license.txt` as well as the header of them.
