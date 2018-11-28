import cv2

blob_coordinates = [
    ((698.0814819335938, 287.91851806640625), 2.8307735919952393),
    ((24.730375289916992, 275.220703125), 7.048484802246094),
    ((164.48095703125, 161.88571166992188), 3.2084474563598633),
    ((600.4986572265625, 123.28521728515625), 7.974984645843506),
    ((541.1138305664062, 43.25203323364258), 3.749695301055908),
    ((392.18328857421875, 29.525123596191406), 8.324203491210938)]

image = cv2.imread('tests/localization/color/kmeans/test_image.jpg')

colors_analyzed = [
    {'red': 3.883003111115027e-269, 'yellow': 1.2664165549094177e-14, 'green': 0.48304802297166255},
    {'red': 0.00033546262790251185, 'yellow': 6.101936677605325e-13, 'green': 1.6309672734573203e-37},
    {'red': 3.3861055331627575e-250, 'yellow': 6.101936677605325e-13, 'green': 0.28372121379170556},
    {'red': 5.637563890966437e-10, 'yellow': 0.0038659201394728045, 'green': 9.314534238094415e-22},
    {'red': 0.9780830788850546, 'yellow': 1.522997974471263e-08, 'green': 2.4495024501760183e-31},
    {'red': 0.9780830788850546, 'yellow': 4.082836041142518e-08, 'green': 1.0973760273238288e-30}]

centroid_rgb_values = [
    [[163.953125, 201.375, 132.71875]],
    [[190.92091837, 94.62244898, 94.23852041]],
    [[161.19444444, 219.49305556, 106.17361111]],
    [[161.64285714, 126.875, 100.81632653]],
    [[196.42361111, 146.23611111, 137.20833333]],
    [[167.72265625, 110.43359375, 98.00390625]],
]

centroid_hsv_values = [
    (93, 123, 283),
    (0, 181, 268),
    (90, 185, 309),
    (25, 136, 227),
    (9, 108, 276),
    (10, 148, 235),
]