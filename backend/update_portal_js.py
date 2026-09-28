import sys

# Append input space JS functions to portal_engine.js
input_js_code = """
// --- USER INPUT SPACE & PATIENT INTAKE ENGINE ---
let modalCustomImg = null;
let editModeTargetId = null;

// Initialize default metabolic parameters on baseline cohort
if (PATIENTS['PAT_001_NORMAL']) {
    Object.assign(PATIENTS['PAT_001_NORMAL'], { hba1c: 6.2, bp: '120/78', eye: 'OD (Right)', va: '6/6 (Normal)', abha: 'ABHA-2026-1042', dmType: 'Type 2 DM (Diet)', symptoms: 'Routine annual checkup' });
}
if (PATIENTS['PAT_002_MILD']) {
    Object.assign(PATIENTS['PAT_002_MILD'], { hba1c: 7.4, bp: '132/84', eye: 'OS (Left)', va: '6/9 (Mild)', abha: 'ABHA-2026-2180', dmType: 'Type 2 DM (Oral)', symptoms: 'Mild occasional blur' });
}
if (PATIENTS['PAT_003_MODERATE']) {
    Object.assign(PATIENTS['PAT_003_MODERATE'], { hba1c: 8.4, bp: '142/88', eye: 'OD (Right)', va: '6/18 (Significant)', abha: 'ABHA-2026-3491', dmType: 'Type 2 DM (Oral + Insulin)', symptoms: 'Blurry central vision & reading difficulty' });
}
if (PATIENTS['PAT_004_SEVERE']) {
    Object.assign(PATIENTS['PAT_004_SEVERE'], { hba1c: 9.6, bp: '158/94', eye: 'OU (Both)', va: '6/36 (Substantial)', abha: 'ABHA-2026-4819', dmType: 'Type 2 DM (Insulin)', symptoms: 'Dark patches & distortion' });
}
if (PATIENTS['PAT_005_PDR']) {
    Object.assign(PATIENTS['PAT_005_PDR'], { hba1c: 10.8, bp: '168/102', eye: 'OD (Right)', va: '6/60 (Severe)', abha: 'ABHA-2026-5921', dmType: 'Type 2 DM (Insulin)', symptoms: 'Floaters, sudden vision dip' });
}
if (PATIENTS['PAT_006_BLURRED']) {
    Object.assign(PATIENTS['PAT_006_BLURRED'], { hba1c: 7.8, bp: '130/82', eye: 'OD (Right)', va: 'Ungradeable', abha: 'ABHA-2026-6102', dmType: 'Type 2 DM', symptoms: 'Annual screening exam' });
}

function openPatientInputModal(isEditMode) {
    editModeTargetId = isEditMode ? currentPatientId : null;
    const modal = document.getElementById('patientInputModal');
    const title = document.getElementById('inputModalTitle');
    if (!modal) return;

    if (isEditMode && currentPatientId && PATIENTS[currentPatientId]) {
        const p = PATIENTS[currentPatientId];
        if (title) title.innerText = 'EDIT PATIENT CLINICAL DATA: ' + p.name;
        document.getElementById('inpName').value = p.name;
        document.getElementById('inpAge').value = p.age;
        document.getElementById('inpGender').value = (p.sex === 'M' || p.sex === 'Male' ? 'Male' : (p.sex === 'F' || p.sex === 'Female' ? 'Female' : p.sex));
        document.getElementById('inpABHA').value = p.abha || 'ABHA-2026-9814';
        document.getElementById('inpDuration').value = parseInt(p.duration) || 9;
        document.getElementById('inpHbA1c').value = p.hba1c || 8.4;
        if (p.bp) {
            const parts = p.bp.split('/');
            document.getElementById('inpBPSys').value = parts[0] || 140;
            document.getElementById('inpBPDia').value = parts[1] || 85;
        }
        if (p.eye) document.getElementById('inpEye').value = p.eye;
        if (p.va) document.getElementById('inpVA').value = p.va;
        if (p.symptoms) document.getElementById('inpSymptoms').value = p.symptoms;
    } else {
        if (title) title.innerText = 'PATIENT INTAKE & CLINICAL DATA ENTRY SPACE';
        document.getElementById('inpName').value = 'Ramesh Verma';
        document.getElementById('inpAge').value = 56;
        document.getElementById('inpGender').value = 'Male';
        document.getElementById('inpABHA').value = 'ABHA-2026-' + Math.floor(Math.random() * 8999 + 1000);
        document.getElementById('inpDuration').value = 9;
        document.getElementById('inpHbA1c').value = 8.4;
        document.getElementById('inpBPSys').value = 142;
        document.getElementById('inpBPDia').value = 88;
        document.getElementById('inpEye').value = 'OD (Right Eye)';
        document.getElementById('inpVA').value = '6/18 (Significant Loss)';
        document.getElementById('inpSymptoms').value = 'Blurry central vision & reading difficulty';
    }
    modalCustomImg = null;
    updateRiskPreview();
    modal.style.display = 'flex';
    logAudit(isEditMode ? `Patient Editor opened for <b>${currentPatientId}</b>.` : 'Patient Intake Form opened for new clinical enrollment.');
}

function closePatientInputModal(event) {
    if (event && event.target !== document.getElementById('patientInputModal') && !event.target.classList.contains('btn-act')) return;
    const modal = document.getElementById('patientInputModal');
    if (modal) modal.style.display = 'none';
}

function quickAutofillPatientData() {
    const demoNames = ['Ramesh Verma', 'Parvati Bai', 'Suresh Choudhary', 'Devendra Patil', 'Shubhangi More'];
    const selectedName = demoNames[Math.floor(Math.random() * demoNames.length)];
    document.getElementById('inpName').value = selectedName;
    document.getElementById('inpAge').value = Math.floor(Math.random() * 25 + 45);
    document.getElementById('inpABHA').value = 'ABHA-2026-' + Math.floor(Math.random() * 8999 + 1000);
    document.getElementById('inpDuration').value = Math.floor(Math.random() * 12 + 4);
    document.getElementById('inpHbA1c').value = (Math.random() * 3.5 + 7.2).toFixed(1);
    document.getElementById('inpBPSys').value = Math.floor(Math.random() * 30 + 130);
    document.getElementById('inpBPDia').value = Math.floor(Math.random() * 15 + 80);
    document.getElementById('inpRBS').value = Math.floor(Math.random() * 100 + 170);
    document.getElementById('inpEye').value = Math.random() > 0.5 ? 'OD (Right Eye)' : 'OS (Left Eye)';
    document.getElementById('inpVA').value = '6/18 (Significant Loss)';
    document.getElementById('inpPreset').value = 'PAT_003_MODERATE';
    updateRiskPreview();
    logAudit(`Demo patient values autofilled for quick screening evaluation.`);
}

function updateRiskPreview() {
    const hba1c = parseFloat(document.getElementById('inpHbA1c')?.value || 8.0);
    const dur = parseInt(document.getElementById('inpDuration')?.value || 5);
    const sys = parseInt(document.getElementById('inpBPSys')?.value || 130);
    const title = document.getElementById('riskPreviewTitle');
    const urg = document.getElementById('riskPreviewUrgency');
    const box = document.getElementById('riskPreviewBox');
    if (!title || !urg) return;

    if (hba1c >= 8.5 || sys >= 145 || dur >= 15) {
        title.style.color = '#ef4444';
        title.innerText = `🚨 HIGH MICROVASCULAR PROGRESSION RISK (HbA1c: ${hba1c}%, BP: ${sys} mmHg)`;
        urg.style.color = '#ef4444';
        urg.innerText = 'HIGH PRIORITY (Accelerated Retinal Damage Risk)';
        if (box) box.style.borderColor = '#ef4444';
    } else if (hba1c >= 7.5 || sys >= 135 || dur >= 8) {
        title.style.color = '#fbbf24';
        title.innerText = `⚠️ ELEVATED SYSTEMIC RISK (HbA1c: ${hba1c}%, Duration: ${dur} Yrs)`;
        urg.style.color = '#fbbf24';
        urg.innerText = 'PRIORITY 2 (Moderate DME Risk)';
        if (box) box.style.borderColor = '#fbbf24';
    } else {
        title.style.color = '#34d399';
        title.innerText = `✓ CONTROLLED SYSTEMIC PROFILE (HbA1c: ${hba1c}%, BP: ${sys} mmHg)`;
        urg.style.color = '#34d399';
        urg.innerText = 'ROUTINE SURVEILLANCE';
        if (box) box.style.borderColor = '#34d399';
    }
}

function handlePresetSelect(val) {
    if (val === 'CUSTOM') {
        document.getElementById('inpCustomFile')?.click();
    }
}

function handleModalCustomUpload(event) {
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
}

function submitPatientInputForm() {
    const name = document.getElementById('inpName')?.value.trim() || 'Anonymous Patient';
    const age = parseInt(document.getElementById('inpAge')?.value) || 50;
    const gender = document.getElementById('inpGender')?.value || 'Male';
    const abha = document.getElementById('inpABHA')?.value || 'ABHA-2026-' + Math.floor(Math.random()*8999+1000);
    const phc = document.getElementById('inpPHC')?.value || 'Nanded Rural PHC #04';
    const duration = parseInt(document.getElementById('inpDuration')?.value) || 5;
    const dmType = document.getElementById('inpDMType')?.value || 'Type 2 DM';
    const hba1c = parseFloat(document.getElementById('inpHbA1c')?.value) || 7.5;
    const bpSys = parseInt(document.getElementById('inpBPSys')?.value) || 130;
    const bpDia = parseInt(document.getElementById('inpBPDia')?.value) || 80;
    const rbs = parseInt(document.getElementById('inpRBS')?.value) || 180;
    const eye = document.getElementById('inpEye')?.value || 'OD (Right Eye)';
    const va = document.getElementById('inpVA')?.value || '6/12 (Moderate)';
    const symptoms = document.getElementById('inpSymptoms')?.value || 'Routine examination';
    const priorTreat = document.getElementById('inpPriorTreat')?.value || 'None';
    const presetKey = document.getElementById('inpPreset')?.value || 'PAT_003_MODERATE';

    let targetId = editModeTargetId;
    let basePatient = (presetKey !== 'CUSTOM' && PATIENTS[presetKey]) ? PATIENTS[presetKey] : PATIENTS['PAT_003_MODERATE'];

    if (!targetId) {
        const cleanName = name.split(' ')[0].toUpperCase().replace(/[^A-Z]/g, '');
        targetId = 'PAT_' + cleanName + '_' + Math.floor(Math.random() * 899 + 100);
    }

    const newPatient = Object.assign({}, basePatient, {
        id: targetId,
        name: name,
        age: age,
        sex: gender[0] || 'M',
        duration: duration + ' Yrs',
        dmType: dmType,
        hba1c: hba1c,
        bp: bpSys + '/' + bpDia,
        rbs: rbs,
        eye: eye,
        va: va,
        abha: abha,
        phc: phc,
        symptoms: symptoms,
        priorTreat: priorTreat,
        rationale: `Clinical Biomarkers: ${basePatient.rationale} Systemic Control: HbA1c ${hba1c}%, BP ${bpSys}/${bpDia} mmHg, Duration ${duration} yrs. Eye Examined: ${eye} (BCVA ${va}). Complaints: ${symptoms}.`
    });

    if (hba1c > 8.5 && newPatient.grade >= 2) {
        newPatient.priority = 1;
        newPatient.priorityText = 'Priority 1 (High DME Risk)';
    }

    PATIENTS[targetId] = newPatient;
    closePatientInputModal();
    populateQueue();
    selectPatient(targetId);

    speakGuidance(`Patient ${name} successfully enrolled. AI screening complete.`);
    logAudit(`<b>Patient Clinical Data Enrolled:</b> ${targetId} (${name}, ${age}y, HbA1c: ${hba1c}%, BP: ${bpSys}/${bpDia}, Eye: ${eye}). Status: ${newPatient.gradeName}`);
    alert(`✅ PATIENT INTAKE & AI SCREENING COMPLETED!\n\nPatient: ${name} (${targetId})\nAge: ${age} | Gender: ${gender} | Eye: ${eye}\nHbA1c: ${hba1c}% | Blood Pressure: ${bpSys}/${bpDia} mmHg\nStaged Severity: ${newPatient.gradeName}\nReferral Urgency: ${newPatient.refTitle}\n\nClinical data recorded to district registry.`);
}
"""

