# ⚙️ GLOBAL AUTOMATION HUB CONFIGURATION MATRIX
import os

class SystemConfig:
    # 🔗 WEBSITE DOMAIN LINKING CONFIG
    # Jab aap free website link karenge, toh is niche wale URL ko change kar dena.
    # Abhi ke liye yeh default Vercel aur local machine ko automatic track karega.
    LIVE_WEBSITE_URL = "https://vercel.app"
    LOCAL_FLASK_PORT = 5000
    
    # 🎛️ HARDWARE PERFORMANCE SETTINGS (UNTOUCHED DEFAULT)
    WEBGPU_ACCELERATION = True
    CACHE_PURGE_INTERVAL_HOURS = 24
    
    # 🎭 RELEVANT THEME CLUSTERS REGISTRY (STRICT EXCLUSIVE MATRIX)
    ALLOWED_THEME_CLUSTERS = [
        "flower_mehndi",
        "bridal_layouts",
        "fight_argue",
        "love_romance",
        "funny_comedy",
        "horror_suspense"
    ]

# Ye line check karegi ke configuration file sahi load ho rahi hai
print(f"[CONFIG ENG] System parameters loaded for: {SystemConfig.LIVE_WEBSITE_URL}")
