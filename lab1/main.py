import argparse
from glob import glob
from random import randint

import requests
from bs4 import BeautifulSoup
from lxml import html


class Crawler:
    def __init__(self, input_directory, mode):
        self.input_directory = input_directory
        self.mode = mode

    def get_all_songs_list(self):
        all_songs_list = []
        if self.mode == 'local':
            for file in glob(f'{self.input_directory}/song*.txt'):
                with open(file, encoding='utf-8') as input_file:
                    all_songs_list.extend([line for line in input_file.readlines() if line != '\n'])
        elif self.mode == 'internet':
            urls = [r'https://www.azlyrics.com/lyrics/samsmith/staywithme.html',
                    r'https://www.azlyrics.com/lyrics/samsmith/restart.html',
                    r'https://www.azlyrics.com/lyrics/samsmith/howdoyousleep.html',
                    r'https://www.azlyrics.com/lyrics/samsmith/young.html',
                    r'https://www.azlyrics.com/lyrics/samsmith/pray.html']
            for index, url in enumerate(urls):
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'lxml')
                text_with_tags = soup.find_all('div')[20]
                text_without_tags = html.fromstring(str(text_with_tags)).text_content()
                with open(f'internet_song_{index + 1}.txt', 'w', encoding='utf-8') as f:
                    print(text_without_tags, file=f)
            for file in glob(f'{self.input_directory}/internet_song*.txt'):
                with open(file, encoding='utf-8') as input_file:
                    all_songs_list.extend([line for line in input_file.readlines() if line != '\n'])
        else:
            print('Wrong mode. Please, use "local" or "internet"!')
            exit()
        return all_songs_list


class Generator:
    def __init__(self, all_songs_list):
        self.all_songs_list = all_songs_list

    def generate_random_row(self):
        random_row = randint(0, len(self.all_songs_list) - 1)
        return self.all_songs_list[random_row]

    def generate_couplet(self):
        couplets_rows = int(args['rows']) - 3 * int(args['chorus'])

        couplet = []
        for row in range(couplets_rows // 3 + couplets_rows % 3):
            couplet.append(self.generate_random_row())
        yield couplet

        couplet = []
        for row in range(couplets_rows // 3):
            couplet.append(self.generate_random_row())
        yield couplet

        couplet = []
        for row in range(couplets_rows // 3):
            couplet.append(self.generate_random_row())
        yield couplet

    def generate_chorus(self):
        chorus = []
        chorus_len = int(args['chorus'])
        for row in range(chorus_len):
            chorus.append(self.generate_random_row())
        return chorus

    def generate_new_song(self):
        new_song_list = []
        couplets_generator = self.generate_couplet()
        chorus = self.generate_chorus()
        for _ in range(3):
            new_song_list.extend(next(couplets_generator))
            new_song_list.extend(['\n'])
            new_song_list.extend(chorus)
            new_song_list.extend(['\n'])
        return new_song_list


class Saver:
    def __init__(self, output_directory, new_song_list):
        self.output_directory = output_directory
        self.new_song_list = new_song_list

    def save_new_song(self):
        with open('new_song.txt', 'w+', encoding='utf-8') as output_file:
            output_file.writelines(self.new_song_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', required=True)
    parser.add_argument('-r', '--rows', required=True)
    parser.add_argument('-c', '--chorus', required=True)
    parser.add_argument('-m', '--mode', required=False, default='local')
    args = vars(parser.parse_args())
    # args = {'directory': r'C:\stp\stp2021', 'rows': '30', 'chorus': '5', 'mode': 'internet'}

    if int(args['rows']) < int(args['chorus']) * 3:
        print('Your song is smaller than 3 choruses')
        exit()

    crawler = Crawler(input_directory=args['directory'], mode=args['mode'])
    generator = Generator(all_songs_list=crawler.get_all_songs_list())
    saver = Saver(output_directory=args['directory'], new_song_list=generator.generate_new_song())

    saver.save_new_song()
