<?php
session_start();
require 'db.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';

    // No hashing - simple check vulnerable to enumeration
    $sql = "SELECT * FROM users WHERE username='$username' AND password='$password' LIMIT 1";
    $res = mysqli_query($conn, $sql);

    if ($res && mysqli_num_rows($res) === 1) {
        $_SESSION['username'] = $username;
        header('Location: home.php');
        exit;
    } else {
        $error = "Invalid credentials";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Login - Vulnerable App</title>
<link rel="stylesheet" href="style.css" />
</head>
<body>
<div class="container">
    <form method="post" class="login-form">
        <h2>Login</h2>
        <?php if (isset($error)): ?>
            <p class="error"><?=htmlspecialchars($error)?></p>
        <?php endif; ?>
        <input type="text" name="username" placeholder="Username" required autofocus />
        <input type="password" name="password" placeholder="Password" required />
        <button type="submit">Log In</button>
    </form>
</div>
</body>
</html>
