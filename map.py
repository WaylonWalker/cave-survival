import noise


def generate_map(width, height):
    scale = 20.0
    octaves = 3
    persistence = 0.5
    lacunarity = 2.0
    map_data = []
    for i in range(width):
        column = []
        for j in range(height):
            noise_value = 0
            frequency = 1.0
            amplitude = 1.0
            for k in range(octaves):
                noise_value += amplitude * noise.snoise2(
                    i / scale * frequency, j / scale * frequency
                )
                frequency *= lacunarity
                amplitude *= persistence
            column.append(noise_value)
        map_data.append(column)
    return map_data
