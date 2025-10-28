import pyhtml

def get_page_html(form_data):
    print("Returning Vaccination Rates page")

    db_path = "immunisation.db"

    # Dropdown data — using Vaccination table
    antigens = [row[0] for row in pyhtml.get_results_from_query(db_path,
        "SELECT DISTINCT antigen FROM Vaccination ORDER BY antigen;")]
    years = [row[0] for row in pyhtml.get_results_from_query(db_path,
        "SELECT DISTINCT year FROM Vaccination ORDER BY year;")]
    countries = [row[0] for row in pyhtml.get_results_from_query(db_path,
        "SELECT DISTINCT Country.name FROM Country ORDER BY Country.name;")]

    antigen = form_data.get("antigen", ["All"])[0]
    year = form_data.get("year", ["All"])[0]
    country = form_data.get("country", ["All"])[0]

    # build SQL — join Country for full names
    query = """
        SELECT Country.name, Vaccination.antigen, Vaccination.year, Vaccination.coverage
        FROM Vaccination
        JOIN Country ON Country.CountryID = Vaccination.country
        WHERE 1=1
    """
    if antigen != "All":
        query += f" AND Vaccination.antigen = '{antigen}'"
    if year != "All":
        query += f" AND Vaccination.year = {year}"
    if country != "All":
        query += f" AND Country.name = '{country}'"

    

    results = pyhtml.get_results_from_query(db_path, query)

    # Dropdown builder
    def make_options(vals, selected):
        html = '<option value="All">All</option>'
        for v in vals:
            sel = "selected" if str(v) == str(selected) else ""
            html += f'<option value="{v}" {sel}>{v}</option>'
        return html

    antigen_options = make_options(antigens, antigen)
    year_options = make_options(years, year)
    country_options = make_options(countries, country)

    # Table content
    if results:
        rows_html = "".join(
            f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}%</td></tr>"
            for r in results
        )
    else:
        rows_html = "<tr><td colspan='4'>No data</td></tr>"

    # HTML + CSS
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Vaccination Rates</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
                margin: 0;
                text-align: center;
            }}
            header {{
                background-color: #4da6ff;
                padding: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            table {{
                margin: 30px auto;
                width: 80%;
                border-collapse: collapse;
            }}
            th, td {{
                border: 1px solid #000;
                padding: 10px;
            }}
            th {{
                background-color: #4da6ff;
                color: white;
            }}
            tr:nth-child(even) {{ background: #f2f2f2; }}
            form {{
                margin-top: 20px;
            }}
            label {{
                font-weight: bold;
                margin-right: 6px;
            }}
            select {{
                margin: 0 10px;
                padding: 6px;
            }}
            input[type="submit"] {{
                background-color: #4da6ff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                cursor: pointer;
                font-weight: bold;
            }}
            input[type="submit"]:hover {{
                background-color: #3385cc;
            }}
        </style>
    </head>
    <body>
        <header>
            <div><img src="download.png" style="height:40px;"> <input type="search" placeholder="Search..."></div>
            <nav>
                <a href="/">Home</a>
                <a href="page_2.html">Rates</a>
                <a href="page_3.html">Improvements</a>
            </nav>
        </header>

        <h1>Vaccination Rates by Country</h1>

        <form method="get" action="/page_2.html">
            <label for="antigen">Antigen:</label>
            <select name="antigen">{antigen_options}</select>

            <label for="year">Year:</label>
            <select name="year">{year_options}</select>

            <label for="country">Country:</label>
            <select name="country">{country_options}</select>

            <input type="submit" value="Filter">
        </form>

        <table>
            <tr><th>Country</th><th>Antigen</th><th>Year</th><th>Coverage (%)</th></tr>
            {rows_html}
        </table>

        <a href="/">← Back to Home</a>
    </body>
    </html>
    """

