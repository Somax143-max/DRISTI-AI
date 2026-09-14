function [structures] = segment_retinal_structures(imgRGB, fovMask, greenEnhanced)
% SEGMENT_RETINAL_STRUCTURES Locates Optic Disc, Fovea, and Segments Retinal Vessels.
%
% Outputs:
%   structures.opticDisc:
%       - mask: Binary mask of optic disc
%       - center: [x, y] coordinates of disc centroid
%       - radius: Estimated disc radius in pixels
%   structures.fovea:
%       - center: [x, y] coordinates of foveal center
%       - fovealAvascularZone: Approximate mask
%   structures.vessels:
%       - mask: Binary mask of segmented retinal vascular tree
%       - skeleton: Morphological vessel skeleton
%       - density: Vascular density ratio
%
% MathWorks Toolboxes: Image Processing Toolbox, Computer Vision Toolbox
% Reference: MathWorks SIH26038 Automated DR Screening

    [rows, cols, ~] = size(imgRGB);
    redChannel = imgRGB(:,:,1);
    
    structures = struct();
    
    % =========================================================================
    % 1. OPTIC DISC (OD) LOCALIZATION & SEGMENTATION
    % =========================================================================
    % Optic disc appears as the brightest region in red & luminance channels.
    % We compute a candidate saliency map combining Red intensity + high regional brightness.
    discSaliency = redChannel .* fovMask;
    
    % Smooth to remove vessel interference inside the disc
    seSmooth = strel('disk', round(min(rows, cols) * 0.02));
    discSaliencySmoothed = imclose(discSaliency, seSmooth);
    
    % Find brightest connected region (top 2% brightest pixels)
    discThreshold = prctile(discSaliencySmoothed(fovMask), 98.0);
    discCandidates = discSaliencySmoothed >= discThreshold;
    discCandidates = bwareafilt(discCandidates, 1); % Largest bright cluster
    
    % Estimate center and radius
    props = regionprops(discCandidates, 'Centroid', 'EquivDiameter');
    if ~isempty(props)
        odCenter = props(1).Centroid; % [x, y]
        odRadius = max(props(1).EquivDiameter / 2, min(rows, cols) * 0.05);
    else
        % Fallback default
        odCenter = [cols * 0.75, rows * 0.5];
        odRadius = min(rows, cols) * 0.07;
    end
    
    % Create Circular Disc Mask
    [X, Y] = meshgrid(1:cols, 1:rows);
    distFromOD = sqrt((X - odCenter(1)).^2 + (Y - odCenter(2)).^2);
    odMask = distFromOD <= odRadius & fovMask;
    
    structures.opticDisc.mask = odMask;
    structures.opticDisc.center = odCenter;
    structures.opticDisc.radius = odRadius;
    
    % =========================================================================
    % 2. FOVEAL CENTER LOCALIZATION
    % =========================================================================
    % Clinical anatomical constraint: The fovea is located approximately 2.5
    % disc diameters temporal to the center of the optic disc, slightly inferior.
    % In fundus imaging, the temporal side is opposite to the nasal side where OD sits.
    % If OD is on the right half, fovea is to the left; if OD is on left, fovea is right.
    if odCenter(1) > cols / 2
        temporalDirection = -1; % OD in right -> Fovea in left
    else
        temporalDirection = 1;  % OD in left -> Fovea in right
    end
    
    foveaExpectedDistance = 2.5 * (2 * odRadius);
    foveaExpectedX = odCenter(1) + temporalDirection * foveaExpectedDistance;
    foveaExpectedY = odCenter(2) + 0.2 * odRadius; % Slightly inferior
    
    % Constrain to valid image bounds
    foveaExpectedX = max(odRadius, min(cols - odRadius, foveaExpectedX));
    foveaExpectedY = max(odRadius, min(rows - odRadius, foveaExpectedY));
    
    % Search in a localized ROI around expected coordinates for darkest Green region
    searchRadius = round(odRadius * 0.8);
    roiMask = ((X - foveaExpectedX).^2 + (Y - foveaExpectedY).^2 <= searchRadius^2) & fovMask;
    
    roiGreen = greenEnhanced;
    roiGreen(~roiMask) = Inf; % Suppress non-ROI
    [~, minIdx] = min(roiGreen(:));
    [foveaY, foveaX] = ind2sub([rows, cols], minIdx);
    
    structures.fovea.center = [foveaX, foveaY];
    structures.fovea.distToOD = sqrt((foveaX - odCenter(1))^2 + (foveaY - odCenter(2))^2);
    structures.fovea.avascularRadius = odRadius * 0.5;
    
    % =========================================================================
    % 3. RETINAL VESSEL SEGMENTATION (Matched Filtering / Top-Hat Morphometry)
    % =========================================================================
    % Retinal blood vessels appear darker than background in the green channel.
    % We compute inverted green channel and use multi-directional top-hat filtering.
    invGreen = 1.0 - greenEnhanced;
    invGreen(~fovMask) = 0;
    
    % Morphological Top-Hat using rotating linear structuring elements (12 angles)
    angles = 0:15:165;
    lineLength = round(min(rows, cols) * 0.02);
    vesselEnhanced = zeros(rows, cols);
    
    for ang = angles
        seLine = strel('line', max(lineLength, 5), ang);
        topHatAng = imtophat(invGreen, seLine);
        vesselEnhanced = max(vesselEnhanced, topHatAng);
    end
    
    % Adaptive local thresholding to obtain binary vessel tree
    localMean = imfilter(vesselEnhanced, fspecial('average', 15), 'replicate');
    vesselCandidates = (vesselEnhanced - localMean) > 0.015 & fovMask;
    
    % Clean up small spurious noise (retaining connected structures > 30 px)
    vesselMask = bwareaopen(vesselCandidates, 30);
    
    % Mask out the Optic Disc border to avoid circular border false vessels
    vesselMask(distFromOD <= odRadius * 0.9) = false;
    
    structures.vessels.mask = vesselMask;
    structures.vessels.skeleton = bwmorph(vesselMask, 'thin', Inf);
    structures.vessels.density = sum(vesselMask(:)) / max(sum(fovMask(:)), 1);
end
