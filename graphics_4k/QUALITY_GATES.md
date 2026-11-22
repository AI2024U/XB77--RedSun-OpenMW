# XB77 4K Race and World Quality Gates

Scope: Morrowind + Tribunal + Bloodmoon only. This is a release checklist, not a record of completed testing.

## Character quality

- [ ] All 10 vanilla playable races; male and female skin/heads; first- and third-person poses
- [ ] Neck joins match diffuse color, normal vectors and seam UVs at common animation poses
- [ ] Wrists/ankles/hands and foot joins have consistent tangents, normals and skin tones
- [ ] Facial silhouette smooth at close dialogue distance, no blocky edges or fake smoothing
- [ ] Vertex weights, named bones, bounding volumes and NIF materials validated
- [ ] Hair/ears/headwear, eyes, mouth, face equipment compatibility
- [ ] Walk, run, jump, swim, idle, weapon swing and spellcasting seams inspected
- [ ] Armor, robes and exposed skin checked against all affected race body shapes

## Environment quality

- [ ] World geometry and texture coverage audit from all three official archives
- [ ] Architecture, terrain, flora, creatures, clutter, equipment and interiors checked
- [ ] UV mapping, tiling and alpha tested without stretching or transparency defects
- [ ] Proper normal/specular maps as supported by pinned Red Sun OpenMW engine version
- [ ] Texture memory budget and mipmaps tested at 1080p, 1440p and 4K output
- [ ] OpenMW log contains no missing model/texture errors associated with XB77

## Release readiness

- [ ] ESP is a real TES3 plugin, validated in a content editor, not a fake header
- [ ] OpenMW Launcher lists ESP and Data Directory separately and correctly
- [ ] Activating/deactivating data directory returns to original mesh/texture state
- [ ] All three ESM dependencies behave correctly and no other expansions are required
- [ ] Red Sun dialogue highlight, controllers, launcher, logs, configs and saves unaffected
- [ ] Asset rights, attribution and redistribution permission documented
- [ ] Windows gameplay captures inspected; independent tester approval recorded
- [ ] Clean ZIP CRC and content manifest checked; no copied game files or private info