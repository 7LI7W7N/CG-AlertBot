# - Import Discord, Requests, KeepAliveHandler and Replit Database
import discord
import requests
from replit import db
from keep_alive import keep_alive


# - Get Crypto Prices
def GetCryptoPrices(Crypto_Name):
  URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
  R = requests.get(url=URL)
  data = R.json()
  # - Looping through the Data
  for i in range(len(data)):
    db[data[i]['id']] = data[i]['current_price']

  if Crypto_Name in db.keys():
    return db[Crypto_Name]
  else:
    return 'Not Found'


# - Check if Crypto is Supported
def CheckCrypto(Crypto_Name):
  if Crypto_Name in db.keys():
    return True
  else:
    return False


# - Instantiate a Discord Client

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# - Client Events

@client.event
async def on_ready():
  print(f'You have logged in as {client}')
  channel = discord.utils.get(client.get_all_channels(), name='crypto')
  await client.get_channel(channel.id).send('COIN GECKO BOT IS ONLINE MFKERs')


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  # - Replies to 'YAH' w. 'YEET'
  if message.content.startswith('YAH'):
    await message.channel.send('YEET')

  # - Send Crypto Prices into Chat
  if message.content.lower() in db.keys():
    await message.channel.send(
        f'The current price of {message.content.upper()} is ${GetCryptoPrices(message.content.lower())} right now.'
    )

  # - List Available Coins in API's JSON Response
  if message.content.startswith('ListCoins'):
    CryptoSupportedList = '\n'.join(
        [f'{i + 1}. {key.upper()}' for i, key in enumerate(db.keys())])
    await message.channel.send(CryptoSupportedList)

  # - Total Coins Supported
  if message.content.startswith('TotalCoins'):
    num_coins = len(db)
    await message.channel.send(
        f'Total number of coins supported in the database: {num_coins}')

  # - Check Coin Support 
  if message.content.startswith('CheckCoin: '):
    CryptoCheck = message.content.split('CheckCoin:',1)[1].strip().lower()
    result = CheckCrypto(CryptoCheck)
    await message.channel.send(str(result))

# - Help Command
  if message.content.startswith('Help'):
    help_msg = ('- **YAH**: Bot replies with YEET\n'
                '- **ListCoins**: List available cryptocurrencies\n'
                '- **TotalCoins**: Show the total number of supported cryptocurrencies\n'
                '- **CheckCoin: CoinName**: Check if a specific cryptocurrency is supported')
    await message.channel.send(help_msg)

# - Ping to UpTimeBot to Keep the Bot Alive
keep_alive()

# - Run the Client and Add Token
BOT_TOKEN = 'TOKEN HERE'
client.run(BOT_TOKEN)
intents = discord.Intents.default()
client = discord.Client(intents=intents)
