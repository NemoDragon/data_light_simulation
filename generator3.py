# n positions with lanterns covers shaped like cones, angle = [0, 90] and adds angles to measurements

import math

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
                square_distance = (x - i * 10) ** 2 + (y - j * 10) ** 2 + z ** 2
                square_radius = (z * math.tan(angle)) ** 2
                square_ground_distance = square_distance - z ** 2
                cos_angle = 1 - (square_ground_distance / square_distance) ** 2 if square_distance > 0 else 0
                if square_ground_distance <= square_radius or angle == 90:
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
    pos, lux = gen_measurements(light_positions=[(10, 10, 10)], light_candels=[1000], light_angles=[60])
    save_measurements_to_file('measurements3.txt', pos, lux)


if __name__ == '__main__':
    main()