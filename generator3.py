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


def gen_random_measurements(light_positions: list[tuple], light_candels: list[int], light_angles: list[int], num_measurements: int = 20):
    if len(light_positions) != len(light_candels):
        raise ValueError('Lights positions and candels must have the same length')
    if len(light_positions) != len(light_angles):
        raise ValueError('Lights positions and angles must have the same length')
    if any(light_angles) < 0 or any(light_angles) > 90:
        raise ValueError('Lights angles must be between 0 and 90 degrees')
    positions = []
    luxes = []
    for i in range(num_measurements):
        lux = 0
        x_pos, y_pos = random.randint(0, 100), random.randint(0, 100)
        positions.append([x_pos, y_pos, 0])
        for k in range(len(light_positions)):
            x, y, z = light_positions[k]
            angle = light_angles[k]
            angle = math.radians(angle)
            square_distance = (x - x_pos) ** 2 + (y - y_pos) ** 2 + z ** 2
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
    # Random test
    # x, y, z = random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)
    # I = random.sample(range(1000, 20000), 6)
    # a = random.sample(range(1, 91), 6)
    # print(x, y, z)
    # print(I, a)

    # Experimen 001 - one light at (50, 50, 50), 1000 candels, 90 degrees
    pos001, lux001 = gen_measurements(light_positions=[(50, 50, 50)], light_candels=[1000], light_angles=[90])
    save_measurements_to_file('measurements/exp001.txt', pos001, lux001)
    posr001, luxr001 = gen_random_measurements(light_positions=[(50, 50, 50)], light_candels=[1000], light_angles=[90])
    save_measurements_to_file('measurements/expr001.txt', posr001, luxr001)

    # Experiment 002 - one light at (50, 50, 50), 10000 candels, 90 degrees
    pos002, lux002 = gen_measurements(light_positions=[(50, 50, 50)], light_candels=[10000], light_angles=[90])
    save_measurements_to_file('measurements/exp002.txt', pos002, lux002)
    posr002, luxr002 = gen_random_measurements(light_positions=[(50, 50, 50)], light_candels=[10000], light_angles=[90])
    save_measurements_to_file('measurements/expr002.txt', posr002, luxr002)

    # Experiment 003 - one light at (50, 50, 50), 100 candels, 90 degrees
    pos003, lux003 = gen_measurements(light_positions=[(50, 50, 50)], light_candels=[100], light_angles=[90])
    save_measurements_to_file('measurements/exp003.txt', pos003, lux003)
    posr003, luxr003 = gen_random_measurements(light_positions=[(50, 50, 50)], light_candels=[100], light_angles=[90])
    save_measurements_to_file('measurements/expr003.txt', posr003, luxr003)

    # Experiment 004 - one light at (50, 50, 50), 1000 candels, 45 degrees
    pos004, lux004 = gen_measurements(light_positions=[(50, 50, 50)], light_candels=[1000], light_angles=[45])
    save_measurements_to_file('measurements/exp004.txt', pos004, lux004)
    posr004, luxr004 = gen_random_measurements(light_positions=[(50, 50, 50)], light_candels=[1000], light_angles=[45])
    save_measurements_to_file('measurements/expr004.txt', posr004, luxr004)

    # Experiment 005 - one light at (50, 50, 50), 1000 candels, 30 degrees
    pos005, lux005 = gen_measurements(light_positions=[(50, 50, 50)], light_candels=[1000], light_angles=[30])
    save_measurements_to_file('measurements/exp005.txt', pos005, lux005)
    posr005, luxr005 = gen_random_measurements(light_positions=[(50, 50, 50)], light_candels=[1000], light_angles=[30])
    save_measurements_to_file('measurements/expr005.txt', posr005, luxr005)

    # Experiment 006 - one light at (50, 50, 50), 1000 candels, 0 degrees
    pos006, lux006 = gen_measurements(light_positions=[(50, 50, 50)], light_candels=[1000], light_angles=[0])
    save_measurements_to_file('measurements/exp006.txt', pos006, lux006)
    posr006, luxr006 = gen_random_measurements(light_positions=[(50, 50, 50)], light_candels=[1000], light_angles=[0])
    save_measurements_to_file('measurements/expr006.txt', posr006, luxr006)

    #Experiment 007 - one light at (50, 50, 1), 1000 candels, 90 degrees (very close to ground)
    pos007, lux007 = gen_measurements(light_positions=[(50, 50, 1)], light_candels=[1000], light_angles=[90])
    save_measurements_to_file('measurements/exp007.txt', pos007, lux007)
    posr007, luxr007 = gen_random_measurements(light_positions=[(50, 50, 1)], light_candels=[1000], light_angles=[90])
    save_measurements_to_file('measurements/expr007.txt', posr007, luxr007)

    # Experiment 008 - one light at (50, 50, 99), 1000 candels, 90 degrees (very high)
    pos008, lux008 = gen_measurements(light_positions=[(50, 50, 99)], light_candels=[1000], light_angles=[90])
    save_measurements_to_file('measurements/exp008.txt', pos008, lux008)
    posr008, luxr008 = gen_random_measurements(light_positions=[(50, 50, 99)], light_candels=[1000], light_angles=[90])
    save_measurements_to_file('measurements/expr008.txt', posr008, luxr008)

    # Experiment 009 - one light at (10, 10, 10), 1000 candels, 90 degrees (corner)
    pos009, lux009 = gen_measurements(light_positions=[(10, 10, 10)], light_candels=[1000], light_angles=[90])
    save_measurements_to_file('measurements/exp009.txt', pos009, lux009)
    posr009, luxr009 = gen_random_measurements(light_positions=[(10, 10, 10)], light_candels=[1000], light_angles=[90])
    save_measurements_to_file('measurements/expr009.txt', posr009, luxr009)

    # Experiment 010 - one light at (90, 90, 10), 1000 candels, 90 degrees (other corner)
    pos010, lux010 = gen_measurements(light_positions=[(90, 90, 10)], light_candels=[1000], light_angles=[90])
    save_measurements_to_file('measurements/exp010.txt', pos010, lux010)
    posr010, luxr010 = gen_random_measurements(light_positions=[(90, 90, 10)], light_candels=[1000], light_angles=[90])
    save_measurements_to_file('measurements/expr010.txt', posr010, luxr010)

    #Experment 011 - one light at (85, 53, 18), 1234 candels, 56 degrees (random)
    pos011, lux011 = gen_measurements(light_positions=[(85, 53, 18)], light_candels=[1234], light_angles=[56])
    save_measurements_to_file('measurements/exp011.txt', pos011, lux011)
    posr011, luxr011 = gen_random_measurements(light_positions=[(85, 53, 18)], light_candels=[1234], light_angles=[56])
    save_measurements_to_file('measurements/expr011.txt', posr011, luxr011)
    
    # Experiment 012 - two lights at (30, 30, 30) and (70, 70, 30), 1000 candels each, 90 degrees
    pos012, lux012 = gen_measurements(light_positions=[(30, 30, 30), (70, 70, 30)],
                                light_candels=[1000, 1000], light_angles=[90, 90])
    save_measurements_to_file('measurements/exp012.txt', pos012, lux012)
    posr012, luxr012 = gen_random_measurements(light_positions=[(30, 30, 30), (70, 70, 30)],
                                light_candels=[1000, 1000], light_angles=[90, 90])
    save_measurements_to_file('measurements/expr012.txt', posr012, luxr012)
    
    # Experiment 013 - two lights at (20, 20, 50) and (80, 80, 50), 1000 candels each, 90 degrees
    pos013, lux013 = gen_measurements(light_positions=[(20, 20, 50), (80, 80, 50)],
                                light_candels=[1000, 1000], light_angles=[90, 90])
    save_measurements_to_file('measurements/exp013.txt', pos013, lux013)
    posr013, luxr013 = gen_random_measurements(light_positions=[(20, 20, 50), (80, 80, 50)],
                                light_candels=[1000, 1000], light_angles=[90, 90])
    save_measurements_to_file('measurements/expr013.txt', posr013, luxr013)

    # Experiment 014 - three lights at (25, 25, 40), (50, 50, 40), (75, 75, 40), 1000 candels each, 90 degrees
    pos014, lux014 = gen_measurements(light_positions=[(25, 25, 40), (50, 50, 40), (75, 75, 40)],
                                light_candels=[1000, 1000, 1000], light_angles=[90, 90, 90])
    save_measurements_to_file('measurements/exp014.txt', pos014, lux014)
    posr014, luxr014 = gen_random_measurements(light_positions=[(25, 25, 40), (50, 50, 40), (75, 75, 40)],
                                light_candels=[1000, 1000, 1000], light_angles=[90, 90, 90])
    save_measurements_to_file('measurements/expr014.txt', posr014, luxr014)

    # Experiment 015 - five lights at (20,20,20), (40,40,40), (60,60,60), (80,80,80), (50,50,50), 1000 candels each, 90 degrees
    pos015, lux015 = gen_measurements(light_positions=[(20, 20, 20), (40, 40, 40), (60, 60, 60), (80, 80, 80), (50, 50, 50)],
                                light_candels=[1000 for i in range(5)], light_angles=[90 for i in range(5)])
    save_measurements_to_file('measurements/exp015.txt', pos015, lux015)
    posr015, luxr015 = gen_random_measurements(light_positions=[(20, 20, 20), (40, 40, 40), (60, 60, 60), (80, 80, 80), (50, 50, 50)],
                                light_candels=[1000 for i in range(5)], light_angles=[90 for i in range(5)])
    save_measurements_to_file('measurements/expr015.txt', posr015, luxr015)

    # Experiment 016 - ten lights in a row at (0,10,10), (10,10,10), ..., (90,10,10), 1000 candels each, 60 degrees
    pos016, lux016 = gen_measurements(light_positions=[(i * 10, 10, 10) for i in range(10)],
                                light_candels=[1000 for i in range(10)], light_angles=[60 for i in range(10)])
    save_measurements_to_file('measurements/exp016.txt', pos016, lux016)
    posr016, luxr016 = gen_random_measurements(light_positions=[(i * 10, 10, 10) for i in range(10)],
                                light_candels=[1000 for i in range(10)], light_angles=[60 for i in range(10)])
    save_measurements_to_file('measurements/expr016.txt', posr016, luxr016)

    # Experiment 017 - ten lights in a column at (90, 0, 10), (90, 10, 10), ..., (90, 90, 10), 1000 candels each, 60 degrees
    pos017, lux017 = gen_measurements(light_positions=[(90, i * 10, 10) for i in range(10)],
                                light_candels=[1000 for i in range(10)], light_angles=[60 for i in range(10)])
    save_measurements_to_file('measurements/exp017.txt', pos017, lux017)
    posr017, luxr017 = gen_random_measurements(light_positions=[(90, i * 10, 10) for i in range(10)],
                                light_candels=[1000 for i in range(10)], light_angles=[60 for i in range(10)])
    save_measurements_to_file('measurements/expr017.txt', posr017, luxr017)

    # Experiment 018 - four lights at the corners at (0,0,20), (0,99,20), (99,0,20), (99,99,20), 1000 candels each, 60 degrees
    pos018, lux018 = gen_measurements(light_positions=[(0, 0, 20), (0, 99, 20), (99, 0, 20), (99, 99, 20)],
                                light_candels=[1000 for i in range(4)], light_angles=[45 for i in range(4)])
    save_measurements_to_file('measurements/exp018.txt', pos018, lux018)
    posr018, luxr018 = gen_random_measurements(light_positions=[(0, 0, 20), (0, 99, 20), (99, 0, 20), (99, 99, 20)],
                                light_candels=[1000 for i in range(4)], light_angles=[45 for i in range(4)])
    save_measurements_to_file('measurements/expr018.txt', posr018, luxr018)


    print('Average lux in exp001:', sum(lux001) / len(lux001))
    print('Average lux in exp002:', sum(lux002) / len(lux002))
    print('Average lux in exp003:', sum(lux003) / len(lux003))
    print('Average lux in exp004:', sum(lux004) / len(lux004))
    print('Average lux in exp005:', sum(lux005) / len(lux005))
    print('Average lux in exp006:', sum(lux006) / len(lux006))
    print('Average lux in exp007:', sum(lux007) / len(lux007))
    print('Average lux in exp008:', sum(lux008) / len(lux008))
    print('Average lux in exp009:', sum(lux009) / len(lux009))
    print('Average lux in exp010:', sum(lux010) / len(lux010))
    print('Average lux in exp011:', sum(lux011) / len(lux011))
    print('Average lux in exp012:', sum(lux012) / len(lux012))
    print('Average lux in exp013:', sum(lux013) / len(lux013))
    print('Average lux in exp014:', sum(lux014) / len(lux014))
    print('Average lux in exp015:', sum(lux015) / len(lux015))
    print('Average lux in exp016:', sum(lux016) / len(lux016))
    print('Average lux in exp017:', sum(lux017) / len(lux017))
    print('Average lux in exp018:', sum(lux018) / len(lux018))

    print('Average lux in expr001:', sum(luxr001) / len(luxr001))
    print('Average lux in expr002:', sum(luxr002) / len(luxr002))
    print('Average lux in expr003:', sum(luxr003) / len(luxr003))
    print('Average lux in expr004:', sum(luxr004) / len(luxr004))
    print('Average lux in expr005:', sum(luxr005) / len(luxr005))
    print('Average lux in expr006:', sum(luxr006) / len(luxr006))
    print('Average lux in expr007:', sum(luxr007) / len(luxr007))
    print('Average lux in expr008:', sum(luxr008) / len(luxr008))
    print('Average lux in expr009:', sum(luxr009) / len(luxr009))   
    print('Average lux in expr010:', sum(luxr010) / len(luxr010))
    print('Average lux in expr011:', sum(luxr011) / len(luxr011))
    print('Average lux in expr012:', sum(luxr012) / len(luxr012))
    print('Average lux in expr013:', sum(luxr013) / len(luxr013))
    print('Average lux in expr014:', sum(luxr014) / len(luxr014))
    print('Average lux in expr015:', sum(luxr015) / len(luxr015))
    print('Average lux in expr016:', sum(luxr016) / len(luxr016))
    print('Average lux in expr017:', sum(luxr017) / len(luxr017))
    print('Average lux in expr018:', sum(luxr018) / len(luxr018))
    
    
    

if __name__ == '__main__':
    main()