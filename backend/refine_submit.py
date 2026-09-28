with open("portal_engine.js", "r", encoding="utf-8") as f:
    code = f.read()

# Update handleModalCustomUpload to trigger real verification immediately
old_modal_upload = """function handleModalCustomUpload(event) {
    const file = event.target.files ? event.target.files[0] : null;
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(e) {
        const img = new Image();
        img.onload = function() {
            modalCustomImg = img;
            customUploadedImg = img;
            document.getElementById('inpPreset').value = 'CUSTOM';
            logAudit(`Custom fundus file selected in intake space: <b>${file.name}</b>`);
        };
        img.src = e.target.result;
    };
    reader.readAsDataURL(file);
}"""

new_modal_upload = """function handleModalCustomUpload(event) {
    const file = event.target.files ? event.target.files[0] : null;
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(e) {
        const base64Data = e.target.result;
        const img = new Image();
        img.onload = function() {
            modalCustomImg = img;
            customUploadedImg = img;
            document.getElementById('inpPreset').value = 'CUSTOM';
            logAudit(`Custom fundus file selected in intake space: <b>${file.name}</b>. Running eye verification...`);
            processRealEyeVerificationAndAnalysis(img, file.name, base64Data);
        };
        img.src = base64Data;
    };
    reader.readAsDataURL(file);
}"""

# Update submitPatientInputForm
old_submit_start = """    let targetId = editModeTargetId;
    let basePatient = (presetKey !== 'CUSTOM' && PATIENTS[presetKey]) ? PATIENTS[presetKey] : PATIENTS['PAT_003_MODERATE'];"""

new_submit_start = """    if (presetKey === 'CUSTOM') {
        if (PATIENTS['PAT_REJECTED'] && PATIENTS['PAT_REJECTED'].isRejected) {
            alert("❌ CANNOT ENROLL PATIENT WITH NON-RETINAL IMAGE!\\n\\nThe uploaded file failed anatomical eye verification. Please provide an authentic ocular fundus camera photograph.");
            return;
        }
    }

    let targetId = editModeTargetId;
    let basePatient = (presetKey === 'CUSTOM' && PATIENTS['PAT_VERIFIED']) ? PATIENTS['PAT_VERIFIED'] : ((presetKey !== 'CUSTOM' && PATIENTS[presetKey]) ? PATIENTS[presetKey] : PATIENTS['PAT_003_MODERATE']);"""

code = code.replace(old_modal_upload, new_modal_upload)
code = code.replace(old_submit_start, new_submit_start)

with open("portal_engine.js", "w", encoding="utf-8") as f:
    f.write(code)
with open("web/portal_engine.js", "w", encoding="utf-8") as f:
    f.write(code)

for path in ["web/index.html", "index.html"]:
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    s_idx = html.find("<script>")
    e_idx = html.find("</script>")
    if s_idx != -1 and e_idx != -1:
        new_html = html[:s_idx + len("<script>")] + "\n" + code + "\n    " + html[e_idx:]
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_html)

print("Updated handleModalCustomUpload & submitPatientInputForm across all files.")
