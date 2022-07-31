import os
import chat_extractor
import argparse


def get_file_list(directory):
    file_list = os.listdir(directory)
    files = [file for file in file_list if file.endswith(".log")]
    return files


def main(args):
    log_dir = args.logdir
    if log_dir[-1] is not '\\':
        log_dir += '\\'
    csv_path = args.csvpath
    files = get_file_list(log_dir)

    csv = open(csv_path, 'w', encoding="utf-8-sig")
    csv.write('timestamp, type, sender, receiver, content\n')

    extractor = chat_extractor.ChatExtractor()
    i, l = 1, len(files)
    for filename in files:
        print("[{0} / {1}] Parsing {2}".format(i, l, filename))
        for line in extractor.extract(log_dir, filename):
            csv.write(line)
        i += 1

    csv.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Merge player chat data from Minecraft server logs into a csv file")

    parser.add_argument('--logdir', required=True)
    parser.add_argument('--csvpath', default="output.csv")

    args = parser.parse_args()
    main(args)
