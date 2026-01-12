import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
import matplotlib.pyplot as plt

def generate_image():
    # 1. Configuration
    # Note: Modern versions of diffusers use 'token' instead of 'use_auth_token'
    authorization_token = "YOUR_HF_TOKEN_HERE" 
    modelid = "CompVis/stable-diffusion-v1-4"
    
    # Check if CUDA is available, otherwise fallback to CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # 2. Load the Pipeline
    print("Loading model... this may take a minute.")
    pipe = StableDiffusionPipeline.from_pretrained(
        modelid, 
        revision="fp16", 
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        token=authorization_token
    )
    pipe.to(device)

    # 3. Get User Input
    textprompt = input("Enter your prompt: ")

    # 4. Run Inference
    print(f"Generating image for: '{textprompt}'...")
    
    # We only use autocast if we are on a GPU (cuda)
    if device == "cuda":
        with autocast(device):
            output = pipe(textprompt, guidance_scale=8.5)
    else:
        output = pipe(textprompt, guidance_scale=8.5)

    image = output.images[0]

    # 5. Display and Save
    plt.imshow(image)
    plt.axis('off')  # Hide the x/y axis for a cleaner look
    
    # Save the image to your project folder
    image.save("generated_output.png")
    print("Image saved as 'generated_output.png'")
    
    plt.show()

if __name__ == "__main__":
    generate_image()