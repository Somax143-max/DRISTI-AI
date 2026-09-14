function [modelName] = build_simulink_model()
% BUILD_SIMULINK_MODEL Programmatically builds the Telemedicine Screening Simulink model.
%
% Generates: telemed_dr_screening.slx
%
% Blocks:
%   - Patient_Arrivals (SimEvents Entity Generator or Continuous Poisson Rate)
%   - Handheld_Camera_Acquisition
%   - Edge_IQA_Quality_Check (Recapture feedback loop block)
%   - Edge_AI_Triage (Local Level 0 filtering block)
%   - Rural_Bandwidth_Constraint (Channel delay and capacity bottleneck)
%   - Ophthalmologist_Tele_Review (Single/Multi-server queue with 30s review)
%   - Diagnostic_Sinks (Normal Cleared, Mild Monitored, Referable Treated)
%
% MathWorks Toolboxes: Simulink, SimEvents (if available)

    modelName = 'telemed_dr_screening';
    
    % Close if already open
    if bdIsLoaded(modelName)
        close_system(modelName, 0);
    end
    
    new_system(modelName);
    open_system(modelName);
    
    set_param(modelName, 'Solver', 'VariableStepDiscrete', 'StopTime', '250');
    
    % Block Positions: [left top right bottom]
    % 1. Patient Arrival Generator
    add_block('simulink/Sources/Constant', [modelName '/Daily_Patient_Target'], ...
        'Value', '400', 'Position', [50, 100, 110, 140]);
    
    add_block('simulink/Sources/Random Number', [modelName '/Arrival_Fluctuation'], ...
        'Mean', '0', 'Variance', '25', 'SampleTime', '1', 'Position', [50, 180, 110, 220]);
        
    add_block('simulink/Math Operations/Add', [modelName '/Total_Arrivals'], ...
        'Position', [160, 135, 190, 185]);
        
    % 2. Handheld Acquisition & IQA Quality Triage
    add_block('simulink/Commonly Used Blocks/Gain', [modelName '/Edge_IQA_Pass_Rate'], ...
        'Gain', '0.975', 'Position', [240, 145, 290, 175]); % 97.5% gradeable after instant recapture
        
    % 3. Edge AI Triage Filter (Filters ~75% normal locally)
    add_block('simulink/Commonly Used Blocks/Gain', [modelName '/Referable_DR_Fraction'], ...
        'Gain', '0.25', 'Position', [340, 145, 390, 175]);
        
    % 4. Rural Bandwidth Bottleneck (Delay & Rate Limiter)
    add_block('simulink/Discontinuities/Rate Limiter', [modelName '/Rural_Bandwidth_Limiter'], ...
        'RisingSlewLimit', '120', 'FallingSlewLimit', '-120', 'Position', [440, 140, 500, 180]);
        
    % 5. Ophthalmologist Review Pool Queue
    add_block('simulink/Continuous/Integrator', [modelName '/Doctor_Backlog_Queue'], ...
        'InitialCondition', '0', 'Position', [550, 145, 580, 175]);
        
    % 6. Scopes & Outputs
    add_block('simulink/Sinks/Scope', [modelName '/Queue_Scope'], ...
        'Position', [650, 140, 690, 180]);
        
    add_block('simulink/Sinks/To Workspace', [modelName '/Queue_Log'], ...
        'VariableName', 'sim_backlog_queue', 'SaveFormat', 'Array', 'Position', [650, 210, 710, 240]);
        
    % Connect Lines
    add_line(modelName, 'Daily_Patient_Target/1', 'Total_Arrivals/1');
    add_line(modelName, 'Arrival_Fluctuation/1', 'Total_Arrivals/2');
    add_line(modelName, 'Total_Arrivals/1', 'Edge_IQA_Pass_Rate/1');
    add_line(modelName, 'Edge_IQA_Pass_Rate/1', 'Referable_DR_Fraction/1');
    add_line(modelName, 'Referable_DR_Fraction/1', 'Rural_Bandwidth_Limiter/1');
    add_line(modelName, 'Rural_Bandwidth_Limiter/1', 'Doctor_Backlog_Queue/1');
    add_line(modelName, 'Doctor_Backlog_Queue/1', 'Queue_Scope/1');
    add_line(modelName, 'Doctor_Backlog_Queue/1', 'Queue_Log/1');
    
    % Save Model
    slxPath = fullfile(fileparts(mfilename('fullpath')), [modelName '.slx']);
    save_system(modelName, slxPath);
    fprintf('Successfully built and saved Simulink model to: %s\n', slxPath);
end
