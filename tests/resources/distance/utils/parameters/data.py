import math

expected_locations = [
    27, 35, 38, 51, 47, 53, 57, 64, 49
]

height = 14.8

real_locations = [(250, 440),
                  (330, 130),
                  (400, 310),
                  (510, 440),
                  (480, 190),
                  (520, 90),
                  (580, 150),
                  (600, 320),
                  (660, 400),
                  (430, 20)]
real_locations = [(u - 40 + 18, v - 300 + 5) for (u, v) in real_locations]

real_angles = [math.atan(math.sqrt(u ** 2 + v ** 2) / (10.0 * height)) for (u, v) in real_locations]

image_circle_radius = 411
