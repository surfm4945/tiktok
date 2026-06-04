import streamlit as st
import yt_dlp
import uuid
import os
import re

# Establish storage path for cached downloads
DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# 🎨 Streamlit Interface Config
st.set_page_config(page_title="TikSave ⚡ - TikTok Downloader", page_icon="⚡", layout="centered")

# Custom UI Styling using standard Markdown injection
st.markdown("""
    <style>
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(45deg, #FF3B5C, #25F4EE);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #888888;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">TikSave ⚡</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Premium Streamlit Video Downloader SaaS Engine</p>', unsafe_allow_html=True)

# Secure input parsing regex validation
def is_valid_tiktok_url(url_string: str) -> bool:
    pattern = r"https?://(www\.)?(tiktok\.com|vt\.tiktok\.com)/.*"
    return re.match(pattern, url_string) is not None

# 📥 Application Input Layer
url_input = st.text_input("Paste TikTok Video URL:", placeholder="https://www.tiktok.com/...")

if st.button("Process Video Stream", use_container_width=True):
    if not url_input.strip():
        st.toast("⚠️ Error: Please provide a valid URL input first.", icon="❌")
    elif not is_valid_tiktok_url(url_input):
        st.error("🔒 Security Halt: The provided link does not match safe standard TikTok domain structures.")
    else:
        # Proceed with download context
        with st.spinner("Initializing safe connection & fetching media streams..."):
            file_id = str(uuid.uuid4())
            output_template = f"{DOWNLOAD_DIR}/{file_id}.%(ext)s"
            
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': output_template,
                'quiet': True,
                'no_warnings': True,
                'geo_bypass': True,
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Extract payload data and download binary file data
                    info_dict = ydl.extract_info(url_input, download=True)
                    ext = info_dict.get('ext', 'mp4')
                    computed_filepath = f"{DOWNLOAD_DIR}/{file_id}.{ext}"
                    
                    if os.path.exists(computed_filepath):
                        st.balloons()
                        st.success("✅ Media Stream Processing Completed Successfully!")
                        
                        # Render Video Preview Player Component
                        st.video(computed_filepath)
                        
                        # Open and map file stream to standard client-side download button
                        with open(computed_filepath, "rb") as video_file:
                            st.download_button(
                                label="📥 Save High-Quality Video to Device",
                                data=video_file,
                                file_name=f"tiksave_{file_id}.{ext}",
                                mime=f"video/{ext}",
                                use_container_width=True
                            )
                            
                        # Clean up local runtime disk environment space instantly after loading byte data
                        os.remove(computed_filepath)
                    else:
                        st.error("System Error: Local stream mapping target resolution failed.")
            except Exception as e:
                st.error(f"Processing Error: Failed to extract media source. Verify that the video is public. Details: {str(e)}")
