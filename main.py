from tkinter import *
import pandas as pd
import random
timer = None

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_study = {}
""" TODO: 2. create function to make the button work."""

try:
    data = pd.read_csv("data/known_words.csv")
    # here I get a list of dictionaries.
except FileNotFoundError:
    main_data = pd.read_csv("data/english_words.csv")
    to_study = pd.DataFrame.to_dict(main_data, orient="records")
else:
    to_study = pd.DataFrame.to_dict(data, orient="records")


def known_word():
    to_study.remove(current_card)  # I am taking out a dictionary from list to_learn
    data_1 = pd.DataFrame(to_study)  # crating a data frame
    data_1.to_csv("data/known_words.csv", index=False)  # I become the df into a csv
    next_word()


# here I am going to take out the word from the dictionary my progress, which had been created initially from
# english word, so now I have another dictionary without that word already learned. now I am going to create a new
# DataFrame and the a CSV with this dictionary, and this new one I´ll use it to catch words that I don´t learn yet.
# That is when I have to use try and exceptions, first of all when I only have one CSV I will have to start taking a
# word from there, but then I will be able to pick up words from the dictionary to study.


def next_word():
    global current_card, timer_screen  # timer_screen was already created out of the function, I have to use it here to
    # start counting when the word that I want to appear. so now I can call after_cancel.
    screen.after_cancel(timer_screen)
    current_card = random.choice(to_study)  # here I get a random dictionary from the list.
    english_word = current_card["English"]
    canvas.itemconfig(language, text="English", fill="black")
    canvas.itemconfig(text_word, text=f"{english_word}", fill="black")
    canvas.itemconfig(card_background, image=img_front)
    timer_screen = screen.after(3000, back_card)  # I have to put this function here in order to any time I press the
    # button, after 3 seconds, the translation is going to appear. Remember the relation with the timer_screen outside
    # the function, and the time_screen above. If I don´t work in this way, and I keep on pressing the mouse, after 3
    # seconds the card will change without matter if I stopped or not.


def back_card():
    spanish_word = current_card["Spanish"]
    canvas.itemconfig(language, text="Spanish", fill="white")
    canvas.itemconfig(text_word, text=f"{spanish_word}", fill="white")
    canvas.itemconfig(card_background, image=img_back)
    screen.after_cancel(back_card)
    # here I have to cancel after, otherwise the screen will continue with the new color for ever.


""" TODO: 1. create interface Tk """

screen = Tk()
screen.title("Flashy", )
screen.config(padx=50, pady=50, bg=BACKGROUND_COLOR, highlightthickness=0)

timer_screen = screen.after(3000, back_card)  # number of seconds and a function to call.

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

img_front = PhotoImage(file="images/card_front.png")
img_back = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=img_front)  # I have to create only one background, but I have to
# download both, so I can change the background in the function directly. Otherwise if I create two different background
# here the second one suppress the firs one.

language = canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"), )
text_word = canvas.create_text(400, 263, text="word", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

all_right = PhotoImage(file="images/right.png")  # I charge a image as a button.
button_right = Button(image=all_right, command=known_word)
button_right.config(padx=50, pady=50)
button_right.grid(row=1, column=0)

remember_me = PhotoImage(file="images/wrong.png")
button_wrong = Button(image=remember_me, command=next_word)
button_wrong.config(padx=50, pady=50)
button_wrong.grid(row=1, column=1)

next_word()

screen.mainloop()
