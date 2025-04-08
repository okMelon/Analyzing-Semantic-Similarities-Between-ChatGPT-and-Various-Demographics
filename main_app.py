import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import analysis as analy
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

MFONT = "Helvetica"
BIGSIZE = 24
BODYSIZE = 14



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
        
        style = ttk.Style()
        style.configure("Big.TButton", font=("Helvetica", 16), padding=20)
        # Pack buttons with some padding
        button1.configure(style="Big.TButton")
        button1.pack(fill="x", padx=100, pady=20)
        button2.configure(style="Big.TButton")
        button2.pack(fill="x", padx=100, pady=20)
        button3.configure(style="Big.TButton")
        button3.pack(fill="x", padx=100, pady=20) 
        button4.configure(style="Big.TButton")
        button4.pack(fill="x", padx=100, pady=20)

class PageTemplate(tk.Frame):
    """Template for all sub-pages with back button"""
    def __init__(self, parent, controller, page_name):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        controller.option_add("*Font", "Helvetica 16")

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
            {"label": "What is the highest level of education you've completed?", "type": "radio", "options": ["Lower than highschool degree", "Highschool Diploma", "Bachelor's Degree", "Master's Degree", "Prefer not to answer"], "height": 1},
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
            label = ttk.Label(self.scrollable_frame, text=field["label"], font=("Helvetica", BODYSIZE))
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
                        value=option,
                        style="Big.TRadiobutton"
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
        
        widget_index = 0
        for field in self.fields:
            widget = self.input_widgets[widget_index]
            if field["type"] == "text":
                if field["height"] > 1:
                    widget.delete("1.0", "end")
                else:
                    widget.delete(0, "end")
            elif field["type"] == "radio":
                _, var = widget
                var.set("")  # Reset selection
            widget_index += 1
        
        messagebox.showinfo("Submission Complete", "Thank you for your responses!")
        self.controller.show_frame(MainPage)


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
        q1sim, q2sim, q3sim, q4sim, q5sim, q6sim, q7sim, q8sim, qtsim = analy.compare_every(int(a[0]), int(a[1]))
        
        
        label = ttk.Label(self.scrollable_frame, text=f"Question 1 similarity: {q1sim:3f}\nQuestion 2 similarity: {q2sim:3f}\nQuestion 3 similarity: {q3sim:3f}\nQuestion 4 similarity: {q4sim:3f}\nQuestion 5 similarity: {q5sim:3f}\nQuestion 6 similarity: {q6sim:3f}\nQuestion 7 similarity: {q7sim:3f}\nQuestion 8 similarity: {q8sim:3f}\n", wraplength=400, font=(MFONT, BODYSIZE))
        label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")
        label = ttk.Label(self.scrollable_frame, text=f"Total Similarity: {qtsim:.4f}", font=(MFONT, BODYSIZE))
        label.grid(row=3, column=1, padx=10, pady=(10, 0), sticky="w")

