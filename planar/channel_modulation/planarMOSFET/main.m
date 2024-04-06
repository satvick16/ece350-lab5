load('planar_lpxxx_w1_n80_data.mat')

% Extracting Vd and Id data
Vd = n1lp065w1n80output(:, 1);
Id = n1lp065w1n80output(:, 2);

% Find indices where Vd is 0 to identify the start of new sequences
sequence_indices = find(Vd == 0);
sequence_indices(end+1) = length(Vd);

counter = 0.0;

% Initialize figure
figure;

% Iterate through each sequence and plot Vd vs Id
for i = 1:length(sequence_indices)-1
    plot(Vd(sequence_indices(i):sequence_indices(i+1)-1), Id(sequence_indices(i):sequence_indices(i+1)-1), 'DisplayName', sprintf('VGS = %.1f V', counter));
    counter = counter + 0.1;
    hold on;
    
    % Find index where Vd is approximately equal to 1
    idx = find(abs(Vd(sequence_indices(i):sequence_indices(i+1)-1) - 1) < 0.01, 1);
    
    % If such index exists, calculate tangent line
    if ~isempty(idx)
        slope = diff(Id(sequence_indices(i)+idx-1:sequence_indices(i)+idx)) / diff(Vd(sequence_indices(i)+idx-1:sequence_indices(i)+idx));
        x_intercept = Vd(sequence_indices(i)+idx-1) - Id(sequence_indices(i)+idx-1) / slope;
        y_intercept = 0;
        
        % Plot tangent line
        plot([x_intercept Vd(sequence_indices(i)+idx-1)], [y_intercept Id(sequence_indices(i)+idx-1)], 'r--', 'DisplayName', '');

        % text(x_intercept, y_intercept, sprintf('(%.2f, %.2f)', x_intercept, y_intercept), 'HorizontalAlignment', 'right', 'VerticalAlignment', 'bottom');
        disp(x_intercept);
    end
end

% Add labels and legend
xlabel('Vd');
ylabel('Id');
title('Vd vs Id at different Vgs');
legend('Location', 'west');
