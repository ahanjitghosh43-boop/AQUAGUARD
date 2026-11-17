import customtkinter as ctk
import pandas as pd
import joblib
import os
import math
from datetime import datetime
from tkinter import messagebox

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ==========================================
# APPLICATION SETTINGS
# ==========================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG_COLOR = "#081426"
CARD_COLOR = "#11243D"
INNER_COLOR = "#192F4D"
ACCENT_COLOR = "#38BDF8"
TEXT_COLOR = "#E2E8F0"
MUTED_COLOR = "#94A3B8"
GREEN_COLOR = "#22C55E"
RED_COLOR = "#EF4444"

MODEL_PATH = os.path.join("models", "best_water_model.pkl")
HISTORY_PATH = os.path.join("results", "prediction_history.csv")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print("Model Loading Error:", e)


# ==========================================
# MAIN APPLICATION
# ==========================================

class AquaGuardApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Load previously saved history
        self.prediction_history = self.load_prediction_history()

        self.title("AQUAGUARD | Water Quality Intelligence")
        self.geometry("1150x950")
        self.minsize(950, 800)

        self.configure(fg_color=BG_COLOR)

        self.main_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=BG_COLOR,
            scrollbar_button_color="#29415F",
            scrollbar_button_hover_color=ACCENT_COLOR
        )

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.create_header()
        self.create_input_section()
        self.create_result_section()
        self.create_statistics_section()
        self.create_history_section()
        self.create_footer()

        # Display previously saved history
        self.display_history()

    # ==========================================
    # PERMANENT HISTORY: LOAD CSV
    # ==========================================

    def load_prediction_history(self):

        try:

            os.makedirs("results", exist_ok=True)

            if os.path.exists(HISTORY_PATH):

                df = pd.read_csv(HISTORY_PATH)

                if not df.empty:

                    return df.to_dict("records")

            return []

        except Exception as e:

            print("History Loading Error:", e)
            return []

    # ==========================================
    # PERMANENT HISTORY: SAVE CSV
    # ==========================================

    def save_prediction_history(self):

        try:

            os.makedirs("results", exist_ok=True)

            df = pd.DataFrame(self.prediction_history)

            df.to_csv(HISTORY_PATH, index=False)

            return True

        except Exception as e:

            messagebox.showerror(
                "Save History Error",
                f"Could not save prediction history:\n{str(e)}"
            )

            return False

    # ==========================================
    # DISPLAY HISTORY
    # ==========================================

    def display_history(self):

        self.history_text.configure(state="normal")
        self.history_text.delete("1.0", "end")

        for index, record in enumerate(
            self.prediction_history, start=1
        ):

            self.history_text.insert(
                "end",
                f"{index}. {record['Date & Time']} | "
                f"{record['Prediction Result']}\n"
            )

        self.history_text.configure(state="disabled")
        self.history_text.see("end")

    # ==========================================
    # HEADER
    # ==========================================

    def create_header(self):

        header = ctk.CTkFrame(
            self.main_frame,
            fg_color=CARD_COLOR,
            corner_radius=18
        )

        header.pack(fill="x", padx=15, pady=(5, 15))

        header_content = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        header_content.pack(fill="x", padx=25, pady=22)

        title_frame = ctk.CTkFrame(
            header_content,
            fg_color="transparent"
        )

        title_frame.pack(side="left")

        self.heading = ctk.CTkLabel(
            title_frame,
            text="AQUAGUARD",
            font=("Arial", 34, "bold"),
            text_color=ACCENT_COLOR
        )

        self.heading.pack(anchor="w")

        self.subtitle = ctk.CTkLabel(
            title_frame,
            text="SMART WATER QUALITY PREDICTION SYSTEM",
            font=("Arial", 12, "bold"),
            text_color=MUTED_COLOR
        )

        self.subtitle.pack(anchor="w", pady=(3, 0))

        status_frame = ctk.CTkFrame(
            header_content,
            fg_color="#153B35",
            corner_radius=20
        )

        status_frame.pack(side="right", padx=5)

        status_text = (
            "● MODEL READY"
            if model is not None
            else "● MODEL ERROR"
        )

        status_color = GREEN_COLOR if model is not None else RED_COLOR

        self.status_label = ctk.CTkLabel(
            status_frame,
            text=status_text,
            font=("Arial", 12, "bold"),
            text_color=status_color
        )

        self.status_label.pack(padx=15, pady=10)

        description = ctk.CTkLabel(
            header,
            text="Analyze water parameters and predict potability using Machine Learning.",
            font=("Arial", 12),
            text_color=TEXT_COLOR
        )

        description.pack(anchor="w", padx=27, pady=(0, 18))

    # ==========================================
    # INPUT SECTION
    # ==========================================

    def create_input_section(self):

        self.input_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=CARD_COLOR,
            corner_radius=18
        )

        self.input_frame.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            self.input_frame,
            text="WATER QUALITY PARAMETERS",
            font=("Arial", 19, "bold"),
            text_color=ACCENT_COLOR
        ).pack(anchor="w", padx=25, pady=(22, 5))

        ctk.CTkLabel(
            self.input_frame,
            text="Enter all nine water quality measurements below.",
            font=("Arial", 12),
            text_color=MUTED_COLOR
        ).pack(anchor="w", padx=25, pady=(0, 15))

        self.fields = [
            ("pH", "ph"),
            ("Hardness", "Hardness"),
            ("Solids", "Solids"),
            ("Chloramines", "Chloramines"),
            ("Sulfate", "Sulfate"),
            ("Conductivity", "Conductivity"),
            ("Organic Carbon", "Organic_carbon"),
            ("Trihalomethanes", "Trihalomethanes"),
            ("Turbidity", "Turbidity")
        ]

        self.entries = {}

        grid_frame = ctk.CTkFrame(
            self.input_frame,
            fg_color="transparent"
        )

        grid_frame.pack(fill="x", padx=15, pady=5)

        for index, (label, key) in enumerate(self.fields):

            row = index // 3
            col = index % 3

            field_card = ctk.CTkFrame(
                grid_frame,
                fg_color=INNER_COLOR,
                corner_radius=12
            )

            field_card.grid(
                row=row,
                column=col,
                padx=8,
                pady=8,
                sticky="nsew"
            )

            ctk.CTkLabel(
                field_card,
                text=label,
                font=("Arial", 13, "bold"),
                text_color=TEXT_COLOR
            ).pack(anchor="w", padx=13, pady=(12, 5))

            entry = ctk.CTkEntry(
                field_card,
                height=38,
                corner_radius=8,
                border_color="#355474",
                fg_color="#0B1B30",
                placeholder_text=f"Enter {label}",
                font=("Arial", 13)
            )

            entry.pack(fill="x", padx=12, pady=(0, 13))

            self.entries[key] = entry

        for col in range(3):
            grid_frame.grid_columnconfigure(col, weight=1)

        button_frame = ctk.CTkFrame(
            self.input_frame,
            fg_color="transparent"
        )

        button_frame.pack(pady=(18, 23))

        self.predict_button = ctk.CTkButton(
            button_frame,
            text="PREDICT WATER QUALITY",
            width=240,
            height=46,
            corner_radius=10,
            font=("Arial", 14, "bold"),
            fg_color="#0284C7",
            hover_color="#0369A1",
            command=self.predict
        )

        self.predict_button.grid(row=0, column=0, padx=10)

        self.clear_button = ctk.CTkButton(
            button_frame,
            text="CLEAR INPUTS",
            width=145,
            height=46,
            corner_radius=10,
            font=("Arial", 13, "bold"),
            fg_color="#334155",
            hover_color="#475569",
            command=self.clear
        )

        self.clear_button.grid(row=0, column=1, padx=10)

    # ==========================================
    # RESULT SECTION
    # ==========================================

    def create_result_section(self):

        self.result_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=CARD_COLOR,
            corner_radius=18
        )

        self.result_frame.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            self.result_frame,
            text="PREDICTION RESULT",
            font=("Arial", 19, "bold"),
            text_color=ACCENT_COLOR
        ).pack(pady=(20, 12))

        self.result_label = ctk.CTkLabel(
            self.result_frame,
            text="Waiting for water parameters...",
            font=("Arial", 23, "bold"),
            text_color=MUTED_COLOR,
            wraplength=750
        )

        self.result_label.pack(pady=10)

        self.confidence_label = ctk.CTkLabel(
            self.result_frame,
            text="",
            font=("Arial", 14, "bold"),
            text_color=TEXT_COLOR
        )

        self.confidence_label.pack(pady=(5, 10))

        self.disclaimer_label = ctk.CTkLabel(
            self.result_frame,
            text="Note: This is an ML-based prediction, not a laboratory water safety certification.",
            font=("Arial", 10),
            text_color=MUTED_COLOR,
            wraplength=850
        )

        self.disclaimer_label.pack(padx=15, pady=(5, 20))

    # ==========================================
    # STATISTICS SECTION
    # ==========================================

    def create_statistics_section(self):

        self.stats_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=CARD_COLOR,
            corner_radius=18
        )

        self.stats_frame.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            self.stats_frame,
            text="PREDICTION ANALYTICS",
            font=("Arial", 19, "bold"),
            text_color=ACCENT_COLOR
        ).pack(pady=(20, 15))

        cards_frame = ctk.CTkFrame(
            self.stats_frame,
            fg_color="transparent"
        )

        cards_frame.pack(fill="x", padx=15, pady=5)

        self.total_label = self.create_stat_card(
            cards_frame, "TOTAL PREDICTIONS", "0", "#38BDF8", 0
        )

        self.potable_label = self.create_stat_card(
            cards_frame, "POTABLE", "0", GREEN_COLOR, 1
        )

        self.not_potable_label = self.create_stat_card(
            cards_frame, "NOT POTABLE", "0", RED_COLOR, 2
        )

        self.chart_frame = ctk.CTkFrame(
            self.stats_frame,
            fg_color=INNER_COLOR,
            corner_radius=12
        )

        self.chart_frame.pack(fill="x", padx=25, pady=(15, 22))

        self.figure = Figure(
            figsize=(6, 3.2),
            dpi=100,
            facecolor=INNER_COLOR
        )

        self.chart_ax = self.figure.add_subplot(111)

        self.chart_canvas = FigureCanvasTkAgg(
            self.figure,
            master=self.chart_frame
        )

        self.chart_canvas.get_tk_widget().pack(pady=10)

        self.update_statistics()

    def create_stat_card(self, parent, title, value, color, column):

        card = ctk.CTkFrame(
            parent,
            fg_color=INNER_COLOR,
            corner_radius=12
        )

        card.grid(
            row=0,
            column=column,
            padx=8,
            pady=8,
            sticky="nsew"
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 11, "bold"),
            text_color=MUTED_COLOR
        ).pack(pady=(15, 5))

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 26, "bold"),
            text_color=color
        )

        value_label.pack(pady=(0, 15))

        parent.grid_columnconfigure(column, weight=1)

        return value_label

    # ==========================================
    # HISTORY SECTION
    # ==========================================

    def create_history_section(self):

        self.history_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=CARD_COLOR,
            corner_radius=18
        )

        self.history_frame.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            self.history_frame,
            text="PREDICTION HISTORY",
            font=("Arial", 19, "bold"),
            text_color=ACCENT_COLOR
        ).pack(anchor="w", padx=25, pady=(20, 10))

        self.history_text = ctk.CTkTextbox(
            self.history_frame,
            height=150,
            corner_radius=10,
            fg_color=INNER_COLOR,
            text_color=TEXT_COLOR,
            font=("Consolas", 12),
            wrap="word"
        )

        self.history_text.pack(fill="x", padx=20, pady=10)
        self.history_text.configure(state="disabled")

        button_frame = ctk.CTkFrame(
            self.history_frame,
            fg_color="transparent"
        )

        button_frame.pack(pady=(5, 20))

        self.export_button = ctk.CTkButton(
            button_frame,
            text="EXPORT TO CSV",
            width=180,
            height=42,
            corner_radius=9,
            font=("Arial", 13, "bold"),
            fg_color="#0284C7",
            hover_color="#0369A1",
            command=self.export_history
        )

        self.export_button.grid(row=0, column=0, padx=10)

        self.clear_history_button = ctk.CTkButton(
            button_frame,
            text="CLEAR HISTORY",
            width=180,
            height=42,
            corner_radius=9,
            font=("Arial", 13, "bold"),
            fg_color="#DC2626",
            hover_color="#991B1B",
            command=self.clear_history
        )

        self.clear_history_button.grid(row=0, column=1, padx=10)

    # ==========================================
    # FOOTER
    # ==========================================

    def create_footer(self):

        self.footer = ctk.CTkLabel(
            self.main_frame,
            text="AQUAGUARD  |  Machine Learning Based Water Quality Prediction",
            font=("Arial", 11),
            text_color=MUTED_COLOR
        )

        self.footer.pack(pady=(20, 5))

        self.developer_label = ctk.CTkLabel(
            self.main_frame,
            text="Developed by Ahanjit Ghosh ™",
            font=("Arial", 12, "bold"),
            text_color=ACCENT_COLOR
        )

        self.developer_label.pack(pady=(0, 20))

    # ==========================================
    # PREDICTION FUNCTION
    # ==========================================

    def predict(self):

        if model is None:

            messagebox.showerror(
                "Model Error",
                "Trained model could not be loaded!"
            )
            return

        input_values = {}

        for key, entry in self.entries.items():

            value = entry.get().strip()

            if not value:

                messagebox.showwarning(
                    "Missing Input",
                    f"Please enter {key}!"
                )

                entry.focus()
                return

            try:

                numeric_value = float(value)

            except ValueError:

                messagebox.showerror(
                    "Invalid Input",
                    f"{key} must contain a numeric value!"
                )

                entry.focus()
                return

            if not math.isfinite(numeric_value):

                messagebox.showerror(
                    "Invalid Input",
                    f"Please enter a finite numeric value for {key}!"
                )

                entry.focus()
                return

            if numeric_value < 0:

                messagebox.showwarning(
                    "Invalid Value",
                    f"{key} cannot be negative!"
                )

                entry.focus()
                return

            input_values[key] = numeric_value

        try:

            input_data = pd.DataFrame([input_values])

            prediction = model.predict(input_data)[0]

            if prediction == 1:

                status = "POTABLE"

                self.result_label.configure(
                    text="WATER IS POTABLE",
                    text_color=GREEN_COLOR
                )

            else:

                status = "NOT POTABLE"

                self.result_label.configure(
                    text="WATER IS NOT POTABLE",
                    text_color=RED_COLOR
                )

            # Create prediction record

            record = {
                "Date & Time": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                **input_values,
                "Prediction Result": status
            }

            # Add record to history

            self.prediction_history.append(record)

            # Permanently save history

            self.save_prediction_history()

            # Update history display

            self.display_history()

            # Update statistics

            self.update_statistics()

            # Prediction confidence

            if hasattr(model, "predict_proba"):

                probabilities = model.predict_proba(input_data)[0]

                predicted_class_index = list(model.classes_).index(
                    prediction
                )

                confidence = probabilities[predicted_class_index] * 100

                self.confidence_label.configure(
                    text=f"Model Prediction Confidence: {confidence:.2f}%"
                )

            else:

                self.confidence_label.configure(text="")

        except Exception as e:

            messagebox.showerror(
                "Prediction Error",
                f"Something went wrong:\n{str(e)}"
            )

    # ==========================================
    # UPDATE STATISTICS AND PIE CHART
    # ==========================================

    def update_statistics(self):

        total = len(self.prediction_history)

        potable = sum(
            1 for record in self.prediction_history
            if record["Prediction Result"] == "POTABLE"
        )

        not_potable = sum(
            1 for record in self.prediction_history
            if record["Prediction Result"] == "NOT POTABLE"
        )

        self.total_label.configure(text=str(total))
        self.potable_label.configure(text=str(potable))
        self.not_potable_label.configure(text=str(not_potable))

        self.chart_ax.clear()
        self.chart_ax.set_facecolor(INNER_COLOR)

        if total == 0:

            self.chart_ax.text(
                0.5,
                0.5,
                "No Predictions Yet",
                ha="center",
                va="center",
                color="white",
                fontsize=14
            )

            self.chart_ax.set_axis_off()

        else:

            self.chart_ax.pie(
                [potable, not_potable],
                labels=["POTABLE", "NOT POTABLE"],
                autopct="%1.1f%%",
                startangle=90,
                colors=[GREEN_COLOR, RED_COLOR],
                textprops={
                    "color": "white",
                    "fontsize": 10
                },
                wedgeprops={
                    "edgecolor": INNER_COLOR,
                    "linewidth": 2
                }
            )

            self.chart_ax.set_title(
                "Water Quality Distribution",
                color="white",
                fontsize=13,
                pad=12
            )

            self.chart_ax.set_aspect("equal")

        self.figure.tight_layout()
        self.chart_canvas.draw_idle()

    # ==========================================
    # CLEAR INPUTS
    # ==========================================

    def clear(self):

        for entry in self.entries.values():
            entry.delete(0, "end")

        self.result_label.configure(
            text="Waiting for water parameters...",
            text_color=MUTED_COLOR
        )

        self.confidence_label.configure(text="")

    # ==========================================
    # EXPORT HISTORY
    # ==========================================

    def export_history(self):

        if not self.prediction_history:

            messagebox.showwarning(
                "No History",
                "There is no prediction history to export!"
            )

            return

        try:

            os.makedirs("results", exist_ok=True)

            df = pd.DataFrame(self.prediction_history)

            df.to_csv(HISTORY_PATH, index=False)

            messagebox.showinfo(
                "Export Successful",
                f"Prediction history exported successfully!\n\n"
                f"File Location:\n{os.path.abspath(HISTORY_PATH)}"
            )

        except Exception as e:

            messagebox.showerror(
                "Export Error",
                str(e)
            )

    # ==========================================
    # CLEAR HISTORY
    # ==========================================

    def clear_history(self):

        if not self.prediction_history:

            messagebox.showinfo(
                "History",
                "No prediction history available!"
            )

            return

        confirm = messagebox.askyesno(
            "Clear History",
            "Are you sure you want to delete all prediction history?"
        )

        if confirm:

            try:

                # Delete permanent CSV file

                if os.path.exists(HISTORY_PATH):
                    os.remove(HISTORY_PATH)

                # Clear in-memory history

                self.prediction_history.clear()

                # Clear history display

                self.display_history()

                # Update statistics

                self.update_statistics()

                self.result_label.configure(
                    text="Waiting for water parameters...",
                    text_color=MUTED_COLOR
                )

                self.confidence_label.configure(text="")

                messagebox.showinfo(
                    "Success",
                    "Prediction history cleared successfully!"
                )

            except Exception as e:

                messagebox.showerror(
                    "Clear History Error",
                    str(e)
                )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app = AquaGuardApp()
    app.mainloop()