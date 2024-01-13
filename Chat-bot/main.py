import re
import lg_res as long


def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses -------------------------------------------------------------------------------------------------------
    response('Hello!', ['hello', 'hi','hii', 'hey', 'sup', 'heyo'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('Yup!', ['ok'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('I\'m doing my work to assist you :)', ['what', 'are', 'you', 'doing'], required_words=['what','doing'])
    # introduction section=======
    response('My name is Chat-Bot and what is your name ?', ['what', 'is', 'your', 'name'], required_words=['your','name'])
    response('Nice to meet you...', ['my', 'name','is'], required_words=['my','name','is'])
    response('Nice to meet you..', ['myself'], required_words=['myself'])

    # end====================na
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Thank you!', ['i', 'love', 'coding', 'palace'], required_words=['coding', 'lol'])

    # Longer responses
    response(long.R_ADVICE, ['help'], required_words=['help'])
   
    response(long.R_born, ['born'], required_words=['born'])
    response(long.R_made, ['made'], required_words=['made'])
    response(long.R_askrep, ['also','fine'], required_words=['also','fine'])
    response(long.R_sugges, ['suggestion'], required_words=['suggestion'])
    response(long.R_sugges, ['give','suggestion'], required_words=['give','suggestion'])
    response(long.R_sugges, ['suggest'], required_words=['suggest'])
    response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
 

    return long.unknown() if highest_prob_list[best_match] < 1 else best_match


# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response


# Testing the response system
while True:
    print('Bot: ' + get_response(input('You: ')))