import distinctipy
from wand.image import Image


def distinct_colors(n):
    """
    create distinct pastel colors for gui objects
    return a list with n distinct color hex codes
    """
    colors = distinctipy.get_colors(n, pastel_factor=0.7)
    colors_to_hex = [distinctipy.distinctipy.get_hex(color) for color in colors]
    return colors_to_hex


def generate_passenger_svg(color, source_image):
    with open(f"graphics/{source_image}.svg", "r") as file:
        svg_code = file.read()
    # update the SVG code with the desired color
    coloured_svg_code = svg_code.format(color, color)
    return coloured_svg_code


# generate distinct colors
colors = distinct_colors(50)

# generate and save images with different colors
for img in {"passenger", "elevator_and_passenger", "passenger_target"}:  # looping on the non-colored svg images
    for index, color in enumerate(colors):
        svg_file_path = f"graphics/{img}_{index}.svg"
        with open(svg_file_path, "w") as svg_file:
            svg_file.write(generate_passenger_svg(color, img))

        # convert SVG to PNG
        png_file_path = f"graphics/{img}_{index}.png"
        with Image(filename=svg_file_path) as svg_image:
            svg_image.save(filename=png_file_path)

