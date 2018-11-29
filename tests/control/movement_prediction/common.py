import numpy as np

old_vectors = [
    [1, 0],
    [0, 0],
    [2 * np.sqrt(2), np.deg2rad(45)],
    [2 * np.sqrt(2), np.deg2rad(-90)],
    [3, np.deg2rad(135)],
]
translations = [
    [0, 0],
    [2, 0],
    [2, np.deg2rad(90)],
    [2, np.deg2rad(-45)],
    [3, np.deg2rad(-135)],
]
new_vectors = [
    [1, 0],
    [2, np.deg2rad(180)],
    [2, np.deg2rad(-90)],
    [2, np.deg2rad(-90)],
    [3 * np.sqrt(2), np.deg2rad(-135)],
]
current_positions = [
    [4, 0],
    [2, np.deg2rad(90)],
    [1, np.deg2rad(-90)],
    [2 * np.sqrt(2), np.deg2rad(-45)],
    [np.sqrt(2), np.deg2rad(45)],
]
movement_vectors = [
    [3, 0],
    [2 * np.sqrt(2), np.deg2rad(45)],
    [1, np.deg2rad(90)],
    [2, 0],
    [4 * np.sqrt(2), np.deg2rad(45)],
]
sum_of_vectors = [
    [2, 0],
    [2, np.deg2rad(180)],
    [2, 0],
    [2 + 2 * np.sqrt(2), np.deg2rad(-90)],
    [3 * np.sqrt(3), -3],
]
