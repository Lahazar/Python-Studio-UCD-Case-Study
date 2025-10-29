import sqlite3

def get_page_html(formdata):
    selected_type = formdata.get("inf_type", [""])[0]
    selected_year = formdata.get("year", [""])[0]

    conn = sqlite3.connect('immunisation.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    all_types = [r["inf_type"] for r in cursor.execute("SELECT DISTINCT inf_type FROM InfectionData").fetchall()]
    all_years = [str(r["year"]) for r in cursor.execute("SELECT DISTINCT year FROM InfectionData").fetchall()]
    all_regions = [r["region"] for r in cursor.execute("SELECT region FROM Region").fetchall()]

    filter_clause = []
    params = []
    if selected_year:
        filter_clause.append("i.year = ?")
        params.append(selected_year)
    if selected_type:
        filter_clause.append("i.inf_type = ?")
        params.append(selected_type)
    where_sql = " AND " + " AND ".join(filter_clause) if filter_clause else ""

    sql = f"""
    SELECT 
        r.region, 
        COALESCE(SUM(i.cases), 0) AS total_cases
    FROM Region r
    LEFT JOIN Country c ON r.region = c.region
    LEFT JOIN InfectionData i ON c.name = i.country{' AND ' + ' AND '.join(filter_clause) if filter_clause else ''}
    GROUP BY r.region
    ORDER BY r.region
    """

    rows = cursor.execute(sql, params).fetchall()
    conn.close()

    def options(all_values, selected):
        return ''.join(
            f'<option value="{v}"{" selected" if v == selected else ""}>{v}</option>'
            for v in all_values if v
        )

    filter_form = f"""
    <form method="get" class="filters" style="margin-bottom:18px;">
        <label>Year:
            <select name="year"><option value="">All</option>{options(all_years, selected_year)}</select>
        </label>
        <label>Infection Type:
            <select name="inf_type"><option value="">All</option>{options(all_types, selected_type)}</select>
        </label>
        <button type="submit">Filter</button>
    </form>
    """

    table_rows = "".join(
        f"<tr><td>{row['region']}</td><td>{row['total_cases']}</td></tr>"
        for row in rows
    ) if rows else "<tr><td colspan='2'>No data found for selected filters.</td></tr>"

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>3B | Infection Data by Region</title>
        <link rel="stylesheet" href="page3B/style.css" />
    </head>
    <body>
        <header>
            <nav class="navbar">
                <div class="nav-left">
                    <img src="page3B/download.png" alt="WHO Logo" class="logo" />
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
                <h1>Infection Data by Region</h1>
                {filter_form}
                <table>
                    <thead>
                        <tr>
                            <th>Region</th>
                            <th>Total Cases</th>
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
