import customtkinter as ctk
from typing import Dict, List

class UnitConverter:
    def __init__(self):
        # Set theme and appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Create main window
        self.window = ctk.CTk()
        self.window.title("Modern Unit Converter")
        self.window.geometry("800x600")
        self.window.resizable(False, False)  # Make window size static
        
        # Complete conversions dictionary
        self.conversions = {
            "Length": {
                "Meters": 1.0,
                "Kilometers": 0.001,
                "Centimeters": 100,
                "Millimeters": 1000,
                "Miles": 0.000621371,
                "Yards": 1.09361,
                "Feet": 3.28084,
                "Inches": 39.3701,
                "Nautical Miles": 0.000539957,
                "Micrometers": 1e6,
                "Nanometers": 1e9
            },
            "Weight": {
                "Kilograms": 1.0,
                "Grams": 1000,
                "Milligrams": 1e6,
                "Pounds": 2.20462,
                "Ounces": 35.274,
                "Metric Tons": 0.001,
                "Short Tons": 0.00110231,
                "Stone": 0.157473
            },
            "Temperature": {
                "Celsius": "C",
                "Fahrenheit": "F",
                "Kelvin": "K"
            },
            "Area": {
                "Square Meters": 1.0,
                "Square Kilometers": 1e-6,
                "Square Miles": 3.861e-7,
                "Square Yards": 1.19599,
                "Square Feet": 10.7639,
                "Square Inches": 1550.0,
                "Hectares": 0.0001,
                "Acres": 0.000247105
            },
            "Volume": {
                "Cubic Meters": 1.0,
                "Liters": 1000,
                "Milliliters": 1e6,
                "Gallons (US)": 264.172,
                "Quarts (US)": 1056.69,
                "Pints (US)": 2113.38,
                "Cups": 4226.75,
                "Fluid Ounces (US)": 33814.0
            },
            "Time": {
                "Seconds": 1.0,
                "Minutes": 1/60,
                "Hours": 1/3600,
                "Days": 1/86400,
                "Weeks": 1/604800,
                "Months": 1/2628000,
                "Years": 1/31536000
            },
            "Digital Storage": {
                "Bytes": 1.0,
                "Kilobytes": 1/1024,
                "Megabytes": 1/1048576,
                "Gigabytes": 1/1073741824,
                "Terabytes": 1/1099511627776,
                "Bits": 8
            }
        }

        self.setup_gui()

    def setup_gui(self):
        # Create tabview
        self.tabview = ctk.CTkTabview(self.window)
        self.tabview.pack(pady=20, padx=20, fill="both", expand=True)

        # Create tabs for each conversion category
        for category in self.conversions.keys():
            self.tabview.add(category)
            self.setup_category_tab(category)

        # Set default tab
        self.tabview.set("Length")

    def setup_category_tab(self, category):
        tab = self.tabview.tab(category)
        
        # Title
        title = ctk.CTkLabel(tab, text=f"{category} Converter", font=("Helvetica", 24, "bold"))
        title.pack(pady=10)

        # Input frame
        input_frame = ctk.CTkFrame(tab)
        input_frame.pack(pady=10, fill="x", padx=20)

        # Input entry with dynamic update
        input_value = ctk.CTkEntry(input_frame, placeholder_text="Enter value")
        input_value.pack(side="left", padx=5, expand=True)

        # From unit selector
        from_unit = ctk.CTkOptionMenu(
            input_frame, 
            values=list(self.conversions[category].keys()),
            command=lambda x: self.dynamic_convert(category, input_value, from_unit, to_unit, result_label)
        )
        from_unit.pack(side="right", padx=5)

        # To unit selector
        output_frame = ctk.CTkFrame(tab)
        output_frame.pack(pady=10, fill="x", padx=20)

        to_unit = ctk.CTkOptionMenu(
            output_frame, 
            values=list(self.conversions[category].keys()),
            command=lambda x: self.dynamic_convert(category, input_value, from_unit, to_unit, result_label)
        )
        to_unit.pack(side="right", padx=5)

        # Result label
        result_label = ctk.CTkLabel(output_frame, text="Result: ", font=("Helvetica", 14))
        result_label.pack(side="left", padx=5)

        # Bind input changes to dynamic conversion
        input_value.bind('<KeyRelease>', 
            lambda event: self.dynamic_convert(category, input_value, from_unit, to_unit, result_label))

        # Set initial values for the option menus
        from_unit.set(list(self.conversions[category].keys())[0])
        to_unit.set(list(self.conversions[category].keys())[1])

        # Add quick conversion table
        self.add_quick_conversion_table(tab, category)

    def add_quick_conversion_table(self, tab, category):
        # Create frame for quick conversion table
        table_frame = ctk.CTkFrame(tab)
        table_frame.pack(pady=10, fill="both", expand=True, padx=20)

        # Add title for quick conversion table
        table_title = ctk.CTkLabel(table_frame, text="Common Conversions", font=("Helvetica", 16, "bold"))
        table_title.pack(pady=5)

        # Create scrollable frame for conversions
        scrollable_frame = ctk.CTkScrollableFrame(table_frame, height=200)
        scrollable_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Add some common conversions
        units = list(self.conversions[category].keys())
        base_unit = units[0]
        
        # Create two columns for conversions
        left_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, padx=5, sticky="nsew")
        right_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        right_frame.grid(row=0, column=1, padx=5, sticky="nsew")
        scrollable_frame.grid_columnconfigure(0, weight=1)
        scrollable_frame.grid_columnconfigure(1, weight=1)

        # Split units between the two columns
        mid_point = len(units) // 2
        for i, unit in enumerate(units):
            if unit == base_unit:
                continue
            
            conversion_text = self.get_common_conversion(category, unit)
            frame = left_frame if i < mid_point else right_frame
            label = ctk.CTkLabel(frame, text=conversion_text, font=("Helvetica", 12))
            label.pack(pady=2, anchor="w")

    def dynamic_convert(self, category, input_widget, from_unit_widget, to_unit_widget, result_label):
        try:
            value = input_widget.get()
            if not value:  # If input is empty
                result_label.configure(text="Result: ")
                return
                
            value = float(value)
            from_unit = from_unit_widget.get()
            to_unit = to_unit_widget.get()

            if category == "Temperature":
                result = self.convert_temperature(value, from_unit, to_unit)
            else:
                # For other conversions
                base_value = value / self.conversions[category][from_unit]
                result = base_value * self.conversions[category][to_unit]

            # Format the result based on its magnitude
            if abs(result) < 0.0001 or abs(result) > 10000:
                formatted_result = f"{result:.4e}"
            else:
                formatted_result = f"{result:.4f}"

            result_label.configure(text=f"Result: {formatted_result} {to_unit}")
        except ValueError:
            result_label.configure(text="Please enter a valid number")

    def get_common_conversion(self, category, unit):
        if category == "Temperature":
            return f"1 {unit} → See converter above"
        
        value = self.conversions[category][unit]
        base_unit = list(self.conversions[category].keys())[0]
        if value < 1:
            return f"1 {base_unit} = {1/value:.4g} {unit}"
        else:
            return f"1 {unit} = {value:.4g} {base_unit}"

    def convert_temperature(self, value: float, from_unit: str, to_unit: str) -> float:
        # Convert to Celsius first
        if from_unit == "Fahrenheit":
            celsius = (value - 32) * 5/9
        elif from_unit == "Kelvin":
            celsius = value - 273.15
        else:
            celsius = value

        # Convert from Celsius to target unit
        if to_unit == "Fahrenheit":
            return (celsius * 9/5) + 32
        elif to_unit == "Kelvin":
            return celsius + 273.15
        else:
            return celsius

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = UnitConverter()
    app.run()



