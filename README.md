[![Open in Streamlit - DOESNT WORK YET](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]()

# Art generator
This is essentially a streamlit app to run [Dalle Flow](https://github.com/jina-ai/dalle-flow#client) with some added functionality.

<br>

<details>
  <summary>CLICK ME IF YOU DON*T HAVE A <b>secrets.toml</b> FILE!</summary>

Create a blank `.streamlit/secrets.toml` file to set compute server and cloud image storage as explained below.

***

## Compute server
As a default, the app calls the DALL-E Flow test server. This works but it is quite slow. One can spin up a private server and specify it in `secrets.toml` file. (To spin up a compute server, follow [this guide](https://github.com/jina-ai/dalle-flow#server)).

Place the url for the live custom compute server in the `secrets.toml` file, like so

```
[SERVER]
url = grpc://dalle-flow.jina.ai:51005
```

***

### Cloud image storage
If a [CLOUDINARY] section is found in the `secrets.toml` file, the app will ping generated images to cloud storage and display a QR code to access the image. A Cloudinary account is easy to set up (2 min) and free up to 1GB. Sign-up and read about the SDK [here](https://cloudinary.com/documentation/django_integration#overview).
Example:

```
[CLOUDINARY]
cloud_name = dxfd3p35h60u
api_key = 3559228886fd32889
api_secret = breUL3VQZhq3RkXdUSfd7H6wC7Xk
```
NB: secret keys above are dummies
</details>

<br>

***

### How to run this in docker
<b>NOTE:</b> You need a secrets.toml file in `/.streamlit` for this to work

```
git clone https://github.com/nthomsencph/dalle-flow-streamlit.git
cd dalle-flow-streamlit

docker build -t datax/dalle-flow:latest .
docker run -p 8501:8501 datax/dalle-flow:latest
```
Navigate to `http://localhost:8501` and BAM!

If you have specified a `cloudinary` section in `.streamlit/secrets.toml`, all images generated will be pinged and logged there. You can log in to Cloudinary to see them. Use your own log in details or the ones in the secrets file if they are specified there.
