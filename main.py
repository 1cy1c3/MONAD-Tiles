import cairo
import random
import asyncio
from concurrent.futures import ThreadPoolExecutor

height, width = 500, 500
colors = [(181, 168, 250), (204, 196, 252), (95, 237, 223), (28, 94, 87), (32, 0, 82), (13, 0, 33), (74, 0, 43),
          (96, 0, 78), (38, 0, 31), (158, 245, 237), (199, 105, 158), (204, 196, 252), (128, 51, 112), (248, 237, 231),
          (191, 247, 242), (217, 156, 191)]


def draw_rectangle(cr, x, y, r, g, b, w, h):
    cr.set_source_rgb(r, g, b)
    cr.rectangle(x, y, w, h)
    cr.fill_preserve()  # Preserve the path for stroking later

    cr.set_source_rgb(0, 0, 0)
    cr.set_line_width(1)
    cr.stroke()  # Stroke the outline of the rectangle


def draw_border(cr, size, r, g, b, w, h):
    cr.set_source_rgb(r, g, b)
    cr.rectangle(0, 0, size, h)
    cr.rectangle(0, 0, w, size)
    cr.rectangle(0, h - size, w, size)
    cr.rectangle(w - size, 0, size, h)
    cr.fill()


def mark_area(dp, i, j, w, h):
    for x in range(i, i + w):
        for y in range(j, j + h):
            dp[x][y] = True
    return dp


def is_rectangle_in_marked_area(dp, i, j, w, h):
    # Iterate over all pixels in the rectangle defined by (i, j, w, h)
    for x in range(i, i + w):
        for y in range(j, j + h):
            # Check if the pixel is marked as True in dp
            if dp[x][y]:
                return True  # Overlap found
    return False  # No overlap found


def main(number):
    min_h, max_h = 30, 100
    min_w, max_w = 30, 100
    min_gap, max_gap = 5, 10

    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(ims)

    dp = [[False] * height for _ in range(width)]
    draw_rectangle(cr, 0, 0, .514, .431, .976, width, height)

    for i in range(4, width - 5):
        for j in range(4, height - 5):
            if dp[i][j] is False:
                w = random.randint(min_w, max_w)
                h = random.randint(min_h, max_h)
                gap_x = random.randint(min_gap, max_gap)
                gap_y = random.randint(min_gap, max_gap)

                while h + j > height or any(dp[i][y] for y in range(j, j + h)):
                    h -= 1

                while w + i > width or any(dp[x][j] for x in range(i, i + w)):
                    w -= 1

                if (w > min_w and h > min_h and not is_rectangle_in_marked_area(dp, i, j, w, h)
                        and i + w < width - min_gap and j + h < height - min_gap):
                    color = random.choice(colors)
                    r, g, b = color[0] / 255.0, color[1] / 255.0, color[2] / 255.0
                    draw_rectangle(cr, i + gap_x, j + gap_y, r, g, b, w - gap_x, h - gap_y)
                    # write_text(cr, i + gap_x, j - h / 2 + gap_y, h / 4)
                    dp = mark_area(dp, i, j, w, h)

    #draw_border(cr, 5, .514, .431, .976, width, height)
    ims.write_to_png(f'examples/{number}.png')


async def run_main(number: int):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, main, number)


async def main_async(n):
    tasks = [run_main(i) for i in range(1, n + 1)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main_async(int(input('Iterations: '))))
