from django.test import TestCase
from django.urls import reverse

from .models import Post


class PostModelTests(TestCase):
    def test_str_returns_title(self):
        post = Post.objects.create(title='Hello', content='World')
        self.assertEqual(str(post), 'Hello')

    def test_get_absolute_url(self):
        post = Post.objects.create(title='Hello', content='World')
        self.assertEqual(post.get_absolute_url(), f'/post/{post.pk}')


class HomeViewTests(TestCase):
    def test_renders_empty_state(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')
        self.assertContains(response, 'No posts yet')

    def test_lists_posts(self):
        Post.objects.create(title='First', content='one')
        Post.objects.create(title='Second', content='two')
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'First')
        self.assertContains(response, 'Second')
        self.assertEqual(len(response.context['posts']), 2)

    def test_shows_new_post_button(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, reverse('post-create'))


class PostCreateViewTests(TestCase):
    def test_get_renders_form(self):
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')

    def test_post_creates_post_and_redirects_home(self):
        response = self.client.post(
            reverse('post-create'),
            {'title': 'New', 'content': 'Body'},
        )
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.get()
        self.assertEqual(post.title, 'New')
        self.assertEqual(post.content, 'Body')

    def test_invalid_post_does_not_create(self):
        response = self.client.post(reverse('post-create'), {'title': '', 'content': ''})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.exists())


class PostUpdateViewTests(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title='Old', content='Old body')

    def test_get_renders_form_with_instance(self):
        response = self.client.get(reverse('post-update', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')
        self.assertContains(response, 'Old')

    def test_post_updates_post_and_redirects_home(self):
        response = self.client.post(
            reverse('post-update', args=[self.post.pk]),
            {'title': 'New title', 'content': 'New body'},
        )
        self.assertRedirects(response, reverse('home'))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'New title')
        self.assertEqual(self.post.content, 'New body')

    def test_get_missing_post_returns_404(self):
        response = self.client.get(reverse('post-update', args=[9999]))
        self.assertEqual(response.status_code, 404)


class PostDeleteViewTests(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title='Doomed', content='bye')

    def test_get_renders_confirm_page(self):
        response = self.client.get(reverse('post-delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_delete.html')
        self.assertContains(response, 'Doomed')

    def test_post_deletes_and_redirects_home(self):
        response = self.client.post(reverse('post-delete', args=[self.post.pk]))
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_get_missing_post_returns_404(self):
        response = self.client.get(reverse('post-delete', args=[9999]))
        self.assertEqual(response.status_code, 404)
