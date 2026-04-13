import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


INTER_AREA = 3
INTER_LINEAR = 1
COLOR_RGB2GRAY = 7
COLOR_BGR2RGB = 4
IMREAD_GRAYSCALE = 0
IMREAD_COLOR = 1
FONT_HERSHEY_SIMPLEX = 0
LINE_AA = 16
BORDER_REPLICATE = 1


def _to_uint8_image(array):
    arr = np.asarray(array)
    if arr.dtype == np.uint8:
        return arr
    if arr.size == 0:
        return arr.astype(np.uint8)
    if np.issubdtype(arr.dtype, np.floating):
        if arr.max(initial=0.0) <= 1.0 and arr.min(initial=0.0) >= 0.0:
            return np.clip(arr * 255.0, 0, 255).astype(np.uint8)
    return np.clip(arr, 0, 255).astype(np.uint8)


def _from_uint8_like(original, array):
    arr = np.asarray(array)
    if np.asarray(original).dtype == np.uint8:
        return arr.astype(np.uint8)
    return arr.astype(np.float64) / 255.0


def imread(path, flag=IMREAD_COLOR):
    image = Image.open(Path(path))
    if flag == IMREAD_GRAYSCALE:
        image = image.convert('L')
        return np.asarray(image)
    image = image.convert('RGB')
    rgb = np.asarray(image)
    return rgb[:, :, ::-1]


def cvtColor(image, code):
    arr = np.asarray(image)
    if code == COLOR_BGR2RGB:
        return arr[:, :, ::-1]
    if code == COLOR_RGB2GRAY:
        if arr.ndim != 3 or arr.shape[2] != 3:
            raise ValueError('COLOR_RGB2GRAY expects an RGB image')
        gray = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
        return gray.astype(arr.dtype if arr.dtype == np.uint8 else np.float64)
    raise ValueError(f'Unsupported color conversion code: {code}')


def resize(image, dsize, interpolation=INTER_LINEAR):
    target_w, target_h = dsize
    src = _to_uint8_image(image)
    pil = Image.fromarray(src)
    resample = Image.BILINEAR if interpolation == INTER_LINEAR else Image.BOX
    resized = pil.resize((target_w, target_h), resample=resample)
    return _from_uint8_like(image, np.asarray(resized))


def _load_font(scale):
    size = max(10, int(round(scale * 24)))
    try:
        return ImageFont.truetype('DejaVuSans.ttf', size=size)
    except Exception:
        return ImageFont.load_default()


def putText(image, text, org, font_face, font_scale, color, thickness=1, lineType=LINE_AA):
    arr = _to_uint8_image(image)
    pil = Image.fromarray(arr)
    draw = ImageDraw.Draw(pil)
    font = _load_font(font_scale)
    x, y = org
    for offset in range(max(1, thickness)):
        draw.text((x, y + offset), text, fill=int(color), font=font)
    arr[:] = np.asarray(pil)
    return arr


def line(image, pt1, pt2, color, thickness=1):
    arr = _to_uint8_image(image)
    pil = Image.fromarray(arr)
    draw = ImageDraw.Draw(pil)
    draw.line([pt1, pt2], fill=int(color), width=max(1, int(thickness)))
    arr[:] = np.asarray(pil)
    return arr


def getRotationMatrix2D(center, angle, scale):
    cx, cy = center
    theta = math.radians(angle)
    alpha = scale * math.cos(theta)
    beta = scale * math.sin(theta)
    return np.array(
        [
            [alpha, beta, (1 - alpha) * cx - beta * cy],
            [-beta, alpha, beta * cx + (1 - alpha) * cy],
        ],
        dtype=np.float64,
    )


def warpAffine(image, matrix, dsize, flags=INTER_LINEAR, borderMode=BORDER_REPLICATE):
    target_w, target_h = dsize
    src = _to_uint8_image(image)
    pil = Image.fromarray(src)

    affine = np.vstack([np.asarray(matrix, dtype=np.float64), [0.0, 0.0, 1.0]])
    inverse = np.linalg.inv(affine)
    coeffs = inverse[:2, :].reshape(-1)
    resample = Image.BILINEAR if flags == INTER_LINEAR else Image.NEAREST
    transformed = pil.transform(
        (target_w, target_h),
        Image.AFFINE,
        data=tuple(float(x) for x in coeffs),
        resample=resample,
        fillcolor=0,
    )
    return _from_uint8_like(image, np.asarray(transformed))
