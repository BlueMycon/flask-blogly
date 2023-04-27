import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase

from app import app, db
from models import User,Post, DEFAULT_IMAGE_URL

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

        test_post = Post(
            title="test1_title",
            content="test1_content",
            user_id=self.user_id
        )

        db.session.add(test_post)
        db.session.commit()

        self.post_id = test_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """Test User Listing"""
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_show_home_page(self):
        """Test Home Redirect"""
        with self.client as c:
            resp = c.get("/")
            self.assertEqual(resp.status_code, 302)

    def test_show_home_page_redirect(self):
        """Test Home Redirect Follow"""
        with self.client as c:
            resp = c.get("/", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_show_add_users_form(self):
        """Test Show Add users Form"""
        with self.client as c:
            resp = c.get("/users/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("New User Form", html)
            self.assertIn("<form", html)

    def test_show_user_info(self):
        """Test User Detail Page"""
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("User Detail Page", html)
            self.assertIn("test1_first", html)
            self.assertIn(DEFAULT_IMAGE_URL, html)
            self.assertIn("test1_title", html)


class PostViewTestCase(TestCase):
    def setUp(self):
        """Create test client, add sample data."""

        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        self.user_id = test_user.id

        test_post = Post(
            title="test1_title",
            content="test1_content",
            user_id=self.user_id
        )

        db.session.add(test_post)
        db.session.commit()

        self.post_id = test_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_show_new_post_form(self):
        """Test Show New Post"""
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}/posts/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("New Post Form", html)
            self.assertIn("<form", html)

    def test_show_post_detail(self):
        """Test Post Detail Page"""
        with self.client as c:
            resp = c.get(f"/posts/{self.post_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Post Detail Page", html)
            self.assertIn("test1_title", html)

    def test_show_post_edit(self):
        """Test Show Post Edit Form"""
        with self.client as c:
            resp = c.get(f"/posts/{self.post_id}/edit")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Edit Post Form", html)
            self.assertIn("test1_title", html)

    def test_handle_post_delete(self):
        """Test Post Delete"""
        with self.client as c:
            resp = c.post(f"/posts/{self.post_id}/delete")
            self.assertEqual(resp.status_code, 302)

    def test_handle_post_delete_follow(self):
        """Test Post Delete Redirect Follow"""
        with self.client as c:
            resp = c.post(f"/posts/{self.post_id}/delete",
                          follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("User Detail Page",html)
            self.assertNotIn("test1_title", html)
