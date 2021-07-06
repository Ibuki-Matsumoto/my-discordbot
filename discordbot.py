import random
import discord
# from giphy_client.rest import ApiException
from dice import diceroll
import io
import aiohttp
import gif_url
from discord.ext import commands
# import giphy_client
# from randomcl import generate_random_color
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from dispander.module import dispand
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import asyncio

client = commands.Bot(case_insensitive=True, command_prefix="/", help_command=None)
ModeFlag = 0
# giphy_token = 'ZRGiPa4b9SXwskqMCVxDCDXh3mrMFDLG'
# api_instance = giphy_client.DefaultApi()
TEXT_CHANNEL = 764217463210508290
token = os.environ['DISCORD_BOT_TOKEN']
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

jsonf = 'discord-spreadsheet-293417-2ba5cc544223.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)

gc = gspread.authorize(credentials)

SPREADSHEET_KEY = "172XF6qN0JFYmrcJkF9Eb99YBnCHHchpM3Zpg1jVarxo"

worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1


@client.event
async def on_ready():
    """起動時に通知してくれる処理"""
    await client.change_presence(activity=discord.Activity(name="サーバー内", type=discord.ActivityType.watching))
    ch_name = "テストチャンネル"
    for channel in client.get_all_channels():
        if channel.name == ch_name:
            await channel.send("再起動完了！")
    print('ログインしました')
    print(client.user.name)  # ボットの名前
    print(client.user.id)  # ボットのID
    print(discord.__version__)  # discord.pyのバージョン
    print('------')


# async def search_gifs(query):
#     try:
#         response = api_instance.gifs_search_get(giphy_token, query, limit=3, rating='g')
#         lst = list(response.data)
#         gif = random.choices(lst)
#
#         return gif[0].url
#
#     except ApiException as e:
#         return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e


