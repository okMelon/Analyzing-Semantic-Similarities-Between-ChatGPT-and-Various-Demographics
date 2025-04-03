import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import analysis as analy

MFONT = "Helvetica"
BIGSIZE = 20
BODYSIZE = 12

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analyzing Semantic Similarities")
        self.geometry("800x600")
        
        # Container frame to hold all pages
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Dictionary to hold all frames/pages
        self.frames = {}
        
        # Create all pages
        for F in (MainPage, Page1, Page2, Page3, Page4):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Show the main page first
        self.show_frame(MainPage)
    
    def show_frame(self, cont):
        """Show a frame for the given page class"""
        frame = self.frames[cont]
        frame.tkraise()

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = ttk.Label(self, text="Main Menu", font=(MFONT, BIGSIZE))
        label.pack(pady=30)
        
        # Create 4 buttons
        button1 = ttk.Button(self, text="Create An Entry",
            command=lambda: controller.show_frame(Page1))
        button2 = ttk.Button(self, text="Compare Two Entries",
            command=lambda: controller.show_frame(Page2))
        button3 = ttk.Button(self, text="Create A Question",
            command=lambda: controller.show_frame(Page3))
        button4 = ttk.Button(self, text="View Graphs",
            command=lambda: controller.show_frame(Page4))
        
        # Pack buttons with some padding
        button1.pack(fill="x", padx=100, pady=10)
        button2.pack(fill="x", padx=100, pady=10)
        button3.pack(fill="x", padx=100, pady=10) 
        button4.pack(fill="x", padx=100, pady=10)

class PageTemplate(tk.Frame):
    """Template for all sub-pages with back button"""
    def __init__(self, parent, controller, page_name):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)

        # Back button in top left
        back_button = ttk.Button(self, text="← Back to Main",
            command=lambda: controller.show_frame(MainPage))
        back_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        
        # Page title
        label = ttk.Label(self, text=page_name, font=(MFONT, BIGSIZE))
        label.grid(row=0, column=1, sticky="w", pady=25)

        # Main content
        self.content_area = tk.Frame(self)
        self.content_area.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)

