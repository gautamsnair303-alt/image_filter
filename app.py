import streamlit as st
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import segno
import base64
import io
import os

# --- 1. GLOBAL WORKSPACE CONFIGURATION ---
st.set_page_config(
    page_title="PixelCraft & QR Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished interface styling
st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1.1rem; color: #4B5563; margin-bottom: 2rem; }
    .section-block { padding: 1.5rem; border-radius: 0.5rem; background-color: #F3F4F6; margin-bottom: 1rem; }
    .error-text { color: #DC2626; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# --- 2. WORKSPACE NAVIGATION ---
st.sidebar.title("⚡ Workspace Hub")
workspace_mode = st.sidebar.radio(
    "Select Functional Engine:",
    ["🎨 Advanced Image Studio", "🔮 Universal QR Engine"]
)
st.sidebar.markdown("---")

# ==========================================
# MODE A: ADVANCED IMAGE STUDIO
# ==========================================
if workspace_mode == "🎨 Advanced Image Studio":
    st.markdown('<div class="main-header">🎨 Advanced Image Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Manipulate, filter, resize, and optimize images with real-time compression metrics.</div>', unsafe_allow_html=True)

    uploaded_img_file = st.file_uploader("Upload target image layer...", type=["png", "jpg", "jpeg"])

    if uploaded_img_file is not None:
        try:
            # Initialize core image object
            original_image = Image.open(uploaded_img_file)
            img_format = original_image.format if original_image.format else "PNG"
            
            # Workspace Control panel split from presentation grid
            st.sidebar.header("⚙️ Studio Adjustment Panel")
            
            # Filter Controller
            selected_filter = st.sidebar.selectbox(
                "Visual Filter State:",
                ["Original", "Black & White", "Sepia Tone", "Gaussian Blur", "Contour Sketch", "Vibrant Saturation", "Retro Negative", "Emboss Art"]
            )
            
            # Direct Manipulation Canvas Tools
            st.sidebar.markdown("### 📐 Canvas Geometry")
            
            # Resize Tool
            orig_w, orig_h = original_image.size
            maintain_aspect = st.sidebar.checkbox("Maintain Aspect Ratio", value=True)
            
            if maintain_aspect:
                new_width = st.sidebar.number_input("Target Width (px):", min_value=1, max_value=8000, value=orig_w)
                ratio = float(new_width) / float(orig_w)
                new_height = int(orig_h * ratio)
                st.sidebar.caption(f"Calculated Height: {new_height}px")
            else:
                new_width = st.sidebar.number_input("Target Width (px):", min_value=1, max_value=8000, value=orig_w)
                new_height = st.sidebar.number_input("Target Height (px):", min_value=1, max_value=8000, value=orig_h)

            # Crop Tool Boundaries
            st.sidebar.markdown("### ✂️ Boundary Slicing (Margins)")
            crop_left = st.sidebar.slider("Crop Left Margin (px)", 0, orig_w // 2, 0)
            crop_right = st.sidebar.slider("Crop Right Margin (px)", 0, orig_w // 2, 0)
            crop_top = st.sidebar.slider("Crop Top Margin (px)", 0, orig_h // 2, 0)
            crop_bottom = st.sidebar.slider("Crop Bottom Margin (px)", 0, orig_h // 2, 0)
            
            # Compression Optimization Setup
            st.sidebar.markdown("### 📉 Compression Engine")
            compression_quality = st.sidebar.slider("Export Quality Target:", 1, 100, 85)

            # --- PROCESSING ENGINE PIPELINE WITH CONTAINMENT SHIELD ---
            with st.spinner("Processing image matrix transformation..."):
                try:
                    # Step 1: Clone reference
                    working_img = original_image.copy()
                    
                    # Step 2: Crop Manipulation
                    if crop_left + crop_right < orig_w and crop_top + crop_bottom < orig_h:
                        crop_box = (crop_left, crop_top, orig_w - crop_right, orig_h - crop_bottom)
                        working_img = working_img.crop(crop_box)
                    else:
                        st.warning("⚠️ Invalid cropping bounds. Slice logic bypassed.")

                    # Step 3: Resize Execution
                    if working_img.size != (new_width, new_height):
                        working_img = working_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                    # Step 4: Apply High-Fidelity Filters
                    if selected_filter == "Black & White":
                        working_img = ImageOps.grayscale(working_img)
                    elif selected_filter == "Sepia Tone":
                        gray = ImageOps.grayscale(working_img)
                        working_img = ImageOps.colorize(gray, "#704214", "#C0B283")
                    elif selected_filter == "Gaussian Blur":
                        working_img = working_img.filter(ImageFilter.GaussianBlur(radius=5))
                    elif selected_filter == "Contour Sketch":
                        working_img = working_img.filter(ImageFilter.CONTOUR)
                    elif selected_filter == "Vibrant Saturation":
                        enhancer = ImageEnhance.Color(working_img)
                        working_img = enhancer.enhance(2.0)
                    elif selected_filter == "Retro Negative":
                        if working_img.mode in ("RGBA", "P"):
                            working_img = working_img.convert("RGB")
                        working_img = ImageOps.invert(working_img)
                    elif selected_filter == "Emboss Art":
                        working_img = working_img.filter(ImageFilter.EMBOSS)

                    # Step 5: Save to memory buffer evaluating real-time dynamic byte metrics
                    img_buffer = io.BytesIO()
                    # Enforce standard saving formats natively mapping back safely
                    save_format = "PNG" if img_format == "PNG" or selected_filter in ["Contour Sketch", "Retro Negative"] else "JPEG"
                    if working_img.mode == "RGBA" and save_format == "JPEG":
                        working_img = working_img.convert("RGB")
                        
                    working_img.save(img_buffer, format=save_format, quality=compression_quality)
                    processed_bytes = img_buffer.getvalue()
                    
                    # Metric calculations
                    orig_bytes_size = uploaded_img_file.size / 1024
                    proc_bytes_size = len(processed_bytes) / 1024
                    optimization_delta = ((proc_bytes_size - orig_bytes_size) / orig_bytes_size) * 100

                except Exception as e:
                    st.error(f"💥 Processing Fault inside filtering sub-routines: {str(e)}")
                    working_img = original_image
                    processed_bytes = uploaded_img_file.getvalue()

            # --- PRESENTATION CANVAS LAYOUT ---
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 📸 Source Environment")
                st.image(original_image, use_container_width=True, caption=f"Original File Dimension: {orig_w}x{orig_h}")
                st.metric("Source Payload Mass", f"{orig_bytes_size:.2f} KB")
                
            with col2:
                st.markdown(f"### ✨ Modded Framework ({selected_filter})")
                st.image(working_img, use_container_width=True, caption=f"Transformed Dimension: {working_img.size[0]}x{working_img.size[1]}")
                st.metric(
                    "Optimized Payload Mass", 
                    f"{proc_bytes_size:.2f} KB", 
                    delta=f"{optimization_delta:.1f}% Weight Shift",
                    delta_color="inverse"
                )

            # Export Trigger Block
            st.markdown("---")
            st.download_button(
                label="📥 Export Dynamic Processed Asset",
                data=processed_bytes,
                file_name=f"processed_studio_output.{save_format.lower()}",
                mime=f"image/{save_format.lower()}",
                use_container_width=True
            )

        except Exception as file_err:
            st.error(f"❌ Structural file system corruption detected during asset ingestion: {str(file_err)}")
    else:
        st.info("💡 Standby Context: Awaiting target image upload protocol execution within active viewport canvas.")


# ==========================================
# MODE B: UNIVERSAL QR ENGINE
# ==========================================
elif workspace_mode == "🔮 Universal QR Engine":
    st.markdown('<div class="main-header">🔮 Universal QR Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Encode structured string entities, deep link configurations, or asset binary maps directly into QR structural matrix modules.</div>', unsafe_allow_html=True)

    # Styling Overrides via Sidebar
    st.sidebar.header("🎨 Matrix Aesthetics Panel")
    dark_color = st.sidebar.color_picker("QR Module (Dark Segment Line Color):", "#000000")
    light_color = st.sidebar.color_picker("Matrix Canvas Background Color:", "#FFFFFF")
    scale_factor = st.sidebar.slider("Matrix Element Scale Multiplexer:", 4, 15, 8)

    # Tab Architecture Mapping to Split Structural Pipelines
    tab_text, tab_link, tab_image = st.tabs(["📝 Text to QR Pipeline", "🔗 Link to QR Pipeline", "🖼️ Image to QR Pipeline"])
    
    payload_data = None
    processing_ready = False

    # Pipeline A: Text to QR
    with tab_text:
        st.markdown("### Paragraph Context Assembly")
        raw_text = st.text_area("Input literal payload context directly (Paragraph/String Blocks):", value="", placeholder="Enter literal text data to be read safely by standard hardware camera arrays...")
        if raw_text.strip():
            payload_data = raw_text
            processing_ready = True

    # Pipeline B: Link to QR
    with tab_link:
        st.markdown("### Web Target Allocation")
        target_url = st.text_input("Absolute Domain Route Configuration Address:", value="", placeholder="https://example.com/target-endpoint")
        if target_url.strip():
            if not target_url.startswith(("http://", "https://")):
                st.warning("⚠️ Absolute Uniform Resource Identifier prefix missing. Automatically injecting structural secure framing 'https://'")
                payload_data = "https://" + target_url.strip()
            else:
                payload_data = target_url.strip()
            processing_ready = True

    # Pipeline C: Image to QR Conversion Matrix Pipeline
    with tab_image:
        st.markdown("### Matrix Structural Binary Conversion")
        st.caption("Converts graphic frames instantly into continuous base64 Data URI blocks mapped directly onto max-capacity QR matrices.")
        qr_asset_file = st.file_uploader("Upload Image to Base64 Encode...", type=["png", "jpg", "jpeg"], key="qr_asset_uploader")
        
        if qr_asset_file is not None:
            try:
                # Containment logic parsing base64 conversions cleanly
                asset_bytes = qr_asset_file.read()
                # Determine mime type context cleanly
                extension = os.path.splitext(qr_asset_file.name)[1].replace(".", "").lower()
                if extension == "jpg": extension = "jpeg"
                
                b64_encoded_str = base64.b64encode(asset_bytes).decode("utf-8")
                data_uri_payload = f"data:image/{extension};base64,{b64_encoded_str}"
                
                # Check absolute scale parameters against hardware rendering metrics
                st.info(f"💾 Ingestion Complete: Derived data payload size tracking at **{len(data_uri_payload)}** character blocks.")
                
                if len(data_uri_payload) > 2953:
                    st.warning("⚠️ High Density Alert: Matrix limits approaching standard tracking thresholds. High capability device or scanner required to safely capture raw buffer block layout.")
                
                payload_data = data_uri_payload
                processing_ready = True
            except Exception as b64_err:
                st.error(f"💥 Shield Intercept: Failed translating raw binary context to string configuration: {str(b64_err)}")

    # --- MATRIX PIPELINE ENGINE & DOWNSTREAM ASSEMBLY ---
    if processing_ready and payload_data:
        st.markdown("---")
        st.markdown("### 🎛️ Compiled Output Environment Matrix")
        
        col_qr_disp, col_qr_stats = st.columns([1, 2])
        
        with col_qr_disp:
            # Strict Try Except Containment Shield Around Matrix Generation Engine
            try:
                # Generate base QR matrix object structure cleanly
                qr_matrix = segno.make(payload_data, error='L') # High-capacity safe standard tolerance
                
                # Render directly to safe standard memory streaming buffer 
                qr_out_buffer = io.BytesIO()
                qr_matrix.save(
                    qr_out_buffer,
                    kind='png',
                    scale=scale_factor,
                    dark=dark_color,
                    light=light_color
                )
                qr_img_bytes = qr_out_buffer.getvalue()
                
                # Display output matrix visual component cleanly
                st.image(qr_img_bytes, caption="Active Realtime QR Matrix Array Block", use_container_width=False)
                
                # Export downstream delivery system trigger channel
                st.download_button(
                    label="📥 Download Output Matrix File",
                    data=qr_img_bytes,
                    file_name="universal_qr_matrix.png",
                    mime="image/png",
                    use_container_width=True
                )
            except Exception as qr_engine_fault:
                st.markdown(f'<div class="error-text">❌ Matrix Compilation Defect: The payload provided exceeded structural code configuration parameters or color definitions are unmappable. [Detail: {str(qr_engine_fault)}]</div>', unsafe_allow_html=True)
                
        with col_qr_stats:
            st.markdown("#### Matrix Core Structural Specifications")
            if 'qr_matrix' in locals():
                st.json({
                    "Target Character Mass": len(payload_data),
                    "Version Matrix Grid Size": qr_matrix.version,
                    "Error Correction Configuration Level": qr_matrix.designator,
                    "Target Rendering Module Hex String Color": dark_color,
                    "Canvas Array Background Canvas Hex String Color": light_color
                })
            else:
                st.info("System tracking: Awaiting operational matrix structural parameters build execution context.")
    else:
        st.markdown("---")
        st.info("💡 Standby Context: Provide data components inside chosen input tabs to activate matrix streaming compilation pipeline parameters.")
