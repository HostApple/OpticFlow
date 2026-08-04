# 🕶️ OpticFlow — High Precision Vision & Hand FX Studio

> Real-time computer vision studio featuring dynamic hand selection masks, gesture-controlled effect engines, Exponential Moving Average (EMA) keypoint smoothing, and a 3D aviator sunglasses face-mesh tracking engine built with OpenCV and MediaPipe.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=for-the-badge&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hands%20%26%20FaceMesh-orange?style=for-the-badge&logo=google)

---

## ✨ Core Features

* **🎯 Sub-Pixel Keypoint Smoothing:** Implements Exponential Moving Average (EMA) filtering across landmark tracks to eliminate micro-jitter without adding frame latency.
* **🕶️ 3D Sunglasses Engine:** Procedurally renders aviator-style sunglasses with dynamic scaling, specular glare lines, rotational tracking, and smooth snap-to-eyes alignment using MediaPipe FaceMesh.
* **✋ Dynamic Selection Masking:**
  * **2-Finger Circle:** Pinch thumb and index to create an adjustable circular effect lens.
  * **4-Finger Bounding Box:** Bring both hands into frame to dynamically target rectangular regions with HUD reticles.
* **✊ Hold-to-Trigger Fist Gestures:** Integrated radial progress ring around palm centroids for seamless effect switching without touch input.
* **🎨 9 Real-Time Image Processing Filters:**
  * Invert, Thermal Map, Cyber Edges, 8-Bit Pixelate, Retro Sepia, Soft Blur, RGB Glitch, Night Vision, and 3D Sunglasses.
* **🖥️ Minimal Dark-Glass HUD:** Semi-transparent HUD overlay displaying real-time FPS, active menu state, and control guides.

---

## 🛠️ Prerequisites & Setup

### 1. Requirements
* Python 3.8 or higher
* Webcam / Video Capture Device

### 2. Install Dependencies

Install OpenCV, NumPy, and MediaPipe using `pip`:

```bash
pip install opencv-python numpy mediapipe
```
### 🎮 OpticFlow Quick Reference Sheet

#### ⌨️ Keyboard Shortcuts
* [1] - [9] : Direct Switch to Effects 1–9
* [F]       : Toggle Fullscreen Mode
* [Q]       : Quit Application

#### ✋ Hand & Facial Gestures
* Pinch (Thumb + Index Tip)   : Drag/position 3D Sunglasses or spawn a circular FX lens
* 2 Hands (4 Fingertips Out)  : Draw a rectangular HUD bounding box with corner brackets
* Hold 1 Fist (0.85 sec)      : Cycle to NEXT effect
* Hold 2 Fists (0.85 sec)     : Cycle to PREVIOUS effect
* Look into Camera            : Auto-snap 3D Sunglasses onto eyes (when face is visible)



## 🌐 Socials:
[![Discord](https://img.shields.io/badge/Discord-%237289DA.svg?logo=discord&logoColor=white)](https://discord.gg/dasadapple) [![Instagram](https://img.shields.io/badge/Instagram-%23E4405F.svg?logo=Instagram&logoColor=white)](https://instagram.com/hostapplealt) [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://youtube.com/@Hostapp7e) [![email](https://img.shields.io/badge/Email-D14836?logo=gmail&logoColor=white)](mailto:senpai.arghyo12@gmail.com) 

# 💻 Tech Stack:
![C](https://img.shields.io/badge/c-%2300599C.svg?style=for-the-badge&logo=c&logoColor=white) ![C++](https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![Windows Terminal](https://img.shields.io/badge/Windows%20Terminal-%234D4D4D.svg?style=for-the-badge&logo=windows-terminal&logoColor=white) ![PowerShell](https://img.shields.io/badge/PowerShell-%235391FE.svg?style=for-the-badge&logo=powershell&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white) ![Cloudflare](https://img.shields.io/badge/Cloudflare-F38020?style=for-the-badge&logo=Cloudflare&logoColor=white) ![.Net](https://img.shields.io/badge/.NET-5C2D91?style=for-the-badge&logo=.net&logoColor=white) ![Flutter](https://img.shields.io/badge/Flutter-%2302569B.svg?style=for-the-badge&logo=Flutter&logoColor=white) ![Express.js](https://img.shields.io/badge/express.js-%23404d59.svg?style=for-the-badge&logo=express&logoColor=%2361DAFB) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) ![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white) ![NPM](https://img.shields.io/badge/NPM-%23CB3837.svg?style=for-the-badge&logo=npm&logoColor=white) ![Next JS](https://img.shields.io/badge/Next-black?style=for-the-badge&logo=next.js&logoColor=white) ![WebGL](https://img.shields.io/badge/WebGL-990000?logo=webgl&logoColor=white&style=for-the-badge) ![Firebase](https://img.shields.io/badge/firebase-a08021?style=for-the-badge&logo=firebase&logoColor=ffcd34) ![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white) ![Adobe Illustrator](https://img.shields.io/badge/adobe%20illustrator-%23FF9A00.svg?style=for-the-badge&logo=adobe%20illustrator&logoColor=white) ![Adobe Photoshop](https://img.shields.io/badge/adobe%20photoshop-%2331A8FF.svg?style=for-the-badge&logo=adobe%20photoshop&logoColor=white) ![Adobe Lightroom](https://img.shields.io/badge/Adobe%20Lightroom-31A8FF.svg?style=for-the-badge&logo=Adobe%20Lightroom&logoColor=white) ![Adobe Premiere Pro](https://img.shields.io/badge/Adobe%20Premiere%20Pro-9999FF.svg?style=for-the-badge&logo=Adobe%20Premiere%20Pro&logoColor=white) ![Blender](https://img.shields.io/badge/blender-%23F5792A.svg?style=for-the-badge&logo=blender&logoColor=white) ![Canva](https://img.shields.io/badge/Canva-%2300C4CC.svg?style=for-the-badge&logo=Canva&logoColor=white) ![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?style=for-the-badge&logo=figma&logoColor=white)
# 📊 GitHub Stats:
![](https://github-readme-stats.shion.dev/api?username=HostApple&theme=onedark&hide_border=false&include_all_commits=false&count_private=false)<br/>
![](https://streak-stats.demolab.com/?user=HostApple&theme=onedark&hide_border=false)<br/>
![](https://github-readme-stats.shion.dev/api/top-langs/?username=HostApple&theme=onedark&hide_border=false&include_all_commits=false&count_private=false&layout=compact)

### ✍️ Random Dev Quote
![](https://quotes-github-readme.vercel.app/api?type=horizontal&theme=radical)

