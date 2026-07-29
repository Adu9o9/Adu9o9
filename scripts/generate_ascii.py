from PIL import Image
import math

# The exact ramp used in the repository
RAMP = [" ", ":", "+", "#", "@"]

def image_to_ascii_svg(image_path, output_path, width=80):
    # 1. Open the user's profile picture and convert to grayscale
    img = Image.open(image_path).convert("L")
    
    # 2. Calculate height to maintain aspect ratio 
    # (multiplying by 0.6 because font advance width is 0.600 em)
    orig_w, orig_h = img.size
    aspect_ratio = orig_h / orig_w
    height = int(width * aspect_ratio * 0.6)
    
    img = img.resize((width, height))
    pixels = img.getdata()
    
    # 3. Map pixels to the character ramp
    ascii_lines = []
    for y in range(height):
        line = ""
        for x in range(width):
            # Invert pixel (0 is black, 255 is white) so dark areas get denser characters
            pixel = 255 - pixels[y * width + x]
            # Map 0-255 to 0-4 (the length of our RAMP)
            ramp_index = math.floor((pixel / 255) * (len(RAMP) - 1))
            line += RAMP[ramp_index]
        ascii_lines.append(line)
    
    # 4. Generate the SVG matching his style
    font_size = 12.9
    line_height = font_size
    svg_height = int(height * line_height + 20)
    svg_width = int(width * font_size * 0.6 + 20)
    
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">',
        f'<style>.d-f{{fill:#6e7681}} @media(prefers-color-scheme:dark){{.d-f{{fill:#c9d1d9}}}}</style>',
        f'<g font-family="monospace" font-size="{font_size}" class="d-f">'
    ]
    
    for i, line in enumerate(ascii_lines):
        safe_line = line.replace(" ", "&#160;") # Preserve spaces in SVG
        y_pos = (i + 1) * line_height
        # Adding the typing animation using SMIL delay
        delay = i * 0.05
        anim = f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.45s" fill="freeze"/>'
        svg.append(f'<text x="10" y="{y_pos:.1f}" opacity="0">{anim}{safe_line}</text>')
        
    svg.append('</g></svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated {output_path} successfully!")

# Ensure your image is in the root directory
# Updated to use your passport photo directly in the root folder
image_to_ascii_svg("ADINATH MANOJ NAMBIAR - Photo.jpeg", "ascii.svg")