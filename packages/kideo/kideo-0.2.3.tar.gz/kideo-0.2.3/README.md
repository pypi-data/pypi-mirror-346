# kideo

**kideo** is a Python package for compressing videos using a fast Rust backend.  
It converts input videos to **WebM format** with:

- 📼 Resolution: 240p  
- 🎞️ Frame rate: 15 fps  
- 🎯 CRF (quality): 28  
- 📦 Format: WebM (VP9 + Opus)

The package **bundles FFmpeg** internally, so users don’t need to install it themselves.

---

## 🚀 Installation

```bash
pip install kideo

# use it like this in python

from kideo import compress_video

compress_video("input.mp4", "output.webm")

