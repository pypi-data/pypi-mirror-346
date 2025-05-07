import time

def pretty_print(text, delay=0.05, end=True, flush=False):
    for char in text:
        print(char, end='' ,flush=True)
        time.sleep(delay)
    print(end='\n' if end else '')

def reverse_pretty_print(text, delay=0.05, end=False):
    result = ""
    for char in reversed(text):
        result = char + result
        print('\r' + result, end='', flush=True)
        time.sleep(delay)
    print(end='\n' if end else '')



def rgb_text(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def interpolate_color(color1, color2, factor):
    return tuple(int(c1 + (c2 - c1) * factor) for c1, c2 in zip(color1, color2))

def generate_gradient_colors(text_length, color_points):
    if text_length < 2 or len(color_points) < 2:
        return [color_points[0]] * text_length

    segment_length = text_length / (len(color_points) - 1)
    colors = []

    for i in range(text_length):
        segment = int(i / segment_length)
        factor = (i % segment_length) / segment_length

        if segment >= len(color_points) - 1:
            segment = len(color_points) - 2
            factor = 1.0

        start_color = color_points[segment]
        end_color = color_points[segment + 1]
        colors.append(interpolate_color(start_color, end_color, factor))

    return colors

def rgb_gradient_text(text, *color_points):
    colors = generate_gradient_colors(len(text), color_points)
    gradient_text = "".join(
        f"\033[38;2;{r};{g};{b}m{c}" for c, (r, g, b) in zip(text, colors)
    )
    gradient_text += "\033[0m"
    return gradient_text

def pretty_gradient_print(text, *color_points, delay=0.05, end=True):
    colors = generate_gradient_colors(len(text), color_points)
    for c, (r, g, b) in zip(text, colors):
        print(f"\033[38;2;{r};{g};{b}m{c}\033[0m", end='', flush=True)
        time.sleep(delay)
    print(end='\n' if end else '')




