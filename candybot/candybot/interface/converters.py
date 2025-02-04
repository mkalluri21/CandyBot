from emoji import UNICODE_EMOJI
from discord.ext.commands import converter
from candybot import commands
from candybot.clients import live
from candybot.interface import database
from candybot.exceptions import ArgumentError


class Context:
    def __init__(self, guild):
        self.bot = live.BOT
        self.guild = guild


async def to_user(arg, server):
    context = Context(server)
    try:
        return await converter.MemberConverter().convert(context, arg)
    except converter.BadArgument:
        raise ArgumentError


async def to_channel(arg, server):
    context = Context(server)
    try:
        return await converter.TextChannelConverter().convert(context, arg)
    except converter.BadArgument:
        raise ArgumentError


async def to_role(arg, server):
    context = Context(server)
    try:
        return await converter.RoleConverter().convert(context, arg)
    except converter.BadArgument:
        raise ArgumentError


def to_candy(arg, server):
    candys = database.get_candy(server.id)
    for candy in candys:
        if (arg == candy.name) or (arg == candy.emoji):
            return candy
    raise ArgumentError


def to_amount(arg, zero_allowed):
    try:
        arg = int(arg)
    except ValueError:
        raise ArgumentError
    if not zero_allowed and arg == 0:
        raise ArgumentError
    return arg


def to_shop_item(arg, server):
    arg = to_amount(arg, False)
    shop = database.get_shop(server.id)
    if arg > len(shop.items):
        raise ArgumentError
    return shop[arg - 1]


def to_command(arg):
    return commands.parse_command(arg, False)[0]


def to_command_name(arg):
    if arg in commands.COMMAND_NAMES:
        raise ArgumentError
    return arg


def to_percent(arg):
    arg = to_amount(arg, True)
    if not 0 <= arg <= 100:
        raise ArgumentError
    return arg


def to_prefix(arg):
    if arg not in r"\/!@#$%^&*()_-+={}[].":
        raise ArgumentError
    return arg


async def to_emoji(arg, server):
    if arg in UNICODE_EMOJI:
        return arg
    context = Context(server)
    try:
        return str(await converter.EmojiConverter().convert(context, arg))
    except converter.BadArgument:
        raise ArgumentError
