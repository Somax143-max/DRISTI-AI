%% =========================================================================
% MATHWORKS - SMART INDIA HACKATHON (SIH26038)
% EXPLAINABLE AI FOR DIABETIC RETINOPATHY SCREENING IN RURAL INDIA
% =========================================================================
% Master Pipeline Runner & Demonstration Script
%
% Toolboxes Used:
%   - Image Processing Toolbox
%   - Computer Vision Toolbox
%   - Deep Learning Toolbox
%   - Statistics and Machine Learning Toolbox
%   - Simulink
%
% Authors: MathWorks SIH26038 Solution Team
% =========================================================================

clear; clc; close all;

% Add paths
projectRoot = fileparts(mfilename('fullpath'));
addpath(fullfile(projectRoot, 'src'));
addpath(fullfile(projectRoot, 'simulink'));

resultsDir = fullfile(projectRoot, 'results');
if ~exist(resultsDir, 'dir')
    mkdir(resultsDir);
end

fprintf('=====================================================================\n');
fprintf('  SIH26038: EXPLAINABLE AI FOR RURAL DIABETIC RETINOPATHY SCREENING  \n');
fprintf('  MathWorks Automated Retinal Screening & Telemedicine Optimization  \n');
fprintf('=====================================================================\n\n');

%% 1. RUN DEMONSTRATION ACROSS ALL ICDR GRADES (0 to 4) + UNGRADEABLE
testCases = {
    struct('id', 'PAT_001_NORMAL',  'grade', 0, 'degraded', false), ...
    struct('id', 'PAT_002_MILD',    'grade', 1, 'degraded', false), ...
    struct('id', 'PAT_003_MODERATE','grade', 2, 'degraded', false), ...
    struct('id', 'PAT_004_SEVERE',  'grade', 3, 'degraded', false), ...
    struct('id', 'PAT_005_PDR',     'grade', 4, 'degraded', false), ...
    struct('id', 'PAT_006_BLURRED', 'grade', 2, 'degraded', true)  ... % Should trigger IQA Reject
};

summaryTable = cell(length(testCases), 8);

for i = 1:length(testCases)
    tc = testCases{i};
    fprintf('>>> Processing Case %d/%d: %s (Target Grade: %d, Degraded: %d)...\n', ...
        i, length(testCases), tc.id, tc.grade, tc.degraded);
    
    % Step 1: Image Acquisition / Generation
    fundusRGB = generate_synthetic_fundus(tc.grade, 512, tc.degraded);
    
    % Step 2: Image Quality Assessment (IQA)
    [isGradeable, qualityClass, feedbackMsg, qMetrics] = assess_image_quality(fundusRGB);
    fprintf('    [IQA] Gradeable: %d | Quality: %s | Focus: %.1f\n', ...
        isGradeable, qualityClass, qMetrics.focusScore);
    fprintf('    [Feedback] %s\n', feedbackMsg);
    
    if ~isGradeable
        fprintf('    [ACTION] Recapture requested on edge device. Halting downstream inference.\n\n');
        summaryTable{i, 1} = tc.id;
        summaryTable{i, 2} = qualityClass;
        summaryTable{i, 3} = 'REJECTED';
        summaryTable{i, 4} = 'N/A (Recapture Requested)';
        summaryTable{i, 5} = 'No';
        summaryTable{i, 6} = 0;
        summaryTable{i, 7} = 0;
        summaryTable{i, 8} = feedbackMsg;
        continue;
    end
    
    % Step 3: Adaptive Illumination & CLAHE Enhancement
    [enhancedRGB, fovMask, greenEnhanced] = enhance_fundus(fundusRGB);
    
    % Step 4: Retinal Landmark & Vascular Segmentation
    structures = segment_retinal_structures(enhancedRGB, fovMask, greenEnhanced);
    
    % Step 5: Sub-pixel Lesion Detection
    maResults = detect_microaneurysms(greenEnhanced, structures.vessels.mask, fovMask, structures.opticDisc.mask);
    exudateResults = detect_exudates(enhancedRGB, greenEnhanced, fovMask, structures.opticDisc.mask, structures.fovea.center, structures.opticDisc.radius);
    hemoResults = detect_hemorrhages_neovascularization(enhancedRGB, greenEnhanced, structures.vessels.mask, fovMask, structures.opticDisc.mask, structures.opticDisc.center, structures.opticDisc.radius);
    
    % Step 6: ICDR Severity Grading & Clinical Rule Engine
    [drGrade, gradeName, isReferable, confScore, rationale, action] = grade_dr_severity(maResults, exudateResults, hemoResults, qMetrics);
    fprintf('    [DIAGNOSIS] %s\n', gradeName);
    fprintf('    [REFERABLE] %d | Confidence: %.1f%% | CSME Risk: %s\n', ...
        isReferable, confScore * 100, exudateResults.csmeRisk);
    
    % Step 7: Explainability Module (Grad-CAM, Lesion Overlay, Clinical Report)
    reportStruct = generate_explainability_report(tc.id, fundusRGB, enhancedRGB, qMetrics, ...
        structures, maResults, exudateResults, hemoResults, drGrade, gradeName, isReferable, ...
        confScore, rationale, action, resultsDir);
    
    fprintf('    [XAI] Composite Ophthalmologist Report saved: %s\n\n', reportStruct.reportImagePath);
    
    % Populate Summary
    summaryTable{i, 1} = tc.id;
    summaryTable{i, 2} = qualityClass;
    summaryTable{i, 3} = sprintf('Grade %d', drGrade);
    summaryTable{i, 4} = gradeName;
    if isReferable, summaryTable{i, 5} = 'YES (URGENT)'; else, summaryTable{i, 5} = 'NO'; end
    summaryTable{i, 6} = maResults.count;
    summaryTable{i, 7} = hemoResults.totalCount;
    summaryTable{i, 8} = sprintf('%.1f%%', confScore * 100);
end

%% 2. DISPLAY SCREENING SUMMARY TABLE
fprintf('=========================================================================================\n');
fprintf('                             CLINICAL SCREENING BATCH SUMMARY                            \n');
fprintf('=========================================================================================\n');
disp(cell2table(summaryTable, 'VariableNames', ...
    {'Patient_ID', 'Image_Quality', 'Assigned_Grade', 'Grade_Description', 'Referable_DR', 'MAs', 'Hemorrhages', 'Confidence'}));

%% 3. EXECUTE SIMULINK TELEMEDICINE WORKFLOW SIMULATION (100,000 PATIENTS)
fprintf('\n=====================================================================\n');
fprintf('  RUNNING SIMULINK WORKFLOW SIMULATION: 100,000 PATIENTS ANNUALLY     \n');
fprintf('=====================================================================\n');

simResults = simulate_telemedicine_workflow(250, 100000, 25, 2);

fprintf('=====================================================================\n');
fprintf('  PIPELINE EXECUTION COMPLETE! All results written to /results/       \n');
fprintf('=====================================================================\n');