class Page4(PageTemplate):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Bar Charts")

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

        LENGTH, WIDTH, DPI = 8, 6, 100
        def update_graph():
        # Graph 1. Age values.
            demographics = analy.create_graph_data()
            # Ages data + labels
            ages_labels = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
            ages_values = [
                analy.average_dem(demographics[0][0], "rtc"), 
                analy.average_dem(demographics[0][1], "rtc"), 
                analy.average_dem(demographics[0][2], "rtc"), 
                analy.average_dem(demographics[0][3], "rtc"), 
                analy.average_dem(demographics[0][4], "rtc"), 
                analy.average_dem(demographics[0][5], "rtc")]

            # Create a matplotlib Figure
            fig = Figure(figsize=(LENGTH, WIDTH), dpi=DPI)
            ax = fig.add_subplot(111)
            ax.bar(ages_labels, ages_values)
            ax.set_ylim(0, 1)
            ax.set_title("Response similarity to ChatGPT responses across age groups")
            ax.set_xlabel("Age ranges")
            ax.set_ylabel("Average similarity score across all questions")

            # Embed the chart in the scrollable_frame
            canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=20)
        # Graph 2. Gender values.
            gender_labels = ['Male', 'Female', 'Non-Binary']
            gender_values = [
                analy.average_dem(demographics[1][0], "rtc"), 
                analy.average_dem(demographics[1][1], "rtc"), 
                analy.average_dem(demographics[1][2], "rtc")]

            # Create a matplotlib Figure
            fig = Figure(figsize=(LENGTH, WIDTH), dpi=DPI)
            ax = fig.add_subplot(111)
            ax.bar(gender_labels, gender_values)
            ax.set_ylim(0, 1)
            ax.set_title("Response similarity to ChatGPT responses across gender groups")
            ax.set_xlabel("Genders ranges")
            ax.set_ylabel("Average similarity score across all responses within given gender groups")

            # Embed the chart in the scrollable_frame
            canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=20)
        # Graph 3. Ethnicity values.
            ethnicity_labels = ['White/Caucasian', 'Asian - Eastern', 'Asian - Indian', 'Hispanic', 'Black', 'Native American']
            ethnicity_values = [
                analy.average_dem(demographics[2][0], "rtc"), 
                analy.average_dem(demographics[2][1], "rtc"), 
                analy.average_dem(demographics[2][2], "rtc"),
                analy.average_dem(demographics[2][3], "rtc"),
                analy.average_dem(demographics[2][4], "rtc"),
                analy.average_dem(demographics[2][5], "rtc")]

            # Create a matplotlib Figure
            fig = Figure(figsize=(LENGTH, WIDTH), dpi=DPI)
            ax = fig.add_subplot(111)
            ax.bar(ethnicity_labels, ethnicity_values)
            ax.set_ylim(0, 1)
            ax.set_xticklabels(ethnicity_labels, rotation=15, ha='center')  # or rotation=45, etc.
            ax.set_title("Response similarity to ChatGPT responses across ethnicity groups")
            ax.set_xlabel("Ethnicity ranges")
            ax.set_ylabel("Average similarity score across all responses within given ethnicity groups")

            # Embed the chart in the scrollable_frame
            canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=20)
        # Graph 4. Education values.
            # Education 0: Highschool Diploma, 1: Bachelor's Degree, 2: Master's Degree, 3: Prefer not to answer, 4: Lower than highschool level education, 5: unlisted
            education_labels = ["Lower than highschool degree", 'Highschool Diploma', "Bachelor's Degree", "Master's Degree"]
            education_values = [
                analy.average_dem(demographics[3][4], "rtc"), 
                analy.average_dem(demographics[3][0], "rtc"), 
                analy.average_dem(demographics[3][1], "rtc"),
                analy.average_dem(demographics[3][2], "rtc")]

            # Create a matplotlib Figure
            fig = Figure(figsize=(LENGTH, WIDTH), dpi=DPI)
            ax = fig.add_subplot(111)
            ax.bar(education_labels, education_values)
            ax.set_ylim(0, 1)
            ax.set_xticklabels(education_labels, rotation=12, ha='center')
            ax.set_title("Average response similarity to ChatGPT responses across education groups")
            ax.set_xlabel("Education levels")
            ax.set_ylabel("Average similarity score across all responses within given education groups")

            # Embed the chart in the scrollable_frame
            canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=20)

            # Income 0: $0 - $4,999, 1: $5,000 - $7,499, 2: $7,500 - $9,999, 3: $10,000 - $12,499, 4: $12,500 - $14,999, 5: $15,000 - $19,999
            # 6: $20,000 - $24,999, 7: $25,000 - $29,999, 8: $30,000 - $34,999, 9: $35,000 - $39,999, 10: $40,000 - $49,999, 11: $50,000 - $59,999 
            # 12: $60,000 - $74,999, 13: $75,000 - $99,999, 14: $100,000 - $149,999, 15: $150,000+, 16: Prefer not to answer, 17: unlisted
            education_labels = ["$0 - $4,999", '$5,000 - $7,499', '$7,500 - $9,999', '$10,000 - $12,499', '$12,500 - $14,999', '$15,000 - $19,999',
                                '$20,000 - $24,999', '$25,000 - $29,999', '$30,000 - $34,999', '$35,000 - $39,999', '$40,000 - $49,999', '$50,000 - $59,999',
                                '$60,000 - $74,999', '$75,000 - $99,999', '$100,000 - $149,999', '$150,000+']
            education_values = [
                analy.average_dem(demographics[4][0], "rtc"), 
                analy.average_dem(demographics[4][1], "rtc"), 
                analy.average_dem(demographics[4][2], "rtc"),
                analy.average_dem(demographics[4][3], "rtc"),
                analy.average_dem(demographics[4][4], "rtc"),
                analy.average_dem(demographics[4][5], "rtc"), 
                analy.average_dem(demographics[4][6], "rtc"), 
                analy.average_dem(demographics[4][7], "rtc"),
                analy.average_dem(demographics[4][8], "rtc"),
                analy.average_dem(demographics[4][9], "rtc"),
                analy.average_dem(demographics[4][10], "rtc"), 
                analy.average_dem(demographics[4][11], "rtc"), 
                analy.average_dem(demographics[4][12], "rtc"),
                analy.average_dem(demographics[4][13], "rtc"),
                analy.average_dem(demographics[4][14], "rtc"),
                analy.average_dem(demographics[4][15], "rtc")]

            # Create a matplotlib Figure
            fig = Figure(figsize=(LENGTH * 2, WIDTH), dpi=DPI)
            ax = fig.add_subplot(111)
            ax.bar(education_labels, education_values)
            ax.set_ylim(0, 1)
            ax.set_xticklabels(education_labels, rotation=15, ha='center')
            ax.set_title("Average response similarity to ChatGPT responses across education groups")
            ax.set_xlabel("Education levels")
            ax.set_ylabel("Average similarity score across all responses within given education groups")

            # Embed the chart in the scrollable_frame
            canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=20)
        update_graph()
        

if __name__ == "__main__":
    app = App()
    app.mainloop()