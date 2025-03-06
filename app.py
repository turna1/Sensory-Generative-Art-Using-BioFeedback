import gradio as gr
import numpy as np
from scipy.signal import spectrogram
import requests
import json
import time
import random

# API settings
url = "https://nexra.aryahcr.cc/api/image/complements"
headers = {"Content-Type": "application/json"}

def generate_image_from_prompt(prompt, model="dalle-mini"):
    data = {"prompt": prompt, "model": model}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_data = response.json()
            image_id = response_data.get("id")
            if not image_id:
                return "Error: No image ID returned in the response."

            while True:
                status_response = requests.get(f"{url}/{image_id}")
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    status = status_data.get("status")
                    if status == "completed":
                        images = status_data.get("images")
                        if images and isinstance(images, list):
                            return images[0]
                        else:
                            return "Error: No images found in the response."
                    elif status == "error":
                        return "Error: Image generation failed."
                    elif status == "pending":
                        time.sleep(1)
                    else:
                        return f"Error: Unexpected status '{status}'."
                else:
                    return f"Error: Status check failed with code {status_response.status_code}."
        else:
            return f"Error: Initial request failed with code {response.status_code}."
    except Exception as e:
        return f"Exception occurred: {str(e)}"

def generate_dynamic_prompt(aura_source, spread, colors, light_pattern, mood, intensity_flow, scaled_duration, scaled_amplitude_variability, scaled_avg_frequency):
    """
    Generate a highly dynamic and diverse prompt for abstract art creation.
    """
    # Randomly select additional features for variety
    textures = random.choice(['fractal florals', 'Celtic knotwork', 'aurelia wisps', 
                              'liquid patterns', 'tessellated mosaics', 'organic fractals'])
    unexpected_elements = random.choice(['glowing spheres', 'swirling nebulas', 'fragments of stardust', 
                                         'iridescent feathers', 'ethereal wings', 'geometric shards'])
    artistic_styles = random.choice(['cubist distortions', 'cosmic surrealism', 'dreamlike overlays', 
                                     'glitch art aesthetics', 'organic layering', 'kaleidoscopic compositions'])

    # Generate the dynamic prompt
    prompt = (
        f"Create an abstract imaginary painting ,Conjure a radiant, ethereal aura, bursting forth or back from {aura_source}. The aura unfurls {spread}, "
        f"a kaleidoscope of variation of {colors}, pulsating with variant of {light_pattern}, radiating variant of {mood}. Incorporate vibrant textures like variant of {textures} "
        f"and unexpected elements like variant of {unexpected_elements}. Use an artistic style inspired by variant of {artistic_styles} to infuse the composition with novelty. "
        f"Let the intensity flow of {intensity_flow} and scaled values of duration ({scaled_duration:.2f}s), amplitude variability ({scaled_amplitude_variability:.2f}), "
        f"and average frequency ({scaled_avg_frequency:.2f} Hz) guide the rhythm and movement of the composition, creating a piece that feels alive, unique, and transcendent."
    )
    return prompt


def mystical_realism_prompt(aura_source, spread, colors, light_pattern, mood, intensity_flow, scaled_duration, scaled_amplitude_variability, scaled_avg_frequency):
    return (
        f"Paint a mystical and surreal scene, where a radiant aura bursts from {aura_source}. The aura unfolds {spread}, "
        f"filled with {colors}, shimmering with {light_pattern}. Its energy radiates {mood}, creating a scene that feels "
        f"both otherworldly and serene. Add textures like celestial waves, glowing tendrils, or ethereal glimmers. Let the rhythm of "
        f"the piece be guided by intensity flow {intensity_flow}, with duration {scaled_duration:.2f}s and variability {scaled_amplitude_variability:.2f}. "
        f"Create a composition that is both calming and transcendental."
    )

def geometric_surrealism_prompt(aura_source, spread, colors, light_pattern, mood, intensity_flow, scaled_duration, scaled_amplitude_variability, scaled_avg_frequency):
    return (
        f"Create an abstract geometric masterpiece where an aura emanates from {aura_source}. The aura expands {spread}, "
        f"dominated by {colors}. It features {light_pattern}, forming sharp patterns, tessellations, and angular flows. "
        f"The mood is {mood}, reflected in layered contrasts and bold lines. Incorporate textures like fractured crystals, kaleidoscopic shards, or reflective mirrors. "
        f"Use the values {intensity_flow}, duration {scaled_duration:.2f}s, and variability {scaled_amplitude_variability:.2f} to guide the artwork’s rhythm. "
        f"The result should feel futuristic, structured, and bold."
    )


