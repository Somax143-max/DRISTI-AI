function [exudateResults] = detect_exudates(imgRGB, greenEnhanced, fovMask, odMask, foveaCenter, odRadius)
% DETECT_EXUDATES Hard/Soft Exudates Segmentation and CSME Risk Assessment.
%
% Clinical Significance:
%   Hard exudates are bright yellow lipid deposits with distinct margins.
%   When hard exudates approach within 1 disc diameter (500 um) of the foveal
%   center, it indicates Clinically Significant Macular Edema (CSME), which
%   demands immediate laser/anti-VEGF treatment to preserve central vision.
%
% Outputs:
%   exudateResults.hardExudateMask  - Binary mask of hard exudates
%   exudateResults.softExudateMask  - Binary mask of soft exudates (cotton-wool)
%   exudateResults.totalAreaPixels  - Total exudate area
%   exudateResults.retinalAreaPct   - Area as percentage of total retina
%   exudateResults.minDistToFovea   - Distance in disc diameters to fovea
%   exudateResults.csmeRisk         - 'High (Urgent Referral)', 'Moderate', 'None'
%
% MathWorks Toolboxes: Image Processing Toolbox
% Reference: ETDRS & ICDR Guidelines

    [rows, cols, ~] = size(imgRGB);
    
    % Step 1: Optic Disc Exclusion
    % The optic disc is bright yellow-orange and must be masked out with a margin
    % to prevent false exudate detections.
    dilatedOD = imdilate(odMask, strel('disk', round(odRadius * 0.35)));
    validRetina = fovMask & (~dilatedOD);
    
    % Step 2: Hard Exudates Detection
    % Hard exudates exhibit high intensity in both Red and Green channels, and high L*
    redCh = imgRGB(:,:,1);
    greenCh = imgRGB(:,:,2);
    
    % Intensity thresholding in Green channel
    gValid = greenCh(validRetina);
    if isempty(gValid)
        gValid = 0;
    end
    brightThresh = prctile(gValid, 97.5);
    
    % Morphological Top-Hat on Green channel with disk SE to isolate compact bright lesions
    seExudate = strel('disk', 6);
    topHatGreen = imtophat(greenEnhanced, seExudate);
    topHatGreen(~validRetina) = 0;
    
    % Combined criterion: High absolute intensity AND high local contrast
    hardCandidates = (greenCh > brightThresh) & (topHatGreen > 0.04) & validRetina;
    
    % Filter out single noisy isolated pixels (< 4 pixels) and gigantic artifacts
    hardExudates = bwareafilt(hardCandidates, [4, round(rows*cols * 0.015)]);
    
    % Step 3: Soft Exudates (Cotton Wool Spots)
    % Cotton wool spots are larger, feathery, faint gray-white micro-infarcts
    seLarge = strel('disk', 18);
    topHatLarge = imtophat(greenEnhanced, seLarge);
    topHatLarge(~validRetina) = 0;
    softCandidates = (topHatLarge > 0.03) & (~hardExudates) & validRetina;
    softExudates = bwareafilt(softCandidates, [25, round(rows*cols * 0.03)]);
    
    % Step 4: Quantitative Spatial & DME Risk Calculation
    totalExudatePixels = sum(hardExudates(:));
    totalRetinalPixels = sum(fovMask(:));
    areaPct = (totalExudatePixels / max(totalRetinalPixels, 1)) * 100.0;
    
    % Distance to Fovea (in Disc Diameters, DD)
    discDiameter = 2 * odRadius;
    [exY, exX] = find(hardExudates);
    
    if isempty(exX)
        minDistDD = Inf;
        csmeRisk = 'None';
    else
        dists = sqrt((exX - foveaCenter(1)).^2 + (exY - foveaCenter(2)).^2);
        minDistPixels = min(dists);
        minDistDD = minDistPixels / discDiameter;
        
        % ETDRS Definition of CSME:
        % High Risk: Hard exudates within 1 Disc Diameter of Foveal center
        if minDistDD <= 1.0
            csmeRisk = 'High (Urgent DME Referral)';
        elseif minDistDD <= 2.0
            csmeRisk = 'Moderate (Close Monitoring)';
        else
            csmeRisk = 'Low (Peripheral Exudates)';
        end
    end
    
    exudateResults = struct();
    exudateResults.hardExudateMask = hardExudates;
    exudateResults.softExudateMask = softExudates;
    exudateResults.totalAreaPixels = totalExudatePixels;
    exudateResults.retinalAreaPct = areaPct;
    exudateResults.minDistToFovea = minDistDD;
    exudateResults.csmeRisk = csmeRisk;
end
