# 🚀 Space Invaders - Full HD Edition(v0.4)

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

## 🌟 What's New in v0.4?

### 🫨 Dynamic Screen Shake

Implemented a multi-intensity trauma system. The entire viewport (including UI and Stars) shakes dynamically:
**Minor:** Enemy destruction.
**Medium:** Player taking damage / Boss hits.
**Critical:** Boss destruction (full screen earthquake).

### 🎨 Visual Overhaul & Particles

**Engine Trail:** The player ship now emits real-time particle sparks that react to movement.
**Enemy Animations:** Aliens now feature a 2-frame "walking" animation (alternating every 500ms).
**Invulnerability Effects:** Added a pulsing shield and a "blink" animation for the player after taking damage.
**Cinematic Fade-In:** A smooth black-to-transparent transition at the start of each mission and level.

### 🔊 Pro Audio Management

**Dedicated Channels:** Transitioned to a multi-channel mixer (Player, Explosions, Boss, PowerUps).
**Sound Priority:** Laser fire no longer cuts off explosion sounds, ensuring a rich acoustic environment.

### 🛠️ Technical Refactoring

**Universal Offset Drawing:** All entity `draw()` methods now support a global `offset` parameter for seamless screen-shake integration.
**State Consistency:** Fixed "sprinting enemies" bug during level transitions by resetting direction and hit-edge logic.

---

## 🌟 What's New in v0.5?

The most significant update yet! **v0.5** introduces a complete gameplay loop with an in-game economy, weapon progression, and a persistent state machine.

---

## 💰 New Features: The Economy System

**Credit System:** Score is now a currency! Earn credits by destroying enemies and defeating bosses.
**The Space Station (Shop):** A new game state between missions where you can spend your hard-earned credits.
**Refined Game Loop:** Added a "Game Over" state with a clear mission failure summary and a "Re-deploy" (Restart) mechanic.

---

## 🔫 Arsenal Upgrades (Weapon Tiers)

Your ship now features a level-based weapon system:
**Level 1 (Standard):** Single central blaster.
**Level 2 (Double Shot):** Dual parallel lasers for wider coverage.
**Level 3 (Triple Spread):** A powerful 3-way spread shot to dominate the fleet.
**Hull Repairs:** Purchase additional lives at the Shop to survive longer waves.

---

## 🛠️ Technical Implementation

**Dictionary-Based Projectiles:** Refactored the bullet system to use dictionaries (`rect`, `vx`, `vy`), allowing for complex trajectories and spread patterns.
**State Machine Expansion:** Added `SHOP` and `GAME_OVER` states for a professional arcade flow.
**Persistence & Reset:** Implemented full game state resets (direction, scores, weapons) to ensure fair play on every restart.
**Boss Rewards:** Defeating a Boss now triggers a massive credit bonus and redirects the player to the Space Station.

---

## 🎮 Controls

**Mouse Move:** Pilot the ship.
**Left Click:** Fire Primary Weapon.
**Space (In Game Over):** Re-deploy to Level 1.
**ESC:** Pause/Resume.