def organic_flow_prompt(aura_source, spread, colors, light_pattern, mood, intensity_flow, scaled_duration, scaled_amplitude_variability, scaled_avg_frequency):
    return (
        f"Design an organic and fluid composition inspired by {aura_source}. The aura flows {spread}, showcasing {colors} in smooth, "
        f"natural gradients and soft transitions. It pulses with {light_pattern}, creating a mood of {mood}. Incorporate textures such as "
        f"flowing water, drifting clouds, or tree rings. Let the intensity flow {intensity_flow}, along with duration {scaled_duration:.2f}s and "
        f"variability {scaled_amplitude_variability:.2f}, shape the organic, evolving rhythm. The result should evoke nature’s harmony and endless motion."
    )

def old_analyze_breathing_and_generate_aura(audio):
    """
    Analyze audio input to extract breathing patterns and generate a unique prompt 
    for abstract art creation inspired by the input's spectrogram.
    """
    if audio is None:
        raise ValueError("No audio input provided.")
    
    sample_rate, data = audio
    max_duration = 30  # seconds
    max_samples = max_duration * sample_rate

    # Truncate or handle empty audio data
    if len(data) > max_samples:
        data = data[:max_samples]
    if data.size == 0:
        raise ValueError("Audio data is empty.")

    # Normalize audio data
    data = data / np.max(np.abs(data))

    # Compute spectrogram
    f, t, Sxx = spectrogram(data, sample_rate)

    # Extract dynamic features
    duration = len(data) / sample_rate
    amplitude_variability = np.std(Sxx)
    avg_frequency = np.mean(f)
    intensity_flow = np.mean(Sxx, axis=0).tolist()

    # Scale dynamic features
    scaled_duration = duration * 1.5
    scaled_amplitude_variability = amplitude_variability * 2
    scaled_avg_frequency = avg_frequency * 1.2

    # Decode into aura properties
    if scaled_duration <= 15:
        spread = "tight and concentrated, like a glowing ember"
    elif 15 < scaled_duration <= 30:
        spread = "flowing outward in gentle waves, like ripples on water "
    else:
        spread = "expansive and boundless, filling the space with light"

    if scaled_amplitude_variability < 0.6:
        colors = "muted and calming tones, like soft blues and greys"
    elif 0.6 <= scaled_amplitude_variability < 1.4:
        colors = "balanced gradients of neutral colors soothing calm"
    else:
        colors = "bold, colorful, vibrant hues, bursting with energy"

    if scaled_avg_frequency < 400:
        light_pattern = "smooth, flowing gradients that shimmer softly"
    elif 400 <= scaled_avg_frequency < 800:
        light_pattern = "dynamic ripples of light, pulsing rhythmically"
    else:
        light_pattern = "sharp, radiant bursts of energy, glowing intensely"

    if scaled_amplitude_variability < 0.8:
        mood = "serene, slow, and contemplative, evoking inner peace"
    elif 0.8 <= scaled_amplitude_variability < 1.6:
        mood = "harmonious and balanced, radiating optimism"
    else:
        mood = "energized and vibrant, alive with intensity"

    # Diverse aura sources
    aura_sources = [
        "a glowing heart emanating warmth",
        "an ancient tree rooted in shimmering soil",
        "a radiant sunbeam breaking through storm clouds",
        "a serene ocean wave reflecting moonlight",
        "a swirling galaxy suspended in the cosmos",
        "a meditating figure surrounded by cascading light",
        "a flickering flame glowing in the dark",
        "a dancer’s graceful movements painted in light",
        "a crystal pulsing with vibrant energy",
        "a mystical cloud of swirling colors",
    ]
    aura_source = random.choice(aura_sources)

    # Generate dynamic prompt
    prompt = generate_dynamic_prompt(
        aura_source, spread, colors, light_pattern, mood, 
        intensity_flow, scaled_duration, scaled_amplitude_variability, scaled_avg_frequency
    )

    # Generate image using the prompt
    return generate_image_from_prompt(prompt)

