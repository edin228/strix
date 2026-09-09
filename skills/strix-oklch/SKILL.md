---
name: strix-oklch
description: "Convert and evaluate web colors in OKLCH when requested or already used by the project. Check actual contrast and display gamut; do not impose a framework or replace unrelated color conventions."
---

# Strix oklch

This is an optional web-color adapter. Read the project's theme and accessibility
contract and inspect actual foreground, background, opacity, and state tokens.
Preserve existing semantic roles and conversion scope. Do not migrate unrelated
colors or add a dependency merely to adopt this color space.

Use an existing tested color library or project conversion tool. Verify current
primary specifications when conversion or accessibility semantics are uncertain.
Preserve alpha and intended appearance, inspect gamut mapping, and compare the
rendered result. Do not equate OKLCH lightness with contrast or assume a constant
chroma is displayable at every lightness and hue.

Evaluate final composited foreground and background pairs with the project's
required accessibility method. Report the method, measured result, applicable
criterion, and text or component role. Heuristic lightness gaps are not passing
contrast evidence. Do not substitute one contrast algorithm for another without
an explicit project decision.

For palettes, inspect meaningful light and dark states and material consumers.
Adjust lightness, chroma, or hue as needed, then remeasure contrast and gamut.
For wide-gamut output preserve a tested fallback appropriate to supported
browsers. Verify support against the project's target versions rather than
embedding a changing global support percentage.

Report affected tokens, conversion and contrast evidence, and remaining visual
limits. Use a before/after table for multiple mappings. Keep framework-specific
theme syntax in project references.
