from flask import Flask, render_template_string, request

app = Flask(__name__)

# Simple recommendation data
recommendations = {
    "rice": {"fertilizer": "urea", "quantity": 50},
    "wheat": {"fertilizer": "dap", "quantity": 40},
    "cotton": {"fertilizer": "npk", "quantity": 60},
    "vegetables": {"fertilizer": "compost", "quantity": 30},
    "fruits": {"fertilizer": "organic mix", "quantity": 35}
}

# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template_string("""
    <html>
    <head>
        <title>Smart Fertigation Advisor</title>
        <style>
            body { font-family: Arial; text-align: center; background:#f0fff0; }
            h1 { font-size: 36px; }
            p { font-size: 22px; }
            button {
                font-size: 22px;
                padding: 15px;
                width: 80%;
                background: green;
                color: white;
                border: none;
                border-radius: 10px;
            }
        </style>
    </head>
    <body>
        <h1>Smart Fertigation Advisor</h1>
        <p>Fertigation means giving fertilizer through irrigation water.<br>
        It helps crops grow better and saves money.</p>
        <br>
        <a href="/form"><button>Start Fertigation Check</button></a>
    </body>
    </html>
    """)

# ---------------- FORM PAGE ----------------
@app.route("/form")
def form():
    return render_template_string("""
    <html>
    <head>
        <title>Enter Details</title>
        <style>
            body { font-family: Arial; text-align: center; background:#f9fff9; }
            label { font-size: 22px; display:block; margin-top:15px; }
            input, select {
                font-size: 20px;
                padding: 10px;
                width: 80%;
                margin-top:5px;
            }
            button {
                font-size: 22px;
                padding: 15px;
                width: 80%;
                margin-top:20px;
                background: green;
                color: white;
                border: none;
                border-radius: 10px;
            }
        </style>
    </head>
    <body>
        <h1>Enter Crop Details</h1>
        <form method="POST" action="/result">
            
            <label>Type of Crop</label>
            <select name="crop" required>
                <option value="rice">Rice</option>
                <option value="wheat">Wheat</option>
                <option value="cotton">Cotton</option>
                <option value="vegetables">Vegetables</option>
                <option value="fruits">Fruits</option>
            </select>

            <label>Fertilizer Type</label>
            <input type="text" name="fertilizer" required>

            <label>Fertilizer Quantity (kg)</label>
            <input type="number" name="quantity" required>

            <br>
            <button type="submit">Check Result</button>
        </form>

        <br>
        <a href="/"><button>Back</button></a>
    </body>
    </html>
    """)

# ---------------- RESULT PAGE ----------------
@app.route("/result", methods=["POST"])
def result():
    crop = request.form["crop"]
    fertilizer = request.form["fertilizer"].lower()
    quantity = float(request.form["quantity"])

    rec = recommendations.get(crop)

    if fertilizer != rec["fertilizer"]:
        message = "Not suitable for this crop"
        color = "#f8d7da"   # red
    elif quantity > rec["quantity"]:
        message = "⚠ Too much fertilizer"
        color = "#fff3cd"   # yellow
    elif quantity < rec["quantity"]:
        message = "✖ Less fertilizer than required"
        color = "#f8d7da"   # red
    else:
        message = "✔ Good choice"
        color = "#c8f7c5"   # green

    return render_template_string(f"""
    <html>
    <head>
        <title>Result</title>
        <style>
            body {{ font-family: Arial; text-align: center; background:#f0fff0; }}
            .box {{
                font-size: 24px;
                padding: 20px;
                margin: 20px;
                background:{color};
            }}
            button {{
                font-size: 22px;
                padding: 15px;
                width: 80%;
                background: green;
                color: white;
                border: none;
                border-radius: 10px;
            }}
        </style>
    </head>
    <body>
        <h1>Result</h1>
        <div class="box">{message}</div>

        <h2>Recommended Fertilizer: {rec["fertilizer"]}</h2>
        <h2>Recommended Quantity: {rec["quantity"]} kg</h2>

        <br>
        <button onclick="window.print()">Print Report</button>
        <br><br>
        <a href="/form"><button>Check Again</button></a>
    </body>
    </html>
    """)

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)