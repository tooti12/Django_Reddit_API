#!/usr/bin/env python3
from django.core.management.base import BaseCommand, CommandError
from reddit.api import Reddit
# NOTE: Django custom mgmt commands:
# https://docs.djangoproject.com/en/4.0/howto/custom-management-commands/


class Command(BaseCommand):
    help = 'Latest posts from Reddit'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('subreddit',type=str, help='The subreddit name your are looking for')
    
    def handle(self, *args, **options):
        subreddit = options.get('subreddit')
        reddit = Reddit(subreddit=subreddit)
        reddit.print_new_post()
        reddit.print_updated_vote_count()
        reddit.print_posts_not_in_top()
        # self.stdout.write(f'{url_int=}')
        self.stdout.write('Done')
