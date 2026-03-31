# MUSICPEDIA (Viberr)

A full-stack Django web application that lets you upload, store, manage, and play your music and videos from the cloud. Access your media from any device, anywhere in the world.

## Features

- **User Authentication** — Register, log in, and log out with Django's built-in auth system
- **Album Management** — Create albums with artist name, title, genre, and cover art (PNG/JPG/JPEG)
- **Song Uploads** — Upload audio files (WAV, MP3, OGG) to albums
- **Video Uploads** — Upload video files (MP4, MKV, AVI, MOV, WMV, FLV, WEBM) with optional thumbnails
- **In-Browser Playback** — Play songs and watch videos directly in the browser
- **Favorites** — Star/unstar albums, songs, and videos (toggled via AJAX)
- **Search** — Search across albums (by title/artist), songs (by title), and videos (by title/artist)
- **Delete** — Remove individual songs, videos, or entire albums (cascade deletes all songs)
- **Django Admin** — Manage Albums, Songs, and Videos through the built-in admin panel

## Tech Stack

| Layer      | Technology               |
|------------|--------------------------|
| Backend    | Django 1.9.4 (Python)    |
| Database   | SQLite                   |
| Frontend   | Bootstrap 3, jQuery      |
| Templating | Django Template Language  |

## Project Structure

```
├── manage.py                          # Django management entry point
├── requirements.txt                   # Python dependencies
├── db.sqlite3                         # SQLite database
├── media/                             # User-uploaded files (album art, audio, video)
│
├── website/                           # Project-level configuration
│   ├── settings.py                    # Django settings (DB, apps, middleware)
│   ├── urls.py                        # Root URL configuration
│   ├── wsgi.py                        # WSGI entry point for deployment
│   └── __init__.py
│
└── music/                             # Main Django app
    ├── models.py                      # Album, Song & Video data models
    ├── views.py                       # View functions
    ├── urls.py                        # App-level URL routing
    ├── forms.py                       # ModelForms (AlbumForm, SongForm, VideoForm, UserForm)
    ├── admin.py                       # Admin site registration
    ├── apps.py                        # App configuration
    ├── tests.py                       # Test file
    ├── migrations/                    # Database migrations
    ├── templates/music/               # HTML templates
    │   ├── base.html                  # Base template (navbar, layout)
    │   ├── base_visitor.html          # Base template for visitors
    │   ├── index.html                 # Album listing / home page
    │   ├── detail.html                # Album detail with song list
    │   ├── create_album.html          # Album creation form
    │   ├── create_song.html           # Song upload form
    │   ├── songs.html                 # All songs listing
    │   ├── videos.html                # All videos listing
    │   ├── create_video.html          # Video upload form
    │   ├── video_detail.html          # Video detail / player page
    │   ├── login.html                 # Login page
    │   ├── register.html              # Registration page
    │   └── form_template.html         # Reusable form template
    └── static/music/                  # Static assets
        ├── style.css                  # Custom styles
        ├── js/main.js                 # jQuery AJAX for favorites
        └── images/background.png      # Background image
```

## Data Models

### Album

| Field         | Type                    | Description                      |
|---------------|-------------------------|----------------------------------|
| `user`        | ForeignKey → User       | The user who owns the album      |
| `artist`      | CharField (max 250)     | Artist name                      |
| `album_title` | CharField (max 500)     | Album title                      |
| `genre`       | CharField (max 100)     | Genre                            |
| `album_logo`  | FileField               | Album cover image                |
| `is_favorite` | BooleanField            | Whether the album is favorited   |

### Song

| Field        | Type                    | Description                       |
|--------------|-------------------------|-----------------------------------|
| `album`      | ForeignKey → Album      | The album this song belongs to    |
| `song_title` | CharField (max 250)     | Song title                        |
| `audio_file` | FileField               | Uploaded audio file               |
| `is_favorite`| BooleanField            | Whether the song is favorited     |

### Video

| Field        | Type                    | Description                       |
|--------------|-------------------------|-----------------------------------|
| `user`       | ForeignKey → User       | The user who owns the video       |
| `title`      | CharField (max 250)     | Video title                       |
| `artist`     | CharField (max 250)     | Artist name                       |
| `genre`      | CharField (max 100)     | Genre                             |
| `video_file` | FileField               | Uploaded video file               |
| `thumbnail`  | FileField (optional)    | Video thumbnail image             |
| `is_favorite`| BooleanField            | Whether the video is favorited    |

## URL Routes

| URL Pattern                                  | View             | Description                              |
|----------------------------------------------|------------------|------------------------------------------|
| `/` or `/music/`                             | `index`          | Home page — lists user's albums          |
| `/register/`                                 | `register`       | User registration                        |
| `/login_user/`                               | `login_user`     | User login                               |
| `/logout_user/`                              | `logout_user`    | User logout                              |
| `/create_album/`                             | `create_album`   | Create a new album                       |
| `/<album_id>/`                               | `detail`         | Album detail page with song list         |
| `/<album_id>/create_song/`                   | `create_song`    | Upload a song to an album                |
| `/<album_id>/delete_album/`                  | `delete_album`   | Delete an album                          |
| `/<album_id>/delete_song/<song_id>/`         | `delete_song`    | Delete a song                            |
| `/<song_id>/favorite/`                       | `favorite`       | Toggle song favorite (JSON response)     |
| `/<album_id>/favorite_album/`                | `favorite_album` | Toggle album favorite (JSON response)    |
| `/songs/<filter_by>/`                        | `songs`          | List songs, filter by `favorites`        |
| `/create_video/`                             | `create_video`   | Upload a new video                       |
| `/video/<video_id>/`                         | `video_detail`   | Video detail / player page               |
| `/video/<video_id>/favorite/`                | `favorite_video` | Toggle video favorite (JSON response)    |
| `/video/<video_id>/delete/`                  | `delete_video`   | Delete a video                           |
| `/videos/<filter_by>/`                       | `videos`         | List videos, filter by `favorites`       |
| `/admin/`                                    | Django Admin     | Admin panel                              |

## Getting Started

### Prerequisites

- Python 2.7+ or Python 3.x
- pip

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Create a superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

4. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

5. **Open in browser:**
   - App: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## User Flow

1. **Register** — Create an account at `/register/`
2. **Log in** — Sign in with your credentials
3. **Create an Album** — Add album details and upload a cover image
4. **Add Songs** — Navigate into an album and upload audio files
5. **Upload Videos** — Click "Add Video" to upload a video with an optional thumbnail
6. **Play Music** — Click the Play button next to any song
7. **Watch Videos** — Click on a video to watch it with the built-in player
8. **Favorite** — Click the star icon on albums, songs, or videos to mark them as favorites
9. **Search** — Use the search bar to find albums, songs, or videos
10. **Manage** — Delete songs, videos, or albums as needed

## Other Files in This Repository

- **`multipleinheritence.py`** — Python practice script demonstrating multiple inheritance with `Calculation1`, `Calculation2`, and `Derived` classes
- **`practice2.py`** — Python practice script demonstrating multi-level inheritance with `Animal` → `Dog` → `Puppy` class hierarchy
