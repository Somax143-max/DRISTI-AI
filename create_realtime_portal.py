# Generator for Real-Time Functional DRISHTI AI Portal
html_parts = []

html_parts.append('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DRISHTI AI | Real-Time Retinal Screening Intelligence (MathWorks SIH26038)</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #070a13;
            --panel-bg: #0d1527;
            --card-bg: #131d33;
            --card-border: #1e293b;
            --accent-blue: #0284c7;
            --accent-cyan: #06b6d4;
            --accent-emerald: #10b981;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --purple: #8b5cf6;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }
        header {
            background: linear-gradient(90deg, #090d16 0%, #111827 50%, #1e1b4b 100%);
            border-bottom: 1px solid #1e293b;
            padding: 10px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .brand { display: flex; align-items: center; gap: 12px; }
        .brand-logo {
            width: 38px; height: 38px;
            background: linear-gradient(135deg, #0284c7, #06b6d4);
            border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 20px; font-weight: 800; color: white;
            box-shadow: 0 4px 14px rgba(6, 182, 212, 0.4);
        }
        .brand-text h1 { font-size: 17px; font-weight: 800; letter-spacing: -0.5px; }
        .brand-text p { font-size: 11px; color: var(--accent-cyan); font-weight: 600; }
        
        .role-switcher {
            display: flex;
            background: #0b1120;
            border: 1px solid #334155;
            padding: 3px;
            border-radius: 9px;
            gap: 3px;
        }
        .role-btn {
            background: none;
            border: none;
            color: #94a3b8;
            font-size: 11.5px;
            font-weight: 700;
            padding: 6px 13px;
            border-radius: 7px;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .role-btn.active {
            background: var(--accent-blue);
            color: white;
            box-shadow: 0 2px 8px rgba(2, 132, 199, 0.4);
        }
        .role-btn:hover:not(.active) { color: white; background: #1e293b; }
        
        .header-status { display: flex; align-items: center; gap: 10px; }
        .net-badge {
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid #10b981;
            color: #34d399;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 6px;
            cursor: pointer;
        }
        .net-badge.offline {
            background: rgba(245, 158, 11, 0.15);
            border-color: #f59e0b;
            color: #fbbf24;
        }
        .pulse-dot {
            width: 7px; height: 7px; border-radius: 50%;
            background: #10b981; box-shadow: 0 0 8px #10b981;
        }
        .pulse-dot.offline { background: #f59e0b; box-shadow: 0 0 8px #f59e0b; }
        
        .main-layout {
            display: grid;
            grid-template-columns: 310px 1fr;
            flex: 1;
            height: calc(100vh - 61px);
        }
        
        .sidebar {
            background-color: #0b1120;
            border-right: 1px solid #1e293b;
            padding: 14px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 14px;
        }
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 10.5px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #64748b;
            font-weight: 800;
            margin-bottom: 6px;
        }
        
        .queue-list { display: flex; flex-direction: column; gap: 6px; }
        .queue-item {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            padding: 10px 12px;
            border-radius: 9px;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            flex-direction: column;
            gap: 3px;
        }
        .queue-item:hover { border-color: var(--accent-cyan); background: #1a2744; transform: translateX(2px); }
        .queue-item.active {
            border-color: var(--accent-cyan);
            background: linear-gradient(135deg, rgba(2, 132, 199, 0.2), rgba(6, 182, 212, 0.1));
            box-shadow: 0 0 12px rgba(6, 182, 212, 0.2);
        }
        .q-top { display: flex; justify-content: space-between; align-items: center; }
        .q-id { font-weight: 700; font-size: 12px; font-family: 'JetBrains Mono', monospace; }
        .p-badge {
            font-size: 9px; font-weight: 800; padding: 2px 7px; border-radius: 10px;
            text-transform: uppercase; letter-spacing: 0.4px;
        }
        .p-urgent { background: rgba(239, 68, 68, 0.25); color: #f87171; border: 1px solid #ef4444; }
        .p-review { background: rgba(245, 158, 11, 0.25); color: #fbbf24; border: 1px solid #f59e0b; }
        .p-routine { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; }
        .p-retake  { background: rgba(225, 29, 72, 0.3); color: #fb7185; border: 1px dashed #e11d48; }
        .q-desc { font-size: 10.5px; color: var(--text-secondary); display: flex; justify-content: space-between; }
        
        .dropzone {
            border: 2px dashed #334155;
            border-radius: 10px;
            padding: 12px;
            text-align: center;
            background: #0d1527;
            cursor: pointer;
            transition: all 0.2s;
        }
        .dropzone:hover, .dropzone.dragover {
            border-color: var(--accent-cyan);
            background: rgba(6, 182, 212, 0.08);
        }
        
        .content {
            padding: 18px 22px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
''')
html_parts.append('''        .quality-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 14px 18px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .quality-header { display: flex; justify-content: space-between; align-items: center; }
        .q-status-badge {
            font-size: 11.5px; font-weight: 800; padding: 4px 12px; border-radius: 20px;
            display: flex; align-items: center; gap: 6px;
        }
        .q-good { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; }
        .q-borderline { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #f59e0b; }
        .q-ungradeable { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #ef4444; }
        
        .q-metrics-row {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11.5px;
        }
        .q-metric-box {
            background: #0b1120;
            padding: 7px 10px;
            border-radius: 7px;
            border: 1px solid #1e293b;
        }
        .q-metric-box span { color: var(--text-secondary); font-size: 9.5px; text-transform: uppercase; display: block; }
        .q-metric-box b { font-size: 13.5px; margin-top: 2px; display: block; }
        
        .guidance-box {
            padding: 9px 12px;
            border-radius: 0 7px 7px 0;
            font-size: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .guidance-recapture {
            background: rgba(239, 68, 68, 0.12);
            border-left: 4px solid #ef4444;
            color: #fca5a5;
        }
        .guidance-enhance {
            background: rgba(6, 182, 212, 0.12);
            border-left: 4px solid #06b6d4;
            color: #7dd3fc;
        }
        
        /* INTERACTIVE SPLIT CANVAS */
        .viewport-box {
            position: relative;
            width: 100%;
            height: 480px;
            background: #000;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #1e293b;
            display: flex;
            align-items: center;
            justify-content: center;
            user-select: none;
        }
        #mainCanvas {
            max-width: 100%;
            max-height: 100%;
            display: block;
        }
        .split-curtain {
            position: absolute;
            top: 0; bottom: 0; width: 4px;
            background: var(--accent-cyan);
            box-shadow: 0 0 12px rgba(6, 182, 212, 0.9);
            cursor: ew-resize;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10;
        }
        .split-handle {
            width: 32px; height: 32px;
            background: #0f172a;
            border: 2px solid var(--accent-cyan);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            color: var(--accent-cyan);
            font-size: 11px; font-weight: bold;
            box-shadow: 0 0 10px rgba(0,0,0,0.8);
            pointer-events: none;
        }
        
        .live-control-toolbar {
            background: #0b1120;
            border: 1px solid #1e293b;
            border-radius: 10px;
            padding: 10px 14px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
            font-size: 11px;
            font-weight: 600;
        }
        .ctrl-item { display: flex; align-items: center; gap: 8px; }
        .ctrl-item input[type=range] { width: 100px; accent-color: var(--accent-cyan); cursor: pointer; }
        .ctrl-item input[type=checkbox] { accent-color: var(--accent-cyan); cursor: pointer; }
        
        .referable-banner {
            border-radius: 12px;
            padding: 16px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
        .ref-urgent {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.25), rgba(153, 27, 27, 0.45));
            border: 1.5px solid #ef4444;
        }
        .ref-routine {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(6, 95, 70, 0.35));
            border: 1.5px solid #10b981;
        }
        .ref-title { font-size: 20px; font-weight: 800; display: flex; align-items: center; gap: 8px; }
        .ref-sub { font-size: 12px; color: #cbd5e1; margin-top: 3px; }
        
        .review-console {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 14px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 14px;
        }
        .stopwatch {
            display: flex;
            align-items: center;
            gap: 8px;
            font-family: 'JetBrains Mono', monospace;
            background: #0b1120;
            border: 1px solid #1e293b;
            padding: 6px 14px;
            border-radius: 7px;
        }
        .stopwatch-time { font-size: 18px; font-weight: 800; color: var(--accent-cyan); }
        
        .action-group { display: flex; gap: 8px; }
        .btn-act {
            border: none; padding: 9px 15px; border-radius: 7px;
            font-size: 12px; font-weight: 700; cursor: pointer; transition: all 0.2s;
            display: flex; align-items: center; gap: 5px;
        }
        .btn-confirm { background: #10b981; color: white; }
        .btn-modify  { background: #334155; color: #f8fafc; }
        .btn-recapture { background: #ef4444; color: white; }
        .btn-refer   { background: var(--accent-blue); color: white; }
        .btn-act:hover { opacity: 0.9; transform: translateY(-1px); }
        
        .sim-control-box {
            background: #0b1120;
            border: 1px solid #1e293b;
            border-radius: 10px;
            padding: 14px;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
        }
        .sim-slider-group { display: flex; flex-direction: column; gap: 4px; }
        .sim-slider-group label { font-size: 11.5px; font-weight: 700; color: #cbd5e1; display: flex; justify-content: space-between; }
        .sim-slider-group input[type=range] { width: 100%; accent-color: var(--accent-cyan); cursor: pointer; }
        
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.8);
            backdrop-filter: blur(6px);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }
        .modal.open { display: flex; }
        .report-sheet {
            background: #ffffff;
            color: #0f172a;
            width: 740px;
            max-height: 90vh;
            overflow-y: auto;
            border-radius: 10px;
            padding: 28px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.8);
            display: flex;
            flex-direction: column;
            gap: 14px;
            font-size: 12.5px;
        }
    </style>
</head>
<body>
''')
html_parts.append('''    <header>
        <div class="brand">
            <div class="brand-logo">D</div>
            <div class="brand-text">
                <h1>DRISHTI AI Screening Engine</h1>
                <p>Real-Time Functional Clinical & Telemedicine Portal | MathWorks SIH26038</p>
            </div>
        </div>

        <!-- ROLE SWITCHER -->
        <div class="role-switcher">
            <button class="role-btn" id="roleField" onclick="setRole('field')">📱 Field Mode (ASHA)</button>
            <button class="role-btn active" id="roleClinical" onclick="setRole('clinical')">👨‍⚕️ Clinical Mode (Ophthalmologist)</button>
            <button class="role-btn" id="roleAdmin" onclick="setRole('admin')">🗺️ District Admin & Simulink</button>
        </div>

        <div class="header-status">
            <!-- VOICE GUIDANCE TOGGLE -->
            <button class="btn-act" id="btnVoiceToggle" style="background:#1e293b; color:#38bdf8; font-size:11px;" onclick="toggleVoice()">🔊 Voice: ON</button>
            <!-- NETWORK STATUS -->
            <div class="net-badge" id="netBadge" onclick="toggleNetwork()">
                <div class="pulse-dot" id="pulseDot"></div>
                <span id="netText">Online: 2.4 Mbps (PHC Uplink)</span>
            </div>
            <button class="btn-act" style="background:#0284c7; color:white; font-size:11px;" onclick="openReportModal()">📄 Report</button>
        </div>
    </header>

    <div class="main-layout">
        <!-- SIDEBAR: PRIORITY QUEUE + LIVE DROPZONE -->
        <div class="sidebar">
            <div>
                <div class="section-header">
                    <span>Priority Triage Queue</span>
                    <span style="font-size: 9.5px; color: var(--accent-cyan);">Sorted by Risk</span>
                </div>
                <div class="queue-list" id="queueList"></div>
            </div>

            <!-- LIVE FILE UPLOAD / DRAG-AND-DROP DROPZONE -->
            <div>
                <div class="section-header">
                    <span>Analyze Custom Retina</span>
                    <span style="font-size: 9.5px; color: #10b981;">Real-Time</span>
                </div>
                <div class="dropzone" id="fileDropzone" onclick="document.getElementById('fileInput').click()">
                    <span style="font-size: 20px;">📤</span>
                    <div style="font-size: 11.5px; font-weight:700; color:#cbd5e1; margin-top:4px;">Drop Any Fundus Image</div>
                    <div style="font-size: 9.5px; color:#64748b;">or click to browse local files (JPG/PNG)</div>
                    <input type="file" id="fileInput" accept="image/*" style="display: none;" onchange="handleFileUpload(event)">
                </div>
            </div>

            <!-- RURAL OFFLINE QUEUE -->
            <div style="background: #0d1527; border: 1px solid #1e293b; border-radius: 9px; padding: 10px; margin-top: auto;">
                <div style="font-size: 10.5px; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin-bottom: 4px;">Offline Rural Hub</div>
                <div style="font-size: 11px; display: flex; justify-content: space-between; color: #cbd5e1; margin-bottom: 6px;">
                    <span>Pending Local Sync: <b id="pendingSyncCount" style="color:#fbbf24;">3 Cases</b></span>
                    <span style="color:#34d399;">9 Synced</span>
                </div>
                <button class="btn-act" style="width:100%; justify-content:center; background:#0284c7; color:white; padding:6px; font-size:10.5px;" onclick="syncOfflineQueue()">🔄 SYNC WHEN CONNECTED</button>
                <div id="syncProg" style="height:3px; background:#1e293b; border-radius:2px; margin-top:6px; display:none; overflow:hidden;">
                    <div style="width:100%; height:100%; background:#10b981; animation:syncMove 1s infinite linear;"></div>
                </div>
            </div>
        </div>

        <!-- MAIN WORKSPACE -->
        <div class="content">
''')
html_parts.append('''            <!-- ROLE 1: FIELD MODE (ASHA) -->
            <div id="view-field" style="display: none; flex-direction: column; gap: 16px;">
                <div style="background:#131d33; border:1px solid #1e293b; border-radius:12px; padding:20px; text-align:center; display:flex; flex-direction:column; align-items:center; gap:14px;">
                    <h2 style="font-size: 20px; font-weight:800; color:#38bdf8;">📱 DRISHTI AI MOBILE SCREENING (FIELD MODE)</h2>
                    <p style="color:#94a3b8; font-size:12.5px; max-width:540px;">Simplified automated screening for rural Primary Health Centre workers using portable handheld cameras.</p>
                    
                    <button class="btn-act" style="background:#0284c7; color:white; padding:12px 24px; font-size:13.5px;" onclick="simulateFieldCapture()">📷 [ CAPTURE / ACQUIRE RETINA ]</button>

                    <div style="background:#0b1120; border:1px solid #1e293b; border-radius:10px; padding:16px; width:100%; max-width:480px; text-align:left; display:flex; flex-direction:column; gap:8px;">
                        <div style="font-size:11px; color:#64748b; font-weight:700;">STEP 1: EDGE QUALITY ASSESSMENT</div>
                        <div style="font-size:15px; font-weight:800; color:#34d399;" id="fieldQStatus">🟢 IMAGE QUALITY: GOOD</div>
                        
                        <div style="font-size:11px; color:#64748b; font-weight:700; margin-top:6px;">STEP 2: RAPID EDGE AI TRIAGE</div>
                        <button class="btn-act" style="background:#10b981; color:white; justify-content:center; padding:10px;" onclick="runFieldAI()">⚡ [ RUN AI SCREENING ]</button>
                        
                        <div style="font-size:11px; color:#64748b; font-weight:700; margin-top:6px;">STEP 3: ACTIONABLE FIELD RESULT</div>
                        <div id="fieldResultBox" style="background:#1e293b; padding:10px; border-radius:7px; font-weight:800; font-size:14px; color:#fbbf24;">
                            ⚠ SPECIALIST REVIEW RECOMMENDED (Moderate NPDR)
                        </div>
                        <button class="btn-act" style="background:#3b82f6; color:white; justify-content:center; padding:10px; margin-top:4px;" onclick="sendToHub()">📤 [ SEND TO DISTRICT TELE-HUB ]</button>
                    </div>
                </div>
            </div>

            <!-- ROLE 2: CLINICAL MODE (OPHTHALMOLOGIST) -->
            <div id="view-clinical" style="display: flex; flex-direction: column; gap: 16px;">
                
                <!-- SMART FUNDUS QUALITY GATE -->
                <div class="quality-card">
                    <div class="quality-header">
                        <div>
                            <span style="font-size: 10.5px; text-transform:uppercase; color:#64748b; font-weight:800; letter-spacing:0.5px;">1. Smart Fundus Image Quality Gate</span>
                            <h3 style="font-size: 15px; font-weight:800; margin-top:2px;" id="qCardTitle">Camera Alignment & Focus Evaluation</h3>
                        </div>
                        <div class="q-status-badge q-good" id="qBadge">● IMAGE QUALITY: ACCEPTABLE</div>
                    </div>

                    <div class="q-metrics-row">
                        <div class="q-metric-box"><span>Blur / Tenengrad Focus</span><b id="mBlur">41.8 (>15.0)</b></div>
                        <div class="q-metric-box"><span>Illumination Balance</span><b id="mIllum">Optimal (0.46)</b></div>
                        <div class="q-metric-box"><span>Retinal FoV Coverage</span><b id="mFoV">86.4% (>75%)</b></div>
                        <div class="q-metric-box"><span>Corneal Glare Ratio</span><b id="mGlare">1.8% (&lt;15%)</b></div>
                    </div>

                    <!-- AI-GUIDED RECAPTURE GUIDANCE -->
                    <div class="guidance-box guidance-enhance" id="qGuidance">
                        <span style="font-size: 16px;">✨</span>
                        <div>
                            <b id="guidanceTitle">Adaptive Auto-Enhancement Active:</b>
                            <span id="guidanceText">Borderline illumination normalized via CLAHE in CIE L*a*b* space. Proceeding to clinical classification.</span>
                        </div>
                    </div>
                </div>

                <!-- REFERABLE DR BANNER -->
                <div class="referable-banner ref-urgent" id="refBanner">
                    <div>
                        <span style="font-size:10.5px; text-transform:uppercase; letter-spacing:1px; font-weight:800; color:#fca5a5;">REFERABLE DR STATUS</span>
                        <div class="ref-title" id="refTitle">🔴 REFER TO OPHTHALMOLOGIST</div>
                        <div class="ref-sub" id="refReason">Priority: HIGH | Reason: Level 2 Moderate NPDR + High DME Risk near foveal zone</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:10.5px; color:#cbd5e1; text-transform:uppercase;">ICDR Severity Staging</div>
                        <div style="font-size:18px; font-weight:800; color:white;" id="icdrGrade">LEVEL 2 — MODERATE NPDR</div>
                    </div>
                </div>

                <!-- REAL-TIME INTERACTIVE VIEWPORT & SPLIT-SLIDER -->
                <div class="quality-card" style="padding:14px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="font-size: 13px; font-weight:800; display:flex; align-items:center; gap:8px;">
                            <span>👁️ Real-Time Interactive Viewport</span>
                            <span style="font-size:10.5px; font-weight:normal; color:#06b6d4;">(Drag divider across canvas to wipe Before / Enhanced)</span>
                        </span>
                        <span style="font-size: 11px; font-family:'JetBrains Mono'; color:#34d399;" id="canvasModeLabel">SPLIT: RAW (LEFT) vs ENHANCED (RIGHT)</span>
                    </div>

                    <div class="viewport-box" id="viewportBox">
                        <canvas id="mainCanvas" width="512" height="512"></canvas>
                        <div class="split-curtain" id="splitCurtain" style="left: 50%;">
                            <div class="split-handle">⬌</div>
                        </div>
                    </div>

                    <!-- REAL-TIME PARAMETER & LESION CONTROL TOOLBAR -->
                    <div class="live-control-toolbar" style="margin-top:8px;">
                        <div class="ctrl-item">
                            <span>CLAHE Clip Limit:</span>
                            <input type="range" id="sliderClip" min="0.01" max="0.05" step="0.005" value="0.02" oninput="updateRealtimeCanvas()">
                            <span id="valClip" style="color:#06b6d4;">0.020</span>
                        </div>
                        <div class="ctrl-item">
                            <span>Illum. Flattening:</span>
                            <input type="range" id="sliderFlatten" min="0" max="100" step="5" value="75" oninput="updateRealtimeCanvas()">
                            <span id="valFlatten" style="color:#06b6d4;">75%</span>
                        </div>
                        <div class="ctrl-item">
                            <span>Grad-CAM Heatmap:</span>
                            <input type="range" id="sliderHeatmap" min="0" max="100" step="5" value="50" oninput="updateRealtimeCanvas()">
                            <span id="valHeatmap" style="color:#06b6d4;">50%</span>
                        </div>
                        <div class="ctrl-item">
                            <label><input type="checkbox" id="chkVessels" checked onchange="updateRealtimeCanvas()"> Vessels (DRIVE)</label>
                        </div>
                        <div class="ctrl-item">
                            <label><input type="checkbox" id="chkMAs" checked onchange="updateRealtimeCanvas()"> MAs (Magenta)</label>
                        </div>
                        <div class="ctrl-item">
                            <label><input type="checkbox" id="chkExudates" checked onchange="updateRealtimeCanvas()"> Exudates (Yellow)</label>
                        </div>
                        <div class="ctrl-item">
                            <label><input type="checkbox" id="chkHemo" checked onchange="updateRealtimeCanvas()"> Hemo (Red)</label>
                        </div>
                    </div>
                </div>

                <!-- LESION EVIDENCE & RELIABILITY METER -->
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">
                    <div class="quality-card">
                        <div style="font-size:11px; font-weight:800; color:#64748b; text-transform:uppercase;">6. EVIDENCE-TO-DECISION CORRELATION</div>
                        <div style="font-size:12px; color:#cbd5e1; line-height:1.5; margin-top:4px;" id="evidenceNarrative">
                            ✓ Microaneurysms detected with sub-pixel parabolic peak interpolation<br>
                            ✓ Hard exudates localized near foveal center (CSME positive)<br>
                            ✓ Grad-CAM attention hotspots precisely align with hemorrhagic clusters
                        </div>
                        <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:6px; font-family:'JetBrains Mono'; font-size:11px; margin-top:8px;">
                            <div class="q-metric-box"><span>MAs</span><b id="liveMAs" style="color:#38bdf8;">19</b></div>
                            <div class="q-metric-box"><span>Hemo</span><b id="liveHemo" style="color:#f87171;">18</b></div>
                            <div class="q-metric-box"><span>Vessel Density</span><b id="liveDensity" style="color:#34d399;">9.4%</b></div>
                            <div class="q-metric-box"><span>CSME Proximity</span><b id="liveCSME" style="color:#fbbf24;">0.12 DD</b></div>
                        </div>
                    </div>

                    <div class="quality-card">
                        <div style="font-size:11px; font-weight:800; color:#64748b; text-transform:uppercase;">8. AI RELIABILITY & CALIBRATION METER</div>
                        <div style="display:flex; flex-direction:column; gap:6px; margin-top:6px;">
                            <div style="display:flex; justify-content:space-between; font-size:11px;">
                                <span>Model Confidence (Temperature Scaled):</span>
                                <b id="lblRelConf" style="color:#06b6d4;">91.5%</b>
                            </div>
                            <div style="width:100%; height:5px; background:#0b1120; border-radius:3px; overflow:hidden;">
                                <div id="barRelConf" style="width:91.5%; height:100%; background:#06b6d4;"></div>
                            </div>

                            <div style="display:flex; justify-content:space-between; font-size:11px; margin-top:2px;">
                                <span>Image Quality Factor:</span>
                                <b id="lblRelQual" style="color:#10b981;">88.0%</b>
                            </div>
                            <div style="width:100%; height:5px; background:#0b1120; border-radius:3px; overflow:hidden;">
                                <div id="barRelQual" style="width:88.0%; height:100%; background:#10b981;"></div>
                            </div>

                            <div style="display:flex; justify-content:space-between; font-size:11px; margin-top:2px;">
                                <span>Explanation Agreement:</span>
                                <b id="lblRelAgr" style="color:#8b5cf6;">92.0%</b>
                            </div>
                            <div style="width:100%; height:5px; background:#0b1120; border-radius:3px; overflow:hidden;">
                                <div id="barRelAgr" style="width:92.0%; height:100%; background:#8b5cf6;"></div>
                            </div>
                        </div>
                        <div style="margin-top:6px; display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:11px; font-weight:700;">Overall Reliability:</span>
                            <span class="q-status-badge q-good" id="relStatusBadge">🟢 HIGH RELIABILITY</span>
                        </div>
                    </div>
                </div>

                <!-- HUMAN IN THE LOOP REVIEW & STOPWATCH -->
                <div class="review-console">
                    <div>
                        <div style="font-size:10.5px; font-weight:800; color:#64748b; text-transform:uppercase;">9. HUMAN-IN-THE-LOOP OPHTHALMOLOGIST CONSOLE</div>
                        <h4 style="font-size:15px; font-weight:800; margin-top:2px;">30-Second Rapid Validation</h4>
                    </div>

                    <div class="stopwatch">
                        <span style="font-size:10.5px; color:#94a3b8;">STOPWATCH:</span>
                        <span class="stopwatch-time" id="reviewStopwatch">00.0s</span>
                        <button onclick="toggleStopwatch()" style="background:none; border:none; color:var(--accent-cyan); cursor:pointer; font-size:12px;">⏸/▶</button>
                        <span style="font-size:9.5px; color:#10b981; font-weight:700;">[&lt;30s TARGET]</span>
                    </div>

                    <div class="action-group">
                        <button class="btn-act btn-confirm" onclick="confirmDiagnosis()">✓ Confirm AI</button>
                        <button class="btn-act btn-modify" onclick="modifyGradePrompt()">✎ Modify Grade</button>
                        <button class="btn-act btn-recapture" onclick="triggerRecapture()">⚠ Request Recapture</button>
                        <button class="btn-act btn-refer" onclick="referSpecialist()">→ Refer Patient</button>
                    </div>
                </div>
            </div>
''')
html_parts.append('''            <!-- ROLE 3: DISTRICT ADMIN & SIMULINK MODE -->
            <div id="view-admin" style="display: none; flex-direction: column; gap: 16px;">
                
                <div style="background:var(--card-bg); border:1px solid var(--card-border); border-radius:12px; padding:16px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                        <div>
                            <span style="font-size:10.5px; text-transform:uppercase; color:#64748b; font-weight:800;">12. District Screening Intelligence</span>
                            <h3 style="font-size:16px; font-weight:800; margin-top:2px;">Nanded District Retinal Tele-Program (Annual Monitoring)</h3>
                        </div>
                        <div class="q-status-badge q-good">● 25 PHCs & 3 Mobile Vans Connected</div>
                    </div>

                    <div style="display:grid; grid-template-columns:repeat(6, 1fr); gap:10px;">
                        <div class="q-metric-box"><span>Patients Screened</span><b style="color:#38bdf8; font-size:18px;">12,458</b></div>
                        <div class="q-metric-box"><span>Referable DR Cases</span><b style="color:#fb7185; font-size:18px;">2,142</b></div>
                        <div class="q-metric-box"><span>High Priority Queue</span><b style="color:#ef4444; font-size:18px;">318</b></div>
                        <div class="q-metric-box"><span>Recaptures Advised</span><b style="color:#fbbf24; font-size:18px;">672</b></div>
                        <div class="q-metric-box"><span>Avg AI Pipeline</span><b style="color:#34d399; font-size:18px;">1.2s</b></div>
                        <div class="q-metric-box"><span>Avg Review Time</span><b style="color:#a78bfa; font-size:18px;">18.4s</b></div>
                    </div>
                </div>

                <!-- SIMULINK INTERACTIVE QUEUING ENGINE & LIVE GRAPH CANVAS -->
                <div style="background:var(--card-bg); border:1px solid var(--card-border); border-radius:12px; padding:16px; display:flex; flex-direction:column; gap:12px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span style="font-size:10.5px; text-transform:uppercase; color:#64748b; font-weight:800;">14 & 15. Real-Time Simulink Resource Optimization Engine</span>
                            <h3 style="font-size:16px; font-weight:800; margin-top:2px;">District Dynamic Queuing Model (100,000+ Target)</h3>
                        </div>
                        <span style="font-size:11px; color:#38bdf8; font-family:'JetBrains Mono';">telemed_dr_screening.slx (Live JS Solver)</span>
                    </div>

                    <div class="sim-control-box">
                        <div class="sim-slider-group">
                            <label><span>Patients / Day:</span> <b id="lblPatientsDay" style="color:#38bdf8;">400</b></label>
                            <input type="range" id="sliderPatients" min="100" max="600" step="25" value="400" oninput="runSimulinkEngine()">
                            <span style="font-size:9.5px; color:#64748b;">Annual Cohort: 25,000 to 150,000</span>
                        </div>
                        <div class="sim-slider-group">
                            <label><span>Rural Bandwidth:</span> <b id="lblBandwidth" style="color:#34d399;">2.4 Mbps</b></label>
                            <input type="range" id="sliderBw" min="0.5" max="10" step="0.5" value="2.4" oninput="runSimulinkEngine()">
                            <span style="font-size:9.5px; color:#64748b;">Cellular Uplink Speed</span>
                        </div>
                        <div class="sim-slider-group">
                            <label><span>District Specialists:</span> <b id="lblDoctors" style="color:#fbbf24;">2 Doctors</b></label>
                            <input type="range" id="sliderDocs" min="1" max="6" step="1" value="2" oninput="runSimulinkEngine()">
                            <span style="font-size:9.5px; color:#64748b;">Ophthalmologist Reading Pool</span>
                        </div>
                    </div>

                    <!-- LIVE SIMULINK CANVAS CHART -->
                    <div style="background:#070a13; border:1px solid #1e293b; border-radius:10px; padding:12px;">
                        <canvas id="simulinkCanvas" width="800" height="220" style="width:100%; height:220px; display:block;"></canvas>
                    </div>

                    <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:10px; font-family:'JetBrains Mono';">
                        <div class="q-metric-box"><span>Annual Screening Capacity</span><b id="simCap" style="color:#34d399; font-size:16px;">100,000</b></div>
                        <div class="q-metric-box"><span>Average Patient Queue Delay</span><b id="simWait" style="color:#38bdf8; font-size:16px;">0.4 hrs (No Backlog)</b></div>
                        <div class="q-metric-box"><span>Annual Cellular Data Saved</span><b id="simDataSaved" style="color:#a78bfa; font-size:16px;">431.3 GB (75.0%)</b></div>
                        <div class="q-metric-box"><span>Doctor Throughput Multiplier</span><b id="simMult" style="color:#34d399; font-size:16px;">7.0x (30s Review)</b></div>
                    </div>

                    <div style="background:#0b1120; border-left:4px solid #38bdf8; padding:12px; border-radius:0 7px 7px 0; font-size:12px; line-height:1.5;" id="whatIfAdvice">
                        <b>🤖 AI Resource Planning Advisory:</b> Target of 100,000+ patients ACHIEVED! Current configuration of <b>2 Specialists</b> and <b>2.4 Mbps</b> cellular link accommodates <b>100,000 patients/year</b> with negligible queue wait time.
                    </div>
                </div>

                <!-- MODEL BENCHMARKS & AUDIT TRAIL -->
                <div style="display:grid; grid-template-columns:1.2fr 1fr; gap:14px;">
                    <div style="background:var(--card-bg); border:1px solid var(--card-border); border-radius:12px; padding:14px;">
                        <span style="font-size:10.5px; text-transform:uppercase; color:#64748b; font-weight:800;">16. Held-Out Indian Benchmark Validation</span>
                        <table style="width:100%; border-collapse:collapse; font-size:11px; font-family:'JetBrains Mono'; margin-top:8px;">
                            <thead>
                                <tr style="border-bottom:1px solid #334155; color:#94a3b8; text-align:left;">
                                    <th style="padding:5px;">Metric</th>
                                    <th style="padding:5px;">Target</th>
                                    <th style="padding:5px;">DRISHTI Pipeline</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr style="border-bottom:1px solid #1e293b;">
                                    <td style="padding:6px; color:#cbd5e1;">Referable Sensitivity</td>
                                    <td style="padding:6px;">&gt; 90.0%</td>
                                    <td style="padding:6px; color:#34d399; font-weight:bold;">94.8%</td>
                                </tr>
                                <tr style="border-bottom:1px solid #1e293b;">
                                    <td style="padding:6px; color:#cbd5e1;">Referable Specificity</td>
                                    <td style="padding:6px;">&gt; 85.0%</td>
                                    <td style="padding:6px; color:#34d399; font-weight:bold;">92.4%</td>
                                </tr>
                                <tr style="border-bottom:1px solid #1e293b;">
                                    <td style="padding:6px; color:#cbd5e1;">AUC-ROC</td>
                                    <td style="padding:6px;">&gt; 0.900</td>
                                    <td style="padding:6px; color:#38bdf8;">0.981</td>
                                </tr>
                                <tr>
                                    <td style="padding:6px; color:#cbd5e1;">Quadratic Kappa</td>
                                    <td style="padding:6px;">&gt; 0.800</td>
                                    <td style="padding:6px; color:#38bdf8;">0.916</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div style="background:var(--card-bg); border:1px solid var(--card-border); border-radius:12px; padding:14px; display:flex; flex-direction:column; gap:6px;">
                        <span style="font-size:10.5px; text-transform:uppercase; color:#64748b; font-weight:800;">19. Live Clinical Audit Log</span>
                        <div style="background:#0b1120; border:1px solid #1e293b; border-radius:7px; padding:8px 10px; font-family:'JetBrains Mono'; font-size:10px; color:#cbd5e1; display:flex; flex-direction:column; gap:4px; max-height:130px; overflow-y:auto;" id="auditLog">
                            <div><span style="color:#64748b;">10:24:02</span> — Fundus capture acquired at Nanded PHC #4</div>
                            <div><span style="color:#64748b;">10:24:04</span> — Image Quality Gate: PASS (Focus: 41.8, Glare: 1.8%)</div>
                            <div><span style="color:#64748b;">10:24:06</span> — Edge AI completed: Level 2 Moderate NPDR (91.5%)</div>
                            <div><span style="color:#64748b;">10:25:12</span> — Prioritized as Priority 1 (High DME Risk)</div>
                            <div><span style="color:#64748b;">10:26:45</span> — Clinical report generated & signed</div>
                        </div>
                    </div>
                </div>

            </div>
''')
html_parts.append('''        </div>
    </div>

    <!-- REPORT MODAL -->
    <div class="modal" id="reportModal" onclick="closeReportModal(event)">
        <div class="report-sheet" onclick="event.stopPropagation()">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; border-bottom:2px solid #0f172a; padding-bottom:10px;">
                <div>
                    <h2 style="font-size:20px; font-weight:800; color:#0284c7;">DRISHTI AI RETINAL SCREENING REPORT</h2>
                    <div style="font-size:11.5px; color:#64748b;">Autonomous Rural Diabetic Retinopathy Tele-Triage System</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-family:'JetBrains Mono'; font-weight:700; font-size:12px;" id="repCaseId">CASE ID: DR-2026-00128</div>
                    <div style="font-size:10.5px; color:#64748b;" id="repDate">Date: 2026-09-05 | Nanded PHC #04</div>
                </div>
            </div>

            <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; background:#f8fafc; padding:10px; border-radius:7px;">
                <div>
                    <div style="font-size:10px; font-weight:700; color:#64748b; text-transform:uppercase;">Patient Token</div>
                    <div style="font-size:12.5px; font-weight:700;" id="repPatId">PAT_003_MODERATE</div>
                    <div style="font-size:11px; color:#64748b;">Age: 58 | Sex: M | Duration: 11 Yrs</div>
                </div>
                <div>
                    <div style="font-size:10px; font-weight:700; color:#64748b; text-transform:uppercase;">Image Quality Gate</div>
                    <div style="font-size:12.5px; font-weight:700; color:#059669;" id="repQuality">ACCEPTABLE (Focus: 41.8, Glare: 1.8%)</div>
                    <div style="font-size:11px; color:#64748b;">Handheld 45° Non-Mydriatic Fundus</div>
                </div>
            </div>

            <div style="border:1.5px solid #0f172a; border-radius:7px; padding:12px; background:#f0fdf4;" id="repResultCard">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-size:10px; font-weight:700; text-transform:uppercase; color:#059669;">ICDR DR Severity Staging</div>
                        <div style="font-size:17px; font-weight:800; color:#0f172a;" id="repGrade">LEVEL 2 — MODERATE NPDR</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:10px; font-weight:700; text-transform:uppercase; color:#dc2626;">Referable Status</div>
                        <div style="font-size:16px; font-weight:800; color:#dc2626;" id="repReferable">YES (REFER TO SPECIALIST)</div>
                    </div>
                </div>
                <div style="margin-top:8px; font-size:11.5px; color:#334155; line-height:1.4;" id="repRationale">
                    Microaneurysms (19) and intraretinal blot hemorrhages (18) detected. Hard exudates present within 0.12 DD of fovea (CSME Positive).
                </div>
            </div>

            <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:8px; font-family:'JetBrains Mono'; font-size:11px;">
                <div style="background:#f1f5f9; padding:7px; border-radius:5px;">MAs: <b id="repMAs">19</b></div>
                <div style="background:#f1f5f9; padding:7px; border-radius:5px;">Hemo: <b id="repHemo">18</b></div>
                <div style="background:#f1f5f9; padding:7px; border-radius:5px;">CSME Proximity: <b id="repCSME">0.12 DD</b></div>
                <div style="background:#f1f5f9; padding:7px; border-radius:5px;">Confidence: <b id="repConf" style="color:#0284c7;">91.5%</b></div>
            </div>

            <div style="background:#f8fafc; border-left:4px solid #0284c7; padding:10px; font-size:12px;">
                <b>Recommended Action:</b> <span id="repAction">Prompt referral to Ophthalmologist within 1-2 weeks.</span>
            </div>

            <div style="display:flex; justify-content:space-between; align-items:flex-end; padding-top:8px; border-top:1px solid #e2e8f0;">
                <div style="font-size:9.5px; color:#64748b; max-width:440px; line-height:1.3;">
                    <b>NOTICE:</b> DRISHTI AI decision-support output. Final clinical sign-off must be performed by a qualified ophthalmologist.
                </div>
                <div style="text-align:right; border:1.5px dashed #059669; padding:4px 10px; border-radius:5px; color:#059669; font-weight:800; font-size:10.5px;">
                    DIGITALLY VALIDATED<br><span style="font-size:8.5px; font-weight:normal; color:#475569;">Dr. R. Sharma, MS (Ophth)</span>
                </div>
            </div>

            <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:4px;">
                <button class="btn-act" style="background:#475569; color:white;" onclick="closeReportModal()">Close</button>
                <button class="btn-act" style="background:#0284c7; color:white;" onclick="window.print()">🖨️ Print / Save PDF</button>
            </div>
        </div>
    </div>
''')
