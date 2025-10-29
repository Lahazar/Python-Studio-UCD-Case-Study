import pyhtml

def get_page_html(form_data):
    print("About to return Page 1...")

    db_path = "immunisation.db"

    # query for main statistics (Spain, Italy, Argentina)
    try:
        query_main = """
            SELECT country, AVG(coverage)
            FROM Vaccination
            WHERE country IN ('ESP', 'ITA', 'ARG')
            GROUP BY country
            ORDER BY country;
        """
        results_main = pyhtml.get_results_from_query(db_path, query_main)
        if results_main:
            main_stats = "".join(
                f"<p><strong>{r[0]}:</strong> {r[1]:.1f}% average coverage</p>"
                for r in results_main
            )
        else:
            main_stats = "<p>No data for Australia, UK, or USA.</p>"
    except Exception as e:
        main_stats = f"<p>Database Error (Main Stats): {e}</p>"

    # query for top 3 improvements in vaccination coverage
    try:
        query_improve = """
            SELECT v1.country, (v2.coverage - v1.coverage) AS improvement
            FROM Vaccination v1
            JOIN Vaccination v2
                ON v1.country = v2.country
                AND v2.year = v1.year + 1
            WHERE v2.coverage > v1.coverage
            GROUP BY v1.country
            ORDER BY improvement DESC
            LIMIT 3;
        """
        results_improve = pyhtml.get_results_from_query(db_path, query_improve)
        if results_improve:
            improve_stats = "".join(
                f"<p><strong>{r[0]}:</strong> +{r[1]:.2f}% improvement</p>"
                for r in results_improve
            )
        else:
            improve_stats = "<p>No improvement data found.</p>"
    except Exception as e:
        improve_stats = f"<p>Database Error (Improvements): {e}</p>"

    # --- HTML layout 
    page_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Global Vaccine Trends</title>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                text-align: center;
                background-color: #f9f9f9;
                color: #111;
            }}

            header {{
                background-color: #4da6ff;
                padding: 10px 0;
                display: flex;
                justify-content: center;
                align-items: center;
            }}

            .header-content {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                width: 90%;
                max-width: 1200px;
            }}

            .logo {{
                height: 45px;
            }}

            input[type="search"] {{
                padding: 8px 12px;
                border: none;
                border-radius: 20px;
                width: 260px;
            }}

            nav a {{
                margin-left: 15px;
                text-decoration: none;
                color: #000;
                font-weight: bold;
            }}

            nav a:hover {{
                color: #004c99;
            }}

            h1 {{
                margin-top: 35px;
                font-size: 32px;
                font-weight: bold;
            }}

            h1 a {{
                text-decoration: none;
                color: #111;
                transition: color 0.3s;
            }}

            h1 a:hover {{
                color: #4da6ff;
            }}

            .stats-section {{
                display: flex;
                justify-content: center;
                gap: 40px;
                flex-wrap: wrap;
                margin-top: 30px;
            }}

            .stat-box {{
                background: white;
                border: 2px solid #4da6ff;
                border-radius: 15px;
                width: 350px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
            }}

            .stat-box h2 {{
                color: #004c99;
            }}

            .facts {{
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 30px;
                margin-top: 30px;
                margin-bottom: 30px;
            }}

            .fact-box {{
                background: white;
                border: 2px solid #000;
                border-radius: 15px;
                width: 230px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.2s ease;
            }}

            .fact-box:hover {{
                transform: translateY(-5px);
            }}

            .fact-box p {{
                font-weight: bold;
                margin-bottom: 10px;
            }}

            .fact-box a {{
                text-decoration: none;
                color: #004c99;
            }}

            .fact-box a:hover {{
                text-decoration: underline;
            }}

            .explore-btn {{
                background-color: #4da6ff;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 25px;
                font-weight: bold;
                cursor: pointer;
                transition: background 0.3s;
                margin-bottom: 40px;
            }}

            .explore-btn:hover {{
                background-color: #3385cc;
            }}
        </style>
    </head>
    <body>

        <header>
            <div class="header-content">
                <div class="left-section">
                    <img src="download.png" alt="WHO Logo" class="logo" />
                </div>

                <div class="middle-section">
                    <input type="search" placeholder="Search..." />
                </div>

                <nav class="right-section">
                    <a href="/">Home</a>
                    <a href="#">Contact</a>
                </nav>
            </div>
        </header>

        <h1><a href="page_3.html">Global Vaccine Trends</a></h1>

        <!-- New top statistics section -->
        <div class="stats-section">
            <div class="stat-box">
                <h2>Spain, Italy, Argentinia Stats</h2>
                {main_stats}
            </div>

            <div class="stat-box">
                <h2>Top 3 Vaccine Improvements</h2>
                {improve_stats}
            </div>
        </div>

        <!-- Original facts section -->
        <div class="facts">
            <div class="fact-box">
                <a href="page_2.html">
                    <p>Vaccination rates by country/region</p>
                </a>
            </div>

            <div class="fact-box">
                <a href="page_3.html">
                    <p>Countries with biggest vaccination improvement</p>
                </a>
            </div>

            <div class="fact-box">
                <a href="/page1b.html">
                    <p>Mission Statement<br>(purpose, personas, team info)</p>
                </a>
            </div>

            <div class="fact-box">
                <a href="/page2b.html">
                    <p>Infection Data by Country and Population</p>
                </a>
            </div>

            <div class="fact-box">
                <a href="/page3b.html">
                    <p>Infection Data by Region</p>
                </a>
            </div>
        </div>

        <button class="explore-btn" onclick="window.location.href='page_3.html'">EXPLORE MORE</button>

    </body>
    </html>
    """
    return page_html
