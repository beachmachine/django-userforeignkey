import datetime
from django.contrib.auth.models import AnonymousUser, User

try:
    # Django 1.10 and above
    from django.urls import reverse
except:
    # Django 1.8 and 1.9
    from django.core.urlresolvers import reverse

from django.utils import timezone
from django.test import TestCase
from django.test import Client


from .models import Poll, Choice, ActualVote


class GeneralAuthTest(TestCase):
    def test_auth_fail(self):
        c = Client()
        response = c.post(reverse('login'), {'username': 'thisuserdoes', 'password': 'notexist'})
        self.assertEqual(response.status_code, 200) # should fail
        self.assertContains(response, "Your username and password didn't match. Please try again")


class PollMethodTests(TestCase):
    def test_was_published_recently_with_future_poll(self):
        """
        was_published_recently() should return False for polls whose
        pub_date is in the future
        """
        future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_poll.was_published_recently(), False)

    def test_was_published_recently_with_old_poll(self):
        """
        was_published_recently() should return False for polls whose pub_date
        is older than 1 day
        """
        old_poll = Poll(pub_date=timezone.now() - datetime.timedelta(days=30))
        self.assertEqual(old_poll.was_published_recently(), False)

    def test_was_published_recently_with_recent_poll(self):
        """
        was_published_recently() should return True for polls whose pub_date
        is within the last day
        """
        recent_poll = Poll(pub_date=timezone.now() - datetime.timedelta(hours=1))
        self.assertEqual(recent_poll.was_published_recently(), True)


def create_poll(question, days=0, choices=[]):
    """
    Creates a poll with the given `question` published the given number of
    `days` offset to now (negative for polls published in the past,
    positive for polls that have yet to be published).
    """
    p =  Poll.objects.create(
        question=question,
        pub_date=timezone.now() + datetime.timedelta(days=days)
    )

    if len(choices) > 0:
        for choice in choices:
            c = Choice.objects.create(
                poll=p,
                choice_text=choice,
            )

    return p


