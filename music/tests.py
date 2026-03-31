from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Album, Song, Video
from .forms import VideoForm


class VideoModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.video = Video.objects.create(
            user=self.user,
            title='Test Video',
            artist='Test Artist',
            genre='Pop',
            video_file=SimpleUploadedFile('test.mp4', b'file_content', content_type='video/mp4'),
        )

    def test_video_creation(self):
        self.assertEqual(self.video.title, 'Test Video')
        self.assertEqual(self.video.artist, 'Test Artist')
        self.assertEqual(self.video.genre, 'Pop')
        self.assertEqual(self.video.user, self.user)

    def test_video_str(self):
        self.assertEqual(str(self.video), 'Test Video - Test Artist')

    def test_video_is_favorite_default(self):
        self.assertFalse(self.video.is_favorite)

    def test_video_thumbnail_optional(self):
        self.assertFalse(self.video.thumbnail)

    def test_video_with_thumbnail(self):
        video = Video.objects.create(
            user=self.user,
            title='Video With Thumb',
            artist='Artist',
            genre='Rock',
            video_file=SimpleUploadedFile('vid.mp4', b'data', content_type='video/mp4'),
            thumbnail=SimpleUploadedFile('thumb.png', b'img', content_type='image/png'),
        )
        self.assertTrue(video.thumbnail)


class VideoFormTest(TestCase):

    def test_valid_form(self):
        video_file = SimpleUploadedFile('test.mp4', b'file_content', content_type='video/mp4')
        form = VideoForm(
            data={'title': 'My Video', 'artist': 'Artist', 'genre': 'Rock'},
            files={'video_file': video_file},
        )
        self.assertTrue(form.is_valid())

    def test_missing_title(self):
        video_file = SimpleUploadedFile('test.mp4', b'file_content', content_type='video/mp4')
        form = VideoForm(
            data={'artist': 'Artist', 'genre': 'Rock'},
            files={'video_file': video_file},
        )
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_missing_video_file(self):
        form = VideoForm(
            data={'title': 'My Video', 'artist': 'Artist', 'genre': 'Rock'},
        )
        self.assertFalse(form.is_valid())
        self.assertIn('video_file', form.errors)

    def test_missing_artist(self):
        video_file = SimpleUploadedFile('test.mp4', b'file_content', content_type='video/mp4')
        form = VideoForm(
            data={'title': 'My Video', 'genre': 'Rock'},
            files={'video_file': video_file},
        )
        self.assertFalse(form.is_valid())
        self.assertIn('artist', form.errors)

    def test_missing_genre(self):
        video_file = SimpleUploadedFile('test.mp4', b'file_content', content_type='video/mp4')
        form = VideoForm(
            data={'title': 'My Video', 'artist': 'Artist'},
            files={'video_file': video_file},
        )
        self.assertFalse(form.is_valid())
        self.assertIn('genre', form.errors)

    def test_form_fields(self):
        form = VideoForm()
        self.assertEqual(
            list(form.fields.keys()),
            ['title', 'artist', 'genre', 'video_file', 'thumbnail'],
        )


class VideoViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.video = Video.objects.create(
            user=self.user,
            title='Existing Video',
            artist='Existing Artist',
            genre='Jazz',
            video_file=SimpleUploadedFile('existing.mp4', b'data', content_type='video/mp4'),
        )

    def test_videos_list_requires_login(self):
        response = self.client.get('/music/videos/all/')
        self.assertTemplateUsed(response, 'music/login.html')

    def test_videos_list_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/music/videos/all/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music/videos.html')
        self.assertIn('videos', response.context)

    def test_videos_list_shows_user_videos(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/music/videos/all/')
        self.assertContains(response, 'Existing Video')

    def test_videos_favorites_filter(self):
        self.client.login(username='testuser', password='testpass123')
        # No favorites yet
        response = self.client.get('/music/videos/favorites/')
        self.assertEqual(response.status_code, 200)
        videos_in_context = response.context['videos']
        self.assertEqual(len(videos_in_context), 0)

        # Mark as favorite
        self.video.is_favorite = True
        self.video.save()
        response = self.client.get('/music/videos/favorites/')
        videos_in_context = response.context['videos']
        self.assertEqual(len(videos_in_context), 1)

    def test_video_detail_requires_login(self):
        response = self.client.get('/music/video/{}/'.format(self.video.pk))
        self.assertTemplateUsed(response, 'music/login.html')

    def test_video_detail_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/music/video/{}/'.format(self.video.pk))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music/video_detail.html')
        self.assertEqual(response.context['video'], self.video)

    def test_video_detail_not_found(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/music/video/99999/')
        self.assertEqual(response.status_code, 404)

    def test_create_video_requires_login(self):
        response = self.client.get('/music/create_video/')
        self.assertTemplateUsed(response, 'music/login.html')

    def test_create_video_get(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/music/create_video/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music/create_video.html')
        self.assertIn('form', response.context)

    def test_create_video_post_valid(self):
        self.client.login(username='testuser', password='testpass123')
        video_file = SimpleUploadedFile('new.mp4', b'video_data', content_type='video/mp4')
        response = self.client.post('/music/create_video/', {
            'title': 'New Video',
            'artist': 'New Artist',
            'genre': 'Rock',
            'video_file': video_file,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music/video_detail.html')
        self.assertEqual(Video.objects.count(), 2)
        new_video = Video.objects.get(title='New Video')
        self.assertEqual(new_video.artist, 'New Artist')
        self.assertEqual(new_video.user, self.user)

    def test_create_video_invalid_file_type(self):
        self.client.login(username='testuser', password='testpass123')
        bad_file = SimpleUploadedFile('bad.txt', b'not_video', content_type='text/plain')
        response = self.client.post('/music/create_video/', {
            'title': 'Bad Video',
            'artist': 'Artist',
            'genre': 'Pop',
            'video_file': bad_file,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music/create_video.html')
        self.assertContains(response, 'Video file must be MP4, MKV, AVI, MOV, WMV, FLV, or WEBM')
        self.assertEqual(Video.objects.count(), 1)  # only the setUp video

    def test_create_video_invalid_thumbnail_type(self):
        self.client.login(username='testuser', password='testpass123')
        video_file = SimpleUploadedFile('good.mp4', b'video_data', content_type='video/mp4')
        bad_thumb = SimpleUploadedFile('thumb.gif', b'gif_data', content_type='image/gif')
        response = self.client.post('/music/create_video/', {
            'title': 'Video Bad Thumb',
            'artist': 'Artist',
            'genre': 'Pop',
            'video_file': video_file,
            'thumbnail': bad_thumb,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music/create_video.html')
        self.assertContains(response, 'Thumbnail must be PNG, JPG, or JPEG')
        self.assertEqual(Video.objects.count(), 1)

    def test_create_video_with_valid_thumbnail(self):
        self.client.login(username='testuser', password='testpass123')
        video_file = SimpleUploadedFile('vid.mp4', b'video_data', content_type='video/mp4')
        thumb = SimpleUploadedFile('thumb.png', b'img_data', content_type='image/png')
        response = self.client.post('/music/create_video/', {
            'title': 'Video With Thumb',
            'artist': 'Artist',
            'genre': 'Pop',
            'video_file': video_file,
            'thumbnail': thumb,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music/video_detail.html')
        new_video = Video.objects.get(title='Video With Thumb')
        self.assertTrue(new_video.thumbnail)

    def test_delete_video(self):
        self.client.login(username='testuser', password='testpass123')
        video_id = self.video.pk
        response = self.client.get('/music/video/{}/delete/'.format(video_id))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Video.objects.filter(pk=video_id).exists())

    def test_favorite_video_toggle(self):
        self.client.login(username='testuser', password='testpass123')
        self.assertFalse(self.video.is_favorite)

        # Toggle to favorite
        response = self.client.get('/music/video/{}/favorite/'.format(self.video.pk))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), {'success': True})
        self.video.refresh_from_db()
        self.assertTrue(self.video.is_favorite)

        # Toggle back to unfavorite
        response = self.client.get('/music/video/{}/favorite/'.format(self.video.pk))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), {'success': True})
        self.video.refresh_from_db()
        self.assertFalse(self.video.is_favorite)

    def test_favorite_video_not_found(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/music/video/99999/favorite/')
        self.assertEqual(response.status_code, 404)

    def test_index_search_includes_videos(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/music/?q=Existing')
        self.assertEqual(response.status_code, 200)
        self.assertIn('videos', response.context)
        video_results = response.context['videos']
        self.assertEqual(len(video_results), 1)
        self.assertEqual(video_results[0].title, 'Existing Video')

    def test_index_search_no_match(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/music/?q=NonexistentThing')
        self.assertEqual(response.status_code, 200)
        self.assertIn('videos', response.context)
        self.assertEqual(len(response.context['videos']), 0)

    def test_other_user_videos_not_shown(self):
        other_user = User.objects.create_user(
            username='otheruser', password='otherpass'
        )
        Video.objects.create(
            user=other_user,
            title='Other Video',
            artist='Other Artist',
            genre='Classical',
            video_file=SimpleUploadedFile('other.mp4', b'data', content_type='video/mp4'),
        )
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/music/videos/all/')
        videos_in_context = list(response.context['videos'])
        self.assertEqual(len(videos_in_context), 1)
        self.assertEqual(videos_in_context[0].title, 'Existing Video')
