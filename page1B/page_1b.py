def get_page_html(formdata):
    html = """
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
                        <a href="index.html">Home</a>
                        <a href="#">About</a>
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
            </main>

        </body>
    </html>
    """
    return html