# chat2csv: Minecraft Chat Extractor
This program extracts chat data from Minecraft server logs, and then merge them into a clean single csv file.

It supports four chat types:
1. `ingame` - General in-game chat: `<{sender}> {content}`
2. `dynmap` - [Dynamic Map](https://www.spigotmc.org/resources/dynmap%C2%AE.274/) web chat: `[WEB] {sender}: {content}`
3. `prompt` - Server prompt message (mostly from the administrator): `[Server] {content}`
4. `whisper` - Whispers: `{sender} issued server command: /tell {receiver} {content}`

## Usage
### Preparing server log files (Craftbukkit / Spigot / Paper)
1. Log files are saved in `[Server Directory]\logs\` by default. Each of them is compressed into a *.gz file.
2. Choose a directory and move all the logs that you'd like to extract chat data from.
3. Decompress *.gz files, and you will see *.log files. File names must be in a form of `yyyy-mm-dd-n.log`.
4. You can specify encodings of the log files and the final csv file with --src-enc and --dest-enc respectively.

### Run the extractor
Run `python chat2csv.py --logdir [log directory] --csvpath [csv file path] --src-enc [encoding of the log files] --dest-enc [encoding of the csv file]`.
`--csvpath` is optional. The program saves the output to `output.csv` as default.
If not specified, the program will assume that the encoding of both log files and final csv file is `utf-8-sig`. Check how your log files are encoded in advance to prevent character breaking.

### CSV structure
The output csv has 5 columns in total: `timestamp`, `type`, `sender`, `receiver`, `content`.

#### Example
| timestamp           | type     | sender      | receiver    | content                                                                     |
|---------------------|----------|-------------|-------------|-----------------------------------------------------------------------------|
| 2015-05-12 21:22:08 | ingame   | sniper_suin |             | who are you?                                                                |
| 2015-08-29 20:41:47 | dynmap   | PlexA       |             | hi guys                                                                     |
| 2016-01-27 18:16:42 | whisper  | Uralskaya   | MoonSeunggi | he was approaching and i had to do something  |
| 2017-01-03 13:25:24 | prompt   |             |             | im coming                                                                   |
| ...                 | ...      | ...         | ...         | ...                                                                         |

