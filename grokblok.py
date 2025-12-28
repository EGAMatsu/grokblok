#-====================================-
#
#     GrokBlok - Shitty ass tool to
# Help artists prevent AI use on their
#               works.
#
#-====================================-
#   Made by Digi-Space Productions
#           aka. EGAMatsu
#-====================================-

import sys
import os
from PIL import Image

def build_merged_palette(p1, p2, colors1=16, colors2=239):
    p1 = p1[:colors1 * 3]
    p2 = p2[:colors2 * 3]

    merged = []

    # make the 16 color palette for the gag image
    for i in range(0, len(p1), 3):
        merged.append((p1[i], p1[i+1], p1[i+2]))

    # make 239 colors
    for i in range(0, len(p2), 3):
        rgb = (p2[i], p2[i+1], p2[i+2])
        if rgb not in merged:
            merged.append(rgb)
        if len(merged) >= 255:  # make 255 a transparent color
            break

    # add a transparency color
    merged.append((0, 0, 0))

    # flatten the color palette
    flat = []
    for r, g, b in merged:
        flat.extend([r, g, b])

    return flat[:256 * 3]


def main():
    if len(sys.argv) != 2:
        print("Usage: python grokblok.py <image>")
        sys.exit(1)

    arg_path = sys.argv[1]
    initial_path = "./InitialImage.png"

    if not os.path.isfile(initial_path) or not os.path.isfile(arg_path):
        print("Missing required image.")
        sys.exit(1)

    # load the images
    frame2_rgb = Image.open(arg_path).convert("RGB")
    w, h = frame2_rgb.size
    frame1_rgb = Image.open(initial_path).convert("RGB").resize((w, h), Image.LANCZOS)

    # make the shared pal.
    q1 = frame1_rgb.convert("P", palette=Image.Palette.ADAPTIVE, colors=16, dither=Image.FLOYDSTEINBERG)
    q2 = frame2_rgb.convert("P", palette=Image.Palette.ADAPTIVE, colors=239, dither=Image.FLOYDSTEINBERG)

    p1 = q1.getpalette()
    p2 = q2.getpalette()

    merged_palette = build_merged_palette(p1, p2)

    frame1_p = q1.copy()
    frame1_p.putpalette(merged_palette)

    lut = list(range(256))
    for i in range(239):
        lut[i] = i + 16
    frame2_p = q2.point(lut)
    frame2_p.putpalette(merged_palette)

    # generate blank frame
    blank = Image.new("P", (w, h), 255)  # 255 = transparent index
    blank.putpalette(merged_palette)

    frames = []

    # add the main image
    frames.append(frame2_p)

    # add blank frames
    for _ in range(1022):
        frames.append(blank.copy())

    # repeat the image again
    final_frame = frame2_p.copy()
    frames.append(final_frame)

    # output
    base, _ = os.path.splitext(arg_path)
    out_gif = base + ".gif"

    # save the gif
    frame1_p.save(
        out_gif,
        save_all=True,
        append_images=frames,
        duration=[40] * (1 + len(frames)),
        loop=1,                             # this disables looping, but twitter will loop reguardless; but this could be useful
                                            # for other sites that do the crap that twitter does.
        disposal=1,
        transparency=255,
        optimize=False
    )

    print(f"Output the \"blok'd\" image to: {out_gif}, enjoy.")

if __name__ == "__main__":
    main()
