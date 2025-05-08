from enum import IntEnum

import disnake

class Color(IntEnum):
    GRAY = 0x2F3136
    GREEN = 0x00FF00
    RED = 0xFF0000
    BLUE = 0x0000FF

# Basic saved class elements. You can customize everything for yourself.
class ClientInfo(IntEnum):
    DEVELOPER_ID = ...
    BOT_GUILD_ID = ...

default_error = (disnake.Forbidden, disnake.HTTPException)

full_errors = (disnake.Forbidden, disnake.HTTPException, disnake.NotFound, disnake.InvalidData, TypeError, ValueError)


# In this file, you specify values that will be used in many places and in order not to constantly change them manually, you write them here once and then use them as much as you want. It works great when you need to specify any ID.