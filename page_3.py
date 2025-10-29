def get_page_html(form_data):
    print("About to return Page 3...")

    # Get selected country from dropdown
    selected_country = form_data.get("country", ["All"])[0]

    # Hardcoded data
    data = [
        {"country": "Uganda", "y2000": 60, "y2024": 95, "improvement": 35},
        {"country": "Australia", "y2000": 80, "y2024": 96, "improvement": 13},
        {"country": "United Kingdom", "y2000": 85, "y2024": 97, "improvement": 13},
    ]

    # Filter data based on user selection
    if selected_country != "All":
        data = [d for d in data if d["country"] == selected_country]

    # Generate table rows
    table_rows = ""
    for d in data:
        table_rows += f"""
            <tr>
                <td>{d['country']}</td>
                <td>{d['y2000']}%</td>
                <td>{d['y2024']}%</td>
                <td>+{d['improvement']}%</td>
            </tr>
        """

    # Generate dropdown options
    country_options = ""
    for c in ["All", "Uganda", "Australia", "United Kingdom"]:
        selected = "selected" if c == selected_country else ""
        country_options += f'<option value="{c}" {selected}>{c}</option>'

    # HTML layout
    page_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Global Vaccine Trends</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
                margin: 0;
                text-align: center;
                color: #111;
            }}
            header {{
                background-color: #4da6ff;
                padding: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            input[type="search"] {{
                border-radius: 15px;
                padding: 6px 12px;
                border: none;
            }}
            nav a {{
                margin: 0 10px;
                text-decoration: none;
                color: #000;
                font-weight: bold;
            }}
            nav a:hover {{
                color: #004c99;
            }}
            h1 {{
                margin-top: 30px;
                font-weight: bold;
            }}
            select {{
                padding: 8px;
                margin: 10px;
                border: 2px solid #333;
                border-radius: 5px;
            }}
            table {{
                margin: 30px auto;
                border-collapse: collapse;
                width: 70%;
                box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
            }}
            th, td {{
                border: 1px solid #000;
                padding: 12px;
                text-align: center;
            }}
            th {{
                background-color: #4da6ff;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            .back-link {{
                display: inline-block;
                margin-top: 25px;
                text-decoration: none;
                color: #4da6ff;
                font-weight: bold;
            }}
            .back-link:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <header>
            <div>
                <img src="download.png" alt="Logo" style="height:40px;">
                <input type="search" placeholder="Search...">
            </div>
            <nav>
                <a href="/">Home</a>
                <a href="page_2.html">Vaccination Rates</a>
                <a href="page_3.html">Vaccine Trends</a>
                <a href="#">Contact</a>
            </nav>
        </header>

        <h1>Countries with Biggest Vaccine Improvement</h1>

        <form method="get" action="/page_3.html">
            <select name="country">{country_options}</select>
            <input type="submit" value="Filter">
        </form>

        <table>
            <tr>
                <th>Country</th>
                <th>2000</th>
                <th>2024</th>
                <th>Improvement</th>
            </tr>
            {table_rows}
        </table>

        <a class="back-link" href="/">← Back to Home</a>
    </body>
    </html>
    """
    return page_html
