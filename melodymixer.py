import tkinter as tk
from tkinter import filedialog
from pygame import mixer 
from PIL import Image, ImageTk

from main import run_main

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
        self.window.title("Melody Mixer")
        self.window.geometry("700x500")
        
        # set up visual stuff here for non reactive elements
        self.setup()
        
        # upload text will show the string thats getting inputted after selecting with upload button
        self.upload_text = tk.Label(self.window, text="Select a *.mid file here!.")
        self.upload_text.pack()

        self.upload_button = tk.Button(self.window, text="Upload Audio File", command=self.upload)
        self.upload_button.pack()
        
        # generate calls main
        self.generate_button = tk.Button(self.window, text="Generate", command=self.generate)
        self.generate_button.pack(pady=10)
        
        # play audio using pygame
        self.audio_text = tk.Label(self.window, text="") # this will update after you select play
        self.audio_text.pack(pady=10)

        self.play_button = tk.Button(self.window, text="Play Audio", command=self.results)
        self.play_button.pack(pady=10)
        
        # close program
        self.close_button = tk.Button(self.window, text="Close", command=self.window.destroy)
        self.close_button.pack(pady=10, padx=5)

        # calls main loop
        self.start()

    
    # set visuals and components here that arent reactive (soph)
    def setup(self):
        
        # set title
        self.label = tk.Label(self.window, text="Melody Mixer")
        self.label.pack(pady=10)

        # Subheading
        subhead_text = "will generate a composed song based on your inputs in a matter of minutes! " \
                       "Please upload one audio file to begin composing." \
                        "by Jess, Cass, Soph, Jas " 
        subhead_label = tk.Label(self.window, text=subhead_text, wraplength=400)
        subhead_label.pack(pady=10)

        
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
        run_main(self.INPUT_FILE) # set the output to this to self.OUTPUT_FILE
    

    # listen to the results
    def results(self, output_file=None):
        
        # select the output file if one wasn't given
        if output_file is None:
            output_file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.midi;*.mp3;*.wav;")])
        
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


# # Title
# title_image = tk.PhotoImage(file="static/Group 4.png")  # Assuming this is your image path
# title_label = tk.Label(self.window, image=title_image)
# title_label.grid(row=0, column=0)

# # Subheading
# subhead_text = "Welcome to Melody Mixer, a generative AI app that can help write " \
#                "a fully composed song based on your inputs in a matter of minutes! " \
#                "Please upload one audio file to begin composing."
# subhead_label = tk.Label(window, text=subhead_text, wraplength=400)
# subhead_label.grid(row=1, column=0)


# # Audio playback section


# # Next page button (placeholder)
# next_page_button = tk.Button(window, text="Next Page", command=start_nn)
# next_page_button.grid(row=5, column=0)

# # Run the Tkinter event loop
# window.mainloop()
