% TODO: crate .csv table for bode plot <12-04-22, lalapopa> %
[r, c] = size(transfer_functions)

for i = 1:c
    [mag, phs, freq] = bode_to_table_format(transfer_functions(i));
    [gain_m, phase_m] = bode_stats(transfer_functions(i));
    out_table_bode = table(mag, phs, freq); 
    writetable(out_table_bode, data_names(i),'Delimiter',','); 
    [gain_m, phase_m] = bode_stats(transfer_function(i));
    out_table_bode_stats = table(gain_m, phase_m);
    writetable(out_table_bode_stats, data_names_bode_stats(i), 'Delimiter', ',');

end


function [mag, phase, freq] = bode_to_table_format(tranfer_function)
    w_v = [0.001:0.01:100]*2*pi;
    [mag_in_gains, phase, freq] = bode(transfer_function, w_v); 
    mag = squeeze(20*log10(mag_in_gains));
    phase = squeeze(phase)

end

function [gain_margins, phase_margins] = bode_stats(transfer_function)
    stats = allmargin(tranfer_function);
    freq_gain = stats.GMFrequency;
    gains = stats.GainMargin;
    gain_margins = [transpose(freq_gain), transpose(gains)];
    freq_phase = stats.PMFrequency;
    phase = stats.PhaseMargin;
    phase_margins = [transpose(freq_phase), transpose(phase)];
end

