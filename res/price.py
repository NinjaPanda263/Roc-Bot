#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import discord.ext.commands
from discord.ext import commands
from discord.utils import get

class Prices():
    def __init__(self, bot_self, sub_command, arg1):
        self.sc = sub_command
        self.bot = bot_self
        self.type = arg1
        self.p_obj = self.get_p_obj()

    def get_p_obj(self):
        conn = sqlite3.connect('rocbot.sqlite')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        query = 'SELECT * FROM '
        if self.sc == 'weapon':
            query = query + 'price_weapon'
        elif self.sc == 'aura':
            query = query + 'price_aura'
        elif self.sc == 'zen':
            query = query + 'price_zen'
        return c.execute(query).fetchall()

    def p_embed(self):
        desc = ''
        for row in self.p_obj:
            desc = desc + str(row['Level']) + '\t' + row['Cost'] + '\n'
        embed = discord.Embed(title='Level' + '\t' + 'Cost', description=desc)
        return embed