# This page is for creating new survey entries
class Page1(PageTemplate):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Page 1 - Survey Form")
        
        # Create a scrollable canvas
        self.canvas = tk.Canvas(self.content_area, borderwidth=0)
        scrollbar = ttk.Scrollbar(self.content_area, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
                )
        )
        self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Form fields configuration
        self.fields = [
            {"label": "What is your name?", "type": "text", "height": 1},
            {"label": "What is your age?", "type": "text", "height": 1},
            {"label": "What is your gender identity?", "type": "radio", "options": ["Male", "Female", "Non-binary", "Prefer not to say/Other"],"height": 1},
            {"label": "What is your ethnicity?", "type": "radio", "options": ["White/Caucasian", "Asian - Eastern", "Asian - Indian", "Hispanic", "Black", "Native American", "Prefer not to answer"], "height": 1},
            {"label": "What is the highest level of education you've completed?", "type": "radio", "options": ["Highschool Diploma", "Bachelor's Degree", "Master's Degree", "Prefer not to answer"], "height": 1},
            {"label": "How much total gross income did all members of your household earn in the past fiscal year?", "type": "radio", "options": ["$0 - $4,999", "$5,000 - $7,499", "$7,500 - $9,999", "$10,000 - $12,499", "$12,500 - $14,999", "$15,000 - $19,999", "$20,000 - $24,999", "$25,000 - $29,999", "$30,000 - $34,999", "$35,000 - $39,999", "$40,000 - $49,999", "$50,000 - $59,999", "$60,000 - $74,999", "$75,000 - $99,999", "$100,000 - $149,999", "$150,000+", "Prefer not to answer"], "height": 1},
            {"label": "What does the phrase: \"Actions speak louder than words\" mean?", "type": "text", "height": 5},
            {"label": "What makes someone a good leader?", "type": "text", "height": 5},
            {"label": "What are some red flags that indicate someone is untrustworthy?", "type": "text", "height": 5},
            {"label": "What does it mean to be successful?", "type": "text", "height": 5},
            {"label": "What does it mean to be happy?", "type": "text", "height": 5},
            {"label": "Imagine you lost something valuable to you. What would you do?", "type": "text", "height": 5},
            {"label": "Complete the prompt: The electrician was...", "type": "text", "height": 5},
            {"label": "Billy walked into his kitchen and saw a broken glass on the floor. What do you think happened?", "type": "text", "height": 5}
            ]
        
        # Store all input widgets
        self.input_widgets = []
        
        # Create form elements
        for i, field in enumerate(self.fields):
            label = ttk.Label(self.scrollable_frame, text=field["label"])
            label.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            
            if field["type"] == "text":
                if field["height"] > 1:
                    text_widget = tk.Text(
                        self.scrollable_frame,
                        height=field["height"],
                        width=50,
                        wrap=tk.WORD
                    )
                    text_scroll = ttk.Scrollbar(self.scrollable_frame, orient="vertical", command=text_widget.yview)
                    text_widget.configure(yscrollcommand=text_scroll.set)
                    text_widget.grid(row=i, column=1, padx=10, pady=(0, 10), sticky="ew")
                    text_scroll.grid(row=i, column=2, sticky="ns", pady=(0, 10))
                    self.input_widgets.append(text_widget)
                else:
                    entry = ttk.Entry(self.scrollable_frame, width=50)
                    entry.grid(row=i, column=1, padx=10, pady=(0, 10), sticky="ew")
                    self.input_widgets.append(entry)
            
            elif field["type"] == "radio":
                var = tk.StringVar()
                radio_frame = ttk.Frame(self.scrollable_frame)
                radio_frame.grid(row=i, column=1, padx=10, pady=(0, 10), sticky="w")
                
                for j, option in enumerate(field["options"]):
                    rb = ttk.Radiobutton(
                        radio_frame,
                        text=option,
                        variable=var,
                        value=option
                    )
                    rb.pack(anchor="w")
                
                # Store both the frame and variable
                self.input_widgets.append((radio_frame, var))
        self.scrollable_frame.columnconfigure(1, weight=1)

        # Submit button
        submit_btn = ttk.Button(
            self.scrollable_frame,
            text="Submit Form",
            command=self.submit_form
        )
        submit_btn.grid(row=len(self.fields), column=0, columnspan=3, pady=20)

    def submit_form(self):
        results = {}
        widget_index = 0
        
        for field in self.fields:
            if field["type"] == "text":
                widget = self.input_widgets[widget_index]
                if field["height"] > 1:
                    results[field["label"]] = widget.get("1.0", "end-1c")
                else:
                    results[field["label"]] = widget.get()
                widget_index += 1
            elif field["type"] == "radio":
                frame, var = self.input_widgets[widget_index]
                results[field["label"]] = var.get()
                widget_index += 1
        
        # My brain is fried and this works
        variable = 0
        a = ["", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        print("\nForm Results:")
        for question, answer in results.items():
            print(f"{question}: {answer}")
            a[variable] = answer
            variable += 1

        analy.add_user(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11], a[12], a[13])
        
        messagebox.showinfo("Submission Complete", "Thank you for your responses!")

  
    


class Page3(PageTemplate):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Create A New Question")
        
        # Create a scrollable canvas
        self.canvas = tk.Canvas(self.content_area, borderwidth=0)
        scrollbar = ttk.Scrollbar(self.content_area, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
                )
        )
        self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Form fields configuration
        self.fields = [
            {"label": "What is your question?", "type": "text", "height": 1},
            {"label": "What is your response to the question you made?", "type": "text", "height": 5},
            ]
        
        # Store all input widgets
        self.input_widgets = []
        
        # Create form elements
        for i, field in enumerate(self.fields):
            label = ttk.Label(self.scrollable_frame, text=field["label"], font=(MFONT, BODYSIZE))
            label.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            
            
            if field["height"] > 1:
                text_widget = tk.Text(
                    self.scrollable_frame,
                    height=field["height"],
                    width=50,
                    wrap=tk.WORD
                )
                text_scroll = ttk.Scrollbar(self.scrollable_frame, orient="vertical", command=text_widget.yview)
                text_widget.configure(yscrollcommand=text_scroll.set)
                text_widget.grid(row=i, column=1, padx=10, pady=(0, 10), sticky="ew")
                text_scroll.grid(row=i, column=2, sticky="ns", pady=(0, 10))
                self.input_widgets.append(text_widget)
            else:
                entry = ttk.Entry(self.scrollable_frame, width=50)
                entry.grid(row=i, column=1, padx=10, pady=(0, 10), sticky="ew")
                self.input_widgets.append(entry)
        self.scrollable_frame.columnconfigure(1, weight=1)

        # Submit button
        submit_btn = ttk.Button(
            self.scrollable_frame,
            text="Submit Form",
            command=self.submit_form
        )
        submit_btn.grid(row=len(self.fields), column=0, columnspan=3, pady=20)

    def submit_form(self):
        results = {}
        widget_index = 0
        
        for field in self.fields:
            if field["type"] == "text":
                widget = self.input_widgets[widget_index]
                if field["height"] > 1:
                    results[field["label"]] = widget.get("1.0", "end-1c")
                else:
                    results[field["label"]] = widget.get()
                widget_index += 1
            elif field["type"] == "radio":
                frame, var = self.input_widgets[widget_index]
                results[field["label"]] = var.get()
                widget_index += 1
        
        # My brain is fried and this works
        variable = 0
        a = ["", ""]
        print("\nForm Results:")
        for question, answer in results.items():
            print(f"{question}: {answer}")
            a[variable] = answer
            variable += 1
        chatgpt_response = ""
        chatgpt_response, similarity = analy.bonus_questions(a[0], a[1])
        
        label = ttk.Label(self.scrollable_frame, text=chatgpt_response, wraplength=400, font=(MFONT, BODYSIZE))
        label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")
        label = ttk.Label(self.scrollable_frame, text=f"Similarity Score: {similarity:.4f}", font=(MFONT, BODYSIZE))
        label.grid(row=3, column=1, padx=10, pady=(10, 0), sticky="w")

