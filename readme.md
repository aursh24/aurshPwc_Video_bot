
# Incase you want to tweak settings and understand things more, kaam ka nahi hai waise tumhare liye, GOODNIGHT Cuties <3

# Universal Video Automation Bot

A premium, automated browser system for watching videos on learning platforms (like Moodle/Tekstac) and navigating to the next activity automatically.

---

## Features

- **Auto-Play & Speedup**: Automatically sets playback speed (default: 2.0x) and starts the video.
- **Iframe Support**: Deep-scans iframes to find video elements hidden in sub-frames.
- **Auto-Seek Nudge**: Automatically seeks to 1 second if the video is stuck at 0.0, forcing the platform to start buffering.
- **Smart Popup Detection**: Finds the "Next activity" popup using three different strategies (JS Text Search, Selenium Native Clicks, and Moodle Selectors).
- **Auto-Navigation**: Extracts the next video URL and navigates directly for a seamless experience.

---

## Requirements

Before running the bot, ensure you have **Python 3.x** and **Chrome Browser** installed.

### Python Libraries
Install the core dependencies using pip:

```bash
pip install selenium webdriver-manager
```

*Note: Your `requirements.txt` might contain many packages, but only these two are strictly required for the bot.*

---

## How to Use

1. **Set your URL**: Open `video_bot.py` and replace the `URL` variable with your course/video link:
   ```python
   URL = "https://your-platform-link-here..."
   ```

2. **Run the Bot**:
   ```bash
   python video_bot.py
   ```

3. **Sit back and Relax**:
   - The bot will open Chrome, maximize the window, and start playing.
   - When the video ends, it will detect the "Next activity" popup and navigate automatically.

---

## Configuration

You can customize these settings at the top of `video_bot.py`:
- `SPEED`: Change `2.0` to any speed you like (e.g., `1.5`, `3.0`).
- `CHECK_INTERVAL`: How often the bot checks video status (default: 2 seconds).

---

## Disclaimer
- **Video Only**: This is designed for video activities. It does NOT solve quizzes or labs.
- **UI Changes**: If the website changes its design, the bot might need minor logic updates.
- **Educational Use**: Use responsibly!

---
*Maintained by AURSH vaii & Antigravity <33*
