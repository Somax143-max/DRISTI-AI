# JS Part 1: Header and Patients dictionary
with open('create_realtime_portal.py', 'a', encoding='utf-8') as f:
    f.write('''html_parts.append("""    <!-- CORE REAL-TIME JAVASCRIPT ENGINE -->
    <script>
    // --- 1. PATIENT DATABASE (ICDR STAGES 0-4 + UNGRADEABLE) ---
    const PATIENTS = {
        'PAT_001_NORMAL': {
            id: 'PAT_001_NORMAL',
            name: 'Rajesh Patil', age: 52, sex: 'M', duration: '4 Yrs',
            grade: 0, gradeName: 'LEVEL 0 — NO APPARENT RETINOPATHY',
            referable: false, refTitle: '🟢 NO REFERRAL REQUIRED',
            refReason: 'Routine annual diabetic eye screening in 12 months at local PHC.',
            priority: 4, priorityText: 'Routine (12 Mo)',
            quality: 'ACCEPTABLE', qClass: 'q-good',
            focus: 44.2, fov: '89.2%', illum: 'Optimal (0.48)', glare: '1.2%',
            guidance: 'Image passes all ISO/IEC quality metrics with excellent optic disc and foveal clarity.',
            guidanceClass: 'guidance-ok', guidanceTitle: 'Optimal Retinal Image:',
            mas: 0, hemo: 0, exudates: 0, density: '8.9%', csme: 'Negative (>2.0 DD)',
            conf: 98.2, qualScore: 94.0, agrScore: 96.5, reliability: 'HIGH',
            rationale: 'Absence of microaneurysms, hemorrhages, hard/soft exudates, or neovascularization. Retinal vascular caliber is normal without focal narrowing.'
        },
        'PAT_002_MILD': {
            id: 'PAT_002_MILD',
            name: 'Sunita Deshmukh', age: 61, sex: 'F', duration: '7 Yrs',
            grade: 1, gradeName: 'LEVEL 1 — MILD NPDR',
            referable: false, refTitle: '🟢 ROUTINE FOLLOW-UP',
            refReason: 'Microaneurysms only. Schedule follow-up dilated exam in 6-12 months.',
            priority: 3, priorityText: 'Mild (6-12 Mo)',
            quality: 'ACCEPTABLE', qClass: 'q-good',
            focus: 38.5, fov: '84.1%', illum: 'Good (0.45)', glare: '2.8%',
            guidance: 'Mild peripheral illumination falloff automatically compensated by CLAHE pipeline.',
            guidanceClass: 'guidance-enhance', guidanceTitle: 'Minor Illumination Falloff Corrected:',
            mas: 5, hemo: 0, exudates: 0, density: '9.1%', csme: 'Negative (>2.0 DD)',
            conf: 94.6, qualScore: 89.5, agrScore: 93.0, reliability: 'HIGH',
            rationale: 'Isolated microaneurysms detected in temporal parafoveal region. No definite hemorrhages or lipid exudates detected.'
        },
''')
''')
print("Part 1 written successfully.")
