# Spotify Voice Assistant

A Python-based voice assistant that allows you to control your Spotify music experience using voice commands. This project leverages Spotify's Web API for functionalities like searching and playing songs, pausing/resuming playback, and navigating between tracks.

## Features

- **Voice Commands:**
  - Play songs by name (e.g., "Play Despacito").
  - Pause and resume playback.
  - Navigate to the next or previous track.
  - Stop Spotify Assistant with the command "Close Spotify."

- **Spotify API Integration:**
  - Search for songs by name.
  - Control playback on an active device.
  - Manage playback across devices.

## Requirements

- Python 3.7+
- A Spotify Premium account (required for playback control).
- The following Python libraries:
  - `requests`
  - `speech_recognition`
  - `pyaudio`

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/spotify-voice-assistant.git
   cd spotify-voice-assistant
