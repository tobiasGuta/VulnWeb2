<?php
$page = isset($_GET['page']) ? $_GET['page'] : 'pages/home.php';
?>
<!DOCTYPE html>
<html>
<head>
    <title>VulnSite</title>
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>
    <header>
        <h1>VulnSite 💀</h1>
        <nav>
            <a href="page.php?page=pages/home.php">Home</a>
            <a href="page.php?page=pages/about.php">About</a>
            <a href="page.php?page=pages/contact.php">Contact</a>
        </nav>
    </header>

    <main>
        <?php
        echo "<pre>";
        echo file_get_contents($page); // 💣 LFI vulnerable
        echo "</pre>";
        ?>
    </main>
</body>
</html>
