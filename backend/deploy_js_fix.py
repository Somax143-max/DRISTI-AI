import sys

with open("portal_engine.js", "r", encoding="utf-8") as f:
    code = f.read()

# Replace verifyAnatomicalRetinaClientSide with the intelligent globe-aware version
old_ver_start = code.find("// CLIENT-SIDE ANATOMICAL RETINAL VERIFIER (ZERO-MOCK FILTER)")
old_ver_end = code.find("// REAL BIOMARKER & LESION EXTRACTION IN BROWSER CANVAS")

new_ver_logic = """// CLIENT-SIDE ANATOMICAL RETINAL VERIFIER (INTELLIGENT GLOBE & DIAGRAM AWARE)
function verifyAnatomicalRetinaClientSide(img) {
    const testCanvas = document.createElement('canvas');
    testCanvas.width = 256; testCanvas.height = 256;
    const tCtx = testCanvas.getContext('2d');
    tCtx.drawImage(img, 0, 0, 256, 256);
    const idata = tCtx.getImageData(0, 0, 256, 256);
    const d = idata.data;

    let totalR = 0, totalG = 0, totalB = 0, activeCount = 0;
    let minX = 256, maxX = 0, minY = 256, maxY = 0;

    // Scan for warm retinal chromatic tissue (R - B > 18 and R - G > 2)
    for (let y = 0; y < 256; y++) {
        for (let x = 0; x < 256; x++) {
            const idx = (y * 256 + x) * 4;
            const r = d[idx], g = d[idx+1], b = d[idx+2];
            
            // Retinal tissue condition
            if ((r - b > 18) && (r - g > 2) && (r > 35)) {
                totalR += r;
                totalG += g;
                totalB += b;
                activeCount++;
                if (x < minX) minX = x;
                if (x > maxX) maxX = x;
                if (y < minY) minY = y;
                if (y > maxY) maxY = y;
            }
        }
    }

    const totalPixels = 256 * 256;
    const activeRatio = activeCount / totalPixels;

    // If less than 4% of image has warm retinal tone, it's not a retina
    if (activeRatio < 0.04) {
        return { isRetina: false, score: 0, reason: "No retinal chromatic tissue detected" };
    }

    const meanR = totalR / Math.max(1, activeCount);
    const meanG = totalG / Math.max(1, activeCount);
    const meanB = totalB / Math.max(1, activeCount);
    const rbRatio = (meanR + 1) / (meanB + 1);
    const rgRatio = (meanR + 1) / (meanG + 1);

    // Retinal globe bounding box and aspect ratio check (circularity)
    const bboxW = Math.max(1, maxX - minX);
    const bboxH = Math.max(1, maxY - minY);
    const aspectRatio = bboxW / bboxH;
    const isRoughlyCircular = (aspectRatio >= 0.65 && aspectRatio <= 1.55);

    // Vessel response inside the warm retinal region
    let vesselHits = 0;
    for (let y = minY + 4; y < maxY - 4; y += 2) {
        for (let x = minX + 4; x < maxX - 4; x += 2) {
            const idx = (y * 256 + x) * 4;
            const r = d[idx], g = d[idx+1], b = d[idx+2];
            if ((r - b > 18) && (r - g > 2)) {
                // Check green channel line contrast
                const gCenter = g;
                const gN = d[((y - 3) * 256 + x) * 4 + 1];
                const gS = d[((y + 3) * 256 + x) * 4 + 1];
                const gE = d[(y * 256 + (x + 3)) * 4 + 1];
                const gW = d[(y * 256 + (x - 3)) * 4 + 1];
                const gBg = (gN + gS + gE + gW) / 4.0;
                if ((gBg - gCenter) > 16) vesselHits++;
            }
        }
    }
    const vesselDensity = vesselHits / Math.max(1, activeCount / 4);

    const passChromatic = (rbRatio > 1.25) && (rgRatio > 1.01) && (meanR > 35);
    const hasVessels = (vesselDensity > 0.005);
    const isRetina = passChromatic && isRoughlyCircular && (hasVessels || activeRatio > 0.15);

    const score = (passChromatic ? 45 : 0) + (isRoughlyCircular ? 30 : 0) + (hasVessels ? 25 : 0);

    return {
        isRetina: isRetina,
        score: score,
        passChromatic: passChromatic,
        rbRatio: rbRatio.toFixed(2),
        rgRatio: rgRatio.toFixed(2),
        activeRatioPct: (activeRatio * 100).toFixed(1),
        vesselDensityPct: (vesselDensity * 100).toFixed(1),
        cx: (minX + maxX) / 2,
        cy: (minY + maxY) / 2,
        radius: Math.max(bboxW, bboxH) / 2
    };
}
"""

if old_ver_start != -1 and old_ver_end != -1:
    code = code[:old_ver_start] + new_ver_logic + "\n" + code[old_ver_end:]
    with open("portal_engine.js", "w", encoding="utf-8") as f:
        f.write(code)
    with open("web/portal_engine.js", "w", encoding="utf-8") as f:
        f.write(code)

    # Sync to HTML
    for path in ["web/index.html", "index.html"]:
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        s_idx = html.find("<script>")
        e_idx = html.find("</script>")
        if s_idx != -1 and e_idx != -1:
            new_html = html[:s_idx + len("<script>")] + "\n" + code + "\n    " + html[e_idx:]
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_html)
            print(f"Updated {path}")
    print("SUCCESS: Updated portal_engine.js with intelligent globe-aware verifier!")
else:
    print("Could not find bounds for verifyAnatomicalRetinaClientSide.")
