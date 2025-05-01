import os
import yt_dlp
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="YT Grab Pro", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
        @keyframes gradient {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        
        @keyframes float {
            0% {transform: translateY(0px);}
            50% {transform: translateY(-10px);}
            100% {transform: translateY(0px);}
        }
        
        @keyframes shine {
            to {background-position: 200% center;}
        }
        
        @keyframes pulse {
            0% {transform: scale(1);}
            50% {transform: scale(1.05);}
            100% {transform: scale(1);}
        }
        
        :root {
            --primary: #6366f1;
            --secondary: #8b5cf6;
            --accent: #ec4899;
            --background: #f8fafc;
        }
        
        body {
            background: linear-gradient(45deg, #f3f4f6, #e5e7eb) !important;
            font-family: 'Segoe UI', system-ui, sans-serif;
        }
        
        .main {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2.5rem;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.3);
            animation: float 6s ease-in-out infinite;
            margin: 1rem auto;
            max-width: 800px;
        }
        
        .header {
            text-align: center;
            padding: 3rem 0;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            background-size: 200% 200%;
            animation: gradient 8s ease infinite;
            color: white;
            border-radius: 20px;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
        }
        
        .header::after {
            content: "";
            position: absolute;
            top: 0;
            left: -100%;
            width: 200%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.2),
                transparent
            );
            animation: shine 3s infinite;
        }
        
        .stTextInput>div>div>input {
            border-radius: 15px !important;
            padding: 14px 24px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            font-size: 1rem;
        }
        
        .stTextInput>div>div>input:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15) !important;
        }
        
        .stSelectbox>div>div>select {
            border-radius: 15px !important;
            padding: 12px 20px !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton>button {
            width: 100%;
            border-radius: 15px !important;
            padding: 16px 32px !important;
            background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
            color: white !important;
            font-weight: 600 !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            position: relative;
            overflow: hidden;
            border: none !important;
            animation: pulse 2s infinite;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(99, 102, 241, 0.3) !important;
            animation: none;
        }
        
        .stButton>button::after {
            content: "";
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                45deg,
                transparent,
                rgba(255, 255, 255, 0.3),
                transparent
            );
            transform: rotate(45deg);
            animation: shine 3s infinite;
        }
        
        .download-info {
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            margin-top: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            animation: slideIn 0.5s ease-out;
        }
        
        .footer {
            text-align: center;
            padding: 2rem 0;
            margin-top: 3rem;
            color: #64748b;
            position: relative;
        }
        
        .platforms {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            margin: 1.5rem 0;
            flex-wrap: wrap;
        }
        
        .platform-badge {
            background: rgba(99, 102, 241, 0.1);
            padding: 0.6rem 1.2rem;
            border-radius: 25px;
            font-size: 0.9rem;
            color: var(--primary);
            border: 1px solid rgba(99, 102, 241, 0.2);
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .platform-badge:hover {
            transform: translateY(-2px);
            background: rgba(99, 102, 241, 0.15);
            box-shadow: 0 4px 6px rgba(99, 102, 241, 0.1);
        }
        
        .platform-badge.active {
            background: var(--primary);
            color: white;
            font-weight: 500;
        }
        
        @keyframes slideIn {
            from {transform: translateY(20px); opacity: 0;}
            to {transform: translateY(0); opacity: 1;}
        }
        
        .stSpinner>div {
            border-color: var(--primary) transparent transparent transparent !important;
        }
        
        .watermark {
            position: fixed;
            bottom: 10px;
            right: 10px;
            opacity: 0.5;
            font-size: 0.8rem;
            color: #64748b;
        }
    </style>
""", unsafe_allow_html=True)

def get_download_dir():
    """
    Returns the default downloads directory for the user's operating system
    """
    if os.name == 'nt': 
        download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    elif os.name == 'posix':  # macOS, Linux, and other Unix-like systems
        download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    else:
        download_dir = os.path.join(os.path.expanduser('~'), 'Videos')
    
    Path(download_dir).mkdir(exist_ok=True)
    
    videos_dir = os.path.join(download_dir, 'YtGrabPro')
    Path(videos_dir).mkdir(exist_ok=True)
    
    return videos_dir

DOWNLOAD_PATH = get_download_dir()

st.markdown('<div class="header"><h1 style="margin:0;font-size:2.5rem;">🚀 YT Grab Pro</h1><p style="margin:0.5rem 0 0;font-size:1.1rem;">Download Videos from Popular Platforms</p></div>', unsafe_allow_html=True)
st.markdown("<div class='main'>", unsafe_allow_html=True)

st.markdown("### 📥 Download Media Content")
url = st.text_input("Paste URL here", placeholder="📌 Example: https://youtube.com/watch?v=... or https://tiktok.com/@user/video/...")

st.markdown(f"**Save location:** {DOWNLOAD_PATH}")
use_custom_path = st.checkbox("Use custom save location")

if use_custom_path:
    custom_path = st.text_input("Custom save location (full path):", 
                               value=DOWNLOAD_PATH,
                               help="Enter a valid path on your device where files should be saved")
    if custom_path and Path(custom_path).exists():
        download_path = custom_path
    else:
        if custom_path:
            st.warning("Path does not exist. Will use default location.")
        download_path = DOWNLOAD_PATH
else:
    download_path = DOWNLOAD_PATH

platform = None
if url:
    if "youtube.com" in url or "youtu.be" in url:
        platform = "YouTube"
    elif "tiktok.com" in url:
        platform = "TikTok"
    elif "instagram.com" in url:
        platform = "Instagram"
    elif "twitter.com" in url or "x.com" in url:
        platform = "Twitter/X"
    elif "facebook.com" in url or "fb.com" in url:
        platform = "Facebook"

# Show format selection only for YouTube
show_formats = platform == "YouTube"

if show_formats:
    format_choice = st.selectbox(
        "🎚️ Select Format",
        ["Best Quality Available", "MP4 720p (if available)", "MP4 480p (if available)", "Audio Only (MP3)"],
        index=0
    )
else:
    format_choice = "Best Quality Available"

advanced_options = st.expander("Advanced Options")
with advanced_options:
    show_available_formats = st.checkbox("Show available formats before downloading")
    fallback_to_best = st.checkbox("Automatically fallback to best available quality", value=True)

if st.button("🚀 Start Download"):
    if not url:
        st.error("Please enter a valid URL.")
    else:
        # Basic options that always apply
        ydl_opts = {
            "outtmpl": f"{download_path}/%(title)s.%(ext)s",
            "quiet": False,  # Set to False to capture more detailed output
            "no_warnings": False,  # We want warnings to help debug
            "ignoreerrors": True,  # Continue on error to allow fallback
        }
        
        # If user wants to see available formats
        if show_available_formats:
            with st.spinner("Fetching available formats..."):
                info_opts = dict(ydl_opts)
                info_opts["listformats"] = True
                info_opts["quiet"] = False
                
                format_output = []
                def format_logger(msg):
                    format_output.append(msg)
                
                try:
                    with yt_dlp.YoutubeDL({"quiet": False, "no_warnings": False}) as ydl:
                        ydl.add_default_info_extractors()
                        info = ydl.extract_info(url, download=False, process=False)
                        
                        with yt_dlp.YoutubeDL({"quiet": False, "listformats": True}) as ydl:
                            ydl.add_default_info_extractors()
                            info = ydl.extract_info(url, download=False)
                            
                            # Format information is stored in info['formats']
                            if 'formats' in info:
                                st.markdown("### Available Formats")
                                format_table = []
                                
                                # Header row
                                format_table.append("| Format Code | Extension | Resolution | Note |")
                                format_table.append("|------------|-----------|------------|------|")
                                
                                for f in info['formats']:
                                    format_id = f.get('format_id', 'N/A')
                                    ext = f.get('ext', 'N/A')
                                    resolution = 'N/A'
                                    
                                    if 'height' in f and 'width' in f:
                                        resolution = f"{f['width']}x{f['height']}"
                                    elif 'height' in f:
                                        resolution = f"{f['height']}p"
                                        
                                    note = f.get('format_note', '')
                                    if f.get('acodec', 'none') == 'none':
                                        note += ' [video only]'
                                    if f.get('vcodec', 'none') == 'none':
                                        note += ' [audio only]'
                                        
                                    format_table.append(f"| {format_id} | {ext} | {resolution} | {note} |")
                                
                                st.markdown("\n".join(format_table))
                except Exception as e:
                    st.warning(f"Could not fetch format information: {str(e)}")
        
        # Set format options based on user selection
        if platform == "YouTube":
            if format_choice == "Audio Only (MP3)":
                ydl_opts.update({
                    "format": "bestaudio/best",
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }],
                })
            elif format_choice == "MP4 720p (if available)":
                if fallback_to_best:
                    ydl_opts["format"] = "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best[height<=720]/best"
                else:
                    ydl_opts["format"] = "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio"
                ydl_opts["merge_output_format"] = "mp4"
            elif format_choice == "MP4 480p (if available)":
                if fallback_to_best:
                    ydl_opts["format"] = "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=480]+bestaudio/best[height<=480]/best"
                else:
                    ydl_opts["format"] = "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=480]+bestaudio"
                ydl_opts["merge_output_format"] = "mp4"
            else:  # Best Quality Available
                ydl_opts["format"] = "bestvideo+bestaudio/best"
                ydl_opts["merge_output_format"] = "mp4"
        elif platform in ["TikTok", "Instagram", "Twitter/X", "Facebook"]:
            if format_choice == "Audio Only (MP3)":
                ydl_opts.update({
                    "format": "bestaudio/best",
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }],
                })
            else:
                # Default to best available for other platforms
                ydl_opts["format"] = "best"
        else:
            # For unknown platforms, use best available
            ydl_opts["format"] = "best"

        with st.spinner("⏳ Downloading... This might take a moment"):
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # First try with selected format
                    try:
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)
                        
                        # Handle case where filename has wrong extension due to post-processing
                        if format_choice == "Audio Only (MP3)" and not filename.endswith('.mp3'):
                            base_filename = os.path.splitext(filename)[0]
                            filename = base_filename + '.mp3'
                            
                        st.success("🎉 Download completed!")
                        st.markdown(f'<div class="download-info">'
                                    f'<strong>Saved file:</strong><br>'
                                    f'<code>{filename}</code><br><br>'
                                    f'<strong>Download location:</strong><br>'
                                    f'<code>{download_path}</code></div>', 
                                    unsafe_allow_html=True)
                    except yt_dlp.utils.DownloadError as e:
                        if "Requested format is not available" in str(e) and fallback_to_best:
                            st.warning("Requested format not available, falling back to best available quality...")
                            
                            # Fallback to best quality
                            fallback_opts = dict(ydl_opts)
                            fallback_opts["format"] = "best"
                            
                            with yt_dlp.YoutubeDL(fallback_opts) as fallback_ydl:
                                info = fallback_ydl.extract_info(url, download=True)
                                filename = fallback_ydl.prepare_filename(info)
                                
                                st.success("🎉 Download completed with best available quality!")
                                st.markdown(f'<div class="download-info">'
                                            f'<strong>Saved file:</strong><br>'
                                            f'<code>{filename}</code><br><br>'
                                            f'<strong>Download location:</strong><br>'
                                            f'<code>{download_path}</code></div>', 
                                            unsafe_allow_html=True)
                        else:
                            # Re-raise if the error is not about format availability or fallback is disabled
                            raise
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Tip: Try selecting a different format or check your URL.")

st.markdown(f"""
    <div class="footer">
        <div class="platforms">
            <span class="platform-badge {'active' if platform == 'YouTube' else ''}">YouTube</span>
            <span class="platform-badge {'active' if platform == 'TikTok' else ''}">TikTok</span>
            <span class="platform-badge {'active' if platform == 'Instagram' else ''}">Instagram</span>
            <span class="platform-badge {'active' if platform == 'Twitter/X' else ''}">Twitter/X</span>
            <span class="platform-badge {'active' if platform == 'Facebook' else ''}">Facebook</span>
        </div>
        <p style="margin:1rem 0">Made with ❤️ by IntechX</p>
        <div style="display:flex; justify-content:center; gap:1rem; margin:1rem 0;">
            <a href="#" style="color:#64748b; text-decoration:none;">📜 Terms</a>
            <a href="#" style="color:#64748b; text-decoration:none;">🔒 Privacy</a>
            <a href="#" style="color:#64748b; text-decoration:none;">📧 Contact</a>
        </div>
        <hr style="height:2rem;border:none;border-top:1px solid #e2e8f0;">
        <p style="font-size:0.8rem; color:#94a3b8;">
            © 2025 YT Grab Pro. All rights reserved.<br>
            This tool is for educational purposes only.
        </p>
    </div>
    <div class="watermark">v2.2.0</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)