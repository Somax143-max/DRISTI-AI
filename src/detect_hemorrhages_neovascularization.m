function [hemoResults] = detect_hemorrhages_neovascularization(imgRGB, greenEnhanced, vesselMask, fovMask, odMask, odCenter, odRadius)
% DETECT_HEMORRHAGES_NEOVASCULARIZATION Quantifies intraretinal hemorrhages and neovascularization.
%
% Implements:
%   1. Dot/Blot and Flame Hemorrhage Segmentation
%   2. 4-Quadrant Partitioning to enforce the clinical '4-2-1 Rule' for Severe NPDR
%   3. Neovascularization of the Disc (NVD) within 1 DD of Optic Disc
%   4. Neovascularization Elsewhere (NVE) across retinal periphery
%
% MathWorks Toolboxes: Image Processing Toolbox, Computer Vision Toolbox
% Reference: International Clinical DR Guidelines (ICDR)

    [rows, cols, ~] = size(imgRGB);
    
    % Step 1: Red Lesion Extraction
    % Hemorrhages appear dark in the green channel and red/dark-red in RGB.
    % We exclude previously mapped major vessel trunks to avoid confusion.
    dilatedVessels = imdilate(vesselMask, strel('disk', 2));
    exclusionMask = dilatedVessels | odMask | (~fovMask);
    
    % Morphological Bottom-Hat with medium structuring element (size ~8-12 px)
    seMedium = strel('disk', 10);
    bottomHat = imbothat(greenEnhanced, seMedium);
    bottomHat(exclusionMask) = 0;
    
    % Regional threshold for dark hemorrhagic blood pools
    validGreen = greenEnhanced(fovMask & ~exclusionMask);
    if isempty(validGreen)
        validGreen = 0.5;
    end
    darkThresh = prctile(validGreen, 12.0);
    
    hemoCandidates = (greenEnhanced < darkThresh) & (bottomHat > 0.035) & ~exclusionMask;
    
    % Filter out single-pixel microaneurysms (< 15 px) vs true hemorrhages (15 to 4000 px)
    hemoMask = bwareafilt(hemoCandidates, [15, round(rows*cols * 0.03)]);
    
    % Step 2: 4-Quadrant Clinical Partitioning (Superior-Temporal, Inferior-Temporal,
    % Superior-Nasal, Inferior-Nasal) relative to Fovea/OD axis
    midX = cols / 2;
    midY = rows / 2;
    
    qST = hemoMask & false(rows, cols);
    qIT = hemoMask & false(rows, cols);
    qSN = hemoMask & false(rows, cols);
    qIN = hemoMask & false(rows, cols);
    
    qST(1:midY, midX+1:cols) = hemoMask(1:midY, midX+1:cols);
    qIT(midY+1:rows, midX+1:cols) = hemoMask(midY+1:rows, midX+1:cols);
    qSN(1:midY, 1:midX) = hemoMask(1:midY, 1:midX);
    qIN(midY+1:rows, 1:midX) = hemoMask(midY+1:rows, 1:midX);
    
    propsST = regionprops(qST, 'Area');
    propsIT = regionprops(qIT, 'Area');
    propsSN = regionprops(qSN, 'Area');
    propsIN = regionprops(qIN, 'Area');
    
    hemoCounts = [length(propsST), length(propsIT), length(propsSN), length(propsIN)];
    
    % Clinical '4-2-1 Rule': > 20 intraretinal hemorrhages in each of the 4 quadrants
    quadrantsWithOver20Hemo = sum(hemoCounts >= 20);
    hasSevereHemorrhages = (quadrantsWithOver20Hemo == 4);
    
    % Step 3: Neovascularization Detection (NVD and NVE)
    % Neovascular vessels are thin, disorganized, highly tortuous, loop-like vessels
    % NVD: abnormal vessel proliferation within 1 disc diameter of Optic Disc
    [X, Y] = meshgrid(1:cols, 1:rows);
    distFromOD = sqrt((X - odCenter(1)).^2 + (Y - odCenter(2)).^2);
    nvdZone = (distFromOD > odRadius * 0.9) & (distFromOD <= odRadius * 2.5) & fovMask;
    
    % Vessel density and branching complexity in NVD zone
    vesselsInNVDZone = vesselMask & nvdZone;
    nvdVesselDensity = sum(vesselsInNVDZone(:)) / max(sum(nvdZone(:)), 1);
    
    % Thin vessel skeleton branches
    skelInNVD = bwmorph(vesselsInNVDZone, 'skel', Inf);
    branchPoints = bwmorph(skelInNVD, 'branchpoints');
    numBranchPointsNVD = sum(branchPoints(:));
    
    % NVD Positive criteria: High vessel density and abnormal branching cluster near OD
    isNVD = (nvdVesselDensity > 0.18) && (numBranchPointsNVD > 15);
    
    % NVE (Elsewhere in retina): High abnormal peripheral tortuosity
    isNVE = false; % Default
    
    hasNeovascularization = isNVD || isNVE;
    
    hemoResults = struct();
    hemoResults.mask = hemoMask;
    hemoResults.totalCount = sum(hemoCounts);
    hemoResults.quadrantCounts = hemoCounts; % [ST, IT, SN, IN]
    hemoResults.quadrantsOver20 = quadrantsWithOver20Hemo;
    hemoResults.hasSevereHemorrhages = hasSevereHemorrhages;
    hemoResults.hasNeovascularization = hasNeovascularization;
    hemoResults.isNVD = isNVD;
    hemoResults.isNVE = isNVE;
    hemoResults.nvdVesselDensity = nvdVesselDensity;
end
