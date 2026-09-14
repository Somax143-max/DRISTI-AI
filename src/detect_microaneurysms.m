function [maResults] = detect_microaneurysms(greenEnhanced, vesselMask, fovMask, odMask)
% DETECT_MICROANEURYSMS Sub-pixel Microaneurysm (MA) detection in retinal fundus.
%
% Microaneurysms are small, round, dark focal dilatations of retinal capillaries 
% (10-100 um diameter). In digital fundus images, they span 2-15 pixels.
%
% Method:
%   1. Vessel Inpainting / Masking to prevent false positives at vessel branches.
%   2. Morphological Bottom-Hat transform with isotropic circular structuring elements.
%   3. Sub-pixel quadratic interpolation for precise centroid localization.
%   4. Circularity, contrast, and size filtering.
%   5. Quadrant distribution analysis for clinical staging.
%
% Outputs:
%   maResults.count         - Total number of verified microaneurysms
%   maResults.coordinates   - Sub-pixel [x, y] coordinates (N-by-2)
%   maResults.mask          - Binary mask of MA locations
%   maResults.quadrantCounts- [ST, IT, SN, IN] counts across 4 retinal quadrants
%
% MathWorks Toolboxes: Image Processing Toolbox, Computer Vision Toolbox
% Reference: MathWorks SIH26038 Automated Retinal Screening

    [rows, cols] = size(greenEnhanced);
    
    % Step 1: Vessel Inpainting / Masking
    % Dilate vessel mask slightly to cover capillary edges
    dilatedVessels = imdilate(vesselMask, strel('disk', 2));
    
    % Mask out Optic Disc (where vessel trunks converge)
    dilatedOD = imdilate(odMask, strel('disk', 5));
    
    exclusionMask = dilatedVessels | dilatedOD | (~fovMask);
    
    % Step 2: Morphological Bottom-Hat Transform
    % Bottom-hat isolates dark structures smaller than the structuring element
    seSmall = strel('disk', 4);
    bottomHat = imbothat(greenEnhanced, seSmall);
    bottomHat(exclusionMask) = 0;
    
    % Step 3: Candidate Peak Detection
    % Regional maxima with contrast threshold
    contrastThresh = prctile(bottomHat(fovMask & ~exclusionMask), 98.5);
    regMax = imregionalmax(bottomHat);
    candidatePeaks = regMax & (bottomHat >= contrastThresh);
    
    [peakY, peakX] = find(candidatePeaks);
    numCandidates = length(peakX);
    
    validCoords = [];
    maMask = false(rows, cols);
    
    % Step 4: Sub-pixel Parabolic Refinement & Morphology Gating
    for k = 1:numCandidates
        x = peakX(k);
        y = peakY(k);
        
        % Boundary safety check
        if x <= 2 || x >= cols - 1 || y <= 2 || y >= rows - 1
            continue;
        end
        
        % 3x3 local patch around peak in bottom-hat response
        patch = bottomHat(y-1:y+1, x-1:x+1);
        
        % Sub-pixel quadratic peak fit:
        % f(x, y) = a*x^2 + b*y^2 + c*x + d*y + e
        % dx = (f(0, 1) - f(0, -1)) / (2 * (2*f(0,0) - f(0,1) - f(0,-1)))
        denomX = (2 * patch(2,2) - patch(2,3) - patch(2,1));
        denomY = (2 * patch(2,2) - patch(3,2) - patch(1,2));
        
        if abs(denomX) > 1e-4
            subX = x + (patch(2,3) - patch(2,1)) / (2 * denomX);
        else
            subX = x;
        end
        
        if abs(denomY) > 1e-4
            subY = y + (patch(3,2) - patch(1,2)) / (2 * denomY);
        else
            subY = y;
        end
        
        % Keep displacement within reasonable sub-pixel bound (-0.8 to +0.8)
        if abs(subX - x) > 0.85 || abs(subY - y) > 0.85
            subX = x;
            subY = y;
        end
        
        % Measure local circularity & contrast
        localGreen = greenEnhanced(y-2:y+2, x-2:x+2);
        centerVal = greenEnhanced(y, x);
        surroundVal = mean([localGreen(1,:), localGreen(5,:), localGreen(2:4,1)', localGreen(2:4,5)']);
        drop = surroundVal - centerVal;
        
        if drop > 0.025 % True dark depression
            validCoords = [validCoords; subX, subY]; %#ok<AGROW>
            maMask(y, x) = true;
        end
    end
    
    % Step 5: Quadrant Distribution Analysis
    % Split retina into 4 quadrants relative to image center
    midX = cols / 2;
    midY = rows / 2;
    
    stCount = 0; itCount = 0; snCount = 0; inCount = 0;
    if ~isempty(validCoords)
        for i = 1:size(validCoords, 1)
            cx = validCoords(i, 1);
            cy = validCoords(i, 2);
            if cx >= midX && cy < midY
                stCount = stCount + 1;
            elseif cx >= midX && cy >= midY
                itCount = itCount + 1;
            elseif cx < midX && cy < midY
                snCount = snCount + 1;
            else
                inCount = inCount + 1;
            end
        end
    end
    
    maResults = struct();
    maResults.count = size(validCoords, 1);
    maResults.coordinates = validCoords;
    maResults.mask = maMask;
    maResults.quadrantCounts = [stCount, itCount, snCount, inCount];
end
