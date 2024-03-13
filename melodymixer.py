import tkinter as tk
from tkinter import filedialog
from pygame import mixer 
from PIL import Image, ImageTk

#from main import run_main

def upload_file(upload_text):
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mid;")])
            
    temp = file_path.rsplit('/',1)[-1]
    temp = temp.replace('.mid', '')
    
    if temp:
        upload_text.config(text="You Selected: " + temp)
        
    return temp


class MelodyMixer:

    def __init__(self):

        self.INPUT_FILE = ''
        self.OUTPUT_FILE = ''
        
        # create window
        self.window = tk.Tk()
        self.window.configure(bg='white')
        self.logo_img = Image.open("static/Group 4.png")
        self.logophoto = ImageTk.PhotoImage(self.logo_img)
        self.logo_lable = tk.Label(self.window, image=self.logophoto, bg='white')
        self.logo_lable.grid(row = 0 , column = 0, columnspan=3, pady=10, padx=10)
        self.window.geometry("800x600")
        self.window.title("Melody Mixer")
        
        # set up visual stuff here for non reactive elements
        self.setup()
        
        # upload text will show the string thats getting inputted after selecting with upload button
        self.upload_text = tk.Label(self.window, text="Select a *.mid file here!", bg='white')
        self.upload_text.grid(row=3, column=0)
        self.upload_text.config(font=("Kozuka Mincho Pro R", 12))

        self.up_img = Image.open("static/Upload.png")
        self.up_button = ImageTk.PhotoImage(self.up_img)
        self.upload_button = tk.Button(self.window, image=self.up_button, bg='white', borderwidth=0,cursor='hand2',highlightthickness = 0, command=self.upload)
        self.upload_button.grid(row=2, column=0)
        
        # generate calls main
        self.mix_img = Image.open("static/Group 9.png")
        self.mix_button = ImageTk.PhotoImage(self.mix_img)
        self.generate_button = tk.Button(self.window, image=self.mix_button,cursor='hand2', borderwidth=0, highlightthickness = 0, command=self.generate)
        self.generate_button.grid(row=4, column = 0, pady=10, padx=40)
        
        # play audio using pygame
        self.audio_text = tk.Label(self.window, text="") # this will update after you select play
        self.audio_text.grid(row=0, column=2, pady=10, padx=10)
        self.audiolabel = tk.Label(self.window, text="Play your song here!", bg='white')
        self.audiolabel.grid(row=3, column=2)
        self.audiolabel.config(font=("Kozuka Mincho Pro R", 12))
        self.play_img = Image.open("static/colourPlay.png")
        self.play_butt = ImageTk.PhotoImage(self.play_img)
        self.play_button = tk.Button(self.window, image=self.play_butt,bg="white",borderwidth=0, cursor='hand2', command=self.results)
        self.play_button.grid(row=2, column=2)
        
        # close program
        self.close_img = Image.open("static/Group 8.png")
        self.close_butt = ImageTk.PhotoImage(self.close_img)
        self.close_button = tk.Button(self.window, image=self.close_butt,borderwidth=0, cursor='hand2', command=self.window.destroy)
        self.close_button.grid(row=4, column=2, padx=10, pady=40)

        # calls main loop
        self.start()

    
    # set visuals and components here that arent reactive (soph)
    def setup(self):
        

        # Subheading
        subhead_text = "Welcome to Melody Mixer a generative AI app that can help write" \
                        " a fully composed song based on your inputs in a matter of minutes!"\
                        " Please upload an audio file to begin composing." \
                        " \n By Jess, Cass, Soph, and Jas " 
        subhead_label = tk.Label(self.window, text=subhead_text, bg = 'white', wraplength=650)
        subhead_label.grid(row=1, column=0, columnspan=3, pady=40,padx=70)
        subhead_label.config(font=("Arial", 12))

        
    def button_state(self, button):
        if button.cget("state") == "normal":
            button.configure(state="disabled")
        else:
            button.configure(state="normal")


    # select input file with fialdialog
    def upload(self):
        self.INPUT_FILE = upload_file(self.upload_text)
        print('[*] sent input file', self.INPUT_FILE)
        
        # make sure there was a file selected then disable button
        if self.INPUT_FILE != '':
            self.button_state(self.upload_button)


    # generate based off input file
    def generate(self):
        print('[*] generating')
        self.button_state(self.generate_button)
        #self.loading_img = Image.open("static/Loading.gif")
        #self.loading = ImageTk.PhotoImage(self.loading_img)
        #self.loading_label = tk.Label(self.window, image=self.loading, bg='white')
        #self.loading_label.grid(row=3, column=1, pady=10, padx=10)
        
        #self.OUTPUT_FILE=run_main(self.INPUT_FILE) # set the output to this to self.OUTPUT_FILE
        
        #self.loading_label.destroy()
       

    # listen to the results
    def results(self, output_file=None):
        
        # select the output file if one wasn't given
        if output_file is None:
            output_file=self.OUTPUT_FILE
            #output_file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mid;*.mp3;*.wav;")])
        
        if output_file:    
            # disable button
            self.button_state(self.play_button)

            mixer.init()
            mixer.music.load(output_file)
            mixer.music.play()
            
            # show what theyre playing
            temp = output_file.rsplit('/',1)[-1]
            self.audio_text.config(text="Now Playing " + temp)
        
    
    def start(self):
        self.window.mainloop()

 
    def reset(self):
        self.window.destroy()
        self.__init__()
        
def main():
    MelodyMixer()

if __name__ == "__main__":
    main()


