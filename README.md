# Spotify API Project

## Introduction
This project showcases two different applications interacting with the Spotify API. One retrieves user-specific data via OAuth authentication, while the other uses the Client Credentials Flow to access public data. Both applications require a Spotify Developer account to obtain the necessary client ID and client secret, which should be stored in a `.env` file.

## Project 1: Spotify User Data
Located in the `/Spotify_User_Data` directory, this application uses OAuth to access user-specific Spotify data. The project was developed using CSS, Html, Python - Flask, with Spotipy to manage API interactions. Key features include:

### Features:
- Display user's last played track.
- Show user's top tracks and artists over different time periods.
- Save playlists to the user’s account.
- Email the user's top tracks in a table format.

### Local Subnet Setup:
The app was configured to run within my local subnet, allowing others connected to it to use the app. Since it’s a demo, there was no need to host it on a public server.

[Watch the demo on YouTube](https://www.youtube.com/watch?v=6bzcADyrt8w).

## Project 2: Spotify Without User Data
In the `/Spotify` directory, this app interacts with Spotify's API using Client Credentials Flow, which does not require user authentication. The process of manually obtaining an access token is done via API calls, which is used to fetch public data like track and artist details.

### Features:
- Obtain an access token manually via the Spotify API.
- Retrieve track details, album information, and artist data.
- Get top tracks by an artist or music recommendations based on a track.

## How to Run
1. Clone the repository.
2. Navigate to the respective directories (`/Spotify_User_Data` or `/Spotify`).
3. Set up your `.env` file with your client ID and client secret.
4. For the Spotify User Data project, run the Flask application within your local subnet for demonstration purposes.

## Requirements
- Python 3.x
- Flask
- Spotipy
- Requests

## Installation
You can install the required packages using pip:

```bash
pip install Flask Spotipy requests