with open('portal_engine.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

# Update selectPatient in js_text to also update the header demographics bar
old_select_str = "    // 6. Reset Stopwatch"
new_select_str = """    // Active Demographics Bar
    const hName = document.getElementById('hdrPatName');
    if (hName) hName.innerText = p.name;
    const hId = document.getElementById('hdrPatId');
    if (hId) hId.innerText = p.id;
    const hMeta = document.getElementById('hdrPatMeta');
    if (hMeta) hMeta.innerText = `Age: ${p.age} | ${p.sex === 'M' || p.sex === 'Male' ? 'Male' : (p.sex === 'F' || p.sex === 'Female' ? 'Female' : p.sex)} | DM: ${p.duration} | HbA1c: ${p.hba1c || 8.4}% | BP: ${p.bp || '130/80'} | Eye: ${p.eye || 'OD'} | BCVA: ${p.va || '6/12'}`;

    // Report Demographics
    const rDemo = document.getElementById('repDemographics');
    if (rDemo) rDemo.innerText = `Age: ${p.age} | Sex: ${p.sex} | Duration: ${p.duration} | HbA1c: ${p.hba1c || 8.4}% | BP: ${p.bp || '130/80'} | Eye: ${p.eye || 'OD'}`;

    // 6. Reset Stopwatch"""

js_text = js_text.replace(old_select_str, new_select_str)

# Append new input space JS
js_text += "\n" + input_js_code

# Save updated portal_engine.js
with open('portal_engine.js', 'w', encoding='utf-8') as f:
    f.write(js_text)
with open('web/portal_engine.js', 'w', encoding='utf-8') as f:
    f.write(js_text)

# Also update the inline script in web/index.html and root index.html
with open('web/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace script block with new full script
script_start = '<script>'
script_end = '</script>'
s_idx = html.find(script_start)
e_idx = html.find(script_end)

if s_idx != -1 and e_idx != -1:
    html = html[:s_idx + len(script_start)] + "\n" + js_text + "\n    " + html[e_idx:]

with open('web/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: portal_engine.js, web/index.html, and index.html updated with complete User Input Space functionality!")
