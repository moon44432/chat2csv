import re


class ChatExtractor:
    def __init__(self, args):
        self.args = args

    def ingame(self, substrings):
        return ',{0},{1},{2},"{3}"\n' .format("ingame", re.sub(self.nickname_star, "", substrings[0]), "", substrings[1])

    def dynmap(self, substrings):
        return ',{0},{1},{2},"{3}"\n' .format("dynmap", re.sub(self.nickname_star, "", substrings[0]), "", substrings[1])

    def prompt(self, substrings):
        return ',{0},{1},{2},"{3}"\n' .format("prompt", "", "", substrings[0])

    def whisper(self, substrings):
        return ',{0},{1},{2},"{3}"\n' .format("whisper", re.sub(self.nickname_star, "", substrings[0]), substrings[1], substrings[2])
    
    nickname_star = "[☆★]"

    patterns_to_remove = [
        r"\[[0-9;]*m",
        r"\bAutoMessage\b"
    ]

    patterns_chat_type = {
        r": <([^~,>:]+)> (.+)": ingame,
        r"\[Not Secure\] <([^~,>:]+)> (.+)": ingame,
        r"\[WEB\] ([^~,>:]+): (.+)": dynmap,
        r"\[Server\] (.+)": prompt,
        r": ([^~,>:]+) issued server command: /tell ([^, ]+) (.+)": whisper,
    }

    def extract_single_line(self, date, line):
        for pattern in self.patterns_to_remove:
            line = re.sub(pattern, '', line)

        for pattern in self.patterns_chat_type.keys():
            m = re.search(pattern, line)
            if m is not None:
                return date + ' ' + line[1:9] + self.patterns_chat_type[pattern](self, m.groups())
        return None

    def extract(self, directory, filename):
        f = open(directory + filename, mode='rb')
        lines = f.readlines()

        str_list = []

        for line in lines:
            # Convert encoding from src_enc to dest_enc
            line = line.decode(self.args.src_enc, errors='ignore').encode(self.args.dest_enc, errors='ignore').decode(self.args.dest_enc)

            string = self.extract_single_line(filename[:10], line)
            if string is not None:
                str_list += string

        f.close()
        return str_list
