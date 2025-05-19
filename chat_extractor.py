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

    def num_ko_char(self, text):
        return len(re.findall('[ㄱ-ㅎㅏ-ㅣ가-힣]', text))
    
    def num_hanja_char(self, text):
        return len(re.findall('[\u2e80-\u2eff\u31c0-\u31ef\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fbf\uf900-\ufaff]', text))

    def extract_single_line(self, date, line):
        for pattern in self.patterns_to_remove:
            line = re.sub(pattern, '', line)

        for pattern in self.patterns_chat_type.keys():
            m = re.search(pattern, line)
            if m is not None:
                return date + ' ' + line[1:9] + self.patterns_chat_type[pattern](self, m.groups())
        return None

    def extract(self, directory, filename, servername, threshold=20):
        with open(directory + filename, mode='rb') as f:
            lines = f.readlines()

        str_list = []

        cnt_cp949 = 0
        cnt_utf8 = 0

        for line in lines:
            # Convert encoding from src_enc to dest_enc
            # line = line.decode(self.args.src_enc, errors='ignore').encode(self.args.dest_enc, errors='ignore').decode(self.args.dest_enc)

            line_utf8 = line.decode(encoding='utf-8', errors='ignore')
            line_euckr = line.decode(encoding='euc-kr', errors='ignore')
            line_cp949 = line.decode(encoding='cp949', errors='ignore')

            num_ko_utf8 = self.num_ko_char(line_utf8)
            num_ko_euckr = self.num_ko_char(line_euckr)
            num_hanja_utf8 = self.num_hanja_char(line_utf8)
            num_hanja_euckr = self.num_hanja_char(line_euckr)

            if cnt_cp949 > threshold:
                line = line_cp949
            elif cnt_utf8 > threshold:
                line = line_utf8
            else:
                if num_ko_utf8 == 0 and num_ko_euckr == 0:
                    line = line_utf8
                else:
                    if num_hanja_utf8 == num_hanja_euckr:
                        if num_ko_utf8 > num_ko_euckr:
                            line = line_utf8
                            cnt_utf8 += 1
                        elif num_ko_utf8 < num_ko_euckr:
                            line = line_cp949
                            cnt_cp949 += 1
                        else:
                            print(f"conflict occurred: {line_utf8} | {line_cp949}")
                            print(f"cnt_cp949: {cnt_cp949}, cnt_utf8: {cnt_utf8}")
                            if cnt_cp949 >= cnt_utf8:
                                line = line_cp949
                            else:
                                line = line_utf8
                    elif num_hanja_utf8 > num_hanja_euckr:
                        line = line_cp949
                        cnt_cp949 += 1
                    else:
                        line = line_utf8
                        cnt_utf8 += 1

            
            line = line.replace('\"', '')
            line = line.replace('\n', '')
            line = line.replace('\r', '')
            line = line.replace('쁾', '')
            line = line.replace('쁿', '')
            string = self.extract_single_line(filename[:10], line)
            if string is not None:
                string = servername + ',' + string
                str_list += string

        return str_list
