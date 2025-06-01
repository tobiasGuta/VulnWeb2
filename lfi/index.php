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
            <a href="?page=pages/home.php">Home</a>
            <a href="?page=pages/about.php">About</a>
            <a href="?page=pages/contact.php">Contact</a>
        </nav>
    </header>

    <main>
        <?php
        // ✅ Actually read the file contents (LFI)
        echo "<pre>";
        echo file_get_contents($page); // Vulnerable as hell
        echo "</pre>";
        ?>
    </main>

</body>
</html>
