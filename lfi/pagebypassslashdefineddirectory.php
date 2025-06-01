<?php
// Error reporting for debugging
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Language list for display
$languages = ['languages/en.php', 'languages/es.php'];

// Get user input (must include 'languages/')
if (isset($_GET['lang'])) {
    $lang = $_GET['lang'];

    // ✅ Require lang to start with 'languages/'
    if (strpos($lang, 'languages/') === 0) {
        // Naive traversal prevention (bypassable with ....//)
        $lang = str_replace(['../', '..\\'], '', $lang);
        $file = $lang;
    } else {
        // ❌ Force 'languages/' prefix
        die("<div style='font-family: monospace; background: #330000; color: #ff6666; padding: 1rem; border-radius: 6px;'>🚫 Invalid path. Must begin with <code>languages/</code></div>");
    }
} else {
    $file = null;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Choose Language - LFI Demo</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #121212;
            color: #eee;
            padding: 2rem;
        }
        h1 {
            margin-bottom: 1rem;
        }
        ul {
            list-style-type: none;
            padding-left: 0;
            margin-bottom: 2rem;
        }
        li {
            margin-bottom: 0.5rem;
        }
        a {
            color: #4fc3f7;
            text-decoration: none;
            font-weight: 600;
        }
        a:hover {
            text-decoration: underline;
        }
        .content {
            background: #222;
            padding: 1rem;
            border-radius: 8px;
            white-space: pre-wrap;
            font-family: monospace;
            max-height: 400px;
            overflow-y: auto;
        }
    </style>
</head>
<body>

<h1>Choose Your Language (LFI Demo)</h1>

<ul>
    <?php foreach ($languages as $language): ?>
        <li><a href="?lang=<?= htmlspecialchars($language) ?>"><?= htmlspecialchars($language) ?></a></li>
    <?php endforeach; ?>
</ul>

<div class="content">
    <?php
    if ($file) {
        include($file); // 🔥 Still vulnerable if user inputs traversal inside languages/
    } else {
        echo "No language selected.";
    }
    ?>
</div>

</body>
</html>
