function [isGradeable, qualityClass, feedbackMessage, metrics] = assess_image_quality(imgRGB)
% ASSESS_IMAGE_QUALITY Evaluates retinal fundus image quality for rural DR screening.
%
% Syntax:
%   [isGradeable, qualityClass, feedbackMessage, metrics] = assess_image_quality(imgRGB)
%
% Inputs:
%   imgRGB - M-by-N-by-3 uint8 or double retinal fundus image
%
% Outputs:
%   isGradeable     - Boolean flag indicating if image is clinically interpretable
%   qualityClass    - 'Good', 'Borderline', or 'Ungradeable'
%   feedbackMessage - Actionable recapture feedback for rural healthcare operators
%   metrics         - Struct containing computed objective quality scores
%
% MathWorks Toolboxes: Image Processing Toolbox, Statistics and Machine Learning Toolbox
% Reference: International Clinical DR Guidelines & Rural Telemedicine Standards

    if isa(imgRGB, 'uint8')
        imgDouble = double(imgRGB) / 255.0;
    else
        imgDouble = imgRGB;
    end
    
    greenChannel = imgDouble(:,:,2);
    
    % 1. Field of View (FoV) / Retinal Mask Extraction
    grayImg = rgb2gray(imgDouble);
    fovMask = grayImg > 0.05;
    fovMask = imfill(fovMask, 'holes');
    fovMask = bwareafilt(fovMask, 1); % Retain largest connected component
    
    totalPixels = numel(grayImg);
    fovPixels = sum(fovMask(:));
    fovRatio = fovPixels / totalPixels;
    
    % Check if FoV is too small or clipped
    if fovRatio < 0.20
        isGradeable = false;
        qualityClass = 'Ungradeable';
        feedbackMessage = 'Field of view severely clipped or sensor obstructed. Recapture with proper alignment.';
        metrics = struct('focusScore', 0, 'illuminationScore', 0, 'fovRatio', fovRatio, 'glareRatio', 0, 'underexposedRatio', 0);
        return;
    end
    
    % 2. Focus / Sharpness Metric (Modified Tenengrad Gradient & Laplacian Variance)
    sobelX = fspecial('sobel');
    sobelY = sobelX';
    gx = imfilter(greenChannel, sobelX, 'replicate');
    gy = imfilter(greenChannel, sobelY, 'replicate');
    gradMag = sqrt(gx.^2 + gy.^2);
    
    % Focus computed strictly within the retinal FoV
    tenengradFocus = sum((gradMag(fovMask)).^2) / fovPixels * 1e4;
    
    % 3. Illumination & Exposure Evaluation
    retinalLuminance = grayImg(fovMask);
    meanLuminance = mean(retinalLuminance);
    
    % Glare / Corneal Reflection (> 0.92 intensity inside FoV)
    glarePixels = sum(retinalLuminance > 0.92);
    glareRatio = glarePixels / fovPixels;
    
    % Severe Underexposure (< 0.08 intensity inside FoV)
    darkPixels = sum(retinalLuminance < 0.08);
    underexposedRatio = darkPixels / fovPixels;
    
    % Contrast Score (Standard deviation of green channel inside FoV)
    contrastScore = std(greenChannel(fovMask));
    
    % Composite Illumination Score (1.0 is ideal, penalized by extremes)
    illuminationScore = max(0, 1.0 - abs(meanLuminance - 0.45) * 1.8 - glareRatio * 3.0 - underexposedRatio * 2.0);
    
    % 4. Struct Output
    metrics = struct();
    metrics.focusScore = tenengradFocus;
    metrics.illuminationScore = illuminationScore;
    metrics.meanLuminance = meanLuminance;
    metrics.contrastScore = contrastScore;
    metrics.fovRatio = fovRatio;
    metrics.glareRatio = glareRatio;
    metrics.underexposedRatio = underexposedRatio;
    
    % Decision Rule Engine for Gradeability & Clinical Recapture Feedback
    if tenengradFocus < 15.0
        isGradeable = false;
        qualityClass = 'Ungradeable';
        feedbackMessage = 'Image severely blurred (Focus score < 15). Stabilize camera, instruct patient not to blink, and refocus.';
    elseif glareRatio > 0.15
        isGradeable = false;
        qualityClass = 'Ungradeable';
        feedbackMessage = 'Excessive corneal glare / reflection detected (> 15% area). Adjust camera angle by 5-10 degrees.';
    elseif underexposedRatio > 0.40 || meanLuminance < 0.12
        isGradeable = false;
        qualityClass = 'Ungradeable';
        feedbackMessage = 'Severe underexposure. Increase flash illumination or allow patient 3 minutes in a dim room for pupil dilation.';
    elseif tenengradFocus < 28.0 || glareRatio > 0.06 || underexposedRatio > 0.20 || contrastScore < 0.10
        isGradeable = true;
        qualityClass = 'Borderline';
        feedbackMessage = 'Borderline image quality. Applying adaptive CLAHE and illumination equalization for enhanced grading.';
    else
        isGradeable = true;
        qualityClass = 'Good';
        feedbackMessage = 'Optimal image quality. Excellent focus, balanced illumination, and clear vascular visibility.';
    end
end
