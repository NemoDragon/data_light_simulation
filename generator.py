# one position

def gen_measurements(light_position: list[int], light_candels: int):
    positions = []
    luxes = []
    x, y, z = light_position
    for i in range(10):
        for j in range(10):
            positions.append([i * 10, j * 10, 0])
            square_distance = (x - i * 10) ** 2 + (y - j * 10) ** 2 + z ** 2
            luxes.append(light_candels / square_distance)
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
    pos, lux = gen_measurements(light_position=[50, 50, 50], light_candels=1000)
    save_measurements_to_file('measurements.txt', pos, lux)


if __name__ == '__main__':
    main()
