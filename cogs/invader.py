#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
import inspect
import discord.ext.commands
from discord.ext import commands
from discord.utils import get
from res.invaders import invader_type

class InvaderCog(commands.Cog, name="Invader Commands"):
    """InvaderCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=['invaders'])
    @commands.guild_only()
    async def invader(self, ctx, *, arg1=None):
        sc = inspect.stack()[0][3]
        if ctx.invoked_subcommand is None and arg1 is None:
            await ctx.send('Invalid invader command passed.')
        else:
            await ctx.send(embed=invader_type(ctx, sc, arg1).i_embed)

    #@invader.command()
    #async def turrets(self, ctx, *, arg1=None):
    #    sc = inspect.stack()[0][3]
    #    await ctx.send(embed=invader_type(ctx, sc, arg1).i_embed)

    @invader.command()
    async def unprotected(self, ctx, *, arg1=None):
        sc = inspect.stack()[0][3]
        await ctx.send(embed=invader_type(ctx, sc, arg1).i_embed)

    @invader.command(aliases=['armoured','armor','armour'])
    async def armored(self, ctx, *, arg1=None):
        sc = inspect.stack()[0][3]
        await ctx.send(embed=invader_type(ctx, sc, arg1).i_embed)

    @invader.command(aliases=['shield'])
    async def shielded(self, ctx, *, arg1=None):
        sc = inspect.stack()[0][3]
        await ctx.send(embed=invader_type(ctx, sc, arg1).i_embed)

    @invader.command()
    async def split(self, ctx, *, arg1=None):
        sc = inspect.stack()[0][3]
        await ctx.send(embed=invader_type(ctx, sc, arg1).i_embed)

def setup(bot):
    bot.add_cog(InvaderCog(bot))
