[r, c] = size(transfer_functions);


for tf_val = 1:c
    [mag, phs, freq] = bode_to_table_format(transfer_functions(tf_val));
    [gain_m, phase_m] = bode_stats(transfer_functions(tf_val));
    out_table_bode = table(mag, phs, freq); 
    writetable(out_table_bode, strcat(FOLDER_BODE, data_names(tf_val)),'Delimiter',','); 

    [gain_m, phase_m, freq_gain, freq_phase] = bode_stats(transfer_functions(tf_val));
    out_table_bode_stats = table(gain_m, freq_gain, phase_m, freq_phase);
    writetable(out_table_bode_stats, strcat(FOLDER_BODE, data_names_bode_stats(tf_val)), 'Delimiter', ',');
end

function [mag, phase, freq] = bode_to_table_format(transfer_function)
    w_v = [0.001:0.01:100]*2*pi;
    [mag_in_gains, phase, freq] = bode(transfer_function, w_v); 
    mag = squeeze(gain_to_dB(mag_in_gains));
    phase = squeeze(phase);

end

function [gains, phase_m, freq_gain, freq_phase] = bode_stats(transfer_function)
    stats = allmargin(transfer_function);
    freq_gain = transpose(stats.GMFrequency);
    gains = transpose(gain_to_dB(stats.GainMargin));
    if ismember(inf, freq_gain)
        inf_index = find(freq_gain == inf);
        freq_gain(inf_index) = [];
        gains(inf_index) = [];
    end

    freq_phase = transpose(stats.PMFrequency);
    phase_m = transpose(stats.PhaseMargin);
    [freq_phase, index] = max(freq_phase);
    phase_m = phase_m(index);



%    if isempty(phase_m)
%        [r_g, c_g] = size(gains);
%        phase_m = zeros(r_g, c_g);
%        freq_phase = zeros(r_g, c_g);
%    end
%
%    if any(size(phase_m) ~= size(gains))
%        [r_g, c_g] = size(gains);
%        [r_p, c_p] = size(phase_m);
%        if r_g > r_p
%            phase_m(r_p+1, :) = zeros(1, 1);
%            freq_phase(r_p+1, :) = zeros(1, 1);
%        end
%    end
end

function [dB] = gain_to_dB(gain_value);
    dB = 20*log10(gain_value);
end

