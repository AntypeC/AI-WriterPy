from tkinter import *
from transformers import QuestionAnsweringPipeline, pipeline
from bs4 import BeautifulSoup
from progress_bar import progress_bar
import requests
import json
import sys
import os

question = ''
context_input = ''
response = ''
topic = ''

question_answerer = pipeline('question-answering')
text_generation = pipeline('text-generation', model='EleutherAI/gpt-neo-125M')

class gui:
    def __init__(self, root):
        self.root = root
        root.title("AIWriterPy by @antype")
        root.geometry('{}x{}'.format(500, 600))
        root.configure(background="#16193B")

        self.greeting = Label(text="INS Homework Assistance", background="#16193B", width=30, height=5)
        self.greeting.config(font =("Courier", 18))

        self.option_question_answering = Button(text="Answer Extractor", width=12, height=2, command=self.question_answering)
        self.option_text_generation = Button(text="Text Generation", width=12, height=2, command=self.text_generation)
        self.clear_button = Button(text="Reset", width=12, height=2, command=self.restart_program)

        self.greeting.pack()
        self.option_question_answering.pack()
        self.option_text_generation.pack()
        self.clear_button.pack()

    def question_answering(self): # question answerer
        inquiry_input = Entry(width=60) # input topic
        context_input = Entry(width=60) # input url / written context

        inquiry_input.pack()
        context_input.pack()

        def generate_answer():
            global question, context, response
            question = inquiry_input.get()
            url = context_input.get()
            if 'http' in url:
                r = requests.get(url)
                soup = BeautifulSoup(r.content, 'html.parser')
                context = soup.getText().replace("\n", "")     
            else:
                context = url
            response = question_answerer({
                'question': question,
                'context': context
            })
            json_formatted_str = json.dumps(response, indent=2)

            answer = Text(root, height = 10, width = 60)
            answer.pack()
            answer.insert(END, json_formatted_str)

            # return inquiry_input, context_input, answer

        Button(text="Generate!", command=generate_answer).pack()


    def text_generation(self): # essay writer
        sentence_starter_input = Entry(width=60) # input topic
        sentence_starter_input.pack()

        def generate_text():
            global topic
            topic = sentence_starter_input.get()
            res = text_generation(topic, max_length=500, do_sample=True, temperature=0.9)

            generated_text = Text(root, height = 10, width = 60)
            generated_text.pack()
            generated_text.insert(END, res[0]["generated_text"])
            
            # return sentence_starter_input, generated_text
            
        Button(text="Generate!", command=generate_text).pack()

    def restart_program(self):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        python = sys.executable
        os.execl(python, python, * sys.argv)
        progress_bar(500)

root = Tk()
app = gui(root)
root.mainloop()