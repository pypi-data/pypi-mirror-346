import argparse
from rotate_group_words import rotate_group_words


def main():
    parser = argparse.ArgumentParser(description="Group words by rotation similarity.")
    parser.add_argument('-w', '--words', type=str, required=True, help='Comma separated list of words')
    args = parser.parse_args()
    words = [w.strip() for w in args.words.split(',') if w.strip()]
    rotate_group_words(words)

if __name__ == "__main__":
    main()