def analyze_breathing_and_generate_aura(audio, style):
    if audio is None:
        raise ValueError("No audio input provided.")
    
    sample_rate, data = audio
    max_duration = 30  # seconds
    max_samples = max_duration * sample_rate

    # Truncate or handle empty audio data
    if len(data) > max_samples:
        data = data[:max_samples]
    if data.size == 0:
        raise ValueError("Audio data is empty.")

    # Normalize audio data
    data = data / np.max(np.abs(data))

    # Compute spectrogram
    f, t, Sxx = spectrogram(data, sample_rate)

    # Extract dynamic features
    duration = len(data) / sample_rate
    amplitude_variability = np.std(Sxx)
    avg_frequency = np.mean(f)
    intensity_flow = np.mean(Sxx, axis=0).tolist()

    # Scale dynamic features
    scaled_duration = duration * 1.5
    scaled_amplitude_variability = amplitude_variability * 2
    scaled_avg_frequency = avg_frequency * 1.2

    # Decode into aura properties
    aura_sources = [
        "a glowing heart emanating warmth",
        "an ancient tree rooted in shimmering soil",
        "a radiant sunbeam breaking through storm clouds",
        "a serene ocean wave reflecting moonlight",
        "a swirling galaxy suspended in the cosmos",
        "a meditating figure surrounded by cascading light",
        "a flickering flame glowing in the dark",
        "a dancer’s graceful movements painted in light",
        "a crystal pulsing with vibrant energy",
        "a mystical cloud of swirling colors",
    ]
    aura_source = random.choice(aura_sources)

    spread = (
        "tight and concentrated, like a glowing ember" if scaled_duration <= 15 else
        "flowing outward in gentle waves, like ripples on water" if scaled_duration <= 30 else
        "expansive and boundless, filling the space with light"
    )
    colors = (
        "muted and calming tones, like soft blues and greys" if scaled_amplitude_variability < 0.6 else
        "balanced gradients of neutral colors soothing calm" if scaled_amplitude_variability < 1.4 else
        "bold, colorful, vibrant hues, bursting with energy"
    )
    light_pattern = (
        "smooth, flowing gradients that shimmer softly" if scaled_avg_frequency < 400 else
        "dynamic ripples of light, pulsing rhythmically" if scaled_avg_frequency < 800 else
        "sharp, radiant bursts of energy, glowing intensely"
    )
    mood = (
        "serene, slow, and contemplative, evoking inner peace" if scaled_amplitude_variability < 0.8 else
        "harmonious and balanced, radiating optimism" if scaled_amplitude_variability < 1.6 else
        "energized and vibrant, alive with intensity"
    )

    # Generate prompt based on selected style
    if style == "Mystical Realism":
        prompt = mystical_realism_prompt(aura_source, spread, colors, light_pattern, mood, intensity_flow, scaled_duration, scaled_amplitude_variability, scaled_avg_frequency)
    elif style == "Geometric Surrealism":
        prompt = geometric_surrealism_prompt(aura_source, spread, colors, light_pattern, mood, intensity_flow, scaled_duration, scaled_amplitude_variability, scaled_avg_frequency)
    elif style == "Organic Flow":
        prompt = organic_flow_prompt(aura_source, spread, colors, light_pattern, mood, intensity_flow, scaled_duration, scaled_amplitude_variability, scaled_avg_frequency)
    else:
        return "Error: Invalid style selected."

    return generate_image_from_prompt(prompt)



# Define the paths to your GIFs
box_breathing_gif = "IMG_0324.gif"
calm_breathing_gif = "IMG_0325.gif"
square_breathing_gif = "IMG_0326.gif"

# Gradio app with Tabs
with gr.Blocks(gr.themes.Glass(primary_hue ="indigo", secondary_hue = "emerald")) as app:
    with gr.Tabs():
        with gr.TabItem("Box Breathing"):
            gr.Image(value=box_breathing_gif, interactive=False, label = "👩‍🏫instruction")
        
        with gr.TabItem("4-7-8 Breathing"):
            gr.Image(value=calm_breathing_gif, interactive=False, label = "👩‍🏫instruction")
        
        with gr.TabItem("Deep Breathing"):
            gr.Image(value=square_breathing_gif, interactive=False, label = "👩‍🏫instruction")

    gr.Markdown("### Record Your Breathing to Generate Your Aura Art")
    
    with gr.Row():
        audio_input = gr.Audio(type="numpy", label="Click to Record Your Breathing")
        style_selector = gr.Dropdown(
            choices=["Mystical Realism", "Geometric Surrealism", "Organic Flow"],
            label="Select Your Art Style"
        )
        aura_output = gr.Image(type="filepath", label="Your Aura Painting")
    with gr.Row():
       submit_button = gr.Button("Create Your Aura")
       submit_button.click(
        analyze_breathing_and_generate_aura,
        inputs=[audio_input, style_selector],
        outputs=aura_output,
    )
    gr.Markdown(
        """
        ### Transform Your Breath into Art 🎨  
        Every breath you take is more than just life—it’s an expression of creativity.  
        Let your inhale and exhale shape an abstract painting, where:  
        - **Deeper breaths** create stronger strokes.  
        - **Wider exhales** expand your aura.  
        Your unique breathing pattern creates a dynamic spectrogram that transforms into a personalized masterpiece.
        """)
        

# Launch the app
app.launch()
