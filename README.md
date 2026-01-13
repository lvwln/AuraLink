# AuraLink: Spatial Gesture OS
![GITFINAL](GITFINAL.gif)

AuraLink is a computer vision-based Human-Computer Interaction (HCI) tool that allows users to control their OS through hand gestures. Built for the future of touchless interfaces.

## Features
- **Air Mouse:** Smooth cursor control using the Index Finger.
- **Pinch-to-Click:** Natural "pinch" gesture for mouse clicks using Euclidean distance.
- **The Boss Key:** Instant "Hide All Windows" (Win+D) when 4 fingers are detected.
- **Signal Smoothing:** Implemented a moving average algorithm to eliminate cursor jitter.

##  Tech Stack
- **Language:** Python 3.10+
- **Vision:** MediaPipe (Hand Landmark Detection)
- **Control:** PyAutoGUI (System-level API)
- **Math:** NumPy / Math (Gesture geometry)

##  Installation
1. Clone the repo: `git clone https://github.com/YOUR_USERNAME/AuraLink.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python air_mouse.py`

##  How it Works
AuraLink maps the 21 hand landmarks provided by MediaPipe to screen coordinates. I implemented a `smooth_factor` to interpolate between the previous and current coordinates, ensuring the user experience feels fluid rather than shaky.
