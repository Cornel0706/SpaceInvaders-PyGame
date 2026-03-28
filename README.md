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

## 🚀 What's New in v0.3?

### 👹 The Mothership (Boss Entity)

**Dynamic Scaling:** The Boss is significantly larger and has a dedicated health system.
**Combat Phases (Enrage Mode):**
Above 50% HP: The Boss moves at standard speed and fires single shots.
Below 50% HP: The Boss enters **Enrage Mode**, increasing its speed by 50% and switching to a **Triple Shot Spread** pattern.
**Smart Projectiles:** Enemies and the Boss now use a dictionary-based projectile system, allowing for diagonal movement.

### 🛠️ Technical Improvements

**Advanced Collision Logic:** Implemented a `hit_something` flag to optimize bullet interactions and prevent insta-death.
**Multi-Point Explosions:** Defeating the Boss triggers a chain reaction o  explosions across its frame.
**State-Based Level Management:** A new level manager that uses the spawn_level_content() operator to toggle between standard waves and Boss encounters.

## 🌟 What's New in v0.3.5?

**State Machine System:** The game logic is now divided into clear states: `MENU`, `GAME`, `PAUSE`, and `LEVEL_UP`.
**Pause Menu:** Press `ESC` during gameplay to freeze the action and choose between *Resume* or *Back to Menu*.
**Asset Management:** All resources (images, sounds, fonts) are organized in the `/assets` folder and loaded centrally via `assets.py`.
**High DPI Support:** Native fix for high-resolution monitors (tested on 2.5K), ensuring crisp visuals without blur.
**Modular Architecture:** Moved from a single-file script to a clean, class-based structure (`entities.py`, `utils.py`, `assets.py`).
