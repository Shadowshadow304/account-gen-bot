import discord, os, glob
from discord.ext import commands

bot = commands.Bot(command_prefix=[".", "$"], intents=discord.Intents.all())
bot.remove_command('help')
directory = os.getcwd()

def getFileName(file):
    file_name = file.split('\\', -1)[-1]
    return file_name.split('.', -1)[0]

def getAccs():
    allAccounts = []
    for file in glob.glob(directory + '/accounts/*.txt'):
        with open(file, 'r', encoding='utf-8') as fp:
            x = len(fp.readlines())
        allAccounts.append(getFileName(file) + ":" + str(x))
    return allAccounts

@bot.event
async def on_ready():
    print("Bot: {0.user}".format(bot))

# make sure your acc lists are mail:pass or user:pass
# or this might not work the way it is intended to.
@bot.slash_command(name="gen", description="Generate an account.")
async def gen(interaction: discord.Interaction, account: str):
    channel = await interaction.user.create_dm()
    for file in glob.glob(directory + '/accounts/*.txt'):
        file_name = file.split('\\', -1)[-1]
        file_name = file_name.split('.', -1)[0]
        # honestly what the fuck is this shit, idk if its optimized enough for big text files
        if file_name.lower() == account.lower():
            if os.stat(file).st_size == 0:
                await interaction.response.send_message("`" + file_name.upper() + "` is out of stock.")
                return
            with open(file, "r+") as fp:
                lines = fp.readlines() 
                acc_line = lines[0]
                fp.seek(0)
                fp.truncate()
                fp.writelines(lines[1:])
            genembed=discord.Embed(title="Generated Account - " + file_name,
                        description="```" + acc_line +"```",
                        color=0x2B2D31)
            genembed.set_footer(text="github.com/Atluzka/account-gen-bot")
            await channel.send(embed=genembed)
            await interaction.response.send_message("Generated account has been sent to your DMs")
            return
    await interaction.response.send_message("account not found")

@bot.slash_command(name="stock", description="Get the amount of stock.")
async def stock(ctx):
    
    account_list = getAccs()
    
    embed=discord.Embed(title="Stock",
                        description="All the currently available accounts to be generated.",
                        color=0x2B2D31)
    embed.set_footer(text="github.com/Atluzka/account-gen-bot")
    for i in account_list:
        rndmlist1 = i.split(":", 1)
        embed.add_field(name=rndmlist1[0].upper(), value="Stock: `" + rndmlist1[1] + "`", inline=True)
    await ctx.respond(embed=embed)
       
bot.run("YOUR DISCORD TOKEN HERE")