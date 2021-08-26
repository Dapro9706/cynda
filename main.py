import random
import math
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands,tasks
import pypokedex
from utilities import *
from numpy import array
from tttFuncs import log, best_move, show_board, is_done, play, find_all_empty
from c4funcs import isDone, playc4, show_boardc4, check_possibile
from PIL import Image
import keep_alive
from datetime import datetime, timedelta

load_dotenv ('a.env')
TOKEN = os.getenv ('DISCORD_TOKEN')

i=discord.Intents().default()
i.members = True
bot = commands.Bot (command_prefix='-', intents = i)
bot.remove_command("help")
ary = []
permit = True

isAlive = False
secondary_help = {
  "TICTACTOE":Help("TicTacToe","Begins Game","-tictactoe <opponent>"),
  "CONNECT4":Help("Connect 4","Begins Game","-connect4 <opponent>"),
  "TICTACTOEAI":Help("TicTacToe AI","Begins tic tac toe game with AI","-tictactoeAI>"),
  "ARRAY":Help("Array","Classified","----"),
  "HP":Help("HP", "Gets pokemon's Hidden Power from ivs", "-hp <ivs>"),
  "HC":Help("HC", "Gets pokemon's Competetive info", "-hc <name> <lvl>"),
  "STAT":Help("Stat","Gets Pokemon's Stats by Name","-stat <name>"),
  "RANDMON":Help("Rand Mon","Gets a Random Mon","-randMon"),
  "RANDABI":Help("Rand Abi","Gets a Random Ability","-randAbi"),
  "INSULT":Help("Insult","ONLY to be used in NSFW channels","-insult <name>"),
  "SEARCH":Help("Search","Google search","-search <query>"),
  "IMGSEARCH":Help("Img Search","Google Images search","-imgSearch <query>"),
  "SPRITE":Help("Sprite","Gets pokemon sprite","-sprite <name> <shiny/default>"),
  "COMPARE":Help("Compare","Compares Mons at Stats","-compare <names>"),
  "PSEARCH":Help("PSearch","Pokemon search","-psearch <name>"),
  "BILLBOARD":Help("Billboard","Current TOP 10 Songs","-billboard"),
  "RULE":Help("Rules","Rules","-rule"),
  "JOKE":Help("Joke","Random Pun","-joke"),
  "DETECT":Help("Detect","Only for Mods","-detect"),
  "GREET":Help("Greet","Greeting","-greet <name>")
}


@bot.event
async def on_message(message):
    if message.content.upper () in ["BACK ME UP CYNDA", "SUPPORT ME CYNDA"]:
        await message.channel.send (random.choice ([
            f"I absolutely agree with {message.author.mention}",
            f"I do think {message.author.mention} is right"
        ]))
    elif message.content.upper () in ["WHAT DO U THINK CYNDA", "WHAT DO YOU THINK CYNDA"]:
        await message.channel.send (random.choice ([
            "Um I'm not sure really"
        ]))
    elif "CYNDA" in message.content.upper ().split (" ") and listComp (["EPIC", "GREAT", "AWESOME", "RAD"],
                                                                       message.content.upper ().split (
                                                                           " ")) and "IS" in message.content.upper ().split (
        " ") and "NOT" not in message.content.upper ().split (" "):
        await message.channel.send (random.choice ([
            "Ooh Thats really high praise from you",
            "Oh my i haven't blushed this much since chikorita said she likes my new hairstyle",
            "Well i am hot stuff"
        ]))
    await bot.process_commands (message)

@bot.command (name="help", help="Shows this message")
async def help(ctx,*args):
  if len(args)==0:
    e=discord.Embed(title="help")
    for i in bot.commands:
      if i not in ["catch"]:
        e.add_field(name=i,value=f"`{i.help}`")
    await ctx.send(embed=e)
  else:
    await ctx.send(embed=secondary_help[args[0].upper()].brr())

