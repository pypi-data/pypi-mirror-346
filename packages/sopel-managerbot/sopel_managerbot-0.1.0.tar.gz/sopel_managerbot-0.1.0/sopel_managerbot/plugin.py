"""sopel-managerbot

"Manager-like" response plugins for Sopel IRC bots.

(Note: Does not manage other Sopel instances.)

Copyright (c) 2025 dgw, technobabbl.es

Licensed under the Eiffel Forum License 2.
"""
from __future__ import annotations

from sopel import plugin

from .util.no import get_no
from .util.yes import get_yes


PREFIX = plugin.output_prefix('[manager] ')


@PREFIX
@plugin.command('approve', 'yes')
def approve_request(bot, trigger):
    try:
        bot.say(get_yes())
    except RuntimeError as e:
        bot.reply(str(e))


@PREFIX
@plugin.command('deny', 'no')
def deny_request(bot, trigger):
    try:
        bot.say(get_no())
    except RuntimeError as e:
        bot.reply(str(e))
