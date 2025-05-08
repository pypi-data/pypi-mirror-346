from typing import Any
import argparse


def group_words(key: str, value: list[str]):
    """
    it keeps a dictionary of
    {
        "abcd" : ["abcd", "cdab", "dabc", "bcda"],
        "efgh": []
        "ghfe" : []
    }

    """
    # use a dictionary to keep the similar items
    pass


def is_similar(a: str, b: str) -> bool:
    """Check if b is a rotation of a"""
    return len(a) == len(b) and b in (a + a)


def rotate_word(word: str, count_of_rotation: int) -> str:
    """
    #TODO implement
    rotate the word 'count_of_rotation' times.

    return the word
    """
    result = word
    for i in range(count_of_rotation):
        result = rotate_word_once(result)

    return result


def rotate_word_once(word: str) -> str:
    the_last_word = word[-1]
    return the_last_word + word[:-1]


def is_distrinct(word: str, list_of_words: list[str]):

    is_similar = is_similar(word, list_of_words)
    pass


def iterating_through_input(words: list[str]) -> Any:
    """
    how to iterate and compare all elements
    # iterate through them all
    """
    result_dic = {}
    visited = set()
    for w in words:
        # instead of adding every possible words, only add those who do not have
        # a key in dictionary
        # finding an element inside the list of values of a key
        # for k in result_dic.keys():
        #     if result_dic[k] == w:
        #         break
        if w in visited:
            continue
        result_dic[w] = []
        visited.add(w)
        for other_word in words:
            if is_similar(w, other_word):
                result_dic[w].append(other_word)
                visited.add(other_word)
                # words.remove(other_word)
    return result_dic


def rotate_group_words(input_list: list[str]):
    """
        Find the distinct words and group similar ones


     Input: list[str]
     #TODO size constraints?

     Process:
        grouping similar strings together
            what is similar: rotate until become similar
                Rotate function
            how to group:
        requirement:
            - not inplace

    expected Output:
        {
            ["abcd", "cdab", "dabc", "bcda"],
            ["efgh"],
            ["ghfe"]
        }
    """

    result = iterating_through_input(input_list)
    pretty_print(result)


def main():
    """
    Given a list of Strings,
       group the strings together
           which forms the exact same word after rotation
                   (keeping the character sequence intact while rotating).
    """
    parser = argparse.ArgumentParser(
        description="Group strings that are rotations of each other.",
        epilog='Example: main -w "[abcd cdab dabc bcda efgh ghfe]" or main -w "abcd, cdab, dabc, bcda, efgh, ghfe"',
    )
    parser.add_argument(
        "-w",
        "--words",
        type=str,
        required=True,
        help='List of words in brackets or comma-separated. Example: -w "[abcd cdab dabc bcda efgh ghfe]" or -w "abcd, cdab, dabc, bcda, efgh, ghfe"',
    )
    args = parser.parse_args()
    # Accept either [word1 word2 ...] or comma-separated
    arg = args.words.strip()
    if arg.startswith("[") and arg.endswith("]"):
        words = arg.strip("[]").split()
    elif "," in arg:
        words = [w.strip() for w in arg.split(",") if w.strip()]
    else:
        words = arg.split()
    rotate_group_words(words)


def pretty_print(groups: list[list[str]]):
    for k, v in groups.items():
        print(f"{k}: [{', '.join(v)}]")


if __name__ == "__main__":
    main()
