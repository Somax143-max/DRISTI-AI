function [fundusRGB] = generate_synthetic_fundus(targetGrade, imgSize, isDegraded)
% GENERATE_SYNTHETIC_FUNDUS Generates biologically realistic synthetic retinal fundus.
%
% Syntax:
%   fundusRGB = generate_synthetic_fundus(targetGrade, imgSize, isDegraded)
%
% Inputs:
%   targetGrade - ICDR DR grade (0 = Normal, 1 = Mild, 2 = Mod, 3 = Severe, 4 = PDR)
%   imgSize     - Scalar or 2-element vector [rows, cols] (default: 512)
%   isDegraded  - Boolean, simulates poor field focus/glare if true (default: false)
%
% MathWorks Toolboxes: Image Processing Toolbox
% Reference: MathWorks SIH26038 Benchmark & Validation Engine

    if nargin < 2 || isempty(imgSize), imgSize = 512; end
    if nargin < 3 || isempty(isDegraded), isDegraded = false; end
    
    if isscalar(imgSize), rows = imgSize; cols = imgSize; else, rows = imgSize(1); cols = imgSize(2); end
    
    % Step 1: Retinal Field of View (FoV) circular aperture
    [X, Y] = meshgrid(1:cols, 1:rows);
    centerX = cols / 2;
    centerY = rows / 2;
    radius = min(rows, cols) * 0.46;
    fovMask = ((X - centerX).^2 + (Y - centerY).^2) <= radius^2;
    
    % Step 2: Retinal Background (Orange-Red with natural radial shading)
    distFromCenter = sqrt((X - centerX).^2 + (Y - centerY).^2) / radius;
    retinalBase = 0.82 - 0.28 * distFromCenter;
    
    redCh = retinalBase * 0.95;
    greenCh = retinalBase * 0.48;
    blueCh = retinalBase * 0.12;
    
    % Add choroidal texture noise
    noiseTex = imgaussfilt(randn(rows, cols) * 0.03, 3);
    redCh = redCh + noiseTex * 0.5;
    greenCh = greenCh + noiseTex * 0.3;
    
    % Step 3: Optic Disc (OD) on Nasal Side (e.g. right side for Right Eye)
    odCenter = [round(cols * 0.76), round(rows * 0.50)];
    odRadius = round(min(rows, cols) * 0.08);
    distOD = sqrt((X - odCenter(1)).^2 + (Y - odCenter(2)).^2);
    odMask = distOD <= odRadius;
    
    % OD is yellowish-orange
    redCh(odMask) = 0.98;
    greenCh(odMask) = 0.85;
    blueCh(odMask) = 0.45;
    
    % Step 4: Fovea & Macular Avascular Zone (Darker red-brown)
    foveaCenter = [round(cols * 0.38), round(rows * 0.51)];
    distFov = sqrt((X - foveaCenter(1)).^2 + (Y - foveaCenter(2)).^2);
    foveaDimming = exp(-distFov.^2 / (2 * (odRadius * 0.9)^2));
    greenCh = greenCh .* (1.0 - 0.35 * foveaDimming);
    blueCh = blueCh .* (1.0 - 0.45 * foveaDimming);
    
    % Step 5: Vascular Tree (Superior & Inferior Temporal Arcades)
    vesselTree = false(rows, cols);
    t = linspace(0, 1, 200);
    
    % Superior arcade arc
    arcSupX = round(odCenter(1) - (odCenter(1) - foveaCenter(1)) * t - 30 * sin(pi*t));
    arcSupY = round(odCenter(2) - (rows * 0.28) * sin(pi*t));
    
    % Inferior arcade arc
    arcInfX = round(odCenter(1) - (odCenter(1) - foveaCenter(1)) * t - 30 * sin(pi*t));
    arcInfY = round(odCenter(2) + (rows * 0.28) * sin(pi*t));
    
    for i = 1:length(t)
        if arcSupX(i) >= 1 && arcSupX(i) <= cols && arcSupY(i) >= 1 && arcSupY(i) <= rows
            vesselTree(arcSupY(i), arcSupX(i)) = true;
        end
        if arcInfX(i) >= 1 && arcInfX(i) <= cols && arcInfY(i) >= 1 && arcInfY(i) <= rows
            vesselTree(arcInfY(i), arcInfX(i)) = true;
        end
    end
    
    vesselTree = imdilate(vesselTree, strel('disk', 3));
    vesselTree = vesselTree & fovMask;
    
    % Darken vessels in green and blue
    greenCh(vesselTree) = greenCh(vesselTree) * 0.35;
    blueCh(vesselTree) = blueCh(vesselTree) * 0.20;
    redCh(vesselTree) = redCh(vesselTree) * 0.75;
    
    % Step 6: Inject Pathological Lesions Based on targetGrade
    rng(42 + targetGrade); % Reproducible
    
    % Grade 1: Microaneurysms only (MAs: 6-12)
    % Grade 2: MAs + Hard Exudates + some hemorrhages
    % Grade 3: Severe Hemorrhages across all 4 quadrants (>80) + MAs
    % Grade 4: Neovascularization + severe hemorrhages
    
    numMAs = 0; numHemo = 0; numExudates = 0; hasNV = false;
    
    switch targetGrade
        case 0
            % Normal - no lesions
        case 1
            numMAs = 8;
        case 2
            numMAs = 18;
            numHemo = 15;
            numExudates = 25;
        case 3
            numMAs = 35;
            numHemo = 85;
            numExudates = 40;
        case 4
            numMAs = 40;
            numHemo = 90;
            numExudates = 50;
            hasNV = true;
    end
    
    % Plant Microaneurysms (tiny dark red/black spots, 2-3 px)
    for k = 1:numMAs
        rx = round(cols * (0.2 + 0.6 * rand()));
        ry = round(rows * (0.2 + 0.6 * rand()));
        if fovMask(ry, rx) && ~odMask(ry, rx)
            maMask = ((X - rx).^2 + (Y - ry).^2) <= 2.5^2;
            greenCh(maMask) = greenCh(maMask) * 0.2;
            blueCh(maMask) = blueCh(maMask) * 0.1;
            redCh(maMask) = redCh(maMask) * 0.5;
        end
    end
    
    % Plant Hemorrhages (dark blotches, 5-10 px)
    for k = 1:numHemo
        rx = round(cols * (0.15 + 0.7 * rand()));
        ry = round(rows * (0.15 + 0.7 * rand()));
        if fovMask(ry, rx) && ~odMask(ry, rx)
            hRad = 3 + 4 * rand();
            hMask = ((X - rx).^2 + (Y - ry).^2) <= hRad^2;
            greenCh(hMask) = greenCh(hMask) * 0.25;
            blueCh(hMask) = blueCh(hMask) * 0.15;
            redCh(hMask) = redCh(hMask) * 0.6;
        end
    end
    
    % Plant Hard Exudates (bright yellowish-white clusters)
    for k = 1:numExudates
        rx = round(foveaCenter(1) + (rand() - 0.5) * odRadius * 3.5);
        ry = round(foveaCenter(2) + (rand() - 0.5) * odRadius * 3.5);
        if rx >= 1 && rx <= cols && ry >= 1 && ry <= rows && fovMask(ry, rx) && ~odMask(ry, rx)
            eRad = 2 + 3 * rand();
            eMask = ((X - rx).^2 + (Y - ry).^2) <= eRad^2;
            redCh(eMask) = 0.98;
            greenCh(eMask) = 0.95;
            blueCh(eMask) = 0.40;
        end
    end
    
    % Grade 4: Neovascularization (NVD) - tortuous network around OD
    if hasNV
        for ang = linspace(0, 2*pi, 25)
            nvX = round(odCenter(1) + (odRadius * 1.3 + 12 * rand()) * cos(ang));
            nvY = round(odCenter(2) + (odRadius * 1.3 + 12 * rand()) * sin(ang));
            if nvX >= 1 && nvX <= cols && nvY >= 1 && nvY <= rows
                greenCh(max(1, nvY-1):min(rows, nvY+1), max(1, nvX-1):min(cols, nvX+1)) = 0.1;
                redCh(max(1, nvY-1):min(rows, nvY+1), max(1, nvX-1):min(cols, nvX+1)) = 0.4;
            end
        end
    end
    
    % Step 7: Assemble RGB and apply FoV mask
    fundusRGB = cat(3, redCh, greenCh, blueCh);
    for c = 1:3
        channel = fundusRGB(:,:,c);
        channel(~fovMask) = 0;
        fundusRGB(:,:,c) = channel;
    end
    fundusRGB = max(0, min(1, fundusRGB));
    
    % Optional field degradation (for testing Image Quality Assessment reject)
    if isDegraded
        % Severe blur
        fundusRGB = imgaussfilt(fundusRGB, 9.0);
        % Corneal glare ring
        glareMask = ((X - centerX*0.85).^2 + (Y - centerY*0.9).^2) <= (radius * 0.25)^2;
        for c = 1:3
            ch = fundusRGB(:,:,c);
            ch(glareMask) = 0.98;
            fundusRGB(:,:,c) = ch;
        end
    end
end
