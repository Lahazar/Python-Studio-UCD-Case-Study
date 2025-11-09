import sqlite3

def get_page_html(formdata):
    conn = sqlite3.connect('immunisation.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(DISTINCT name) FROM Country")
    total_countries = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(cases) FROM InfectionData")
    infection_cases = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(DISTINCT year) FROM InfectionData")
    total_years = cursor.fetchone()[0] or 0

    cursor.execute("SELECT inf_type, COUNT(*) FROM InfectionData GROUP BY inf_type ORDER BY COUNT(*) DESC LIMIT 1")
    most_common_type_row = cursor.fetchone()
    most_common_type = most_common_type_row[0] if most_common_type_row else 'N/A'

    cursor.execute(
        """SELECT country, population FROM CountryPopulation 
           WHERE year = (SELECT MAX(year) FROM CountryPopulation)
           ORDER BY population DESC LIMIT 1"""
    )
    pop_row = cursor.fetchone()
    largest_country = pop_row[0] if pop_row else 'N/A'
    largest_population = pop_row[1] if pop_row else 0

    conn.close()

    html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="UTF-8">
            <title>Mission Statement | Vaccination Dashboard</title>
            <link rel="stylesheet" href="page1B/style.css">
        </head>
        <body>
            <header>
                <nav class="navbar">
                    <div class="nav-left">
                        <img src="page1B/download.png" alt="WHO Logo" class="logo">
                    </div>
                    <div class="nav-center">
                        <input type="search" placeholder="Search..."/>
                    </div>
                    <div class="nav-right">
                        <a href="/">Home</a>
                        <a href="/page1b.html">About</a>
                        <a href="#">Contact</a>
                    </div>
                </nav>
            </header>
            <main class="hero">
                <section>
                    <h2>Empowering Data-Driven Disease Control</h2>
                    <h1>Accelerate Vaccine Research and Action with Trusted Global Data</h1>
                    <p>This platform brings together real-time vaccination and infection data, segmented by economic status and region, supporting epidemiologists and researchers tackling emerging health challenges.</p>
                    <button>Get Started</button>
                    <button>Learn More</button>
                </section>
                <section class="db-facts" style="margin-top:36px;">
                    <h3>Data Highlights</h3>
                    <ul>
                        <li>This database tracks <strong>{total_countries}</strong> countries worldwide.</li>
                        <li>An incredible <strong>{infection_cases:,}</strong> infection cases recorded across <strong>{total_years}</strong> years.</li>
                        <li>The most reported infection type is <strong>{most_common_type}</strong>.</li>
                        <li>The largest population in the most recent year is <strong>{largest_country}</strong> with <strong>{largest_population:,}</strong> people.</li>
                    </ul>
                </section>
            </main>
        </body>
    </html>
    """
    return html
