import os
import face_recognition
import cv2
from PIL import Image, UnidentifiedImageError
import streamlit as st
from rembg import remove
from io import BytesIO
import zipfile

# Utility Functions
def load_reference_image(image_file):
    """Load and encode a reference image."""
    try:
        image = face_recognition.load_image_file(image_file)
        encodings = face_recognition.face_encodings(image)
        if not encodings:
            raise ValueError("No face detected in the reference image.")
        return encodings[0]
    except Exception as e:
        st.error(f"Error loading reference image: {e}")
        return None

def process_group_photos(group_folder, reference_encodings, tolerance=0.5, resize_factor=0.5):
    """Detect and identify faces in group photos with larger green boxes and thicker lines."""
    matched_photos = []
    for filename in os.listdir(group_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(group_folder, filename)
            try:
                # Load the original image
                image = face_recognition.load_image_file(image_path)
                original_image = Image.fromarray(image)  # Keep the original for download
                
                # Resize the image for faster processing
                height, width = image.shape[:2]
                small_image = cv2.resize(image, (int(width * resize_factor), int(height * resize_factor)))

                # Detect faces and encode them
                face_locations = face_recognition.face_locations(small_image, model="hog")
                face_encodings = face_recognition.face_encodings(small_image, face_locations)

                # Scale back the face locations to match the original image size
                face_locations = [(int(top / resize_factor) - 20,  # Expand top by 20 pixels
                                   int(right / resize_factor) + 20,  # Expand right by 20 pixels
                                   int(bottom / resize_factor) + 20,  # Expand bottom by 20 pixels
                                   int(left / resize_factor) - 20)   # Expand left by 20 pixels
                                  for top, right, bottom, left in face_locations]

                match_found = False
                for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
                    matches = face_recognition.compare_faces(reference_encodings, face_encoding, tolerance=tolerance)
                    if any(matches):
                        match_found = True
                        # Draw a larger green box with thicker lines around the matched face
                        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 5)  # Line thickness set to 5

                # Add the image with green boxes to matched_photos if a match is found
                if match_found:
                    matched_photos.append(Image.fromarray(image))
            except Exception as e:
                st.error(f"Error processing photo {filename}: {e}")
    return matched_photos

def download_photos(photos, name):
    """Create a ZIP file for downloading."""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        for i, photo in enumerate(photos):
            buf = BytesIO()
            photo.save(buf, format="JPEG")
            zf.writestr(f"{name}_photo_{i+1}.jpg", buf.getvalue())
    zip_buffer.seek(0)
    return zip_buffer

# App Configuration
st.set_page_config(page_title="Event Photo Finder Using Selfie", page_icon="📸", layout="wide")

