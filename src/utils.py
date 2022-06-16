# -*- coding: utf-8 -*-
import copy
from math import sqrt, ceil, floor
import numpy as np
from PIL import Image, ImageDraw
from io import BytesIO
import streamlit as st

USE_CLOUDINARY = False
if "CLOUDINARY" in st.secrets:

    import cloudinary
    from cloudinary import uploader
    import qrcode

    cloudinary.config(
        cloud_name=st.secrets["CLOUDINARY"]["cloud_name"],
        api_key=st.secrets["CLOUDINARY"]["api_key"],
        api_secret=st.secrets["CLOUDINARY"]["api_secret"],
    )
    USE_CLOUDINARY = True


def return_image_sprites(
    da,
    canvas_size: int = 512,
    min_size: int = 16,
    channel_axis: int = -1,
    image_source: str = "tensor",
    skip_empty: bool = False,
    show_index: bool = True,
) -> None:
    """Generate a sprite image for all image tensors
     in this DocumentArray-like object.

    An image sprite is a collection of images put into
    a single image. It is always square-sized.
    Each sub-image is also square-sized and equally-sized.

    :param output: Optional path to store the visualization.
    If not given, show in UI
    :param canvas_size: the size of the canvas
    :param min_size: the minimum size of the image
    :param channel_axis: the axis id of the color channel,
           ``-1`` indicates the color channel info at the last axis
    :param image_source: specify where the image comes from, can be
           ``uri`` or ``tensor``. empty tensor will fallback to uri
    :param skip_empty: skip Document who has no .uri or .tensor.
    :param show_progress: show a progresbar.
    """
    if not da:
        raise ValueError(f"{da!r} is empty")

    img_per_row = ceil(sqrt(len(da)))
    img_size = int(canvas_size / img_per_row)

    if img_size < min_size:
        # image is too small, recompute the size
        img_size = min_size
        img_per_row = int(canvas_size / img_size)

    max_num_img = img_per_row**2
    sprite_img = np.zeros(
        [img_size * img_per_row, img_size * img_per_row, 3], dtype="uint8"
    )
    img_id = 0

    try:
        for _idx, d in enumerate(da):
            if not d.uri and d.tensor is None:
                if skip_empty:
                    continue
                else:
                    raise ValueError(
                        "Document has neither `uri`"
                        + "nor `tensor`, can not be plotted"
                    )

            _d = copy.deepcopy(d)

            if image_source == "uri" or (
                image_source == "tensor" and _d.content_type != "tensor"
            ):
                _d.load_uri_to_image_tensor()
                channel_axis = -1
            elif image_source not in ("uri", "tensor"):
                raise ValueError("image_source can be only `uri` or `tensor`")

            _d.set_image_tensor_channel_axis(
                channel_axis, -1
            ).set_image_tensor_shape(shape=(img_size, img_size))

            row_id = floor(img_id / img_per_row)
            col_id = img_id % img_per_row

            if show_index:
                _img = Image.fromarray(_d.tensor)
                draw = ImageDraw.Draw(_img)
                draw.text((0, 0), str(_idx), (255, 255, 255))
                _d.tensor = np.asarray(_img)

            sprite_img[
                (row_id * img_size) : ((row_id + 1) * img_size),
                (col_id * img_size) : ((col_id + 1) * img_size),
            ] = _d.tensor

            img_id += 1
            if img_id >= max_num_img:
                break
    except Exception as ex:
        raise ValueError(
            "Bad image tensor. Try different `image_source` or `channel_axis`"
        ) from ex

    return Image.fromarray(sprite_img)


def img2bytes(img):

    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def upload_to_cloudinary(img_bytes, img_name):
    """Uploa dto cloudinary. Returns public URI"""
    try:
        r = uploader.upload(img_bytes, public_id=img_name)
        return r.get("url")
    except Exception:
        print("Failed to upload to cloudinary")  # noqa
        return False


def make_qr(uri):

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=4,
    )
    qr.add_data(uri)
    qr.make(fit=True)

    return img2bytes(qr.make_image(fill_color="white", back_color="black"))
