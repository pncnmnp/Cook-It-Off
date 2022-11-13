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

Recipe = [
    "You preheat the pan",
    "You mix the egg",
    "You cook the egg in the pan",
    "You mix the brocoli",
    "You mix the salt",
    "You mix the pepper",
    "You mix the mushrooms",
    "You serve the final dish!",
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
        marker = "<>"
        for keyword in keywords:
            sent = sent.replace(keyword, marker)
        tokens = [token.strip() for token in sent.split(marker) if token.strip()]
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

    def progress(self, user_choice):
        if self.pointer >= len(Recipe):
            return str()

        correct_choice = self.recipe[self.pointer]
        tokens = self.parse_input(correct_choice)
        if user_choice != correct_choice:
            nudge = self.nudge()
            self.pattern_garbage()
            verb = conjugate(verb=tokens[0], tense=PRESENT + PARTICIPLE, number=SG)
            correct = " You should be " + verb + " the " + tokens[1]
            return nudge + correct
        else:
            some_GPT = self.sprinkle_GPT(tokens)
            self.pointer += 1
            if some_GPT:
                return self.affirmations() + "\n" + some_GPT
            return self.affirmations()
