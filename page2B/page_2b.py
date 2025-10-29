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

    sql = """
    SELECT
        i.country,
        i.year,
        i.inf_type,
        i.cases,
        cp.population
    FROM InfectionData i
    LEFT JOIN CountryPopulation cp ON i.country = cp.country AND i.year = cp.year
    """
    filters = []
    params = []
    if selected_country:
        filters.append("i.country = ?")
        params.append(selected_country)
    if selected_year:
        filters.append("i.year = ?")
        params.append(selected_year)
    if selected_type:
        filters.append("i.inf_type = ?")
        params.append(selected_type)
    if filters:
        sql += " WHERE " + " AND ".join(filters)
    sql += " ORDER BY i.year DESC, i.country, i.inf_type LIMIT 50"
    rows = cursor.execute(sql, params).fetchall()

    conn.close()

    # Simple summary calculations here without numpy
    total_cases = sum(row['cases'] for row in rows if row['cases'] is not None)
    count_cases = sum(1 for row in rows if row['cases'] is not None)
    avg_cases = (total_cases / count_cases) if count_cases > 0 else 0
    country_count = len(set(row['country'] for row in rows if row['country']))

    summary_html = f"""
    <div class="summary-panel" style="margin-left:28px;padding:14px 22px;background:#f2f8ff;border-radius:8px;min-width:200px;display:inline-block;vertical-align:top;">
        <div><strong>Total Cases:</strong> {total_cases}</div>
        <div><strong>Average Cases:</strong> {avg_cases:.1f}</div>
        <div><strong>Countries:</strong> {country_count}</div>
    </div>
    """

    def options(all_values, selected):
        return ''.join(
            f'<option value="{v}"{" selected" if v == selected else ""}>{v}</option>'
            for v in all_values if v
        )

    filter_form = f"""
    <form method="get" class="filters" style="margin-bottom:18px;">
        <label>Country:
            <select name="country"><option value="">All</option>{options(all_countries, selected_country)}</select>
        </label>
        <label>Year:
            <select name="year"><option value="">All</option>{options(all_years, selected_year)}</select>
        </label>
        <label>Infection Type:
            <select name="inf_type"><option value="">All</option>{options(all_types, selected_type)}</select>
        </label>
        <button type="submit">Filter</button>
        <button type="submit" name="export" value="1">Export CSV</button>
    </form>
    """

    table_rows = "".join(
        f"<tr><td>{row['country']}</td><td>{row['year']}</td><td>{row['inf_type']}</td><td>{row['cases']}</td><td>{row['population'] if row['population'] is not None else '-'}</td></tr>"
        for row in rows
    ) if rows else "<tr><td colspan='5'>No data found for selected filters.</td></tr>"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Infection Data by Country</title>
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
                    <a href="/">Home</a>
                    <a href="#">About</a>
                    <a href="#">Contact</a>
                </div>
            </nav>
        </header>
        <main>
            <section class="dashboard-card">
                <h1>Infection Data by Country and Population</h1>
                {summary_html}
                {filter_form}
                <table>
                    <thead>
                        <tr>
                            <th>Country</th>
                            <th>Year</th>
                            <th>Infection Type</th>
                            <th>Cases</th>
                            <th>Population</th>
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
