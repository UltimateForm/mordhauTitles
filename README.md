# mordhauBattleEye

This bot conjoins two bots: [mordhauMigrantTitles](https://github.com/UltimateForm/mordhauMigrantTitles) & [mordhauPersistentTitles](https://github.com/UltimateForm/mordhauPersistentTitles)


- [mordhauBattleEye](#mordhaubattleeye)
  - [Usage](#usage)
    - [Setup](#setup)
    - [Example .env](#example-env)
  - [mordhauMigrantTitles](#mordhaumigranttitles)
    - [What it do?](#what-it-do)
    - [Important note](#important-note)
    - [FAQs](#faqs)
  - [mordhauPersistentTitles](#mordhaupersistenttitles)
    - [What it do?](#what-it-do-1)
      - [Discord usage](#discord-usage)
    - [Important notes](#important-notes)

## Usage
You need at least Docker installed and a terminal that can run .sh files (linux or unix-like system)

### Setup

1. clone repo or download code
1. create .env file in same folder as code with these parameters:
    1. RCON_PASSWORD
    1. RCON_ADDRESS
    1. RCON_PORT
    2. RCON_CONNECT_TIMEOUT (optional)
    3. D_TOKEN (discord bot auth token)
    4. TITLE (optional)
2. run `sh restart.sh` in terminal
    1. if you're familar with docker or python you don't necessarily need to this, you can run this bot anywhere and however you want

### Example .env
```
RCON_PASSWORD=superD_uprSecurePw
RCON_ADDRESS=192.168.0.52
RCON_PORT=27019
RCON_CONNECT_TIMEOUT=10
D_TOKEN=sNb5gkzmvnJ8W9rxHP23kNV5s7GDwtY4J4cY4JNbbM5Bctd8UFURsv8TAShsPdPDXFcaai2WlPaHy3Rxis5C3m5dHXk1leUU
TITLE=KING
```


## mordhauMigrantTitles

### What it do?

This bot, in essence, is a form of encouragement for bloodshed by introducing an unique tag that migrates via kill. Title's name is configurable in .env file. Here below it is further described.

- On a round that just started, given a player of name JohnWick, upon him killing another player of name KevinSpacey, given that is the first kill in the round, JohnWick is awarded title "REX" (his name becomes `[REX] JohnWick`) and server message is spawned:
  > JohnWick has defeated KevinSpacey and claimed the vacant REX title
- On a round where player JohnWick is the current holder of REX title, when he is killed by player DonnieYen, JohnWick's name loses "REX" tag and DonnieYen's name is changed to  `[REX] DonnieYen` and server message is spawned:
  > DonnieYen has defeated [REX] JohnWick and claimed his REX title

### Important note
1. this hasn't been stress tested
   1. I tested on a small server with 20-30 ppl
   2. most of my testing has been on personal local server with bots

### FAQs
- How does the first title holder gets selected? (as in when there's no current holder)
  - first killer dectected while title is vacant gets awarded the title
- What happens when current title holder leaves server?
  - title is made vacant, conditions regarding vacant titles apply


## mordhauPersistentTitles

This a Discord X RCON bot that is used to implement persistent tags (via RCON's `renameplayer`) and salutes (via RCON's `say`)

### What it do?

This bot allows you to 
- have custom tags (or titles) in front of player's names, i.e. you can tag a player with name "FFAer" or "Champion". These tags will last until they're removed. **Note that if you add a tag to player while he is ingame he will need to either rejoin server or wait till next round for tag to take effect**
  - the difference between this and the much simpler rcon's `renameplayer` is that this one will persist across sessions, the tag will persist even after player logs out or round ends
- have specific server messages automatically spawn when selected players join server

These features are managed via discord

#### Discord usage

I will not tell you here how to setup a discord bot, there's already plenty of guides about that. The bot code here does not manage permissions so it's on you to manage the access.

Commands:
- .setTagFormat {tag format}
  - sets the tag format, must always include {0} which is the placeholder for the tag
  - example: `.setTagFormat -{0}-`
- .setSaluteTimer {number of seconds}
  - sets the time in seconds for salute to show up in server,
  - example: `.setSaluteTimer 2`
- .addTag {playfab id} {tag}
  - sets a tag for a playfab id
  - example: `.addTag D98123JKAS78354 CryBaby`
- .removeTag {playfab id}
  - removes tag for playfabid
  - example: `.removeTag D98123JKAS78354`
- .addSalute {playfab id} {salute text}
  - adds salute for playfab id
  - use quotes ("") for multi word salutes
  - example: `.addSalute D98123JKAS78354 "Welcome back Dan"`
- .removeSalute {playfab id}
  - removes salute for playfab id
  - example: `.removeSalute D98123JKAS78354`
- .ptConf
  - shows full config
  - example: `.ptConf`


### Important notes
1. This bot doesn't use (yet) the native discord commands
2. This bot hasn't been stress tested, a previous version has been tested on a server with 20-40 players, but was different code