class PollViewTests(TestCase):
    def test_index_view_with_no_polls(self):
        """
        If no polls exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_index_view_with_a_past_poll(self):
        """
        Polls with a pub_date in the past should be displayed on the index page.
        """
        create_poll(question="Past poll.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: Past poll.>']
        )

    def test_index_view_with_a_future_poll(self):
        """
        Polls with a pub_date in the future should not be displayed on the
        index page.
        """
        create_poll(question="Future poll.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.", status_code=200)
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_index_view_with_future_poll_and_past_poll(self):
        """
        Even if both past and future polls exist, only past polls should be
        displayed.
        """
        create_poll(question="Past poll.", days=-30)
        create_poll(question="Future poll.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: Past poll.>']
        )

    def test_index_view_with_two_past_polls(self):
        """
        The polls index page may display multiple polls.
        """
        create_poll(question="Past poll 1.", days=-30)
        create_poll(question="Past poll 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: Past poll 2.>', '<Poll: Past poll 1.>']
        )


class PollIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_poll(self):
        """
        The detail view of a poll with a pub_date in the future should
        return a 404 not found.
        """
        future_poll = create_poll(question='Future poll.', days=5)
        response = self.client.get(reverse('polls:detail', args=(future_poll.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_poll(self):
        """
        The detail view of a poll with a pub_date in the past should display
        the poll's question.
        """
        past_poll = create_poll(question='Past Poll.', days=-5)
        response = self.client.get(reverse('polls:detail', args=(past_poll.id,)))
        self.assertContains(response, past_poll.question, status_code=200)


class PollVoteTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='johndoe', email='johndoe@mail.com', password='top_secret')

        self.user2 = User.objects.create_user(
            username='homersimpson', email='h.simpson@springfield.com', password='top_secret')

        self.user3 = User.objects.create_user(
            username='mrburns', email='mrburns@aol.com', password='top_secret')

    def test_vote_poll_anonymous(self):
        """
        Should not be allowed to vote when not logged in
        """
        poll = create_poll(question='What is the question?', choices=['I dont know', 'Whatever', '42'])

        choices = Choice.objects.filter(poll=poll)

        site = reverse('polls:vote', args=(poll.id, ))

        response = self.client.get(site, {'choice': choices[0].id}, )

        self.assertEqual(response.status_code, 302)
        self.assertTrue("/results/" not in response.url)
        self.assertTrue("/login/" in response.url)

    def test_vote_poll_authed(self):
        """
            Should be allowed to vote, and vote should count
        """
        poll = create_poll(question='What is the question?', choices=['I dont know', 'Whatever', '42'])

        choices = Choice.objects.filter(poll=poll)

        site = reverse('polls:vote', args=(poll.id,))

        c = Client()
        response = c.post(reverse("login"), {'username': 'johndoe', 'password': 'top_secret'})
        self.assertEqual(response.status_code, 302) # should work
        self.assertTrue("/accounts/profile/" in response.url)

        response = c.post(site, {'choice': choices[0].id}, )
        self.assertEqual(response.status_code, 302) # should work
        self.assertTrue("/results/" in response.url)

        c = Client()
        response = c.post(reverse("login"), {'username': 'homersimpson', 'password': 'top_secret'})
        self.assertEqual(response.status_code, 302)  # should work
        self.assertTrue("/accounts/profile/" in response.url)


        response = c.post(site, {'choice': choices[1].id}, )
        self.assertEqual(response.status_code, 302)  # should work
        self.assertTrue("/results/" in response.url)

        c = Client()
        response = c.post(reverse("login"), {'username': 'mrburns', 'password': 'top_secret'})
        self.assertEqual(response.status_code, 302)  # should work
        self.assertTrue("/accounts/profile/" in response.url)

        response = c.post(site, {'choice': choices[0].id}, )
        self.assertEqual(response.status_code, 302)  # should work
        self.assertTrue("/results/" in response.url)

        # there should now be 2 votes for choices[0] and 1 for choices[1]
        self.assertEqual(choices[0].votes, 2)
        self.assertEqual(choices[1].votes, 1)
        self.assertEqual(choices[2].votes, 0)

        # check if ActualVotes is there
        votes = ActualVote.objects.filter(poll=poll)
        self.assertTrue(len(votes) == 3)
        # check if the user, which is set by UserForeignKey, is populated properly
        self.assertTrue(votes[0].user == self.user1)
        self.assertTrue(votes[1].user == self.user2)
        self.assertTrue(votes[2].user == self.user3)


    def test_vote_poll_multivote(self):
        """
            Should be allowed to vote, and vote should count
        """
        poll = create_poll(question='What is the question?', choices=['I dont know', 'Whatever', '42'])

        choices = Choice.objects.filter(poll=poll)

        site = reverse('polls:vote', args=(poll.id,))

        c = Client()
        response = c.post(reverse("login"), {'username': 'johndoe', 'password': 'top_secret'})
        self.assertEqual(response.status_code, 302)  # should work
        self.assertTrue("/accounts/profile/" in response.url)

        response = c.post(site, {'choice': choices[0].id}, )
        self.assertEqual(response.status_code, 302)  # should work
        self.assertTrue("/results/" in response.url)

        # vote again
        response = c.post(site, {'choice': choices[1].id}, )
        self.assertContains(response, "You already voted", status_code=200)

        # vote again
        response = c.post(site, {'choice': choices[2].id}, )
        self.assertContains(response, "You already voted", status_code=200)

        # vote again
        response = c.post(site, {'choice': choices[0].id}, )
        self.assertContains(response, "You already voted", status_code=200)

        # check if ActualVotes is there (should only be 1 vote)
        votes = ActualVote.objects.filter(poll=poll)
        self.assertTrue(len(votes) == 1)
