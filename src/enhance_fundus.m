function [enhancedRGB, fovMask, greenEnhanced] = enhance_fundus(imgRGB)
% ENHANCE_FUNDUS Adaptive enhancement for retinal fundus images in rural field conditions.
%
% Implements:
%   1. Automatic circular Retinal FoV mask extraction
%   2. Large-kernel morphological background illumination normalization
%   3. CLAHE on L* channel in CIE L*a*b* space (preserves retinal chromaticity)
%   4. Edge-preserving bilateral / guided filtering for noise reduction
%   5. High-contrast Green channel extraction for lesion & vessel detection
%
% MathWorks Toolboxes: Image Processing Toolbox
% Reference: MathWorks SIH26038 DR Pipeline

    if isa(imgRGB, 'uint8')
        imgDouble = double(imgRGB) / 255.0;
    else
        imgDouble = imgRGB;
    end
    
    % Step 1: FoV Mask extraction
    grayImg = rgb2gray(imgDouble);
    fovMask = grayImg > 0.05;
    fovMask = imfill(fovMask, 'holes');
    fovMask = bwareafilt(fovMask, 1);
    
    % Step 2: CIE L*a*b* Color Space Conversion
    % Enhancing only Luminance (L*) avoids introducing artificial color shifts
    % which could cause false lesion classifications.
    cform = makecform('srgb2lab');
    labImg = applycform(imgDouble, cform);
    L = labImg(:,:,1) / 100.0; % Normalize 0 to 1
    
    % Step 3: Background Illumination Field Estimation & Flattening
    % Approximate background using morphological closing with large disk SE
    seRadius = round(min(size(grayImg)) * 0.06); % Adaptive disk radius ~6% of image size
    se = strel('disk', max(seRadius, 15));
    bgLuminance = imclose(L, se);
    
    % Normalize illumination within FoV
    meanBg = mean(bgLuminance(fovMask));
    normalizedL = (L ./ (bgLuminance + 1e-4)) * meanBg;
    normalizedL = max(0, min(1, normalizedL));
    
    % Step 4: CLAHE (Contrast-Limited Adaptive Histogram Equalization)
    % ClipLimit ~0.02 prevents noise amplification while uncovering faint microaneurysms
    claheL = adapthisteq(normalizedL, 'ClipLimit', 0.02, 'Distribution', 'rayleigh', 'NumTiles', [8 8]);
    
    % Blend CLAHE with normalized L for natural appearance
    L_enhanced = 0.75 * claheL + 0.25 * normalizedL;
    
    % Step 5: Edge-Preserving Denoising on Luminance
    % Bilateral filter suppresses CMOS sensor noise while keeping retinal micro-vessels sharp
    try
        L_denoised = imbilatfilt(L_enhanced, 0.01, 2.0);
    catch
        % Fallback for older MATLAB versions
        L_denoised = medfilt2(L_enhanced, [3 3]);
    end
    
    % Step 6: Reconstruct RGB Image
    labImg(:,:,1) = L_denoised * 100.0;
    cformBack = makecform('lab2srgb');
    enhancedRGB = applycform(labImg, cformBack);
    enhancedRGB = max(0, min(1, enhancedRGB));
    
    % Mask out non-retinal background to pure black
    for c = 1:3
        ch = enhancedRGB(:,:,c);
        ch(~fovMask) = 0;
        enhancedRGB(:,:,c) = ch;
    end
    
    % Step 7: Green Channel Extraction & Linear Contrast Stretch
    greenChannel = enhancedRGB(:,:,2);
    gRetina = greenChannel(fovMask);
    lowP = prctile(gRetina, 1);
    highP = prctile(gRetina, 99);
    greenEnhanced = (greenChannel - lowP) / (highP - lowP + 1e-6);
    greenEnhanced = max(0, min(1, greenEnhanced));
    greenEnhanced(~fovMask) = 0;
end
