import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="PPT Maker - Agentic AI",
    page_icon="📊",
    layout="wide"
)

# Modern, premium UI CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1c1c1e;
        background-color: #f9fafb;
    }

    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        text-align: center;
        color: #0f172a;
        margin-bottom: 0.5rem;
        letter-spacing: -0.03em;
    }

    .sub-header {
        text-align: center;
        font-size: 1.1rem;
        color: #475569;
        margin-bottom: 2.5rem;
    }

    .card {
        background: white;
        border-radius: 18px;
        padding: 2.2rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.04);
        transition: all 0.25s ease;
    }

    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.08);
    }

    .feature-card {
        background: #f8fafc;
        border-left: 4px solid #2563eb;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }

    .feature-card h4 {
        color: #0f172a;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }

    .feature-card p {
        color: #475569;
        font-size: 0.9rem;
    }

    .status-box {
        padding: 1rem 1.2rem;
        border-radius: 10px;
        margin-top: 1.2rem;
        font-weight: 500;
    }

    .success {
        background-color: #ecfdf5;
        border: 1px solid #bbf7d0;
        color: #166534;
    }

    .error {
        background-color: #fef2f2;
        border: 1px solid #fecaca;
        color: #b91c1c;
    }

    .info {
        background-color: #eff6ff;
        border: 1px solid #bfdbfe;
        color: #1d4ed8;
    }

    .btn-primary {
        background: linear-gradient(135deg, #2563eb, #1e40af);
        color: white;
        border: none;
        padding: 0.9rem 1.2rem;
        border-radius: 10px;
        font-weight: 600;
        width: 100%;
        cursor: pointer;
        transition: 0.2s ease;
        font-size: 1rem;
    }

    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
    }

    .btn-download {
        display: inline-block;
        margin-top: 0.8rem;
        padding: 0.9rem 1.2rem;
        border-radius: 10px;
        font-weight: 600;
        text-decoration: none;
        text-align: center;
        color: white;
        background: linear-gradient(135deg, #059669, #065f46);
        transition: 0.25s ease;
    }

    .btn-download:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);
    }

    .upload-area {
        border: 2px dashed #d1d5db;
        border-radius: 14px;
        padding: 2.5rem;
        text-align: center;
        background-color: #f8fafc;
        transition: all 0.3s ease;
        color: #475569;
    }

    .upload-area:hover {
        border-color: #2563eb;
        background-color: #f1f5f9;
    }

    .upload-icon {
        font-size: 2.8rem;
        color: #2563eb;
        margin-bottom: 0.8rem;
    }

    .file-info {
        background: #f1f5f9;
        padding: 1rem;
        border-radius: 10px;
        color: #1e293b;
        margin-top: 0.8rem;
    }

    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
        gap: 1.2rem;
        margin-top: 1.5rem;
    }

    .feature-item {
        background: #f8fafc;
        border-radius: 12px;
        padding: 1.5rem 1rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .feature-item:hover {
        background: #eff6ff;
        transform: translateY(-3px);
    }

    .feature-icon {
        font-size: 1.8rem;
        color: #2563eb;
        margin-bottom: 0.5rem;
    }

    .feature-title {
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 0.3rem;
    }

    .feature-desc {
        font-size: 0.9rem;
        color: #475569;
    }

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid #e2e8f0;
    }

</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">📊 PPT Maker</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Convert PDF or Text files into elegant PowerPoint presentations powered by Agentic AI</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

# Left Column — Upload + Processing
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Upload Your Document")

    uploaded_file = st.file_uploader("Choose a PDF or TXT file", type=["pdf", "txt"], label_visibility="collapsed")

    if uploaded_file is not None:
        st.markdown(f"""
        <div class="file-info">
            <strong>📁 File Uploaded:</strong> {uploaded_file.name}<br>
            <strong>Size:</strong> {uploaded_file.size:,} bytes
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="upload-area">
            <div class="upload-icon">📤</div>
            <h4>Drag & Drop your file here</h4>
            <p>or click to browse</p>
            <small>Supported formats: PDF, TXT</small>
        </div>
        """, unsafe_allow_html=True)

    if st.button("✨ Generate Presentation", type="primary", use_container_width=True):
        if uploaded_file:
            with st.spinner("Processing your document with AI..."):
                try:
                    files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    response = requests.post('http://localhost:5000/upload', files=files)
                    if response.status_code == 200:
                        result = response.json()
                        if result.get('success'):
                            st.markdown(f"""
                            <div class="status-box success">
                                ✅ Successfully created {result["slides_count"]} slides!
                            </div>
                            <a href="http://localhost:5000{result["download_path"]}" target="_blank" class="btn-download">
                                📥 Download Presentation
                            </a>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div class='status-box error'>❌ {result.get('error', 'Unknown error')}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='status-box error'>❌ Server Error: {response.json().get('error', 'Unknown')}</div>", unsafe_allow_html=True)
                except requests.exceptions.ConnectionError:
                    st.markdown("<div class='status-box error'>❌ Backend not reachable. Please start Flask server.</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f"<div class='status-box error'>❌ {str(e)}</div>", unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please upload a file first")

    st.markdown('</div>', unsafe_allow_html=True)

# Right Column — Info / Features
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("About This Tool")

    st.markdown("""
    <div class="feature-card">
        <h4>🤖 Agentic AI Processing</h4>
        <p>Uses a local Llama-3.2-3B model for semantic understanding and intelligent slide structuring.</p>
    </div>
    <div class="feature-card">
        <h4>📊 Smart Formatting</h4>
        <p>Applies modern presentation themes, clear hierarchy, and consistent slide layouts.</p>
    </div>
    <div class="feature-card">
        <h4>⚡ Lightning Fast</h4>
        <p>Optimized AI pipeline ensures quick conversions with minimal latency.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<h4 style="margin-top: 2rem;">How It Works</h4>', unsafe_allow_html=True)

    st.markdown("""
    <div class="features-grid">
        <div class="feature-item">
            <div class="feature-icon">1️⃣</div>
            <div class="feature-title">Upload</div>
            <div class="feature-desc">Choose your PDF or text file to begin</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">2️⃣</div>
            <div class="feature-title">AI Analysis</div>
            <div class="feature-desc">AI extracts, summarizes, and structures your content</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">3️⃣</div>
            <div class="feature-title">Generate</div>
            <div class="feature-desc">Slides are created with consistent, professional design</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">Agentic AI PPT Maker • Turning documents into insights ✨</div>', unsafe_allow_html=True)
