import sys

# Script to inject the User Input Space into the portal
with open('web/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add CSS
css_to_add = """
        /* USER INPUT SPACE & CLINICAL INTAKE SHEET */
        .input-sheet {
            background: #0d1527;
            color: #f8fafc;
            width: 820px;
            max-width: 95vw;
            max-height: 92vh;
            overflow-y: auto;
            border-radius: 12px;
            border: 1px solid #1e293b;
            padding: 24px;
            box-shadow: 0 16px 50px rgba(0,0,0,0.9);
            display: flex;
            flex-direction: column;
            gap: 14px;
            font-size: 12.5px;
        }
        .form-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
        }
        .form-grid-2 {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }
        .form-group {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .form-group label {
            font-size: 10px;
            font-weight: 700;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }
        .form-control {
            background: #131d33;
            border: 1px solid #1e293b;
            border-radius: 6px;
            padding: 7px 10px;
            color: #f8fafc;
            font-size: 12px;
            font-family: inherit;
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        .form-control:focus {
            border-color: #0284c7;
            box-shadow: 0 0 0 2px rgba(2, 132, 199, 0.25);
        }
        .section-tag {
            font-size: 11px;
            font-weight: 800;
            color: #38bdf8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 1px solid #1e293b;
            padding-bottom: 4px;
            margin-top: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
    </style>"""

html = html.replace('    </style>', css_to_add)

# 2. Add Top Header Button
old_hdr_btn = '<button class="btn-act" style="background:#0284c7; color:white; font-size:11px;" onclick="openReportModal()">'
new_hdr_btn = '<button class="btn-act" style="background:#059669; color:white; font-size:11px; font-weight:700;" onclick="openPatientInputModal(false)">➕ Input Patient Data</button>\n            ' + old_hdr_btn
html = html.replace(old_hdr_btn, new_hdr_btn)

# 3. Add Sidebar Button
old_sidebar_start = '<div class="sidebar">\n            <div>\n                <div class="section-header">'
new_sidebar_start = '<div class="sidebar">\n            <button class="btn-act" style="width:100%; justify-content:center; background:#059669; color:white; padding:9px 12px; font-size:11.5px; font-weight:700; margin-bottom:12px; box-shadow:0 2px 10px rgba(5,150,105,0.35);" onclick="openPatientInputModal(false)">➕ REGISTER NEW PATIENT</button>\n            <div>\n                <div class="section-header">'
html = html.replace(old_sidebar_start, new_sidebar_start)

# 4. Add Active Patient Demographics Bar in Clinical Mode
old_clinical_start = '<div id="view-clinical" style="display: flex; flex-direction: column; gap: 16px;">\n                \n                <!-- SMART FUNDUS QUALITY GATE -->'
new_clinical_bar = """<div id="view-clinical" style="display: flex; flex-direction: column; gap: 16px;">
                <!-- ACTIVE PATIENT DEMOGRAPHICS & QUICK EDIT BAR -->
                <div style="background:var(--card-bg); border:1px solid var(--card-border); border-radius:10px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                    <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
                        <div style="font-size:14px; font-weight:800; color:#f8fafc;" id="hdrPatName">Ganesh Kulkarni</div>
                        <div style="font-size:11px; font-family:'JetBrains Mono'; color:#38bdf8; background:#0d1527; padding:2px 8px; border-radius:4px; border:1px solid #1e293b;" id="hdrPatId">PAT_003_MODERATE</div>
                        <div style="font-size:11.5px; color:#94a3b8;" id="hdrPatMeta">Age: 58 | Male | DM: 11 Yrs | HbA1c: 8.4% | BP: 142/88 | Eye: OD (Right) | BCVA: 6/18</div>
                    </div>
                    <div style="display:flex; gap:6px;">
                        <button class="btn-act" style="background:#1e293b; color:#cbd5e1; padding:5px 10px; font-size:10.5px;" onclick="openPatientInputModal(true)">✏️ Edit Clinical Data</button>
                        <button class="btn-act" style="background:#059669; color:white; padding:5px 10px; font-size:10.5px;" onclick="openPatientInputModal(false)">➕ Input Patient Data</button>
                    </div>
                </div>

                <!-- SMART FUNDUS QUALITY GATE -->"""
html = html.replace(old_clinical_start, new_clinical_bar)

# 5. Add Field Mode Button
old_field_btn = '<button class="btn-act" style="background:#0284c7; color:white; padding:12px 24px; font-size:13.5px;" onclick="simulateFieldCapture()">📷 [ CAPTURE / ACQUIRE RETINA ]</button>'
new_field_btn = old_field_btn + '\n                    <button class="btn-act" style="background:#059669; color:white; padding:10px 18px; font-size:12.5px; font-weight:700;" onclick="openPatientInputModal(false)">📝 [ ENTER / EDIT PATIENT CLINICAL DATA ]</button>'
html = html.replace(old_field_btn, new_field_btn)

# 6. Update Report Modal Demographics
old_rep_demo = '<div style="font-size:11px; color:#64748b;">Age: 58 | Sex: M | Duration: 11 Yrs</div>'
new_rep_demo = '<div style="font-size:11px; color:#475569; margin-top:2px;" id="repDemographics">Age: 58 | Sex: M | Duration: 11 Yrs | HbA1c: 8.4% | BP: 142/88 | Eye: OD</div>'
html = html.replace(old_rep_demo, new_rep_demo)

# 7. Add Patient Input Modal HTML before closing script
input_modal_html = """
    <!-- PATIENT DATA INPUT SPACE MODAL -->
    <div class="modal" id="patientInputModal" onclick="closePatientInputModal(event)">
        <div class="input-sheet" onclick="event.stopPropagation()">
            <!-- HEADER -->
            <div style="display:flex; justify-content:space-between; align-items:flex-start; border-bottom:1px solid #1e293b; padding-bottom:12px;">
                <div>
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="font-size:18px;">📋</span>
                        <h2 style="font-size:18px; font-weight:800; color:#38bdf8;" id="inputModalTitle">PATIENT INTAKE & CLINICAL DATA ENTRY SPACE</h2>
                    </div>
                    <div style="font-size:11px; color:#94a3b8; margin-top:2px;">Rural Health Center Screening Portal | Ayushman Bharat Health Account (ABDM) Compatible</div>
                </div>
                <div style="display:flex; gap:8px; align-items:center;">
                    <button class="btn-act" style="background:#0284c7; color:white; font-size:10.5px;" onclick="quickAutofillPatientData()">⚡ Quick Autofill Demo Patient</button>
                    <button class="btn-act" style="background:#334155; color:white; padding:4px 8px;" onclick="closePatientInputModal()">✕</button>
                </div>
            </div>

            <!-- SECTION 1: DEMOGRAPHICS -->
            <div class="section-tag">
                <span>1. Patient Demographics & Health Identity</span>
                <span style="color:#64748b; font-weight:normal; font-size:9.5px;">ABDM Integration</span>
            </div>
            <div class="form-grid">
                <div class="form-group">
                    <label>Patient Full Name *</label>
                    <input type="text" id="inpName" class="form-control" placeholder="e.g. Ramesh Verma" value="Ramesh Verma" required>
                </div>
                <div class="form-group">
                    <label>Age (Years) *</label>
                    <input type="number" id="inpAge" class="form-control" min="18" max="100" value="56" required>
                </div>
                <div class="form-group">
                    <label>Gender *</label>
                    <select id="inpGender" class="form-control">
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                        <option value="Other">Other</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>ABHA ID / Health Token</label>
                    <input type="text" id="inpABHA" class="form-control" placeholder="ABHA-9182-4521-0089" value="ABHA-2026-9814">
                </div>
                <div class="form-group">
                    <label>Primary Health Centre (PHC)</label>
                    <input type="text" id="inpPHC" class="form-control" value="Nanded PHC #04 - Rural Center">
                </div>
                <div class="form-group">
                    <label>Contact Phone</label>
                    <input type="tel" id="inpPhone" class="form-control" placeholder="+91 98230 45612" value="+91 98230 45612">
                </div>
            </div>

            <!-- SECTION 2: SYSTEMIC BIOMARKERS -->
            <div class="section-tag">
                <span>2. Systemic Metabolic & Diabetes Profile</span>
                <span style="color:#34d399; font-weight:normal; font-size:9.5px;">Biomarker Risk Engine</span>
            </div>
            <div class="form-grid">
                <div class="form-group">
                    <label>Diabetes Duration (Years)</label>
                    <input type="number" id="inpDuration" class="form-control" min="0" max="60" value="9" oninput="updateRiskPreview()">
                </div>
                <div class="form-group">
                    <label>Diabetes Classification</label>
                    <select id="inpDMType" class="form-control">
                        <option value="Type 2 DM (Oral Hypoglycemics)">Type 2 DM (Oral Hypoglycemics)</option>
                        <option value="Type 2 DM (Insulin Dependent)">Type 2 DM (Insulin Dependent)</option>
                        <option value="Type 1 DM">Type 1 DM</option>
                        <option value="Pre-Diabetes / Borderline">Pre-Diabetes / Borderline</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>HbA1c Level (%) *</label>
                    <input type="number" id="inpHbA1c" class="form-control" step="0.1" min="4.0" max="18.0" value="8.4" oninput="updateRiskPreview()">
                </div>
                <div class="form-group">
                    <label>Systolic Blood Pressure (mmHg)</label>
                    <input type="number" id="inpBPSys" class="form-control" min="70" max="240" value="142" oninput="updateRiskPreview()">
                </div>
                <div class="form-group">
                    <label>Diastolic Blood Pressure (mmHg)</label>
                    <input type="number" id="inpBPDia" class="form-control" min="40" max="140" value="88" oninput="updateRiskPreview()">
                </div>
                <div class="form-group">
                    <label>Random Blood Sugar (mg/dL)</label>
                    <input type="number" id="inpRBS" class="form-control" min="50" max="600" value="210">
                </div>
            </div>

            <!-- SECTION 3: OPHTHALMIC DATA -->
            <div class="section-tag">
                <span>3. Ophthalmic Examination & Clinical Symptoms</span>
                <span style="color:#64748b; font-weight:normal; font-size:9.5px;">Laterality & Acuity</span>
            </div>
            <div class="form-grid">
                <div class="form-group">
                    <label>Eye Examined *</label>
                    <select id="inpEye" class="form-control">
                        <option value="OD (Right Eye)">Right Eye (OD)</option>
                        <option value="OS (Left Eye)">Left Eye (OS)</option>
                        <option value="OU (Bilateral)">Bilateral (OU)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Visual Acuity (Snellen)</label>
                    <select id="inpVA" class="form-control">
                        <option value="6/6 (Normal)">6/6 (Normal)</option>
                        <option value="6/9 (Mild Reduction)">6/9 (Mild Reduction)</option>
                        <option value="6/12 (Moderate)">6/12 (Moderate)</option>
                        <option value="6/18 (Significant Loss)" selected>6/18 (Significant Loss)</option>
                        <option value="6/24">6/24</option>
                        <option value="6/36">6/36</option>
                        <option value="6/60 (Severe)">6/60 (Severe Impairment)</option>
                        <option value="Counting Fingers / Hand Movements">Counting Fingers / Hand Movements</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Chief Visual Complaint</label>
                    <select id="inpSymptoms" class="form-control">
                        <option value="Blurry central vision & reading difficulty" selected>Blurry central vision & reading difficulty</option>
                        <option value="Floaters & dark spots">Floaters & dark spots</option>
                        <option value="Distorted lines (Metamorphopsia)">Distorted lines (Metamorphopsia)</option>
                        <option value="Sudden painless vision loss">Sudden painless vision loss</option>
                        <option value="Asymptomatic routine annual screen">Asymptomatic routine annual screen</option>
                    </select>
                </div>
                <div class="form-group" style="grid-column: span 3;">
                    <label>Prior Retinal Interventions / Medical History</label>
                    <input type="text" id="inpPriorTreat" class="form-control" placeholder="None, or previous PRP Laser / Anti-VEGF / Cataract Surgery" value="No prior laser. Diagnosed hypertension on amlodipine.">
                </div>
            </div>

            <!-- SECTION 4: FUNDUS IMAGE SOURCE -->
            <div class="section-tag">
                <span>4. Retinal Fundus Image Source</span>
                <span style="color:#06b6d4; font-weight:normal; font-size:9.5px;">Real-Time AI Ingestion</span>
            </div>
            <div class="form-grid-2">
                <div class="form-group">
                    <label>Select Retinal Presentation / Preset</label>
                    <select id="inpPreset" class="form-control" onchange="handlePresetSelect(this.value)">
                        <option value="PAT_003_MODERATE" selected>Preset: Moderate NPDR with Hard Exudates (CSME Risk)</option>
                        <option value="PAT_001_NORMAL">Preset: Normal Healthy Retina (Routine Screen)</option>
                        <option value="PAT_002_MILD">Preset: Mild NPDR (Isolated Microaneurysms)</option>
                        <option value="PAT_004_SEVERE">Preset: Severe NPDR (Extensive 4-Quadrant Hemorrhages)</option>
                        <option value="PAT_005_PDR">Preset: Proliferative DR (Active Neovascularization)</option>
                        <option value="PAT_006_BLURRED">Preset: Defective Quality (Motion Blur & Glare Flash)</option>
                        <option value="CUSTOM">Upload My Own Local Fundus File (JPG/PNG)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Or Upload Custom Fundus Image File</label>
                    <input type="file" id="inpCustomFile" class="form-control" accept="image/*" onchange="handleModalCustomUpload(event)">
                </div>
            </div>

            <!-- SYSTEMIC + RETINAL RISK PREVIEW BAR -->
            <div style="background:#070a13; border:1px solid #1e293b; border-radius:8px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center;" id="riskPreviewBox">
                <div>
                    <span style="font-size:10px; color:#94a3b8; text-transform:uppercase; font-weight:700;">Calculated Combined Microvascular Risk</span>
                    <div style="font-size:13px; font-weight:800; color:#fbbf24;" id="riskPreviewTitle">⚠️ ELEVATED SYSTEMIC RISK (HbA1c: 8.4%, BP: 142/88)</div>
                </div>
                <div style="font-size:11px; color:#cbd5e1; text-align:right;">
                    <div>Estimated Referral Urgency: <b style="color:#ef4444;" id="riskPreviewUrgency">PRIORITY 1 (4-6 Weeks)</b></div>
                </div>
            </div>

            <!-- FOOTER BUTTONS -->
            <div style="display:flex; justify-content:flex-end; gap:10px; margin-top:6px;">
                <button class="btn-act" style="background:#334155; color:white;" onclick="closePatientInputModal()">Cancel</button>
                <button class="btn-act" style="background:#059669; color:white; font-weight:800; padding:10px 20px; font-size:13px; box-shadow:0 4px 14px rgba(5,150,105,0.4);" onclick="submitPatientInputForm()">🚀 RUN AI SCREENING & ENROLL PATIENT</button>
            </div>
        </div>
    </div>
"""

# Insert modal right after the closing </div> of reportModal
report_modal_end = '        </div>\n    </div>'
idx = html.find(report_modal_end)
if idx != -1:
    idx += len(report_modal_end)
    html = html[:idx] + "\n" + input_modal_html + html[idx:]

with open('web/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML updated with User Input Space modal and access buttons.")
