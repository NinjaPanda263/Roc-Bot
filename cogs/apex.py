#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
import discord.ext.commands
import sqlite3
from discord.ext import commands
from discord.utils import get
from rapidfuzz import process, fuzz
from res.common import sanitise_input, ship_search, customemoji, get_em_colour
from res.data import ShipData, ApexLister, ApexData
import re


def sql_apex_num_obj():
    # connect to the sqlite database
    conn = sqlite3.connect('rocbot.sqlite')
    # return a class sqlite3.row object which requires a tuple input query
    conn.row_factory = sqlite3.Row
    # make an sqlite connection object
    c = conn.cursor()
    # using a defined view s_info find the ship
    c.execute('''
select
    ship.id as id,
    apex_tier.name as rank,
    apex_ships.apex_num as apex_num
from apex_ships inner join ship on apex_ships.ship_name = ship.id
inner join apexs on apex_ships.apex_id = apexs.id
inner join apex_tier on apex_ships.apex_tier = apex_tier.id;
    ''')
    # return the ship object including the required elemnts
    a_obj = c.fetchall()
    # close the databse connection
    conn.close()
    # return the sqlite3.cursor object
    return a_obj

def sql_ship_obj():
    conn = sqlite3.connect('rocbot.sqlite')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('select * from s_info')
    s_obj = c.fetchall()
    conn.close()
    return s_obj

def sql_rank_obj():
    conn = sqlite3.connect('rocbot.sqlite')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('select name from apex_tier')
    r_obj = c.fetchall()
    conn.close()
    return r_obj

def get_ship_image(ship_name):
    urlgit =    "https://raw.githubusercontent.com/ewong18/Roc-Bot/master/ships/"
    return f"{urlgit}ship_{ship_name}.png"


class ApexCog(commands.Cog, name="Apex Commands"):
    """ApexCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='apex')
    @commands.guild_only()
    # arg1 is everthing after the command
    async def apex(self, ctx, *, arg1):
        rank_list = [i[0] for i in sql_rank_obj()]
        tokens = arg1.split(" ")
        s_obj = sql_ship_obj()
        ##If no apex rank is given, show list of available apexes
        if len(tokens)==1:
            s_obj = ShipData(ctx, arg1).s_obj
            apex_embed_title = f"Apexes for {s_obj['name']}"
            colour = get_em_colour(s_obj['affinity'])
            embed = discord.Embed(
                title=apex_embed_title,
                description = ApexLister(ctx, arg1).embed_list,
                color=colour)
            #embed.set_image(url=get_ship_image(s_obj['number']))
            await ctx.send(embed=embed)
        ##If rank is given
        else:
            a_obj = sql_apex_num_obj()
            s_obj = ShipData(ctx, arg1).s_obj
            apex_tier = process.extractOne(arg1, rank_list)[0]
            apex_obj = ApexData(ctx, s_obj['name'],apex_tier)
            colour = get_em_colour(s_obj['affinity'])
            embed = discord.Embed(title=apex_obj.embed_title, color=colour, description=apex_obj.embed_desc)
            for i in a_obj:
                if i['id'] == s_obj['number'] and i['rank'] == apex_tier:
                    embed.set_thumbnail(url=get_ship_image(f"{i['id']}_apex_{i['apex_num']}"))
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ApexCog(bot))

