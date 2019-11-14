"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    selected = []
    for paragraph in paragraphs:
        if select(paragraph):
            selected.append(paragraph)
    if k > len(selected) - 1:
        return ''
    else:
        return selected[k]
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def select(paragraph):
        wordlist = split(lower(remove_punctuation(paragraph)))
        for word1 in topic:
            for word2 in wordlist:
                if word1 == word2:
                    return True
        return False
    return select
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    if typed_words == []:
        return 0.0
    index, correct = 0, 0
    while index < len(reference_words) and index < len(typed_words):
        if typed_words[index] == reference_words[index]:
            correct +=1
        index += 1
    return 100 * correct/len(typed_words)

    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    return (len(typed)/5)/(elapsed/60)
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than or equal to LIMIT.
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    smallest_diff = diff_function(user_word, valid_words[0], limit)
    closest_word = valid_words[0]
    for word in valid_words:
        if word == user_word:
            return user_word
        elif diff_function(user_word, word, limit) < smallest_diff:
            smallest_diff = diff_function(user_word, word, limit)
            closest_word = word
    if smallest_diff > limit:
        return user_word
    else:
        return closest_word
    # END PROBLEM 5


def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    difference = abs(len(goal) - len(start))
    def diff_count(start, goal, difference):
        if start[0] != goal[0]:
            difference += 1
        if len(start) == 1 or len(goal) == 1 or difference > limit:
            return difference
        else:
            return diff_count(start[1:len(start)], goal[1:len(goal)], difference)
    return diff_count(start, goal, difference)

    # END PROBLEM 6

def edit_diff(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    if limit < 0:
        return 0
    elif(len(start) < 1 or len(goal) < 1):
        return abs(len(goal) - len(start))
    elif start[0] == goal[0]:
        return edit_diff(start[1: len(start)], goal[1: len(goal)], limit)
    else:
        add_diff = 1 + edit_diff(start, goal[1: len(goal)], limit - 1)  # Fill in these lines
        remove_diff = 1 + edit_diff(start[1: len(start)], goal, limit - 1)
        substitute_diff = 1 + edit_diff (start[1: len(start)], goal[1: len(goal)], limit - 1)
        # BEGIN
        "*** YOUR CODE HERE ***"
        return min(add_diff, remove_diff, substitute_diff)
        # END


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'




###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    accuracy = 0
    for word in typed:
        if prompt[typed.index(word)] != word:
            send({'id': id, 'progress': accuracy/len(prompt)})
            return accuracy/len(prompt)
        else:
            accuracy += 1
    send({'id': id, 'progress': accuracy/len(prompt)})
    return accuracy/len(prompt)
    # END PROBLEM 8


def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    elapsed_times = [] #An intermediate array with individual times for words rather than total time elapsed
    fastest = [] #The array we return

    #First we extract the times it takes to type each word by subtracting the total elapsed time from the previous word

    player = 0

    while player < len(word_times):
        elapsed_times.append([])
        fastest.append([])
        index = 1
        while index < len(word_times[player]):
            elapsed_times[player].append(word_time(word(word_times[player][index]), elapsed_time(word_times[player][index]) - elapsed_time(word_times[player][index - 1])))
            index += 1
        player +=1

    #Now we find the fastest for each word

    index = 0
    while index < len(elapsed_times[0]):
        current_word_times = []
        for player in elapsed_times:
            current_word_times.append(elapsed_time(player[index]))
        fastest_time = min(current_word_times)
        fastest_players = []
        timeindex = 0
        while timeindex < len(current_word_times):
            if current_word_times[timeindex] <= fastest_time + margin:
                fastest_players.append([timeindex, elapsed_times[timeindex]])
            timeindex +=1
        player = 0
        while player < len(fastest_players):
            fastest[fastest_players[player][0]].append(word(fastest_players[player][1][index]))
            player +=1
        index += 1
    return fastest



    # END PROBLEM 9


def word_time(word, elapsed_time):
    """A data abstraction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]


def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = False  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