@client.event
async def on_message(message, ):
    """メッセージを処理"""
    global result, judge, ModeFlag
    if message.author.bot:  # ボットのメッセージを回避
        return

    if ModeFlag == 1:
        kensaku = message.content
        ModeFlag = 0
        count = 0

        for url in search(kensaku, lang="jp", num=5):
            await message.channel.send(url)
            count += 1
            if count == 5:
                break

    await dispand(message)

    if message.content == "湯婆婆":
        await message.channel.send("契約書だよ。そこに名前を書きな。")
        await asyncio.sleep(1)
        await message.channel.send(f"(あなたは契約書に`{message.author.display_name}`と書き込んだ。)")

        name = message.author.display_name
        await asyncio.sleep(2)
        await message.channel.send(f"フン。`{name}`というのかい。贅沢な名だねぇ。")

        new_name = random.choice(name.replace(" ", ""))
        await asyncio.sleep(4)
        await message.channel.send(f"今からお前の名前は`{new_name}`だ。"
                                       f"いいかい、`{new_name}`だよ。分かったら返事をするんだ、`{new_name}`!!")

        await message.author.edit(nick=new_name)

        await message.channel.send(f"(あなたのニックネームは`{new_name}`になった。)")

    if "🥺" in message.content:
        if message.author.id == 716276943313567806:
            import_value = int(worksheet.acell("A1").value)
            export_value = import_value+1
            worksheet.update_cell(1, 1, export_value)
            await message.add_reaction("🥺")
        else:
            await message.add_reaction("💩")

    if message.content == "/pien":
        vl = int(worksheet.acell("A1").value)
        await message.channel.send("るるさんのぴえん力は" + str(vl) + "だよ！")

    if message.content == "/google":
        ModeFlag = 1
        await message.channel.send("検索ワードを入力してください")

    if message.content.startswith("おやす"):
        await message.channel.send("ゆっくり休んでね")

    if message.content.startswith("おは"):
        await message.channel.send("おはようございます！")

    if message.content.startswith("おつ"):
        await message.channel.send("お疲れ様です")

    if message.content == "/おみくじ":
        # Embedを使ったメッセージ送信 と ランダムで要素を選択
        embed = discord.Embed(title="おみくじ", description=f"{message.author.mention}さんの今日の運勢を占いますね！",
                              color=0x2ECC69)
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.add_field(name="[運勢] ", value=random.choice(('大吉', "中吉", '吉', "末吉", "小吉", '凶', '大凶')), inline=False)
        await message.channel.send(embed=embed)

    if message.content == "/dm":
        # ダイレクトメッセージ送信
        dm = await message.author.create_dm()
        await dm.send(f"{message.author.mention}さん、どうしましたか？")

    # if message.content == "/info":
    #     embed = discord.Embed(title="しいなくんの概要", description=f"{client.user.mention}と戯れるbot", color=0x7fffff)
    #     embed.set_thumbnail(url=client.user.avatar_url)
    #     embed.add_field(name="開発者", value="なるせ", inline=True)
    #     embed.add_field(name="Twitter", value="@kamiki_toraba https://twitter.com/kamiki_toraba", inline=True)
    #     await message.channel.send(embed=embed)

    # if message.content == "/help":
    #     embed = discord.Embed(title="コマンドの説明", color=0xff8ec6)
    #     embed.set_author(name="しいなくん's profile", icon_url=client.user.avatar_url)
    #     embed.set_thumbnail(url=client.user.avatar_url)
    #     embed.add_field(name="/おみくじ", value="大吉、吉、凶、大凶の４つで占います", inline=False)
    #     embed.add_field(name="/ダイレクトメッセージ", value="botをDMに召喚出来ます。メモ代わりにでもどうぞ", inline=False)
    #     embed.add_field(name="/じゃんけん", value="！じゃんけんと入力後、botのメッセージの後ぐー、ちょき、ぱー"
    #                                          "を選ぶ事でじゃんけんが出来ます！", inline=False)
    #     embed.add_field(name="/info", value="botやbotの作者についての情報が出ます", inline=False)
    #     embed.add_field(name="/help", value="この情報出せたなら分かってるだろ？", inline=False)
    #     embed.add_field(name="/猫", value="猫のgifをランダムで返信するよ", inline=False)
    #     embed.add_field(name="/dice XdY", value="XとYに数字を代入することでダイスを振ることができるよ！", inline=False)
    #     embed.add_field(name="/google", value="コマンド入力後に検索ワードを入力するとgoogle検索結果が５つ表示されます", inline=False)
    #     embed.add_field(name="/gif (任意の検索ワード)", value="検索ワードを指定する事でgiphyからランダムにgifを検索して表示します", inline=False)
    #
    #     await message.channel.send(embed=embed)

    if message.content.startswith("/dice "):
        say = message.content

        order = say.strip("/dice")
        cnt, mx = list(map(int, order.split("d")))
        dice = diceroll(cnt, mx)
        await message.channel.send(dice[cnt])
        del dice[cnt]

        await message.channel.send(dice)

    if message.content == "//cleanup":
        if message.author.guild_permissions.administrator:
            await message.channel.purge()
            await message.channel.send("塵と化せ！")
        else:
            await message.channel.send("なんだお前！？")

    if message.content == "/じゃんけん":
        await message.channel.send("最初はぐー、じゃんけん")

        shinajk = random.choice(("ぐー", "ちょき", "ぱー"))
        draw = "引き分けかぁ..."
        wn = "君の勝ちだよ！負けちゃった..."
        lst = random.choice(("僕の勝ち！お前ざっこｗｗｗｗｗｗｗｗｗｗｗｗやめたら？人生",
                             "僕の勝ちだね、また挑戦してきて"))

        def jankencheck(m):
            return (m.author == message.author) and (m.content in ['ぐー', 'ちょき', 'ぱー'])

        reply = await client.wait_for("message", check=jankencheck)
        if reply.content == shinajk:
            judge = draw
        else:
            if reply.content == "ぐー":
                if shinajk == "ちょき":
                    judge = wn
                else:
                    judge = lst

            elif reply.content == "ちょき":
                if shinajk == "ぱー":
                    judge = wn
                else:
                    judge = lst

            else:
                if shinajk == "ぐー":
                    judge = wn
                else:
                    judge = lst

        await message.channel.send(judge)

    # elif message.content == "/猫":

        # async with aiohttp.ClientSession() as session:
        #     async with session.get(gif_url.get_random_photo()) as resp:
        #         if resp.status != 200:
        #             return await message.channel.send('Could not download file...')
        #         data = io.BytesIO(await resp.read())
        #         await message.channel.send(file=discord.File(data, "cool_image.gif"))

    if message.content == "/roles":
        print(message.guild.roles)

    await client.process_commands(message)

    text_chat = client.get_channel(TEXT_CHANNEL)
    if message.channel.type == discord.ChannelType.private:
        aaa = str(message.content)
        bbb = str(message.author.id)
        member_mention = "<@" + bbb + ">"
        await text_chat.send(f"{member_mention}" + aaa)


@client.command()
async def ping(ctx):
    await ctx.send('pong')


@client.command()
async def neko(ctx):
    await ctx.send("にゃーん")


@client.command(name="足し算")
async def add(ctx, a: int, b: int):
    await ctx.send(a + b)


@client.command(name="引き算")
async def minus(ctx, a: int, b: int):
    await ctx.send(a - b)


@client.command(name="掛け算")
async def kakezan(ctx, a: int, b: int):
    await ctx.send(a * b)


@client.command(name="割り算")
async def warizan(ctx, a: int, b: int):
    await ctx.send(a / b)


@client.command(name="余り")
async def amari(ctx, a: int, b: int):
    await ctx.send(a % b)


@client.command(name="gif")
async def random_gif(ctx, *args):
    gif = await search_gifs(args)
    await ctx.send('Gif URL : ' + gif)


@client.command()
async def member(ctx):
    arg = ctx.guild.member_count
    text = f'このサーバーには{arg}人のメンバーがいます'
    await ctx.send(text)


@client.command()
async def news(ctx):
    url = "https://news.google.com/?hl=ja&gl=JP&ceid=JP:ja"

    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')

    rs = random.randint(1, 5)

    await ctx.send(soup.find_all("h3")[rs].getText())


client.run(token)
