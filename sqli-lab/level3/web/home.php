<?php
session_start();
require 'db.php';

if (!isset($_SESSION['username'])) {
    header('Location: index.php');
    exit;
}

$sql = "SELECT username FROM users";
$res = mysqli_query($conn, $sql);
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Home - Vulnerable App</title>
<link rel="stylesheet" href="style.css" />
</head>
<body>
<div class="container">
    <h2>Welcome, <?=htmlspecialchars($_SESSION['username'])?></h2>
    <a href="logout.php" class="logout">Logout</a>

    <h3>Users:</h3>
    <ul>
        <?php while ($row = mysqli_fetch_assoc($res)): ?>
            <li><a href="profile.php?user=<?=urlencode($row['username'])?>"><?=htmlspecialchars($row['username'])?></a></li>
        <?php endwhile; ?>
    </ul>
</div>
</body>
</html>
