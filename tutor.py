from owlready2 import *
import tkinter as tk
from tkinter import ttk

# Load the ontology
ontology_file = "physics_laws_ontology.owl"  # Update with your OWL file name
try:
    ontology = get_ontology(ontology_file).load()
    print("Ontology loaded successfully!")
except Exception as e:
    print(f"Error loading ontology: {e}")
    exit()

# Helper function to resolve entity names
def resolve_entity(entity):
    if isinstance(entity, str):
        return entity
    if hasattr(entity, "name"):
        return entity.name
    if hasattr(entity, "iri"):
        return entity.iri
    return str(entity)

# Fetch individuals of a specific class
def get_individuals_of_class(class_name):
    cls = ontology.search_one(iri=f"*{class_name}")
    if cls:
        return [resolve_entity(ind) for ind in cls.instances()]
    return []

# Fetch examples for a concept
def get_examples(concept_name):
    concept = ontology.search_one(iri=f"*{concept_name}")
    if concept and hasattr(concept, "hasExample"):
        return [example.label[0] for example in concept.hasExample if hasattr(example, "label")]
    return ["No examples available."]

# Fetch questions for a concept
def get_questions(concept_name):
    concept = ontology.search_one(iri=f"*{concept_name}")
    if concept and hasattr(concept, "hasQuestion"):
        return [question for question in concept.hasQuestion]
    return []

# Fetch hint and answer for a question
def get_hint_and_answer(question):
    hint = question.hasHint[0].label[0] if hasattr(question, "hasHint") and question.hasHint else "No hint available."
    answer = question.hasAnswer[0].label[0] if hasattr(question, "hasAnswer") and question.hasAnswer else "No answer available."
    return hint, answer

# GUI for tutoring system
def create_gui():
    root = tk.Tk()
    root.title("Physics Intelligent Tutoring System")
    root.geometry("1000x800")
    root.configure(bg="#f5f5f5")

    # Header
    header = tk.Label(
        root, text="Physics Intelligent Tutoring System", font=("Helvetica", 24, "bold"), bg="#0056a3", fg="white"
    )
    header.pack(fill="x", pady=10)

    # Frame for concept selection
    concept_frame = tk.Frame(root, bg="#f5f5f5", padx=20, pady=20)
    concept_frame.pack(fill="x", padx=20, pady=10)

    tk.Label(
        concept_frame, text="Select a Physics Concept:", font=("Helvetica", 14), bg="#f5f5f5"
    ).grid(row=0, column=0, padx=10, pady=5, sticky="w")

    concepts = get_individuals_of_class("PhysicsConcept")
    concept_var = tk.StringVar(value=concepts[0] if concepts else "No concepts available")
    concept_menu = ttk.Combobox(concept_frame, textvariable=concept_var, values=concepts, state="readonly", font=("Helvetica", 12))
    concept_menu.grid(row=0, column=1, padx=10, pady=5)

    # Example Section
    example_frame = tk.LabelFrame(root, text="Example", font=("Helvetica", 16, "bold"), bg="#f5f5f5", fg="#333")
    example_frame.pack(fill="x", padx=20, pady=10)

    example_label = tk.Label(
        example_frame, text="", font=("Helvetica", 14), bg="#ffffff", fg="#333", wraplength=900, justify="left", anchor="nw", padx=10, pady=10, relief="solid"
    )
    example_label.pack(fill="both", expand=True)

    # Question Section
    question_frame = tk.LabelFrame(root, text="Question", font=("Helvetica", 16, "bold"), bg="#f5f5f5", fg="#333")
    question_frame.pack(fill="x", padx=20, pady=10)

    question_label = tk.Label(question_frame, text="", font=("Helvetica", 14), bg="#f5f5f5", wraplength=900)
    question_label.pack(pady=10)

    hint_label = tk.Label(question_frame, text="Hint: ", font=("Helvetica", 14), bg="#f5f5f5", fg="#007f00", wraplength=900)
    hint_label.pack(pady=5)

    answer_entry = tk.Entry(question_frame, font=("Helvetica", 14), width=50, bd=2, relief="groove")
    answer_entry.pack(pady=10)

    feedback_label = tk.Label(question_frame, text="Feedback: ", font=("Helvetica", 14), bg="#f5f5f5", fg="#d9534f", wraplength=900)
    feedback_label.pack(pady=10)

    # Submit Button
    def submit_answer():
        nonlocal current_question, current_answer
        user_answer = answer_entry.get().strip().lower()
        if current_question:
            correct_answer = current_answer.strip().lower()
            if user_answer == correct_answer:
                feedback_label.config(text="Feedback: Correct! Your answer matches the expected response.", fg="#007f00")
            else:
                feedback_label.config(text=f"Feedback: Incorrect. The correct answer is: {current_answer}", fg="#d9534f")
        else:
            feedback_label.config(text="No question selected.")

    submit_button = tk.Button(
        question_frame, text="Submit Answer", font=("Helvetica", 14, "bold"), bg="#0056a3", fg="white", padx=20, pady=10, command=submit_answer
    )
    submit_button.pack(pady=10)

    # Update UI
    current_question = None
    current_answer = ""

    def update_ui(*args):
        nonlocal current_question, current_answer
        selected_concept = concept_var.get()

        # Update examples
        examples = get_examples(selected_concept)
        example_label.config(text="\n".join(examples))

        # Update questions
        questions = get_questions(selected_concept)
        if questions:
            current_question = questions[0]
            question_label.config(text=f"Question: {current_question.label[0] if hasattr(current_question, 'label') and current_question.label else 'No label'}")
            hint, answer = get_hint_and_answer(current_question)
            hint_label.config(text=f"Hint: {hint}")
            current_answer = answer
        else:
            current_question = None
            question_label.config(text="No questions available.")
            hint_label.config(text="Hint: N/A")
            feedback_label.config(text="Feedback: N/A")

    concept_var.trace("w", update_ui)
    update_ui()

    root.mainloop()

if __name__ == "__main__":
    create_gui()