class Page2(PageTemplate):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Compare Two Entries")
        
        # Create a scrollable canvas
        self.canvas = tk.Canvas(self.content_area, borderwidth=0)
        scrollbar = ttk.Scrollbar(self.content_area, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
                )
        )
        self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Form fields configuration
        self.fields = [
            {"label": "What is the first entry's uid?", "type": "text", "height": 1},
            {"label": "What is the second entry's uid?", "type": "text", "height": 1},
            ]
        
        # Store all input widgets
        self.input_widgets = []
        
        # Create form elements
        for i, field in enumerate(self.fields):
            label = ttk.Label(self.scrollable_frame, text=field["label"], font=(MFONT, BODYSIZE))
            label.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            
            
            if field["height"] > 1:
                text_widget = tk.Text(
                    self.scrollable_frame,
                    height=field["height"],
                    width=50,
                    wrap=tk.WORD
                )
                text_scroll = ttk.Scrollbar(self.scrollable_frame, orient="vertical", command=text_widget.yview)
                text_widget.configure(yscrollcommand=text_scroll.set)
                text_widget.grid(row=i, column=1, padx=10, pady=(0, 10), sticky="ew")
                text_scroll.grid(row=i, column=2, sticky="ns", pady=(0, 10))
                self.input_widgets.append(text_widget)
            else:
                entry = ttk.Entry(self.scrollable_frame, width=50)
                entry.grid(row=i, column=1, padx=10, pady=(0, 10), sticky="ew")
                self.input_widgets.append(entry)
        self.scrollable_frame.columnconfigure(1, weight=1)

        # Submit button
        submit_btn = ttk.Button(
            self.scrollable_frame,
            text="Submit Form",
            command=self.submit_form
        )
        submit_btn.grid(row=len(self.fields), column=0, columnspan=3, pady=20)

    def submit_form(self):
        results = {}
        widget_index = 0
        
        for field in self.fields:
            if field["type"] == "text":
                widget = self.input_widgets[widget_index]
                if field["height"] > 1:
                    results[field["label"]] = widget.get("1.0", "end-1c")
                else:
                    results[field["label"]] = widget.get()
                widget_index += 1
            elif field["type"] == "radio":
                frame, var = self.input_widgets[widget_index]
                results[field["label"]] = var.get()
                widget_index += 1
        
        # My brain is fried and this works
        variable = 0
        a = ["", ""]
        print("\nForm Results:")
        for question, answer in results.items():
            print(f"{question}: {answer}")
            a[variable] = answer
            variable += 1
        q1sim, q2sim, q3sim, q4sim, q5sim, q6sim, q7sim, q8sim, qtsim = analy.compare_every(a[0], a[1])
        
        
        label = ttk.Label(self.scrollable_frame, text=f"Question 1 similarity: {q1sim:3f}\nQuestion 2 similarity: {q2sim:3f}\nQuestion 3 similarity: {q3sim:3f}\nQuestion 4 similarity: {q4sim:3f}\nQuestion 5 similarity: {q5sim:3f}\nQuestion 6 similarity: {q6sim:3f}\nQuestion 7 similarity: {q7sim:3f}\nQuestion 8 similarity: {q8sim:3f}\n", wraplength=400, font=(MFONT, BODYSIZE))
        label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")
        label = ttk.Label(self.scrollable_frame, text=f"Total Similarity: {qtsim:.4f}", font=(MFONT, BODYSIZE))
        label.grid(row=3, column=1, padx=10, pady=(10, 0), sticky="w")

class Page4(PageTemplate):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Page 4")
        
        content = ttk.Label(self, text="This is Page 4 content")
        content.grid(row=1, column=0, columnspan=2)

if __name__ == "__main__":
    app = App()
    app.mainloop()