<?php
$base_dir = __DIR__ . '/languages/';
$lang_raw = isset($_GET['lang']) ? $_GET['lang'] : 'EN';
$lang = urldecode($lang_raw);

$simulated = false;

if (strpos($lang, "\0") !== false || strpos($lang, '%00') !== false) {
    $truncated = explode('%00', $lang)[0];
    $truncated = explode("\0", $truncated)[0];
    $real_path = $truncated;
    $simulated = true;
} else {
    $real_path = $base_dir . $lang . '.php';
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>VulnSite</title>
    <link rel="stylesheet" href="assets/style.css">
    <style>
        .lang-selector {
            background-color: #1e1e1e;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }

        .lang-selector h3 {
            margin-top: 0;
        }

        .lang-selector a {
            display: inline-block;
            margin: 5px 10px 5px 0;
            padding: 6px 10px;
            background: #2a2a2a;
            border-radius: 6px;
            color: #00ffe7;
            text-decoration: none;
            transition: background 0.2s;
        }

        .lang-selector a:hover {
            background: #333;
        }

        code {
            background: #000;
            padding: 2px 6px;
            border-radius: 4px;
            color: #00ffe7;
        }

        pre {
            background: #000;
            padding: 10px;
            border-radius: 8px;
            overflow-x: auto;
        }

        .output {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <header>
        <h1>VulnSite 💀</h1>
        <nav>
            <a href="page.php?page=pages/home.php">Home</a>
            <a href="page.php?page=pages/about.php">About</a>
            <a href="page.php?page=pages/contact.php">Contact</a>
            <a href="blackbox.php">LFI Demo</a>
        </nav>
    </header>

    <main>
        <h1>🕵️‍♂️ Black Box LFI Demo - <code>lang</code> param</h1>
        <p>Trying to include: 
            <code><?= $simulated ? htmlspecialchars($real_path) : 'languages/' . htmlspecialchars($lang) . '.php' ?></code>
        </p>

        <div class="output">
            <?php
            try {
                if ($simulated) {
                    echo "<p><strong style='color: #00ffe7;'>[Simulation]</strong> Null byte detected! Including raw file instead of PHP logic.</p>";
                    if (file_exists($real_path)) {
                        echo "<pre>" . htmlspecialchars(file_get_contents($real_path)) . "</pre>";
                    } else {
                        echo "<pre style='color:red;'>Error: File not found at " . htmlspecialchars($real_path) . "</pre>";
                    }
                } else {
                    if (!file_exists($real_path)) {
                        throw new Exception("Warning: include(languages/{$lang}.php): failed to open stream: No such file or directory in " . __FILE__ . " on line " . __LINE__);
                    }
                    include $real_path;
                }
            } catch (Exception $e) {
                echo "<pre style='color:red;'>" . htmlspecialchars($e->getMessage()) . "</pre>";
            }
            ?>
        </div>

        <div class="lang-selector">
            <h3>🌐 Try Switching Languages</h3>
            <a href="?lang=EN">lang=EN</a>
            <a href="?lang=ES">lang=ES</a>
        </div>
    </main>
</body>
</html>
