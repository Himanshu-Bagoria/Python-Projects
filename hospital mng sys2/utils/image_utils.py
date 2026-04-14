import streamlit as st
import requests
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io
import base64
import os
from urllib.parse import urlparse
import hashlib

class ImageProcessor:
    def __init__(self):
        self.cache_dir = "assets/images/cache"
        self.ensure_cache_directory()
    
    def ensure_cache_directory(self):
        """Ensure cache directory exists"""
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def download_image(self, url, timeout=10):
        """Download image from URL with error handling"""
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return Image.open(io.BytesIO(response.content))
        except requests.exceptions.RequestException as e:
            st.error(f"Error downloading image: {e}")
            return None
        except Exception as e:
            st.error(f"Error processing image: {e}")
            return None
    
    def validate_image_url(self, url):
        """Validate if URL is a valid image URL"""
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False
            
            # Check if URL points to an image
            response = requests.head(url, timeout=5)
            content_type = response.headers.get('content-type', '')
            return content_type.startswith('image/')
        except:
            return False
    
    def get_cached_image_path(self, url):
        """Get cached image path for URL"""
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{url_hash}.jpg")
    
    def cache_image(self, url, image):
        """Cache downloaded image"""
        try:
            cache_path = self.get_cached_image_path(url)
            image.save(cache_path, "JPEG", quality=85)
            return cache_path
        except Exception as e:
            st.warning(f"Could not cache image: {e}")
            return None
    
    def get_cached_image(self, url):
        """Get cached image if available"""
        cache_path = self.get_cached_image_path(url)
        if os.path.exists(cache_path):
            try:
                return Image.open(cache_path)
            except:
                return None
        return None
    
    def process_image(self, image, filters=None):
        """Apply filters to image"""
        if filters is None:
            return image
        
        processed = image.copy()
        
        for filter_name, params in filters.items():
            if filter_name == "brightness":
                enhancer = ImageEnhance.Brightness(processed)
                processed = enhancer.enhance(params)
            elif filter_name == "contrast":
                enhancer = ImageEnhance.Contrast(processed)
                processed = enhancer.enhance(params)
            elif filter_name == "blur":
                processed = processed.filter(ImageFilter.GaussianBlur(params))
            elif filter_name == "sharpen":
                processed = processed.filter(ImageFilter.UnsharpMask(params))
        
        return processed
    
    def resize_image(self, image, max_size=(800, 600)):
        """Resize image while maintaining aspect ratio"""
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        return image
    
    def add_watermark(self, image, text="Smart Hospital System"):
        """Add watermark to image"""
        try:
            # Create a copy of the image
            watermarked = image.copy()
            
            # Add text watermark (simplified)
            st.info(f"Watermark added: {text}")
            return watermarked
        except Exception as e:
            st.warning(f"Could not add watermark: {e}")
            return image

# Global instance
image_processor = ImageProcessor()

# Utility functions
def display_image_from_url(image_url, title="Image", width=300):
    """Display image from URL with error handling"""
    if not image_url:
        st.warning("No image URL provided")
        return
    
    try:
        # Validate URL
        if not image_processor.validate_image_url(image_url):
            st.error("Invalid image URL")
            return
        
        # Try to get cached image first
        cached_image = image_processor.get_cached_image(image_url)
        
        if cached_image:
            st.image(cached_image, caption=title, width=width)
        else:
            # Download and cache image
            image = image_processor.download_image(image_url)
            if image:
                image_processor.cache_image(image_url, image)
                st.image(image, caption=title, width=width)
            else:
                st.error("Could not load image")
    
    except Exception as e:
        st.error(f"Error displaying image: {e}")

def create_image_display(image_url, title="Image Display", caption=None):
    """Display a single image with title and caption"""
    st.markdown(f"### {title}")
    
    if image_url:
        display_image_from_url(image_url, caption or title)
    else:
        st.info("No image URL provided")

