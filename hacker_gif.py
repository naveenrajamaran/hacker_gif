from PIL import Image, ImageDraw, ImageFont, ImageSequence
import sys

charset = "^_`abcdefghijklmnopqrstuvwxyz~*+-.:<=>{}0123456789?@ABCDEFGHIJKLMNOPQRSTUVWXYZ#$%&"
font_size = 10 

font = ImageFont.truetype("Consolas.ttf", size=font_size)
pix_w, pix_h = font.getsize("#")

def process_image(im):
    size = im.size
    w = int(size[0]/pix_w)
    h = int(size[1]/pix_w)
    im = im.convert("RGB")
    im = im.resize((w,h))
    out_im = Image.new("RGB", size, (0, 0, 0))
    dc = ImageDraw.Draw(out_im)
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b = im.getpixel((x, y))
            r = int(r / 6) * 6
            g = int(g / 6) * 6
            b = int(b / 6) * 6
            n = (r + g + b) / (255.0 * 3)
            ch = charset[int((len(charset) - 1) * n)]
            dc.text((x * pix_w, y * pix_h), ch, fill=(r, g, b), font=font)
    return out_im

def main():
    try:
        filename = sys.argv[1]
        out_filename = sys.argv[2]
    except IndexError:
        print ("Usage: %s <input file> <output file>") % sys.argv[0]        
        return
    im = Image.open(filename)
    if im.format == "GIF":
        frames = []
        for frame in ImageSequence.Iterator(im):
            frame = process_image(frame)
            frames.append(frame)
        frames[0].save(out_filename, format=im.format,
            save_all=True, append_images=frames[1:], 
            loop=im.info["loop"], duration=im.info["duration"])
    else:
        pim = process_image(im)
        pim.save(out_filename, format=im.format)
    im.close()

if __name__ == "__main__":
    main()