@bot.command (name="tictactoe", help="Begins Game")
async def init(ctx, o):
    players = {
        "X": "",
        "O": ""
    }
    smartCounter = 0
    turn = ["X", "O"]
    global isAlive
    if not isAlive:
        otherPlayer = o
        await ctx.send (f"{otherPlayer} do u accept {ctx.message.author.mention}'s challenge(y/n)")

        def ch(msg):
            return msg.content in ['y', 'n', "yes", "no"]

        msg = await bot.wait_for ("message", check=ch)
        if msg.content in ['y', "yes"]:
            bpic = Image.open ("data/board.png")
            players['X'] = ctx.author.mention
            players['O'] = o
            board = array ([
                [" ", " ", " "],
                [" ", " ", " "],
                [" ", " ", " "]
            ])
            isAlive = True
            await log (ctx, "Toss Heads X play first Tails O Play first")
            ch = random.choice (["Heads", "Tails"])
            turn = ["X", "O"] if ch == "Heads" else ["O", "X"]
            await log (ctx, f"its a {ch}")

            await show_board (ctx, board, bpic)
            while not is_done (board)[0]:

                if not players[turn[smartCounter]] == "Computer":
                    lis = [f"{num}\N{COMBINING ENCLOSING KEYCAP}" for num in range (1, 10)]
                    msg = await ctx.send (f"Play Ur Move {players[turn[smartCounter]]}>")
                    for i in find_all_empty (board):
                        await msg.add_reaction (lis[i])

                    def check(reaction, user):
                        return user.mention[2:] in [players[turn[smartCounter]][2:], players[turn[smartCounter]][3:]]

                    reaction, user = await bot.wait_for ('reaction_add', check=check)

                    a = int (str (reaction)[0]) - 1
                else:
                    await log (ctx, "my Turn")
                    a = best_move (board)
                play (board, turn[smartCounter], (a // 3, a % 3))
                smartCounter = (smartCounter + 1) % 2
                await show_board (ctx, board, bpic)

            await show_board (ctx, board, bpic)
            # evaluating final Position
            if not is_done (board)[1] is None:
                await log (ctx, f"\n\nWinner is {players[is_done (board)[1]]}")
            else:
                await log (ctx, "\n\nCall a Tie")

    else:
        await ctx.send ("> A Game is Already Running")
    isAlive = False


@bot.command (name="array", help="Dev meet ur reckoning")
async def arr(ctx, *args):
    global ary, permit

    if args[0] == "add":
        addition = ""
        for i in range (1, len (args)):
            addition += args[i] + " "
        ary.append (addition)
        await ctx.send (f"Added {addition}")
    elif args[0] == "clear":
        ary = []
        await ctx.send ("Cleared")
    elif args[0] == "toggle":
        permit = not permit
        await ctx.send ("Toggling permits")
    elif args[0] == "do":
        if permit:
            for i in ary:
                await ih (ctx, i)
    elif args[0] == "show":
        tes = ""
        try:
            tes = ary[int (args[1]) - 1]
        except (IndexError, TypeError):
            for i in range (len (ary)):
                tes += f"{i + 1}. {ary[i]}\n"
        await ctx.send (embed=discord.Embed (title="Array", description=tes))
    elif args[0] == "remove":
        try:
            ary.pop (int (args[1]) - 1)
            await ctx.send (f"Removed {args[1] + 1} element")
        finally:
            pass
    elif args[0]=="help":
      await ctx.send (embed=discord.Embed (title="Next Gen Command",description="**__Commands__**\n__add <stuff>__ - adds stuff to array\n__clear__ - clears array\n__do__ - does imgSearch for array\n__HIDDEN COMMAND xD__ - Turns (on/off)\n__show__ - Displays Array\n__remove <index>__ - removes element in index"))


@bot.command (name="connect4", help="Begins Game")
async def initc4(ctx, o):
    players = {
        "X": "Computer",
        "O": "Human"
    }
    smartCounter = 0
    turn = ["X", "O"]
    global isAlive
    if not isAlive:
        otherPlayer = o
        await ctx.send (f"{otherPlayer} do u accept {ctx.author.mention}'s challenge(y/n)")

        def ch(msg):
            return msg.content in ['y', 'n', "yes", "no"]

        msg = await bot.wait_for ("message", check=ch)
        if msg.content in ['y', "yes"]:
            board = array ([[" " for i in range (7)] for i in range (6)])
            turn = ["X", "O"]
            smartCounter = 0

            players['X'] = ctx.author.mention
            players['O'] = o

            await show_boardc4 (ctx, board)

            while not isDone (board)[0]:
                try:
                    lis = [f"{num}\N{COMBINING ENCLOSING KEYCAP}" for num in range (1, 8)]
                    msg = await ctx.send (f"column to play {players[turn[smartCounter]]}:")
                    for i in check_possibile (board):
                        await msg.add_reaction (lis[i])

                    def check(reaction, user):
                        return user.mention[2:] in [players[turn[smartCounter]][3:], players[turn[smartCounter]][2:]]

                    reaction, user = await bot.wait_for ('reaction_add', check=check)

                    a = int (str (reaction)[0]) - 1
                    playc4 (board, turn[smartCounter], a)
                    smartCounter += 1
                    smartCounter %= 2
                    await show_boardc4 (ctx, board)
                except RuntimeError:
                    await log (ctx, "Invalid Column(Already Filled)")

            await show_boardc4 (ctx, board)
            if isDone (board)[1] is not None:
                await log (ctx, f"{players[isDone (board)[1]]} is the winner")
            else:
                await log (ctx, "Call a tie")
    else:
        await ctx.send ("> A Game is Already Running")
    isAlive = False


@bot.command (name="tictactoeAI", help="Begins Game u v/s MAH AI")
async def initAI(ctx):
    bpic = Image.open ("data/board.png")
    smartCounter = 0
    turn = ["X", "O"]
    players = {
        "X": "Computer",
        "O": "Human"
    }
    board = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]
    players['O'] = ctx.message.author.mention
    board = array (board)

    await log (ctx, "Toss Heads Computer play first Tails U Play first")
    ch = random.choice (["Heads", "Tails"])
    turn = ["X", "O"] if ch == "Heads" else ["O", "X"]
    await log (ctx, f"it is {ch}")

    while not is_done (board)[0]:
        await show_board (ctx, board, bpic)
        if not players[turn[smartCounter]] == "Computer":
            lis = [f"{num}\N{COMBINING ENCLOSING KEYCAP}" for num in range (1, 10)]
            msg = await ctx.send (f"Play Ur Move {players[turn[smartCounter]]}>")
            for i in find_all_empty (board):
                await msg.add_reaction (lis[i])

            def check(reaction, user):
                return user.mention[2:] in [players[turn[smartCounter]][2:], players[turn[smartCounter]][3:]]

            reaction, user = await bot.wait_for ('reaction_add', check=check)

            a = int (str (reaction)[0]) - 1
        else:
            await log (ctx, "my Turn")
            a = best_move (board)
        play (board, turn[smartCounter], (a // 3, a % 3))
        smartCounter = (smartCounter + 1) % 2

    await show_board (ctx, board, bpic)
    # evaluating final Position
    if not is_done (board)[1] is None:
        await log (ctx, f"\n\nWinner is {players[is_done (board)[1]]}")
    else:
        await log (ctx, "\n\nCall a Tie")


@bot.event
async def on_ready():
    print('ready')

@bot.command (name='hp', help="Hidden Power Calculator")
async def hp(ctx, *ivs):
    end_str = ""
    if not len (ivs) == 6:
        await ctx.send ("6 iv value required")
        return 0
    for i in range (6):
        ivs[i] = int (ivs[i])
        if ivs[i] % 2 == 0:
            end_str += "E"
        elif ivs[i] % 2 == 1:
            end_str += "O"
    a = ""
    if end_str == "OEEOEO" or end_str == "EEEOEO" or end_str == "OOOOEE" or end_str == "EOOOEE" or end_str == "OEOOEE":
        a = "Bug"
    if end_str == "OOOOOO":
        a = "Dark"
    if end_str == "EOOOOO" or end_str == "OEOOOO" or end_str == "EEOOOO" or end_str == "OOEOOO":
        a = "Dragon"
    if end_str == "EOEOOE" or end_str == "OEEOOE" or end_str == "EEEOOE" or end_str == "OOOEOO":
        a = "Electric"
    if end_str == "EEOEEE" or end_str == "OOEEEE" or end_str == "EOEEEE" or end_str == "OEEEEE" or end_str == "EEEEEE":
        a = "Fighting"
    if end_str == "OEOEOE" or end_str == "EEOEOE" or end_str == "OOEEOE" or end_str == "EOEEOE":
        a = "Fire"
    if end_str == "EEEEEO" or end_str == "OOOEEE" or end_str == "EOOEEE" or end_str == "OEOEEE":
        a = "Flying"
    if end_str == "OEOOEO" or end_str == "EEOOEO" or end_str == "OOEOEO" or end_str == "EOEOEO":
        a = "Ghost"
    if end_str == "EOOEOO" or end_str == "OEOEOO" or end_str == "EEOEOO" or end_str == "OOEEOO" or end_str == "EOEEOO":
        a = "Grass"
    if end_str == "EEEOEE" or end_str == "OOOEEO" or end_str == "EOOEEO" or end_str == "OEOEEO":
        a = "Ground"
    if end_str == "EOEOOO" or end_str == "OEEOOO" or end_str == "EEEOOO" or end_str == "OOOOOE":
        a = "Ice"
    if end_str == "EEOEEO" or end_str == "OOEEEO" or end_str == "EOEEEO" or end_str == "OEEEEO":
        a = "Poison"
    if end_str == "EOOOOE" or end_str == "OEOOOE" or end_str == "EEOOOE" or end_str == "OOEOOE":
        a = "Psychic"
    if end_str == "EEOOEE" or end_str == "OOEOEE" or end_str == "EOEOEE" or end_str == "OEEOEE":
        a = "Rock"
    if end_str == "OEEEOE" or end_str == "EEEEOE" or end_str == "OOOOEO" or end_str == "EOOOEO":
        a = "Steel"
    if end_str == "OEEEOO" or end_str == "EEEEOO" or end_str == "OOOEOE" or end_str == "EOOEOE":
        a = "Water"
    await ctx.send (a)


@bot.command (name='stat', help="Read Stats")
async def stat(ctx, name):
    try:
        mon = pypokedex.get (name=name)
        await ctx.send (mon.sprites.front["default"])
        name = mon.name
        st = f"**{name}**:\n" \
             f"**Type**:{mon.types}\n" \
             f"**Stats**: {print_stats ([mon.base_stats.hp, mon.base_stats.attack, mon.base_stats.defense, mon.base_stats.sp_atk, mon.base_stats.sp_def, mon.base_stats.speed])}" \
             f", Total:{mon.base_stats.hp + mon.base_stats.attack + mon.base_stats.defense + mon.base_stats.sp_atk + mon.base_stats.sp_def + mon.base_stats.speed} \n"
        await ctx.send (st)
    except:
        await ctx.send ("Cant find " + name)


@bot.command (name='hc', help="For Hyper Competitive")
async def hc(ctx, name, lvl):
    st = ""
    try:
        lvl = int (lvl)
        mon = pypokedex.get (name=name)
        name = mon.name
        Types = mon.types
        stats = [mon.base_stats.hp, mon.base_stats.attack, mon.base_stats.defense,
                 mon.base_stats.sp_atk, mon.base_stats.sp_def, mon.base_stats.speed]
        maxStats = [0 for i in range (6)]
        minStats = [0 for i in range (6)]
        maxStats[0] = math.floor ((2 * int (stats[0]) + 31 + math.floor (252 / 4)) * lvl / 100) + lvl + 10
        minStats[0] = math.floor ((2 * int (stats[0])) * lvl / 100) + lvl + 10
        for i in range (1, 6):
            maxStats[i] = math.floor (
                (math.floor ((2 * int (stats[i]) + 31 + math.floor (252 / 4)) * lvl / 100) + 5) * 1.1)
            minStats[i] = math.floor ((math.floor ((2 * int (stats[i])) * lvl / 100) + 5) * 0.9)
        st += f"Types: {Types}\n"
        st += f"Base Stats:** {print_stats (stats)}**\n"
        st += f"Maximum Possible for each Stats:** {print_stats (maxStats)}**\n"
        st += f"Minimum Possible for each Stats:** {print_stats (minStats)}**\n"
        s_name = ["HP", "Atk", "Def", "SpAtk", "SpDef", "Spe"]
        avg = 0
        temp = bubble_sort (stats, s_name, avg)
        st += f"Stats in increasing order:** {s_name[0]} {s_name[1]} {s_name[2]} {s_name[3]} {s_name[4]} {s_name[5]} **\n"
        bestStats = []
        st1 = ""
        for i in range (4, 6):
            if temp[i] > avg:
                bestStats.append (s_name[i])
                st1 += s_name[i] + " "
        st += f"Best Stats: {st1}\n"
        st += "Guessed Format:\n"
        st += await get_format (bestStats)
        e = discord.Embed (title=f"{name} Lvl: {lvl} \n")
        e.set_image (url=mon.sprites.front["default"])
        e.description = st
        await ctx.send (embed=e)
    except:
        await ctx.send ("Cant find " + name)


@bot.command (name="randMon", help="Rand mon")
async def randMon(ctx):
    a = random.randrange (1, 894)
    await hc (ctx, pypokedex.get (dex=int (a)).name, 100)


@bot.command (name="randAbi", help="Rand ability")
async def randAb(ctx):
    a = random.randrange (1, 894)
    abi = pypokedex.get (dex=int (a)).abilities[
        random.choice (range (len (pypokedex.get (dex=int (a)).abilities)))].name
    await ctx.send (abi)
    await ctx.send (searchAbi (abi))


@bot.command (name="insult", help="God LEVEL command")
async def insult(ctx, *args, plural=False):
    key="is a" if not False else "are"
    s = ""
    insults = ["Fucking", "Dumb", "Shitty", "Stupid", "Bloody", "Creepy"]
    insults1 = ["idiot", "Matherchod", "Wastey", "Gandu", "Loser", "Bot", "AHole", "Bitch Lasagna",
                "Gay", "Homo", "Ass", "Lauda", "Dick Head", "Doofus"]
    for i in args:
        s += i + " "
    await ctx.send (s + key+" " + random.choice (insults) + " " + random.choice (insults1))


@bot.command (name="search", help="google")
async def se(ctx, *args):
    st = ""
    for i in args:
        st += i + " "
    await ctx.send (search (st))

@commands.has_permissions(administrator = True)
@bot.command (name="detect", help="SIAN specialty")
async def de(ctx):
    await ctx.send("detecting life @everyone")

@bot.command (name="test", help="SIAN specialty")
async def test(ctx):
    await ctx.send(ctx.message.attachments[0].url)

@bot.command (name="sprite", help="Pokemon sprite")
async def sprite(ctx, name, mode):
    try:
        name = pypokedex.get (dex=int (name)).name
        await ctx.send (name)
        try:
            await ctx.send (pypokedex.get (name=name).sprites.front[mode])
        except:
            await ctx.send ("Doesnt Match Any Entries")
    except:
        await ctx.send (name)
        try:
            await ctx.send (pypokedex.get (name=name).sprites.front[mode])
        except:
            await ctx.send ("Doesnt Match Any Entries")


@bot.command (name="compare", help="compares mons at stat")
async def comp(ctx, *args):
    for i in range (len (args)):
        p = []
        try:
            p.append (pypokedex.get (name=args[i]))
            stats = [p[i].base_stats.hp, p[i].base_stats.attack, p[i].base_stats.defense
                , p[i].base_stats.sp_atk, p[i].base_stats.sp_def, p[i].base_stats.speed]
            await ctx.send (p[i].sprites.front["default"])
            await ctx.send (p[i].name + "      dex - #" + str (p[i].dex))
            for j in p[i].abilities:
                if j.is_hidden:
                    await ctx.send ("Hidden Ability :" + j.name)
                else:
                    await ctx.send ("Ability :" + j.name)
            await ctx.send (print_stats (stats))
        except:
            await ctx.send (f"{args[i]} not found")


@bot.command (name="psearch", help="Searches pokemon.com")
async def pd(ctx, name):
    await ctx.send (pypokedex.get (name=name).sprites.front['default'])
    for i in psearch (name):
        await ctx.send (i)


@bot.command (name="greet", help="greetings")
async def g(ctx, name):
    await ctx.send ("hey " + name)


@bot.command (name="billboard", help="Searches billboard.com for top 10 songs")
async def pd(ctx):
    send = ""
    for i in song_search ():
        send += i + "\n"
    await ctx.send (send)


@bot.command (name="cricket", help="cricket score")
async def cr(ctx):
    lis = csearch ()
    await ctx.send (lis[0])
    await ctx.send (lis[1] + " v/s " + lis[2])
    await ctx.send (lis[3])
    await ctx.send (lis[4])


@bot.command (name="rule", help="rules i mean duh")
async def manual(ctx):
    with open("b.txt") as f:
      desc="".join(f.readlines())
    await ctx.send(embed=discord.Embed(title="Rules",description=desc))


@bot.command (name="imgSearch", help="google images search")
async def ih(ctx, *args):
    st = " ".join(args)
    await ctx.send (random.choice (imgsearch (st)))


@bot.command (name="joke", help="just joking")
async def j(ctx):
    await ctx.send (random.choice (pun ()))

@bot.command (name="catch",help="Mod catch")
@commands.has_permissions(administrator = True)
async def mc(ctx,channel,user,*args):
    await ctx.channel.purge(limit=1)
    await ctx.send(embed=discord.Embed(description="Gotta Catch em all"))
    args=" ".join(args)
    channel=bot.get_channel(int(channel.replace("<#","").replace(">","")))
    await channel.send(user)
    await channel.send("https://tenor.com/view/%E0%B8%9C%E0%B8%B5-horror-scary-insidious-gif-15783267")
    await channel.send(args)

keep_alive.keep_alive()

@tasks.loop (minutes=1)
async def wish():
    midnight = "18 30"

    if(datetime.utcnow ().strftime("%H %M") == midnight):
      dat = (datetime.now()+timedelta(days=1)).strftime("%b %d").split(" ")
      
      wishes=[
        "It is your birthday! Remember that researchers have said that Birthdays are good for your health and people who have more birthdays live longer. May you get more birthdays",
        "Happy birthday, kiddo! I hope you blow all candles yourself insteading of asking the firefighters",
        "Congratulations on this one more year of survival through your math class. You got this!",
        "May you grow old and rich, so that you can leave me a big inheritance.",
        "As you grow into manhood, may life bless you with children who love you just as much as you love making them!"
      ]
      for ch in [872022725479264311,763724647371636736]:
        message_channel = bot.get_channel (ch)

        def conv(a):
            a = a.split (" ")
            a[1] = a[1].zfill (2)
            return a
        m = list (map (conv,(await bot.get_channel (846725437471850496).fetch_message (846725545424584736)).content.split ("\n")[1:-1]))


        for i in m:
            if i[:2]==dat:
              await bday_embed(message_channel,f"Happy BIRTHDAY {i[2]}!!",random.choice(wishes))
      message_channel = bot.get_channel (753607318368944179)
      

      m = list (map (conv,(await bot.get_channel (863280043551096841).fetch_message (846725545424584736)).content.split ("\n")[1:-1]))

      
      for i in m:
          if i[:2]==dat:
            await bday_embed(message_channel,f"Happy BIRTHDAY {i[2]}!!",random.choice(wishes))
            


@wish.before_loop
async def before():
    await bot.wait_until_ready ()
    print ("Finished waiting")


wish.start ()

bot.run(TOKEN)  