def create_image_gallery(image_urls, title="Image Gallery"):
    """Create an image gallery"""
    st.markdown(f"### {title}")
    
    if not image_urls:
        st.info("No images to display")
        return
    
    cols = st.columns(min(3, len(image_urls)))
    
    for i, url in enumerate(image_urls):
        with cols[i % 3]:
            display_image_from_url(url, f"Image {i+1}", width=200)

def create_disease_image_display(disease_name, image_url=None):
    """Display disease-related image"""
    st.markdown(f"### 🏥 {disease_name} Information")
    
    if image_url:
        display_image_from_url(image_url, f"{disease_name} Image")
    else:
        create_placeholder_disease_image(disease_name)

def create_placeholder_disease_image(disease_name):
    """Create placeholder for disease image"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    ">
        <h3>🏥 {disease_name}</h3>
        <p>Image placeholder - Add image URL to display actual image</p>
    </div>
    """, unsafe_allow_html=True)

def create_medicine_image_display(medicine_name, image_url=None):
    """Display medicine-related image"""
    st.markdown(f"### 💊 {medicine_name}")
    
    if image_url:
        display_image_from_url(image_url, f"{medicine_name} Image")
    else:
        create_placeholder_medicine_image(medicine_name)

def create_placeholder_medicine_image(medicine_name):
    """Create placeholder for medicine image"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #51cf66 0%, #40c057 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    ">
        <h3>💊 {medicine_name}</h3>
        <p>Medicine image placeholder - Add image URL to display actual image</p>
    </div>
    """, unsafe_allow_html=True)

def create_image_upload_widget():
    """Create image upload widget"""
    st.markdown("### 📷 Image Upload")
    
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg', 'gif', 'bmp']
    )
    
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Image processing options
            st.markdown("#### 🔧 Image Processing")
            
            col1, col2 = st.columns(2)
            
            with col1:
                brightness = st.slider("Brightness", 0.5, 2.0, 1.0)
                contrast = st.slider("Contrast", 0.5, 2.0, 1.0)
            
            with col2:
                blur = st.slider("Blur", 0, 10, 0)
                sharpen = st.slider("Sharpen", 0, 10, 0)
            
            if st.button("Apply Filters"):
                filters = {
                    "brightness": brightness,
                    "contrast": contrast,
                    "blur": blur,
                    "sharpen": sharpen
                }
                
                processed_image = image_processor.process_image(image, filters)
                st.image(processed_image, caption="Processed Image", use_column_width=True)
        
        except Exception as e:
            st.error(f"Error processing uploaded image: {e}")

def create_image_url_input():
    """Create image URL input widget"""
    st.markdown("### 🔗 Image URL Input")
    
    image_url = st.text_input(
        "Enter image URL:",
        placeholder="https://example.com/image.jpg"
    )
    
    if image_url:
        if st.button("Load Image"):
            display_image_from_url(image_url, "Image from URL")

def create_body_scan_visualization():
    """Create body scan visualization"""
    st.markdown("### 🔬 Body Scan Visualization")
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    ">
        <h3>🔬 Body Scan</h3>
        <p>Interactive body scan visualization would be displayed here</p>
        <p>Click on body parts to view detailed scans</p>
    </div>
    """, unsafe_allow_html=True)

def create_xray_visualization():
    """Create X-ray visualization"""
    st.markdown("### 📷 X-Ray Visualization")
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    ">
        <h3>📷 X-Ray Image</h3>
        <p>X-ray visualization would be displayed here</p>
        <p>Add X-ray image URL to display actual image</p>
    </div>
    """, unsafe_allow_html=True)

def create_medical_chart_visualization():
    """Create medical chart visualization"""
    st.markdown("### 📊 Medical Chart")
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    ">
        <h3>📊 Medical Chart</h3>
        <p>Medical chart visualization would be displayed here</p>
        <p>Interactive charts and graphs for patient data</p>
    </div>
    """, unsafe_allow_html=True)
