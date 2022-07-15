from tkinter import *
from transformers import QuestionAnsweringPipeline, pipeline # GPT-Neo is only available for PyTorch, not TensorFlow.
from bs4 import BeautifulSoup
from progress_bar import progress_bar
import requests
import json
import sys
import os

question_answerer = pipeline('question-answering')
text_generation = pipeline('text-generation', model='EleutherAI/gpt-neo-125M')

class gui:
    def __init__(self, root):
        self.root = root
        root.title("AIWriterPy by @antype")
        root.geometry('{}x{}'.format(600, 600))
        root.configure(background="#16193B")

        self.set_layout = 0
        self.json_formatted_str = None
        self.improvised_text = None

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
        self.set_layout = 1

        def generate_answer():
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
            self.json_formatted_str = json.dumps(response, indent=2)

        while self.set_layout == 1:
            inquiry_input = Entry(width=60) # input question
            inquiry_input.insert(0, "Enter your question here...")
            context_input = Entry(width=60) # input url / written context
            context_input.insert(0, "Source (url / written context)...")
            question_answering_button = Button(text="Generate!", command=generate_answer)

            inquiry_input.pack()
            context_input.pack()
            question_answering_button.pack()

            if self.json_formatted_str is not None:

                answer = Text(root, height = 10, width = 60)
                answer.pack()
                answer.insert(END, self.json_formatted_str)
        else:
            pass


    def text_generation(self): # essay writer
        self.set_layout = 2

        def generate_text():
            topic = sentence_starter_input.get()
            res = text_generation(topic, max_length=250, do_sample=True, temperature=0.9)
            self.improvised_text = res[0]["generated_text"]

        while self.set_layout == 2:
            sentence_starter_input = Entry(width=60) # input topic for discussion
            sentence_starter_input.insert(0, "Enter your chosen topic here...")
            text_generation_button = Button(text="Generate!", command=generate_text)

            sentence_starter_input.pack()
            text_generation_button.pack()

            if self.improvised_text is not None:
                generated_text = Text(root, height = 10, width = 60)
                generated_text.pack()
                generated_text.insert(END, self.improvised_text)
        else:
            pass

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