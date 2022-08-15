from tkinter import *
from transformers import QuestionAnsweringPipeline, pipeline # GPT-Neo is only available for PyTorch, not TensorFlow.
from bs4 import BeautifulSoup
import requests
import json
import re

question_answerer = pipeline('question-answering')
text_generation = pipeline('text-generation', model='EleutherAI/gpt-neo-125M')

_width = 45

class gui:
    def __init__(self, root):
        self.root = root
        root.title("AI Toolbox")
        root.geometry('{}x{}'.format(500, 600))
        root.configure(background="#16193B")
        self.ai_tools = ai_tools

        # self.status_code = 0

        self.inquiry_input = Entry(width=_width) # input question
        self.temp_text = ["Enter your question here...", "Source (url / written context)...", "Enter your chosen topic here..."]
        self.inquiry_input.insert(0, self.temp_text[0])
        self.inquiry_input.bind("<FocusIn>", self.del_temp_text(self.inquiry_input))

        self.context_input = Entry(width=_width) # input url / written context
        self.context_input.insert(0, self.temp_text[1])
        self.context_input.bind("<FocusIn>", self.del_temp_text(self.context_input))

        self.question_answering_button = Button(text="Generate!")
        self.question_answering_button.bind("<Button-1>", self.question_answering_buttonFunc)

        self.sentence_starter_input = Entry(width=_width) # input topic for discussion
        self.sentence_starter_input.insert(0, self.temp_text[2])
        self.context_input.bind("<FocusIn>", self.del_temp_text(self.sentence_starter_input))

        self.text_generation_button = Button(text="Generate!")
        self.text_generation_button.bind("<Button-1>", self.text_generation_buttonFunc)

        self.prompt = Text(root, height = 20, width = _width+10)

        self.greeting = Label(text="INS Homework Assistance", background="#16193B", width=30, height=5)
        self.greeting.place(x=80, y=0)
        self.greeting.config(font =("Courier", 18))

        self.option_question_answering = Button(text="Answer Extractor", width=12, height=2)
        self.option_question_answering.place(x=20, y=100)
        self.option_question_answering.bind("<Button-1>", self.genFuncGui1)

        self.option_text_generation = Button(text="Text Generation", width=12, height=2)
        self.option_text_generation.place(x=170, y=100)
        self.option_text_generation.bind("<Button-1>", self.genFuncGui2)

        self.clear_button = Button(text="Citation", width=12, height=2)
        self.clear_button.place(x=320, y=100)
        self.clear_button.bind("<Button-1>", self.citation)

    def del_temp_text(self, func):
        if any(i in func.get() for i in self.temp_text):
            func.delete(0, 'end')

    def genFuncGui1(self, *kwargs):
        self.clearFunction()
        self.inquiry_input.place(x=20, y=160)
        self.context_input.place(x=20, y=190)
        self.question_answering_button.place(x=160, y=230)

    def genFuncGui2(self, *kwargs):
        self.clearFunction()
        self.sentence_starter_input.place(x=20, y=160)
        self.text_generation_button.place(x=160, y=200)

    def output(self, pos_x, pos_y, feed, *kwargs):
        if (self.prompt['state'] == DISABLED):
            self.prompt['state'] = NORMAL
        else:
            self.prompt['state'] = NORMAL
        self.prompt.place(x=pos_x, y=pos_y)
        self.prompt.delete('1.0', END)
        self.prompt.insert(END, feed)
        self.prompt.config(state=DISABLED)

    def question_answering_buttonFunc(self, *kwargs):
        self.ai_tools.__contains__(context_feed=self.context_input.get(), question=self.inquiry_input.get())
        self.output(pos_x=20, pos_y=270, feed=json_formatted_str)

    def text_generation_buttonFunc(self, *kwargs):
        self.ai_tools.text_generation(topic=self.sentence_starter_input.get())
        self.output(pos_x=20, pos_y=240, feed=improvised_text)

    def clearFunction(self, *kwargs):
        self.inquiry_input.place_forget()
        self.context_input.place_forget()
        self.question_answering_button.place_forget()
        self.sentence_starter_input.place_forget()
        self.text_generation_button.place_forget()
        self.prompt.place_forget()

    def citation(self, *kwargs):
        self.clearFunction()
        kv = re.compile(r'\b(?P<key>\w+)={(?P<value>[^}]+)}')
        bibtex_file = """
        @software{gpt-neo,

        author       = {Black, Sid and
                        Leo, Gao and
                        Wang, Phil and
                        Leahy, Connor and
                        Biderman, Stella},
        title        = {{GPT-Neo: Large Scale Autoregressive Language 
                        Modeling with Mesh-Tensorflow}},
        month        = mar,
        year         = 2021,
        note         = {{If you use this software, please cite it using 
                        these metadata.}},
        publisher    = {Zenodo},
        version      = {1.0},
        doi          = {10.5281/zenodo.5297715},
        url          = {https://doi.org/10.5281/zenodo.5297715}
        }

        @article{gao2020pile,
        title={The Pile: An 800GB Dataset of Diverse Text for Language Modeling},
        author={Gao, Leo and Biderman, Stella and Black, Sid and Golding, Laurence and Hoppe, Travis and Foster, Charles and Phang, Jason and He, Horace and Thite, Anish and Nabeshima, Noa and others},
        journal={arXiv preprint arXiv:2101.00027},
        year={2020}
        }
        """
        json_formatted_bib = json.dumps(dict(kv.findall(bibtex_file)), indent=2)
        self.output(pos_x=20, pos_y=160, feed=json_formatted_bib)

class ai_tools:
    def __contains__(context_feed, question):

    # def question_answering(context_feed, question, *kwargs):
        global json_formatted_str

        if 'http' in context_feed:
            r = requests.get(context_feed)
            soup = BeautifulSoup(r.content, 'html.parser')
            context = soup.getText().replace("\n", "")     
        else:
            context = context_feed
        response = question_answerer({
            'question': question,
            'context': context
        })
        json_formatted_str = json.dumps(response, indent=2)
        

    def text_generation(topic):
        global improvised_text

        res = text_generation(topic, max_length=700, do_sample=True, temperature=0.9)
        improvised_text = res[0]["generated_text"]


root = Tk()
app = gui(root)
root.mainloop()
