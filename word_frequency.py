import re

STOP_WORDS = [
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has',
    'he', 'i', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to',
    'were', 'will', 'with'
]


class FileReader:
    def __init__(self, filename):
        self.filename = filename

    def read_contents(self):
        this_file = open(self.filename)
        text = this_file.read()
        this_file.close()
        return text


class WordList:
    def __init__(self, text):
        self.text = text
        self.word_list = []

    def extract_words(self):
        """
        This should get all words from the text. This method
        is responsible for lowercasing all words and stripping
        them of punctuation.
        """
        str = self.text.lower()
        words = re.sub(r'[?|—|:|"|,|\.\n|\.|\s|\n|\t|\v|\f|\r]+', "*", str)
        self.word_list = words.split("*")
        

    def remove_stop_words(self):
        """
        Removes all stop words from our word list. Expected to
        be run after extract_words.
        """
        self.word_list = [word for word in self.word_list if len(word) > 1 and word not in STOP_WORDS] #The len(word) check is here because there's still one piece of white space I haven't pinned down in each file.  I haven't taken the time to figure out a quick way to look at all the whitespace characters yet, but none of the ones I included takes care of that one lonely space.  Will keep on it.
        self.word_list.sort()

    def get_freqs(self):
        """
        Returns a data structure of word frequencies that
        FreqPrinter can handle. Expected to be run after
        extract_words and remove_stop_words. The data structure
        could be a dictionary or another type of object.
        """
        dictionary = {}
        for word in self.word_list:
            if word in dictionary:
                dictionary[word] += 1
            else:
                dictionary[word] = 1
        letter_sorted = sorted(dictionary.items(), key=lambda entry: entry[0])   #sorts dictionary into alphabetized tuples
        count_sorted = sorted(letter_sorted, key=lambda seq: seq[1], reverse=True) #sorts alphabetical tuples into count order
        return count_sorted        


class FreqPrinter:
    def __init__(self, freqs):
        self.freqs = freqs

    def print_freqs(self):
        """
        Prints out a frequency chart of the top 10 items
        in our frequencies data structure.

        Example:
          her | 33   *********************************
        which | 12   ************
          all | 12   ************
         they | 7    *******
        their | 7    *******
          she | 7    *******
         them | 6    ******
         such | 6    ******
       rights | 6    ******
        right | 6    ******
        """
        words = list(self.freqs)[0:10]
        print()
        for word in words:
            print(word[0].rjust(15) + "  |  " + str(word[1]).ljust(3) + " " + (word[1] * "*"))

if __name__ == "__main__":
    import argparse
    import sys
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description='Get the word frequency in a text file.')
    parser.add_argument('file', help='file to read')
    args = parser.parse_args()

    file = Path(args.file)
    if file.is_file():
        reader = FileReader(file)
        word_list = WordList(reader.read_contents())
        word_list.extract_words()
        word_list.remove_stop_words()
        printer = FreqPrinter(word_list.get_freqs())
        printer.print_freqs()
    else:
        print(f"{file} does not exist!")
        sys.exit(1)
