#! /usr/bin/env python3

sillyStringOfFields = '31, 84, 86, 6070, 7295, 7296, 7741, 70, 71, 82, 7762, 7282, 7289, 7293, 7294, 7283, 83, 85, 88, 6004, 6457, 6509, 7057, 7058, 7059, 7068, 7084, 7085, 7086, 7087, 7088, 7089, 7094, 7184, 7219, 7220, 7221, 7280, 7281, 7284, 7285, 7286, 7287, 7288, 7290, 7291, 7308, 7309, 7310, 7311, 7607, 7633, 7635, 7636, 7637, 7638, 7639, 7644, 7655, 7671, 7672, 7674, 7675, 7676, 7677, 7678, 7679, 7724, 7681, 7682, 7683, 7684, 7685, 7686, 7687, 7688, 7689, 7690, 7694, 7695, 7696, 7697, 7702, 7703, 7704, 7706, 7707, 7708, 7714, 7718, 7768'
sillyString = sillyStringOfFields.replace(' ', '')
with open('sillyStringOfFields.txt', 'w') as outfile:
    outfile.write(sillyString)
