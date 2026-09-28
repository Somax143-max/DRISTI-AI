const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

// Check that virtualExplorerModal exists in index.html
if (!html.includes('id="virtualExplorerModal"')) {
    console.error("FAIL: virtualExplorerModal not found in index.html");
    process.exit(1);
}
console.log("PASS: virtualExplorerModal exists in index.html");

// Check that buttons exist
if (!html.includes('openVirtualExplorerModal()')) {
    console.error("FAIL: openVirtualExplorerModal() call not found in index.html");
    process.exit(1);
}
console.log("PASS: openVirtualExplorerModal buttons exist");

// Check that JS functions exist in portal_engine.js
const js = fs.readFileSync('portal_engine.js', 'utf8');
const requiredSymbols = [
    'SAMPLE_IMAGES_MANIFEST',
    'openVirtualExplorerModal',
    'closeVirtualExplorerModal',
    'setSampleFilter',
    'filterSampleImages',
    'renderSampleExplorerGrid',
    'selectSampleCard',
    'executeLoadSelectedSample',
    'renderModalPresetGrid',
    'selectModalPreset',
    'createSyntheticFundusDataUrl'
];

for (const sym of requiredSymbols) {
    if (!js.includes(sym)) {
        console.error(`FAIL: Symbol ${sym} missing in portal_engine.js`);
        process.exit(1);
    }
    console.log(`PASS: Symbol ${sym} present in portal_engine.js`);
}

// Check syntax of portal_engine.js and web/portal_engine.js
const vm = require('vm');
try {
    new vm.Script(js);
    console.log("PASS: portal_engine.js parses without syntax error");
} catch (e) {
    console.error("FAIL: portal_engine.js syntax error:", e);
    process.exit(1);
}

const webJs = fs.readFileSync('web/portal_engine.js', 'utf8');
try {
    new vm.Script(webJs);
    console.log("PASS: web/portal_engine.js parses without syntax error");
} catch (e) {
    console.error("FAIL: web/portal_engine.js syntax error:", e);
    process.exit(1);
}

console.log("ALL VIRTUAL EXPLORER INTEGRITY CHECKS PASSED!");
