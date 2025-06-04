<?php include('config.php'); ?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>RootPress - Blog Viewer</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #f4f4f4;
            color: #333;
            margin: 0;
            padding: 0;
        }

        header {
            background: #222;
            color: white;
            padding: 20px;
            text-align: center;
        }

        .container {
            max-width: 900px;
            margin: 30px auto;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        h1 {
            margin-top: 0;
        }

        .article {
            margin-bottom: 40px;
        }

        .footer {
            text-align: center;
            color: #aaa;
            margin-top: 50px;
            padding-bottom: 20px;
        }

        code {
            background: #eee;
            padding: 2px 6px;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <header>
        <h1>RootPress Blog</h1>
        <p>Where stories are injected... literally</p>
    </header>

    <div class="container">
        <p><strong>🧪 Try this:</strong> Change the URL parameter like <code>?id=1</code>, <code>?id=0 UNION SELECT ...</code></p>
        <hr>

        <?php
        error_reporting(E_ALL);
        ini_set('display_errors', 1);

        if (isset($_GET['id'])) {
            $id = $_GET['id'];
            $query = "SELECT * FROM articles WHERE id = $id"; // VULNERABLE

            $result = $conn->query($query);

            if ($result) {
                if ($result->num_rows > 0) {
                    while($row = $result->fetch_assoc()) {
                        echo "<div class='article'>";
                        echo "<h2>" . $row['title'] . "</h2>";
                        echo "<p>" . $row['content'] . "</p>";
                        echo "</div>";
                    }
                } else {
                    echo "<p><em>No article found.</em></p>";
                }
            } else {
                echo "<p><strong>SQL Error:</strong> " . $conn->error . "</p>";
            }
        } else {
            echo "<p><em>No article selected. Try ?id=1</em></p>";
        }
        ?>
    </div>

    <div class="footer">
        <p>© 2025 RootPress. Powered by vulnerable PHP.</p>
    </div>
</body>
</html>
