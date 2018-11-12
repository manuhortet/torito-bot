import io

from PIL import Image, ImageDraw, ImageFont, ImageSequence


def draw_outline(drawable, x, y, text, font):
    for x in range(x-2, x+2, 2):
        for y in range(y-2, y+2, 2):
            drawable.text((x, y), text, fill=1, font=font)
    drawable.text((x, y), text, fill=255, font=font)


def lines(drawable, text, font, size):
    words = text.split(" ")
    lines = []
    new_line = []
    i = 0
    while i < len(words):
        new_line.append(words[i])
        line = " ".join(new_line)
        w, h = drawable.textsize(line, font)
        i += 1
        if w > size:
            lines.append(line)
            new_line = []
    if new_line and lines:
        lines.append(" ".join(new_line))
        return lines
    return lines if lines else [" ".join(new_line)]


def longlines(drawable, x, final_text, font, size):
    for line in final_text:
        w, h = drawable.textsize(line, font)
        if w > size:
            return x - (w - size)
        if w > (size * 4/5):
            return x - (size - w)
    return x


def update_coordinates(x, y, x_torero):
    if x > 140:
        x += 22
        y -= 2
        x_torero -= 5
    else:
        x += 18
    return x, y, x_torero


def memify_torito(torito_text=None, torero_text=None, output='res/memified_torito.gif'):
    im = Image.open("res/torito.png")
    drawable = ImageDraw.Draw(im)

    x, y, x_torero = -45, 50, 270
    font = ImageFont.truetype("res/impact.ttf", 20)
    if not torito_text:
        torito_text = input("Torito: ").rstrip()
        torero_text = input("Torero: ").rstrip()
    final_torito_text = lines(drawable, torito_text, font, 70)
    final_torero_text = lines(drawable, torero_text, font, 40)
    text_width, text_height = drawable.textsize(final_torito_text[0], font)
    x = longlines(drawable, x, final_torito_text, font, size=70)
    x_torero = longlines(drawable, x_torero, final_torero_text, font, size=50)

    im = Image.open('res/torito.gif')

    frames = []
    for frame in ImageSequence.Iterator(im):
        x, y, x_torero = update_coordinates(x, y, x_torero)
        drawable = ImageDraw.Draw(frame)

        # torito (size on x: 70)
        new_y_location = y + text_height
        for line in reversed(final_torito_text):
            new_y_location -= text_height
            draw_outline(drawable, x, new_y_location, line, font)

            # torero (size on x: 50, aprox(260,310))
        if x < 225:
            new_y_location = 53 + text_height
            for line in reversed(final_torero_text):
                new_y_location -= text_height
                draw_outline(drawable, x_torero, new_y_location, line, font)

        del drawable

        b = io.BytesIO()
        frame.save(b, format="GIF")
        frame = Image.open(b)
        frames.append(frame)

        frames[0].save(output, save_all=True,
                       append_images=frames[1:])


if __name__ == '__main__':
    memify_torito()
