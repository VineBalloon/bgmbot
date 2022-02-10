#!/user/bin/env python
import io
import os
# from asyncio import sleep
from typing import List, Optional

from nextcord import FFmpegOpusAudio, Interaction, Intents, SelectOption, VoiceChannel, VoiceClient, VoiceState
from nextcord.ext import commands
from nextcord.ui import View, Select, select
    

if __name__ == "__main__":
    TOKKEY = "TOKEN"
    token = os.getenv(TOKKEY)
    if token is None:
        raise Exception(f"Couldn't find a bot token in the environment variable ${TOKKEY}; set it using `export TOKEN=(your token)`")

    intents = Intents().none()
    intents.guilds = True
    intents.voice_states = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    # get bgms
    bgms = os.listdir("bgms")
    bgms.sort()

    # construct options
    opts = []
    for bgm in bgms:
        # yeet extension
        name = bgm.split(".")[0]

        # Make PascalCase Great Again
        name = " ".join([x.capitalize() for x in name.split("_")])
        opts.append(SelectOption(label=name, value=bgm))

    # keep a global here teehee
    vclient: Optional[VoiceClient] = None

    # define our selector view
    class BGMSelector(View):
        # define selector callback
        @select(placeholder="Pick a BGM :3", options=opts)
        async def callback(self, selector: Select, interaction: Interaction):
            try:
                # get value user has chosen
                chosen = selector.values[0]
                print(f"User {interaction.user.id} has chosen {chosen}")

                # locate the user
                vstate: Optional[VoiceState] = interaction.user.voice
                if vstate is None:
                    await interaction.response.send_message(f"You're not in voice, baka!")
                    return

                # location acquired
                vchannel: Optional[VoiceChannel] = vstate.channel
                if vchannel is None:
                    await interaction.response.send_message(f"Something's wrong, I can't find you! :confused:")
                    return

                # join the channel
                global vclient
                if vclient is None:
                    vclient = await vchannel.connect()

                if vclient.is_playing():
                    vclient.stop()

                # it HAS to exist, right?
                source = FFmpegOpusAudio(f"./bgms/{chosen}", before_options="-stream_loop -1")

                # let it rip!
                vclient.play(source)

            except Exception as e:
                print(e)
                await interaction.response.send_message(f"Tell my developer that I called them a big idiot")

    @bot.slash_command(name="play", description="Brings up a UI for you to select the currently playing BGM")
    async def play(interaction: Interaction):
        await interaction.response.send_message(content=":thinking: + :arrow_down: = :musical_note:", view=BGMSelector(timeout=600), ephemeral=True)

    @bot.slash_command(name="stop", description="Stops the music")
    async def stop(interaction: Interaction):
        await interaction.response.send_message(content="There is no stopping this train, make me /leave")

    @bot.slash_command(name="leave", description="Leaves the voice channel")
    async def leave(interaction: Interaction):
        global vclient
        if vclient is None:
            await interaction.response.send_message(content="Not even connected, dummy!")
            return

        await vclient.disconnect()
        vclient = None

        await interaction.response.send_message(content="Hmph!")

    bot.run(token)
