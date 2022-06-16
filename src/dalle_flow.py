# -*- coding: utf-8 -*-
from docarray import Document
from utils import return_image_sprites
import streamlit as st
from PIL import Image

from utils import img2bytes, upload_to_cloudinary, make_qr

# if "SERVER" in st.secrets:
#     SERVER_URL = st.secrets["SERVER"]["url"]
# else:
#     SERVER_URL = "grpc://dalle-flow.jina.ai:51005"
# print(SERVER_URL)  # noqa


def run_flow(SERVER_URL, action, kwargs):

    if action == "generation":

        func = request_generation
        proc_text = "Doing fancy calculations... 🪄🤖"

    elif action == "diffusion":

        func = request_diffusion
        proc_text = "Doing even more fancy calculations... 🪄🤖"
        kwargs["fav"] = st.session_state["da"][kwargs.get("fav")]

    elif action == "resolution":

        func = request_resolution
        proc_text = "Doing slightly less fancy calculations... 🌮"
        kwargs["fav"] = st.session_state["da"][kwargs.get("fav")]
        st.session_state["upscaled_view"] = True

    else:
        raise ValueError("Invalid action")

    with st.spinner(text=proc_text):
        da, img = func(SERVER_URL, **kwargs)

    # update session state
    st.session_state["main_img"] = img
    st.session_state["da"] = da

    # ping to cloudinary
    run_qr_flow(img2bytes(img))


def run_qr_flow(img_bytes):

    cloud_uri = upload_to_cloudinary(img_bytes, st.session_state["prompt"])
    if cloud_uri:
        st.session_state["qr_img"] = make_qr(cloud_uri)


def request_diffusion(server_url, fav, num_images=9, skip_rate=0.8):
    diffused = fav.post(
        f"{server_url}",
        parameters={"skip_rate": skip_rate, "num_images": num_images},
        target_executor="diffusion",
    ).matches
    return diffused, return_image_sprites(diffused)


def request_generation(server_url, prompt, num_images=9):

    da = (
        Document(text=prompt)
        .post(server_url, parameters={"num_images": num_images})
        .matches
    )
    return da, return_image_sprites(da)


def request_resolution(server_url, fav):
    doc = fav.post(f"{server_url}/upscale", target_executor="upscaler")
    doc.load_uri_to_image_tensor()  # load the data URI to a tensor
    return doc, Image.fromarray(
        doc.tensor
    )  # convert the tensor to a PIL image
