import pyhtml

def get_page_html(form_data):
    print("Returning Vaccine Improvement page")

    db_path = "immunisation.db"

    # Dropdown options
    countries = [row[0] for row in pyhtml.get_results_from_query(
        db_path, "SELECT DISTINCT Country.name FROM Country ORDER BY Country.name;"
    )]
    antigens = [row[0] for row in pyhtml.get_results_from_query(
        db_path, "SELECT DISTINCT Antigen.name FROM Antigen ORDER BY Antigen.name;"
    )]

    selected_country = form_data.get("country", ["All"])[0]
    selected_antigen = form_data.get("antigen", ["All"])[0]
    top10 = form_data.get("top10", ["false"])[0].lower() == "true"

    # SQL query: join Vaccination + Country + Antigen, compare 2020 vs 2024
    query = """
        SELECT 
            Country.name AS country,
            Antigen.name AS antigen,
            v2020.coverage AS coverage_2020,
            v2024.coverage AS coverage_2024,
            (v2024.coverage - v2020.coverage) AS improvement
        FROM Vaccination v2020
        JOIN Vaccination v2024 
            ON v2020.country = v2024.country 
            AND v2020.antigen = v2024.antigen
        JOIN Country ON Country.CountryID = v2020.country
        JOIN Antigen ON Antigen.AntigenID = v2020.antigen
        WHERE v2020.year = 2020
          AND v2024.year = 2024
    """

    if selected_country != "All":
        query += f" AND Country.name = '{selected_country}'"
    if selected_antigen != "All":
        query += f" AND Antigen.name = '{selected_antigen}'"

    query += " ORDER BY improvement DESC"
    query += " LIMIT 10;" if top10 else " LIMIT 50;"

    results = pyhtml.get_results_from_query(db_path, query)

    # Dropdown builders
    def make_options(values, selected):
        html = '<option value="All">All</option>'
        for v in values:
            sel = "selected" if v == selected else ""
            html += f'<option value="{v}" {sel}>{v}</option>'
        return html

    country_options = make_options(countries, selected_country)
    antigen_options = make_options(antigens, selected_antigen)

    # Table rows
    if results:
        rows_html = "".join(
            f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}%</td><td>{r[3]}%</td><td>+{round(r[4],2)}%</td></tr>"
            for r in results
        )
    else:
        rows_html = "<tr><td colspan='5'>No data available</td></tr>"

    # HTML page
    return f"""
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
            form {{
                margin-top: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-wrap: wrap;
                gap: 10px;
            }}
            label {{
                font-weight: bold;
                margin-right: 5px;
            }}
            select {{
                padding: 8px;
                border: 2px solid #333;
                border-radius: 5px;
            }}
            input[type="submit"], .top10-btn {{
                background-color: #4da6ff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                cursor: pointer;
                font-weight: bold;
                transition: background 0.3s;
            }}
            input[type="submit"]:hover, .top10-btn:hover {{
                background-color: #3385cc;
            }}
            table {{
                margin: 30px auto;
                border-collapse: collapse;
                width: 80%;
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

        <h1>Countries with Biggest Vaccine Improvement (2020–2024)</h1>

        <!-- Unified Filter + Top 10 Button -->
        <form method="get" action="/page_3.html">
            <label for="country">Country:</label>
            <select name="country">{country_options}</select>

            <label for="antigen">Antigen:</label>
            <select name="antigen">{antigen_options}</select>

            <input type="submit" value="Filter">

            <button class="top10-btn" type="submit" name="top10" value="true">Top 10 Improvements</button>
        </form>

        <table>
            <tr>
                <th>Country</th>
                <th>Antigen</th>
                <th>2020</th>
                <th>2024</th>
                <th>Improvement</th>
            </tr>
            {rows_html}
        </table>

        <a class="back-link" href="/">← Back to Home</a>
    </body>
    </html>
    """
