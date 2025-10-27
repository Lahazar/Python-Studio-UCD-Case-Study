import sqlite3

def get_page_html(formdata):
    selected_type = formdata.get("inf_type", [""])[0]
    selected_country = formdata.get("country", [""])[0]
    selected_year = formdata.get("year", [""])[0]

    conn = sqlite3.connect('immunisation.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    all_types = [r["inf_type"] for r in cursor.execute("SELECT DISTINCT inf_type FROM InfectionData").fetchall()]
    all_countries = [r["country"] for r in cursor.execute("SELECT DISTINCT country FROM InfectionData").fetchall()]
    all_years = [str(r["year"]) for r in cursor.execute("SELECT DISTINCT year FROM InfectionData").fetchall()]

    where = []
    params = []
    if selected_type:
        where.append("inf_type = ?")
        params.append(selected_type)
    if selected_country:
        where.append("country = ?")
        params.append(selected_country)
    if selected_year:
        where.append("year = ?")
        params.append(selected_year)

    sql = "SELECT inf_type, country, year, cases FROM InfectionData"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY year DESC, country, inf_type LIMIT 50;"
    rows = cursor.execute(sql, params).fetchall()
    conn.close()

    def options(options, selected):
        return ''.join(f'<option value="{o}"{" selected" if o == selected else ""}>{o}</option>' for o in options)

    filter_form = f"""
    <form method="get" class="filters" style="margin-bottom:18px;">
        <label>Country:
            <select name="country"><option value="">All</option>{options(all_countries, selected_country)}</select>
        </label>
        <label>Year:
            <select name="year"><option value="">All</option>{options(all_years, selected_year)}</select>
        </label>
        <label>Infection type:
            <select name="inf_type"><option value="">All</option>{options(all_types, selected_type)}</select>
        </label>
        <button type="submit">Filter</button>
    </form>
    """

    table_rows = "".join(
        f"<tr><td>{row['country']}</td><td>{row['year']}</td><td>{row['inf_type']}</td><td>{row['cases']}</td></tr>"
        for row in rows
    )

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Infection Dashboard | 2B</title>
        <link rel="stylesheet" href="page2B/style.css">
    </head>
    <body>
        <header>
            <nav class="navbar">
                <div class="nav-left">
                    <img src="page2B/download.png" alt="WHO Logo" class="logo">
                </div>
                <div class="nav-center">
                    <input type="search" placeholder="Search..."/>
                </div>
                <div class="nav-right">
                    <a href="index.html">Home</a>
                    <a href="#">About</a>
                    <a href="#">Contact</a>
                </div>
            </nav>
        </header>
        <main>
            <section class="dashboard-card">
                <h1>Infection Data Records</h1>
                {filter_form}
                <table>
                    <thead>
                        <tr>
                            <th>Country</th>
                            <th>Year</th>
                            <th>Infection Type</th>
                            <th>Cases</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
            </section>
        </main>
    </body>
    </html>
    """
    return html
