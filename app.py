from tkinter import *
from transformers import QuestionAnsweringPipeline, pipeline
from bs4 import BeautifulSoup
import requests

question = ''
context_input = ''
response = ''
topic = ''

question_answerer = pipeline('question-answering')
text_generation = pipeline('text-generation', model='EleutherAI/gpt-neo-125M')

class gui:
    def __init__(self, root):
        self.root = root
        root.title("AIWriterPy by Antype Cryptous")
        root.geometry("720x480")
        root.configure(background="#16193B")

        self.greeting = Label(text="Digital Homework Automater", background="#16193B", width=30, height=5)
        self.greeting.config(font =("Courier", 18))
        self.greeting.pack()

        self.option_question_answering = Button(text="Question Answering", width=25, height=5, command=self.question_answering)
        self.option_question_answering.pack()

        self.option_text_generation = Button(text="Text Generation", width=25, height=5, command=self.text_generation)
        self.option_text_generation.pack()

    def question_answering(self): # question answerer
        inquiry_input = Entry(width=50) # input topic
        inquiry_input.pack()

        context_input = Entry(width=50) # input url / written context
        context_input.pack()

        def generate_answer():
            global question, context, response
            question = inquiry_input.get()
            url = context_input.get()
            if 'http' in url:
                r = requests.get(url)
                soup = BeautifulSoup(r.content, 'html.parser')
                context = soup.getText()
            else:
                context = url
            response = question_answerer({
                'question': question,
                'context': context,
            })

            answer = Text(root, height = 5, width = 52)
            answer.pack()
            answer.insert(END, response)

        Button(text="Generate!", command=generate_answer).pack()


    def text_generation(self): # essay writer
        topic_input = Entry(width=50) # input topic
        topic_input.pack()

        def generate_text():
            global topic
            topic = topic_input.get()
            res = text_generation(topic, max_length=500, do_sample=True, temperature=0.9)

            generated_text = Text(root, height = 5, width = 52)
            generated_text.pack()
            generated_text.insert(END, res[0]["generated_text"])
            
        Button(text="Generate!", command=generate_text).pack()


root = Tk()
app = gui(root)
root.mainloop()