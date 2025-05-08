from typing import Any


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
    if len(word) == 0 or len(word) == 1: return word
    the_last_word = word[-1]
    return the_last_word + word[:-1]



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


def pretty_print(groups: list[list[str]]):
    for k, v in groups.items():
        print(f"{k}: [{', '.join(v)}]")
