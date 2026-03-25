# 🚀 Space Invaders - Full HD Edition (v0.1)

A modern take on the classic Space Invaders, built with **Pygame**. Optimized for high-resolution displays (up to 2.5K) with smooth mouse controls and dynamic audio.

## ✨ Features

- **High Resolution Support:** Auto-scaling and DPI aware.
- **Mouse Controls:** Fluid movement and click-to-shoot mechanics.
- **Dynamic Audio:** Laser SFX, explosions, and background music.
- **Persistent High Score:** Saves your best performance to a local file.
- **Lives System:** 3 lives to survive the alien onslaught.

## 🚀 What's New in v0.2?

We have transitioned from a basic prototype to a fully-featured arcade experience. This update focuses on **Game Juice**—the small details that make a game satisfying to play.

### ✨ Key Features

 **Dynamic Particle System:** Enemies now explode into colorful debris when destroyed, providing satisfying visual feedback.
 **Power-Up System:**
 **Blue Shield🛡️:** Grants 5 seconds of total invulnerability.
 **Red Heart ❤️:** Adds an extra life to your ship.
 **State Management:** Smooth transitions between **Main Menu**, **In-Game**, **Level Up**, and **Game Over** screens.
 **Progressive Difficulty:** Enemies move faster and shoot more frequently as you advance through levels.
 **High Score System:** Your best performance is automatically saved and loaded from `highscore.txt`.

---

## 🕹️ Controls

| Key / Action | Function |
| **Mouse Move** | Navigate your spaceship |
| **Left Click** | Fire Laser |
| **Enter** | Start Game (Menu) |
| **'R' Key** | Restart Game (Game Over screen) |
| **'M' Key** | Return to Main Menu (Game Over screen) |
| **ESC** | Quit to Menu / Exit |

---

## 🛠️ Technical Highlights

**DPI Awareness:** Uses `ctypes` to ensure the game looks crisp on high-resolution monitors without Windows scaling blur.
**Parallax Background:** A multi-layered star system creates a sense of depth and speed.
**Collision Logic:** Implemented a robust "Invulnerability Frame" (i-frame) system to prevent instant deaths from multiple hits.

---
