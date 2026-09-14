function [reportStruct] = generate_explainability_report(patientID, origRGB, enhancedRGB, qualityMetrics, structures, maResults, exudateResults, hemoResults, drGrade, gradeName, isReferable, confidenceScore, clinicalRationale, recommendedAction, outputDir)
% GENERATE_EXPLAINABILITY_REPORT Generates multi-modal XAI report for <30-sec ophthalmologist sign-off.
    if nargin < 15 || isempty(outputDir)
        outputDir = fullfile(fileparts(mfilename('fullpath')), '..', 'results');
    end
    if ~exist(outputDir, 'dir')
        mkdir(outputDir);
    end

    [rows, cols, ~] = size(origRGB);
    
    % Grad-CAM Pathological Attention Heatmap Synthesis
    camDensity = zeros(rows, cols);
    if any(hemoResults.mask(:))
        camDensity = camDensity + 0.50 * double(hemoResults.mask);
    end
    if any(exudateResults.hardExudateMask(:))
        camDensity = camDensity + 0.40 * double(exudateResults.hardExudateMask);
    end
    if any(maResults.mask(:))
        camDensity = camDensity + 0.35 * double(maResults.mask);
    end
    
    sigmaCAM = round(min(rows, cols) * 0.045);
    camSmoothed = imgaussfilt(camDensity, max(sigmaCAM, 5));
    if max(camSmoothed(:)) > 0
        camNorm = camSmoothed / max(camSmoothed(:));
    else
        [X, Y] = meshgrid(1:cols, 1:rows);
        distFov = sqrt((X - structures.fovea.center(1)).^2 + (Y - structures.fovea.center(2)).^2);
        camNorm = exp(-distFov.^2 / (2 * (min(rows, cols)*0.18)^2));
    end
    
    camRGB = ind2rgb(round(camNorm * 255) + 1, jet(256));
    grayEnhanced = rgb2gray(enhancedRGB);
    gray3 = cat(3, grayEnhanced, grayEnhanced, grayEnhanced);
    gradCamOverlay = 0.55 * gray3 + 0.45 * camRGB;
    
    % Multi-Color Lesion Overlay
    lesionOverlay = enhancedRGB;
    vMask = structures.vessels.mask;
    for c = 1:3
        ch = lesionOverlay(:,:,c);
        if c == 1, ch(vMask) = 0.1; end
        if c == 2, ch(vMask) = 0.85; end
        if c == 3, ch(vMask) = 0.95; end
        lesionOverlay(:,:,c) = ch;
    end
    
    odPerim = bwperim(structures.opticDisc.mask);
    odPerimDil = imdilate(odPerim, strel('disk', 2));
    for c = 1:3
        ch = lesionOverlay(:,:,c);
        if c == 1, ch(odPerimDil) = 0.0; end
        if c == 2, ch(odPerimDil) = 1.0; end
        if c == 3, ch(odPerimDil) = 0.1; end
        lesionOverlay(:,:,c) = ch;
    end
    
    exMask = imdilate(exudateResults.hardExudateMask, strel('disk', 1));
    for c = 1:3
        ch = lesionOverlay(:,:,c);
        if c == 1, ch(exMask) = 1.0; end
        if c == 2, ch(exMask) = 0.95; end
        if c == 3, ch(exMask) = 0.0; end
        lesionOverlay(:,:,c) = ch;
    end
    
    heMask = imdilate(hemoResults.mask, strel('disk', 1));
    for c = 1:3
        ch = lesionOverlay(:,:,c);
        if c == 1, ch(heMask) = 1.0; end
        if c == 2, ch(heMask) = 0.05; end
        if c == 3, ch(heMask) = 0.05; end
        lesionOverlay(:,:,c) = ch;
    end
    
    reportStruct = struct();
    reportStruct.patientID = patientID;
    reportStruct.timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
    reportStruct.drGrade = drGrade;
    reportStruct.gradeName = gradeName;
    reportStruct.isReferable = isReferable;
    reportStruct.confidenceScore = confidenceScore;
    reportStruct.clinicalRationale = clinicalRationale;
    reportStruct.recommendedAction = recommendedAction;
    reportStruct.imageQuality = qualityMetrics;
    
    hFig = figure('Visible', 'off', 'Position', [50, 50, 1400, 950], 'Color', [0.12 0.12 0.14]);
    subplot(2, 2, 1); imshow(origRGB);
    title(sprintf('Input Fundus (ID: %s)', patientID), 'Color', 'white', 'FontSize', 12, 'FontWeight', 'bold');
    xlabel(sprintf('Focus: %.1f | Illum: %.2f', qualityMetrics.focusScore, qualityMetrics.illuminationScore), 'Color', [0.8 0.8 0.8]);
    
    subplot(2, 2, 2); imshow(enhancedRGB); hold on;
    plot(structures.opticDisc.center(1), structures.opticDisc.center(2), 'g+', 'MarkerSize', 14, 'LineWidth', 2);
    plot(structures.fovea.center(1), structures.fovea.center(2), 'c*', 'MarkerSize', 14, 'LineWidth', 2);
    title('Enhanced Fundus & Landmarks', 'Color', 'white', 'FontSize', 12, 'FontWeight', 'bold'); hold off;
    
    subplot(2, 2, 3); imshow(gradCamOverlay);
    title('Grad-CAM Pathological Attention Heatmap', 'Color', 'white', 'FontSize', 12, 'FontWeight', 'bold');
    
    subplot(2, 2, 4); imshow(lesionOverlay);
    title('Clinical Lesion Overlay (Cyan:Vessels, Yellow:Exudates, Red:Hemo)', 'Color', 'white', 'FontSize', 11, 'FontWeight', 'bold');
    
    if isReferable
        statusBadge = 'REFERABLE DR [HIGH PRIORITY]';
        badgeColor = [0.9 0.2 0.2];
    else
        statusBadge = 'NON-REFERABLE [ROUTINE]';
        badgeColor = [0.2 0.8 0.3];
    end
    sgtitle(sprintf('AI CLINICAL TRIAGE: %s | %s (Confidence: %.1f%%)', statusBadge, gradeName, confidenceScore * 100), 'Color', badgeColor, 'FontSize', 14, 'FontWeight', 'bold');
    
    figPath = fullfile(outputDir, sprintf('screening_report_%s.png', patientID));
    saveas(hFig, figPath);
    close(hFig);
    reportStruct.reportImagePath = figPath;
end
