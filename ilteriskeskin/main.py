import wikipedia

WORDLIST_FILE = "wordlist/test_wordlist.txt"
WIKIPEDIA_RESULT_FILE = "wordlist/wiki_results.txt"


def read_wordlist(wordlist_file):
    with open(wordlist_file) as words_file:
        words = words_file.readlines()
        for i in words:
            search_wikipedia(i)


def search_wikipedia(word):
    wikipedia.set_lang('tr')
    with open(WIKIPEDIA_RESULT_FILE, "a") as wiki_result:
        try:
            page = wikipedia.page(word)
            wiki_result.write(page.title)
            wiki_result.write(":")
            wiki_result.write(page.summary)
            wiki_result.write("\n")
        except:
            print(word, ": not found")


if __name__ == "__main__":
    read_wordlist(WORDLIST_FILE)
