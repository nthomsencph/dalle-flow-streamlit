# -*- coding: utf-8 -*-
import streamlit as st
from dalle_flow import run_flow

# set the logo and title
st.set_page_config(page_title="AI ART - DALLE FLOW")


def main():

    """
    Streamlit app for AI art generation.
    """

    #################
    # SIDEBAR
    #################

    # SIDEBAR TITLE
    st.sidebar.markdown(
        '<p style="font-size: 4em; font-weight: 1100;">AI ART</p>',
        unsafe_allow_html=True,
    )
    st.sidebar.write(
        """AI may soon change the way we think about art.
        Already, intuitive and intelligent artwork can be created.
        Try it out for yourself! ⭐
        """
    )
    st.sidebar.markdown(
        """This app wraps [Dalle-Flow](https://github.com/jina-ai/dalle-flow) from [Jina AI](https://github.com/jina-ai): A human-in-the-middle process for co-creating art with models DALL-E
        and GLIDE ([OpenAI, 2021](https://openai.com/research/)). Write text, iterate over the generated images, upscale the resolution and share your work! 🎉
        """
    )
    st.sidebar.markdown("##")
    num_images = st.sidebar.slider("# IMAGES", 4, 16, 4) // 2
    img_var = 1 - st.sidebar.slider("SKIP RATE", 0.0, 1.0, 0.5)
    SERVER_URL = st.sidebar.text_input(
        "SERVER URL", "grpc://dalle-flow.jina.ai:51005"
    )
    if SERVER_URL == "grpc://dalle-flow.jina.ai:51005":
        st.sidebar.warning(
            "Using Jina AI default server. Can take 10+ minutes to generate images"
        )

    #################
    # 1. MAIN PANE
    #################

    prompt = st.text_input("", placeholder="Enter your text here ✏️")

    if "prompt" in st.session_state and "main_img" in st.session_state:
        if prompt != st.session_state["prompt"]:
            del st.session_state["main_img"]

    #################
    # 1.1. Initial generation stage
    #################

    if prompt and "main_img" not in st.session_state:
        st.session_state["prompt"] = prompt
        run_flow(
            SERVER_URL,
            "generation",
            {"prompt": prompt, "num_images": num_images},
        )
        st.markdown("#")

    if "main_img" in st.session_state:
        st.image(
            st.session_state["main_img"], use_column_width=False, width=700
        )

    #################
    # 1.2. Diffusion and resolution stage
    #################

    if (
        "main_img" in st.session_state
        and "upscaled_view" not in st.session_state
    ):
        st.markdown("##")
        st.write(
            """
            Select ID of your favorite. Diffusion yields similar
            images while upscaling yields a higher resolution.
            """
        )
        col1, col2, col3 = st.columns([4, 1, 1])
        fav_id = col1.number_input(
            "",
            min_value=0,
            max_value=16,
            value=0,
        )
        col2.markdown("#")
        col2.button(
            "Diffuse! 🎨",
            on_click=run_flow,
            args=(
                SERVER_URL,
                "diffusion",
                {
                    "fav": fav_id,
                    "num_images": num_images * 2,
                    "skip_rate": img_var,
                },
            ),
        )
        col3.markdown("#")
        col3.button(
            "Upscale 🖼️",
            on_click=run_flow,
            args=(
                SERVER_URL,
                "resolution",
                {"fav": fav_id},
            ),
        )

    if "main_img" in st.session_state:
        st.sidebar.write("DOWNLOAD YOUR ARTWORK 🚀")
        st.sidebar.image(
            st.session_state["qr_img"], use_column_width=True, width=75
        )


if __name__ == "__main__":
    main()
