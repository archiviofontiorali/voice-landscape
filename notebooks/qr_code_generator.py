import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import django
    import os, sys
    from pathlib import Path
    from typing import Optional

    import qrcode
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer

    from PIL import Image
    from PIL import ImageDraw, ImageFont

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "voices.settings")
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

    django_project_path = Path().cwd() / "app"
    if str(django_project_path) not in sys.path:
        sys.path.insert(0, str(django_project_path))

    django.setup()


@app.cell
def _():
    from django.conf import settings
    from website.models import Place, Landscape


    landscape = Landscape.objects.get(default=True)

    for _place in landscape.places.all():
        print(_place.slug)
    return landscape, settings


@app.function(hide_code=True)
def create_qr_code(url: str, box_size: int = 10, padding: int = 4) -> Image.Image:
    """
    Return the binary PNG data for a QR‑code that encodes *url*.

    Parameters
    ----------
    url:
        The URL (or any text) you want to embed.
    box_size:
        Pixel size of each QR‑module. Larger → bigger image.
    border:
        Width of the quiet zone (in modules) around the QR‑code.

    Returns
    -------
    bytes
        PNG‑encoded image data.
    """
    qr = qrcode.QRCode(
        version=None,  # let the library pick the smallest version
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=padding,
    )
    qr.add_data(url)
    qr.make(fit=True)
    image = qr.make_image(
        fill_color="black",
        back_color="white",
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
    )
    image = image.get_image()

    return image


@app.cell(hide_code=True)
def _():
    def _font(font_size: int = 10, multiplier: float = 1.0):
        size = int(font_size * multiplier)
        return ImageFont.truetype(
            "/usr/share/fonts/TTF/FiraCodeNerdFontMono-Regular.ttf", size=size
        )
        # return ImageFont.load_default(size=size)


    def _text_size(draw: ImageDraw, text: str, font) -> tuple[int, int]:
        l, t, r, b = draw.textbbox([0, 0], text, font=font)
        return r - l, b - t


    def _add_text(img, text, x, y, **kwargs):
        draw = ImageDraw.Draw(img)
        draw.text((x, y), text, **kwargs)


    def add_info_qr_code(
        qr_img: Image.Image,
        title: str,
        url: str,
        subtitle: Optional[str] = None,
        *,
        font_size: int = 10,
        border: int = 20,
        padding: int = 0,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> Image.Image:
        """Return a new image with text centered underneath the QR code."""
        dummy = ImageDraw.Draw(qr_img)

        title_font = _font(font_size, 2.0)
        title_width, title_height = _text_size(dummy, title.upper(), title_font)

        url_font = _font(font_size, 0.75)
        url_width, url_height = _text_size(dummy, url, url_font)

        subtitle_font = _font(font_size, 1.75)
        if subtitle:
            subtitle_width, subtitle_height = _text_size(
                dummy, subtitle.upper(), subtitle_font
            )
        else:
            subtitle_width = subtitle_height = 0

        if width is None:
            width = max(qr_img.width, title_width, subtitle_width, url_width)
            width += 2 * border

        if height is None:
            height = qr_img.height + title_height + subtitle_height + url_height
            height += 4 * border

        img = Image.new("RGB", (width, height), "white")

        # Add qr-code in the center
        xi, yi = (width - qr_img.width) // 2, (height - qr_img.height) // 2
        img.paste(qr_img, (xi, yi))

        xu, yu = (width - url_width) // 2, (height + qr_img.height) // 2 + padding
        _add_text(img, url, xu, yu, fill="black", font=url_font)

        xs, ys = ((width - subtitle_width) // 2, yi - padding - subtitle_font.size)
        if subtitle:
            _add_text(img, subtitle.upper(), xs, ys, fill="gray", font=subtitle_font)

        xt, yt = (
            (width - title_width) // 2,
            (ys if subtitle else yi) - padding // 2 - title_font.size,
        )
        _add_text(img, title.upper(), xt, yt, fill="black", font=title_font)

        return img

    return (add_info_qr_code,)


@app.cell
def _():
    create_qr_code("https://voci.afor.dev")
    return


@app.cell
def _(add_info_qr_code, landscape, settings):
    INCH2CM = 2.54
    DPI = 300

    width = height = int(DPI * INCH2CM)

    qr_codes = []

    for place in landscape.places.all():
        title = place.qr_title
        subtitle = place.qr_subtitle
        url = f"https://{settings.DOMAIN}/qr/{place.slug}"

        box_size = 14 if len(url) < 45 else 12
        qr_code = create_qr_code(url, box_size=box_size)
        qr_code = add_info_qr_code(
            qr_code, title, url, subtitle=subtitle, width=width, height=height, font_size=20
        )

        qr_codes.append((place.slug, qr_code))

    mo.hstack([mo.image(q[1], height=400) for q in qr_codes], justify="center")
    return (qr_codes,)


@app.cell
def _():
    save = mo.ui.run_button("success", label="Save in .data")
    save
    return (save,)


@app.cell
def _(qr_codes, save):
    mo.stop(not save.value)
    QR_CODE_PATH = Path(".data/qr_codes")
    QR_CODE_PATH.mkdir(exist_ok=True, parents=True)
    for slug, qr in qr_codes:
        qr.save(Path(f".data/qr_codes/{slug}.png"))
    return


if __name__ == "__main__":
    app.run()
