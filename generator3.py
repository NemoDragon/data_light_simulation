# n positions with lanterns covers shaped like cones, angle = [0, 90] and adds angles to measurements

import math
import random

def gen_measurements(light_positions: list[tuple], light_candels: list[int], light_angles: list[int]):
    if len(light_positions) != len(light_candels):
        raise ValueError('Lights positions and candels must have the same length')
    if len(light_positions) != len(light_angles):
        raise ValueError('Lights positions and angles must have the same length')
    if any(light_angles) < 0 or any(light_angles) > 90:
        raise ValueError('Lights angles must be between 0 and 90 degrees')
    positions = []
    luxes = []
    for i in range(10):
        for j in range(10):
            lux = 0
            positions.append([i * 10, j * 10, 0])
            for k in range(len(light_positions)):
                x, y, z = light_positions[k]
                angle = light_angles[k]
                angle = math.radians(angle)
                square_distance = (x - i * 10) ** 2 + (y - j * 10) ** 2 + z ** 2
                square_radius = (z * math.tan(angle)) ** 2
                square_ground_distance = square_distance - z ** 2
                cos_angle = z / (square_distance ** 0.5) if square_distance > 0 else 0
                print(cos_angle, square_ground_distance, square_radius)
                if square_ground_distance <= square_radius or light_angles[k] == 90:
                    lux += light_candels[k] * cos_angle / square_distance
            luxes.append(lux)
    return positions, luxes


def save_measurements_to_file(filename: str, positions: list[list[int]], luxes: list[int]) -> None:
    with open(filename, 'w') as file:
        file.write('{')
        for p in positions:
            file.write('{')
            file.write(str(p[0]))
            file.write(',')
            file.write(str(p[1]))
            file.write(',')
            file.write(str(p[2]))
            file.write('}')
            file.write(',')
        file.write('}')
        file.write(',')
        file.write('\n')
        file.write('{')
        for l in luxes:
            file.write(str(l))
            file.write(',')
        file.write('}')


def main() -> None:
    x, y, z = random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)
    I = random.sample(range(1000, 20000), 6)
    a = random.sample(range(1, 91), 6)
    print(x, y, z)
    print(I, a)
    pos, lux = gen_measurements(light_positions=[(x, y, z), (x, z, y), (y, x, z), (y, z, x), (z, x, y), (z, y, x)], light_candels=I, light_angles=a)
    save_measurements_to_file('measurements/exp015.txt', pos, lux)


if __name__ == '__main__':
    main()