def get_page_html(form_data):
    print("About to return Page 3...")
    # HTML content for Page 3
    page_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Global Vaccine Trends</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
                margin: 0;
                text-align: center;
                color: #111;
            }
            header {
                background-color: #4da6ff;
                padding: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            input[type="search"] {
                border-radius: 15px;
                padding: 6px 12px;
                border: none;
            }
            nav a {
                margin: 0 10px;
                text-decoration: none;
                color: #000;
                font-weight: bold;
            }
            nav a:hover {
                color: #004c99;
            }
            h1 {
                margin-top: 30px;
                font-weight: bold;
            }
            select {
                padding: 8px;
                margin: 10px;
                border: 2px solid #333;
                border-radius: 5px;
            }
            table {
                margin: 30px auto;
                border-collapse: collapse;
                width: 70%;
                box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
            }
            th, td {
                border: 1px solid #000;
                padding: 12px;
                text-align: center;
            }
            th {
                background-color: #4da6ff;
                color: white;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            .back-link {
                display: inline-block;
                margin-top: 25px;
                text-decoration: none;
                color: #4da6ff;
                font-weight: bold;
            }
            .back-link:hover {
                text-decoration: underline;
            }
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

        <form>
            <select name="antigen">
                <option value="All">All Antigens</option>
                <option value="Measles">Measles</option>
                <option value="Polio">Polio</option>
                <option value="COVID-19">COVID-19</option>
            </select>

            <select name="year">
                <option value="All">All Years</option>
                <option value="2000">2000</option>
                <option value="2024">2024</option>
            </select>
        </form>

        <table>
            <tr>
                <th>Country</th>
                <th>2000</th>
                <th>2024</th>
                <th>Improvement</th>
            </tr>
            <tr>
                <td>Uganda</td>
                <td>60%</td>
                <td>95%</td>
                <td>+35%</td>
            </tr>
            <tr>
                <td>Australia</td>
                <td>80%</td>
                <td>96%</td>
                <td>+13%</td>
            </tr>
            <tr>
                <td>United Kingdom</td>
                <td>85%</td>
                <td>97%</td>
                <td>+13%</td>
            </tr>
        </table>

        <a class="back-link" href="/">← Back to Home</a>
    </body>
    </html>
    """
    return page_html
