import numpy as np
import matplotlib.pyplot as plt

# Funktsiya dlya vychisleniya skalyarnogo proizvedeniya dvuh vektorov
def dot_product(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

# Algoritm Cirrus-Beka dlya otsecheniya otrezkov
def cyrus_beck_clip(line_start, line_end, polygon):
    d = np.array(line_end) - np.array(line_start)  # Vektor napravleniya otrezka
    t_enter = 0  # Parametr t na vkhode
    t_exit = 1   # Parametr t na vykhode

    for i in range(len(polygon)):
        # Naidemy normal k tekushemu rebru polygon
        p1 = polygon[i]
        p2 = polygon[(i + 1) % len(polygon)]
        edge = np.array(p2) - np.array(p1)
        normal = np.array([-edge[1], edge[0]])  # Perpendikulyarnyi vektor (normal)

        # Vycheslyaem vektor, vedushchiy ot starta otrezka do tochki p1
        w = np.array(line_start) - np.array(p1)

        # Vycheslyaem skalyarnye proizvedeniya
        numerator = -dot_product(w, normal)
        denominator = dot_product(d, normal)

        if denominator != 0:
            t = numerator / denominator
            if denominator > 0:  # Vkhod v polygon
                t_enter = max(t_enter, t)
            else:  # Vykhod iz polygona
                t_exit = min(t_exit, t)

            if t_enter > t_exit:
                return None  # Otrezok ne vidim

    if t_enter <= t_exit:
        # Vycheslyaem tochki peresecheniya s polygonom
        clipped_start = line_start + t_enter * d
        clipped_end = line_start + t_exit * d
        return clipped_start, clipped_end
    return None

# Funktsiya dlya vizualizatsii otsecheniya otrezka
def draw_plot(lines, polygon):
    fig, ax = plt.subplots()

    # Risuyem polygon
    polygon.append(polygon[0])  # Zamykayem polygon
    polygon = np.array(polygon)
    ax.plot(polygon[:, 0], polygon[:, 1], 'k-', lw=2)

    # Risuyem otrezki do otsecheniya
    for line in lines:
        line_start, line_end = line
        ax.plot([line_start[0], line_end[0]], [line_start[1], line_end[1]], 'r--', label='Do otsecheniya')

    # Otsechenie otrezkov
    for line in lines:
        result = cyrus_beck_clip(np.array(line[0]), np.array(line[1]), polygon[:-1].tolist())
        if result:
            clipped_start, clipped_end = result
            ax.plot([clipped_start[0], clipped_end[0]], [clipped_start[1], clipped_end[1]], 'g-', lw=2, label='Posle otsecheniya')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Otsechenie otrezkov algoritmom Cirrus-Beka')
    plt.grid(True)
    plt.show()

# Primer ispolzovaniya
if __name__ == "__main__":
    # Zadaem polygon (vypukly)
    polygon = [
        [10, 10],
        [100, 30],
        [90, 100],
        [30, 90]
    ]

    # Otrezki dlya otsecheniya
    lines = [
        ([0, 0], [50, 50]),
        ([20, 80], [80, 20]),
        ([60, 60], [120, 120]),
        ([0, 100], [100, 0]),
        ([70, 10], [70, 120])
    ]

    # Vizualizatsiya
    draw_plot(lines, polygon)
