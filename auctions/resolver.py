import threading
import time
from django.contrib.auth.models import User
from django.utils import timezone

from core.emails import notify_winner, notify_bidders
from .models import Auction


class ResolveThread(threading.Thread):

    def run(self):

        # FOR TESTING PURPOSES
        # author = 'Linus'
        # title = 'Ford Focus'
        # description = 'A car of brand Ford and model Focus'
        # deadline = timezone.now() + timedelta(minutes=2)
        # min_price = 10.50
        # leader = User.objects.get(username='TestUser')
        #
        # auction = Auction.objects.create(
        #     author=author,
        #     title=title,
        #     description=description,
        #     deadline=deadline,
        #     min_price=min_price,
        #     leader=leader.username,
        # )
        # auction.save()

        while True:
            # Update every second
            time.sleep(1)
            # print(timezone.now())
            active_auction_list = Auction.objects.filter(state='Active')

            for auction in active_auction_list:

                if auction.deadline <= timezone.now():

                    if auction.leader != '':

                        winner = User.objects.get(username=auction.leader)
                        auction.state = 'Adjudicated'
                        auction.save()

                        # Notify winner and bidders
                        notify_winner(winner, auction)
                        notify_bidders(winner, auction)
                    else:
                        # There were no bidders
                        pass

