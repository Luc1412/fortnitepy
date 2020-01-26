"""This example makes use of one main account and multiple sub-accounts."""

import fortnitepy
import asyncio
import functools

# sub-account credentials
credentials = {
    "email1": "password1",
    "email2": "password2",
    "email3": "password3",
    "email4": "password4",
    "email5": "password5",
    "email6": "password6",
    "email7": "password7",
    "email8": "password8",
    "email9": "password9",
    "email10": "password10",
}

class MyClient(fortnitepy.Client):
    def __init__(self):
        super().__init__(
            email="",
            password=""
        )
        self.instances = {}

    async def event_sub_ready(self, client):
        self.instances[client.user.id] = client
        print('Sub client {0.user.display_name} ready.'.format(client))

    async def event_sub_friend_request(self, request):
        print('Sub client {0.client.user.display_name} received a friend request.'.format(request))
        await request.accept()

    async def event_sub_party_member_join(self, member):
        print("{0.display_name} joined sub client {0.client.user.display_name}'s party.".format(member))            

    async def event_ready(self):
        print('Main client ready. Launching sub-accounts...')

        clients = []
        for email, password in credentials.items():
            client = fortnitepy.Client(
                email=email,
                password=password,
                default_party_member_config=(
                    functools.partial(fortnitepy.ClientPartyMember.set_outfit, 'CID_175_Athena_Commando_M_Celestial'), # galaxy skin
                )
            )

            # register events here
            client.add_event_handler('friend_request', self.event_sub_friend_request)
            client.add_event_handler('party_member_join', self.event_sub_party_member_join)

            clients.append(client)
        
        try:
            await fortnitepy.start_multiple(
                clients, 
                ready_callback=self.event_sub_ready,
                all_ready_callback=lambda: print('All sub clients ready')
            )
        except fortnitepy.AuthException:
            print('An error occured while starting sub clients. Closing gracufully.')
            await self.logout()

    async def event_logout(self):
        await fortnitepy.close_multiple(list(self.instances.values()))
        print('Successfully logged out of all sub accounts.')

    async def event_friend_request(self, request):
        await request.accept()
    
client = MyClient()
client.run()