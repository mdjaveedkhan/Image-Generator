import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from flask import Flask, render_template, request, jsonify
import io
import base64

app = Flask(__name__)

# --- CONFIGURATION ---
# Replace with your actual Hugging Face token
MODEL_ID = "segmind/tiny-sd"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Load the model once when the server starts
print(f"Starting server on {DEVICE}...")
pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID, 
    revision="fp16" if DEVICE == "cuda" else "main", 
    torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
    use_auth_token=HF_TOKEN
)
pipe.to(DEVICE)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', 'A beautiful sunset')

    # Run Inference
    if DEVICE == "cuda":
        with autocast(DEVICE):
            image = pipe(prompt, guidance_scale=8.5).images[0]
    else:
        image = pipe(prompt, guidance_scale=8.5).images[0]

    # Convert image to base64 string to send to HTML
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return jsonify({"image": img_str})

if __name__ == '__main__':
    # Render provides a $PORT environment variable. We must use it!
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
