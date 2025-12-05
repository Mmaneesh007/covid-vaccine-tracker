"""
Image Optimizer for Web Use
Converts and optimizes images from Stock Pictures folder for web deployment
"""

from PIL import Image
import os
from pathlib import Path

# Paths
STOCK_DIR = Path(r"c:\Users\Manish\Desktop\COVID-19 vaccine tracker\Stock Pictures")
OUTPUT_DIR = Path(r"c:\Users\Manish\Desktop\COVID-19 vaccine tracker\assets\optimized")

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Image sizes for responsive design
SIZES = {
    'thumbnail': 400,      # For cards, previews
    'medium': 800,         # For tablets
    'large': 1920,         # For desktop hero images
}

# Quality settings
JPEG_QUALITY = 85
WEBP_QUALITY = 80

def optimize_image(input_path, output_dir, filename):
    """
    Optimize a single image and create multiple sizes
    """
    try:
        print(f"\nProcessing: {filename}")
        
        # Open image
        img = Image.open(input_path)
        
        # Convert RGBA to RGB if needed
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get base name without extension
        base_name = Path(filename).stem
        original_size = input_path.stat().st_size / 1024  # KB
        print(f"  Original size: {original_size:.1f} KB")
        
        # Create different sizes
        for size_name, max_dimension in SIZES.items():
            # Resize maintaining aspect ratio
            img_copy = img.copy()
            img_copy.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
            suffix = f'_{size_name}'
            
            # Save as optimized JPEG
            jpeg_path = output_dir / f"{base_name}{suffix}.jpg"
            img_copy.save(jpeg_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)
            jpeg_size = jpeg_path.stat().st_size / 1024  # KB
            reduction = ((original_size - jpeg_size) / original_size) * 100
            print(f"  >> JPEG ({size_name}): {jpeg_size:.1f} KB (-{reduction:.0f}%)")
            
            # Save as WebP (better compression)
            webp_path = output_dir / f"{base_name}{suffix}.webp"
            img_copy.save(webp_path, 'WEBP', quality=WEBP_QUALITY, method=6)
            webp_size = webp_path.stat().st_size / 1024  # KB
            reduction_webp = ((original_size - webp_size) / original_size) * 100
            print(f"  >> WebP ({size_name}): {webp_size:.1f} KB (-{reduction_webp:.0f}%)")
        
        print(f"  [OK] Completed: {filename}")
        
    except Exception as e:
        print(f"  [ERROR] processing {filename}: {str(e)}")

def main():
    print("*** Image Optimization for Web Use ***")
    print("=" * 50)
    
    # Get all image files
    image_extensions = {'.jpg', '.jpeg', '.png'}
    images = [f for f in os.listdir(STOCK_DIR) 
              if Path(f).suffix.lower() in image_extensions]
    
    print(f"\nFound {len(images)} images to optimize")
    print(f"Output directory: {OUTPUT_DIR}\n")
    
    # Process each image
    for img_file in images:
        input_path = STOCK_DIR / img_file
        optimize_image(input_path, OUTPUT_DIR, img_file)
    
    print("\n" + "=" * 50)
    print("[DONE] Optimization Complete!")
    print(f"\nOptimized images saved to: {OUTPUT_DIR}")
    print("\nGenerated sizes:")
    for size_name, dimension in SIZES.items():
        print(f"  - {size_name}: {dimension}px max dimension (JPEG + WebP)")
    
    print("\nUsage in HTML:")
    print("  <picture>")
    print("    <source srcset='path/to/image_large.webp' type='image/webp' media='(min-width: 1200px)'>")
    print("    <source srcset='path/to/image_medium.webp' type='image/webp' media='(min-width: 768px)'>")
    print("    <img src='path/to/image_thumbnail.jpg' alt='Description'>")
    print("  </picture>")

if __name__ == "__main__":
    main()
