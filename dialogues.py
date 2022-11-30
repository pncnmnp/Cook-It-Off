import json
import random

from inflect import conjugate, PRESENT, PARTICIPLE, SG

# Here is a sample code we use to generate the paraphrases:

# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# tokenizer = AutoTokenizer.from_pretrained("Vamsi/T5_Paraphrase_Paws")
# model = AutoModelForSeq2SeqLM.from_pretrained("Vamsi/T5_Paraphrase_Paws")
# sentence = "You are doing a great job!"
# text =  "paraphrase: " + sentence + " </s>"
# encoding = tokenizer.encode_plus(text,pad_to_max_length=True, return_tensors="pt")
# input_ids, attention_masks = encoding["input_ids"], encoding["attention_mask"]
# outputs = model.generate(
#     input_ids=input_ids, attention_mask=attention_masks,
#     max_length=256,
#     do_sample=True,
#     top_k=120,
#     top_p=0.99,
#     early_stopping=True,
#     num_return_sequences=50
# )
# lines = []
# for output in outputs:
#     line = tokenizer.decode(output, skip_special_tokens=True,clean_up_tokenization_spaces=True)
#     lines.append(line)
# set(lines)

# Here is a sample code we use to generate ad-libs using GPT

# from transformers import AutoTokenizer, AutoModelForCausalLM
# tokenizer = AutoTokenizer.from_pretrained("gpt2")
# model = AutoModelForCausalLM.from_pretrained("gpt2", pad_token_id = tokenizer.eos_token_id)
# prompt = "Always remember, when cooking vegetables it is important to "
# sents = []
# input_ids = tokenizer(prompt, return_tensors="pt").input_ids
# # generate up to 300 tokens
# for i in range(0, 10):
#   outputs = model.generate(input_ids, max_length=300, num_beams=4, do_sample=True, no_repeat_ngram_size=2, early_stopping=True)
#   sents.append(tokenizer.batch_decode(outputs, skip_special_tokens=True))
# print(sents)

# How do we want to parse the recipe?
# If list > 1 - optional stuff
# If list == 1 - non optional stuff
Recipe = [
    ["You preheat the pan"],
    ["You mix the egg"],
    ["You mix the brocoli", "You mix the mushrooms"],
    ["You cook the egg in the pan"],
    ["You remove the egg from the pan"],
    ["You mix the salt", "You mix the pepper"],
    ["You serve the final dish!"],  # This step needs to be there in every single recipe
]

Veggie_List = ["brocoli", "mushrooms"]


class Dialogue:
    def __init__(self, script_file, paraphrase_file, recipe=None):
        self.script = json.load(open(script_file))
        self.paraphrases = json.load(open(paraphrase_file))
        self.pointer = 0
        self.recipe = recipe if recipe else Recipe
        self.one_time_dialogue = {
            "secret_sauce": False,
            "favorite_food": False,
            "old-man": False,
            "veggies": False,
        }
        self.non_optional_done = []

    def pattern_garbage(self):
        """
        For more context:
        https://github.com/clips/pattern/issues/295#issuecomment-841625057
        """
        try:
            l = conjugate("heat", PRESENT + PARTICIPLE, number=SG)
        except:
            pass

    def secret_sauce(self):
        """
        "Remember, the secret sauce to make a nice <Food-Item> is"
        "You know what's the secret to a nice <Food-Item>? It is "
        "One of the first things I learned when making an <Food-Item> was "
        """
        self.one_time_dialogue["secret_sauce"] = True
        return random.choice(self.script["secret"]).split(".")[0]

    def favorite_food(self):
        """
        "I love eating "
        "My favorite food of all time is "
        "My favorite breakfast food is "
        """
        self.one_time_dialogue["favorite_food"] = True
        return random.choice(self.script["love-food"])

    def old_man_advice(self):
        """
        "My old man used to say that "
        "My favorite pearls of wisdom is "
        """
        self.one_time_dialogue["old-man"] = True
        sent = random.choice(self.script["old-man"])
        end = " My apologies! I get philosophical at times. Back to cooking!"
        return sent + end

    def veggie_advice(self):
        """
        "Always remember, when cooking vegetables it is important to "
        """
        self.one_time_dialogue["veggies"] = True
        return random.choice(self.script["veggies"])

    def affirmations(self):
        """
        Generates nice affirmations when user is following the right steps
        """
        return random.choice(self.paraphrases["affirmation"])

    def nudge(self):
        """
        Starting statement to nudge in the right direction
        """
        return random.choice(self.paraphrases["nudge"])

    def parse_input(self, sent):
        keywords = ["You", "the", "in", "from"]
        tokens = list()
        for word in sent.strip().split():
            if word not in keywords:
                tokens.append(word)
        return tokens

    def sprinkle_GPT(self, tokens):
        if not self.pointer and not self.one_time_dialogue["secret_sauce"]:
            return self.secret_sauce()
        prob = random.random()
        threshold = 0.2
        if prob > threshold:
            if not self.one_time_dialogue["veggies"] and tokens[1] in Veggie_List:
                return self.veggie_advice()
        elif prob < threshold:
            if not self.one_time_dialogue["favorite_food"]:
                return self.favorite_food()
            if not self.one_time_dialogue["old-man"]:
                return self.old_man_advice()
        else:
            return None

    def pointer_loc(self, user_choice):
        current_choices = self.recipe[self.pointer]
        choices = len(current_choices)
        # Non-optional choice action
        if user_choice in current_choices and choices == 1:
            self.pointer += 1
            return True, user_choice
        elif choices == 1:
            return False, current_choices[0]

        # Optional choice action
        if user_choice in current_choices and choices > 1:
            self.non_optional_done.append(user_choice)
            return True, user_choice
        elif user_choice in self.recipe[self.pointer + 1]:
            correct_choice = self.recipe[self.pointer + 1][0]
            self.pointer += 2
            return True, correct_choice
        else:
            return False, self.recipe[self.pointer + 1][0]

    def report_card(self):
        speech = "Great job! You've completed the recipe! Time to taste it.....\n"
        salt = [action for action in self.non_optional_done if "salt" in action]
        pepper = [action for action in self.non_optional_done if "pepper" in action]
        vegs = [
            [action for action in self.non_optional_done if veg in action]
            for veg in Veggie_List
        ]
        if not any(salt):
            speech += " No salt!!! Seriously?\n"
        if not any(pepper):
            speech += "Not a big fan of pepper, eh?\n"
        if not any(vegs):
            speech += " Having some veggies might make it look less blend!\n"
        return speech

    def progress(self, user_choice):
        if self.pointer >= len(Recipe):
            return str()

        # For non-optional case there can only be one correct choice
        # For optional cases, there can be muliple correct choices
        decision, correct_choice = self.pointer_loc(user_choice)
        tokens = self.parse_input(correct_choice)
        if not decision:
            nudge = self.nudge()
            self.pattern_garbage()
            verb = conjugate(verb=tokens[0], tense=PRESENT + PARTICIPLE, number=SG)
            correct = " You should be " + verb + " the " + " ".join(tokens[1:])
            return nudge + correct
        else:
            if self.pointer >= len(Recipe):
                report_card = self.report_card()
                return report_card
            some_GPT = self.sprinkle_GPT(tokens)
            if some_GPT:
                return self.affirmations() + "\n" + some_GPT
            return self.affirmations()