# Custom Styles
st.markdown(
    """
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f7f7f7;
        }
        .header {
            background-color: #FF5722;
            padding: 20px;
            text-align: center;
            color: white;
            font-size: 24px;
            border-radius: 8px;
        }
        .footer {
            background-color: #333;
            color: white;
            padding: 10px;
            position: fixed;
            bottom: 0;
            width: 100%;
            text-align: center;
            font-size: 14px;
            border-radius: 8px;
        }
        .highlight {
            color: #FF5722;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown('<div class="header">📸 Event Photo Finder Using Selfie</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📂 Input Configuration")
group_photos_folder = st.sidebar.text_input("📁 Enter Group Photos Folder Path", "/User/Downloads")
st.sidebar.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Search Photos", "🗑️ Remove Background", "✂️ Crop Photos", "👫 Search With Friends"
])

# Tab 1: Search Photos
with tab1:
    st.markdown('<p class="highlight">🔍 Search Photos Using a Selfie</p>', unsafe_allow_html=True)
    reference_image_file = st.file_uploader("📤 Upload a Selfie (Reference Image)", type=["jpg", "jpeg", "png"])
    tolerance = st.slider("🎯 Match Tolerance (Lower is stricter)", 0.3, 0.7, 0.5)

    if reference_image_file:
        reference_encoding = load_reference_image(reference_image_file)
        if reference_encoding is not None:
            matched_photos = process_group_photos(group_photos_folder, [reference_encoding], tolerance=tolerance)
            if matched_photos:
                st.success(f"✅ Found {len(matched_photos)} matched photos!")
                # Display photos in a 4x4 grid
                num_photos = len(matched_photos)
                rows = (num_photos + 3) // 4
                for row in range(rows):
                    cols = st.columns(4)
                    for i in range(4):
                        idx = row * 4 + i
                        if idx < num_photos:
                            with cols[i]:
                                st.image(matched_photos[idx], caption=f"Photo {idx + 1}")

                # Download Button
                zip_file = download_photos(matched_photos, "matched_photos")
                st.download_button("📥 Download All Matched Photos", data=zip_file, file_name="matched_photos.zip")
            else:
                st.warning("⚠️ No matches found.")

# Tab 2: Remove Background
with tab2:
    st.subheader("🗑️ Remove Background From Photos")
    bg_image_file = st.file_uploader("📤 Upload a photo to remove background", type=["jpg", "jpeg", "png"])
    if bg_image_file:
        try:
            image = Image.open(bg_image_file)
            st.image(image, caption="📸 Original Photo", use_column_width=True)
            if st.button("🪄 Remove Background"):
                result = remove(image.convert("RGB"))
                st.image(result, caption="✅ Background Removed", use_column_width=True)

                # Download Button
                buf = BytesIO()
                result.save(buf, format="PNG")
                st.download_button(
                    "📥 Download Background Removed Photo",
                    data=buf.getvalue(),
                    file_name="background_removed.png",
                    mime="image/png",
                )
        except UnidentifiedImageError:
            st.error("❌ Unable to process the uploaded file. Please ensure it is a valid image file.")

# Tab 3: Crop Photos
with tab3:
    st.subheader("✂️ Crop Photos")
    crop_image_file = st.file_uploader("📤 Upload a photo to crop", type=["jpg", "jpeg", "png"])
    crop_ratio = st.radio("📏 Select Crop Ratio:", ["1:1 (Square)", "16:9", "4:3"])
    if crop_image_file:
        image = Image.open(crop_image_file)
        width, height = image.size

        # Calculate Crop Ratios
        if crop_ratio == "1:1 (Square)":
            new_size = min(width, height)
            left = (width - new_size) // 2
            top = (height - new_size) // 2
            right = left + new_size
            bottom = top + new_size
        elif crop_ratio == "16:9":
            new_width = width
            new_height = int(width / 16 * 9)
            top = (height - new_height) // 2
            left, right, bottom = 0, width, top + new_height
        elif crop_ratio == "4:3":
            new_width = width
            new_height = int(width / 4 * 3)
            top = (height - new_height) // 2
            left, right, bottom = 0, width, top + new_height

        # Crop the image
        cropped_image = image.crop((left, top, right, bottom))
        st.image(cropped_image, caption="✅ Cropped Photo", use_column_width=True)

        # Download Button
        buf = BytesIO()
        cropped_image.save(buf, format="JPEG")
        st.download_button(
            "📥 Download Cropped Photo",
            data=buf.getvalue(),
            file_name="cropped_photo.jpg",
            mime="image/jpeg",
        )

# Tab 4: Search With Friends
with tab4:
    st.subheader("👫 Search Photos With Friends")
    selfie1 = st.file_uploader("📤 Upload Selfie 1", type=["jpg", "jpeg", "png"], key="selfie1")
    selfie2 = st.file_uploader("📤 Upload Selfie 2", type=["jpg", "jpeg", "png"], key="selfie2")

    if selfie1 and selfie2:
        ref_enc1 = load_reference_image(selfie1)
        ref_enc2 = load_reference_image(selfie2)

        if ref_enc1 is not None and ref_enc2 is not None:
            matched_photos = process_group_photos(group_photos_folder, [ref_enc1, ref_enc2], tolerance=0.5)
            if matched_photos:
                st.success(f"✅ Found {len(matched_photos)} photos with both individuals!")
                for i, photo in enumerate(matched_photos):
                    st.image(photo, caption=f"Matched Photo {i + 1}")
                # Download Button
                zip_file = download_photos(matched_photos, "friends_matched")
                st.download_button("📥 Download All Matched Photos", data=zip_file, file_name="friends_photos.zip")
            else:
                st.warning("⚠️ No matches found.")

# Footer
st.markdown('<div class="footer">© 2025 Event Photo Finder | Built with ❤️ using Streamlit</div>', unsafe_allow_html=True)
