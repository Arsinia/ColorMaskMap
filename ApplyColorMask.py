import os
import numpy as np
import subprocess
import imageio.v3 as iio


def process_image(diffuse_filename, output_filename, color_mask_filenames, selected_colors_filenames):
    # Convert the diffuse image to a NumPy array
    subprocess.run(["texconv.exe", "-ft", "png", "-y", diffuse_filename],
                   capture_output=True)

    diffuse_temp_name, _ = os.path.splitext(diffuse_filename)
    diffuse_temp_name += '.png'
    diffuse_array = iio.imread(diffuse_temp_name)

    # Initialize an empty output image
    output_array = np.zeros_like(diffuse_array, dtype=np.float32)

    output_array += diffuse_array

    for cmm_ind in range(len(color_mask_filenames)):

        color_mask_filename = color_mask_filenames[cmm_ind]
        selected_colors_filename = selected_colors_filenames[cmm_ind]

        # Read the color mask and selected colors images as NumPy arrays
        color_mask_array = iio.imread(color_mask_filename)
        selected_colors_array = iio.imread(selected_colors_filename)

        # Extract the selected colors from the image
        selected_colors_array = np.split(selected_colors_array, 3, axis=1)

        for i, selected_color in enumerate(selected_colors_array):

            # Skip if color is plain white
            if np.array_equal(selected_color[0, 0], [255, 255, 255, 255]):
                continue

            target_intensity = np.average(selected_color[0, 0, 0:3])

            # Normalize the color mask so that it has values between 0 and 1
            normalized_mask = color_mask_array[:, :, i] / 255.0

            intensity = (output_array[:, :, 0] + output_array[:, :, 1] + output_array[:, :, 2]) / 3.0
            average_intensity = np.average(intensity, weights=normalized_mask)
            intensity_adjust = target_intensity - average_intensity

            for c in range(3):
                output_array[:, :, c] = (intensity + intensity_adjust) * normalized_mask + (
                            output_array[:, :, c] * (1 - normalized_mask))
                output_array[:, :, c] *= 1 + (normalized_mask * ((selected_color[0, 0, c] / 255.0) - 1))

    # Clamp the output image to the valid range (0-255) and convert it to uint8
    output_array = np.clip(output_array, 0, 255).astype(np.uint8)

    output_temp_name, _ = os.path.splitext(output_filename)
    output_temp_name += '.png'
    iio.imwrite(output_temp_name, output_array)

    # Convert the output image to a BC7 SRGB DDS file using texconv
    subprocess.run(["texconv.exe", "-f", "BC7_UNORM_SRGB", "-y", "-sepalpha", "-srgb", output_temp_name])

    os.remove(output_temp_name)
    os.remove(diffuse_temp_name)


# Read the input and output filenames from a text file
with open("ColorMasks.txt") as f:
    for line in f:
        if line[0] == ';':
            continue
        filenames = line.strip().split()
        diffuse_filename, output_filename = filenames[0:2]
        color_mask_filenames = []
        selected_colors_filenames = []
        for i in range(0, int(len(filenames) / 2) - 1):
            color_mask_filenames.append(filenames[(2 * i) + 2])
            selected_colors_filenames.append(filenames[(2 * i) + 3])
        process_image(diffuse_filename, output_filename, color_mask_filenames, selected_colors_filenames)
