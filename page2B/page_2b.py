import sqlite3

def get_page_html(formdata):
    conn = sqlite3.connect('immunisation.db')
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute('SELECT country, antigen, year, coverage FROM Vaccination LIMIT 25;')
    rows = cursor.fetchall()
    conn.close()

    table_rows = ""
    for row in rows:
        table_rows += (
            f"<tr>"
            f"<td>{row['country']}</td>"
            f"<td>{row['antigen']}</td>"
            f"<td>{row['year']}</td>"
            f"<td>{row['coverage']}</td>"
            f"</tr>"
        )

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Vaccination Dashboard | 2B</title>
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
                <h1>Vaccination Coverage Records</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Country</th>
                            <th>Antigen</th>
                            <th>Year</th>
                            <th>Coverage (%)</th>
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