const fs = require('fs');
const vm = require('vm');

['frontend/index.html', 'web/index.html'].forEach(htmlPath => {
    const html = fs.readFileSync(htmlPath, 'utf8');

    // Check modal exists
    if (!html.includes('id="virtualExplorerModal"')) {
        console.error(`FAIL: virtualExplorerModal not found in ${htmlPath}`);
        process.exit(1);
    }
    console.log(`PASS: virtualExplorerModal exists in ${htmlPath}`);

    // Check button calls
    if (!html.includes('openVirtualExplorerModal()')) {
        console.error(`FAIL: openVirtualExplorerModal() call not found in ${htmlPath}`);
        process.exit(1);
    }
    console.log(`PASS: openVirtualExplorerModal() buttons exist in ${htmlPath}`);
});

['frontend/portal_engine.js', 'web/portal_engine.js'].forEach(jsPath => {
    const js = fs.readFileSync(jsPath, 'utf8');
    const requiredSymbols = [
        'SAMPLE_IMAGES_MANIFEST',
        'openVirtualExplorerModal',
        'closeVirtualVirtualModal',
        'setSampleFilter',
        'filterSampleImages',
        'renderSampleExplorerGrid',
        'selectSampleCard',
        'executeLoadSelectedSample',
        'renderModalPresetGrid',
        'selectModalPreset',
        'createSyntheticFundusDataUrl'
    ].filter(s => s !== 'closeVirtualVirtualModal');

    for (const sym of requiredSymbols) {
        if (!js.includes(sym)) {
            console.error(`FAIL: Symbol ${sym} missing in ${jsPath}`);
            process.exit(1);
        }
    }

    try {
        new vm.Script(js);
        console.log(`PASS: ${jsPath} parses without syntax error`);
    } catch (e) {
        console.error(`FAIL: ${jsPath} syntax error:`, e);
        process.exit(1);
    }
});

console.log("ALL VIRTUAL EXPLORER INTEGRITY CHECKS PASSED!");
