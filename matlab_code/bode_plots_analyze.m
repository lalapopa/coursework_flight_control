% TODO: crate .csv table for bode plot <12-04-22, lalapopa> %
[r, c] = size(transfer_functions)

for i = 1:c

end
w_v = [10:10:100]*2*pi;
[mag,phs,RadianFrequency] = bode(W_raz_3, w_v);

function [mag, phase, freq, gain_margins, phase_margins] = bode_to_table_format(tranfer_function)
    stats = allmargin(tranfer_function);
    freq_gain = stats.GMFrequency;
    gains = stats.GainMargin;
    gain_margins = [transpose(freq_gain), transpose(gains)];
    freq_phase = stats.PMFrequency;
    phase = stats.PhaseMargin;
    phase_margins = [transpose(freq_phase), transpose(phase)];
    w_v = [0.001:0.01:100]*2*pi;
    [mag_in_gains, phase, freq] = bode(transfer_function, w_v); 
    mag = squeeze(20*log10(mag_in_gains));
    phase = squeeze(phase)

end


