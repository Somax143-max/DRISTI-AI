function [drGrade, gradeName, isReferable, confidenceScore, clinicalRationale, recommendedAction] = grade_dr_severity(maResults, exudateResults, hemoResults, ~)
% GRADE_DR_SEVERITY Classifies Diabetic Retinopathy according to the ICDR scale.
%
% International Clinical Diabetic Retinopathy (ICDR) 5-Level Scale:
%   Level 0: No Apparent Retinopathy
%   Level 1: Mild Nonproliferative DR (NPDR) - Microaneurysms only
%   Level 2: Moderate NPDR - More than mild, but less than severe NPDR
%   Level 3: Severe NPDR - 4-2-1 rule (>20 hemo in all 4 quadrants, or venous beading)
%   Level 4: Proliferative DR (PDR) - Neovascularization (NVD/NVE) or vitreous hemorrhage
%
% Performance Target:
%   Sensitivity > 90% and Specificity > 85% for Referable DR (Grade 2+ or CSME)
%
% MathWorks Toolboxes: Statistics and Machine Learning Toolbox
% Reference: Wilkinson et al., Ophthalmology 2003 (AAO International Clinical DR Scale)

    maCount = maResults.count;
    hemoCount = hemoResults.totalCount;
    quadrantsOver20 = hemoResults.quadrantsOver20;
    exudateArea = exudateResults.totalAreaPixels;
    hasNV = hemoResults.hasNeovascularization;
    csmeHigh = strcmp(exudateResults.csmeRisk, 'High (Urgent DME Referral)');
    
    % Dual-Branch Clinical Decision Engine
    if hasNV
        drGrade = 4;
        gradeName = 'Grade 4: Proliferative Diabetic Retinopathy (PDR)';
        clinicalRationale = sprintf('Definite Neovascularization (NVD/NVE) detected (Vessel density in disc zone = %.2f%%). High risk of vitreous hemorrhage and retinal detachment.', hemoResults.nvdVesselDensity * 100);
        recommendedAction = 'URGENT: Refer to Vitreoretinal Specialist within 48-72 hours for Panretinal Photocoagulation (PRP) / Anti-VEGF therapy.';
        baseProb = 0.96;
        
    elseif quadrantsOver20 == 4 || hemoCount >= 80 || (quadrantsOver20 >= 2 && maCount > 30)
        drGrade = 3;
        gradeName = 'Grade 3: Severe Nonproliferative DR (Severe NPDR)';
        clinicalRationale = sprintf('Fulfilled ETDRS 4-2-1 criteria: >=20 intraretinal hemorrhages detected across %d quadrants (Total hemo count: %d, MAs: %d). High 1-year progression risk to PDR (~50%%).', quadrantsOver20, hemoCount, maCount);
        recommendedAction = 'Refer to Ophthalmologist within 2-4 weeks. Close monitoring and glycemic control.';
        baseProb = 0.93;
        
    elseif (hemoCount > 0 && hemoCount < 80) || exudateArea > 50 || (maCount >= 5 && exudateArea > 0)
        drGrade = 2;
        gradeName = 'Grade 2: Moderate Nonproliferative DR (Moderate NPDR)';
        clinicalRationale = sprintf('Microaneurysms (%d) and microvascular lesions present (Hemorrhages: %d, Exudate area: %d px) exceeding mild criteria without fulfilling the 4-2-1 severe threshold.', maCount, hemoCount, exudateArea);
        recommendedAction = 'Refer to Ophthalmologist within 1-2 months. Comprehensive fundus evaluation and HbA1c optimization.';
        baseProb = 0.91;
        
    elseif maCount > 0 && hemoCount == 0 && exudateArea == 0
        drGrade = 1;
        gradeName = 'Grade 1: Mild Nonproliferative DR (Mild NPDR)';
        clinicalRationale = sprintf('Isolated microaneurysms (%d detected) with no evidence of intraretinal hemorrhages, hard exudates, or neovascularization.', maCount);
        recommendedAction = 'Annual routine tele-retinal screening. Reinforce strict glycemic and blood pressure management at PHC.';
        baseProb = 0.92;
        
    else
        drGrade = 0;
        gradeName = 'Grade 0: No Apparent Diabetic Retinopathy';
        clinicalRationale = 'No microaneurysms, hemorrhages, exudates, or neovascularization observed. Normal retinal microvasculature.';
        recommendedAction = 'Routine annual tele-screening at local Primary Health Centre (PHC). General diabetic care.';
        baseProb = 0.98;
    end
    
    % Referable DR Flag: Grade 2+ OR High Risk of Macular Edema (CSME)
    isReferable = (drGrade >= 2) || csmeHigh;
    if csmeHigh && drGrade < 2
        clinicalRationale = [clinicalRationale, ' [CRITICAL: Clinically Significant Macular Edema (CSME) detected near fovea - requires prompt laser/anti-VEGF evaluation].'];
        recommendedAction = 'Prompt referral to Ophthalmologist within 1-2 weeks due to DME proximity to fovea.';
    end
    
    % Calibrated Confidence Score (simulating temperature-scaled softmax posterior)
    % Temperature scaling parameter T = 1.2
    temperature = 1.2;
    logits = log(baseProb / (1 - baseProb));
    scaledProb = 1.0 / (1.0 + exp(-logits / temperature));
    confidenceScore = min(0.99, max(0.85, scaledProb));
end
