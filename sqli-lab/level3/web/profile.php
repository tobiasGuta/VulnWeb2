<?php
session_start();
require 'db.php';

if (!isset($_SESSION['username'])) {
    header('Location: index.php');
    exit;
}

$loggedInUser = $_SESSION['username'];
$profileUser = $_GET['user'] ?? $loggedInUser;

// Fetch profile info
$sql = "SELECT username FROM users WHERE username = '$profileUser'";
$res = mysqli_query($conn, $sql);

if (!$res || mysqli_num_rows($res) === 0) {
    die("User not found.");
}

$user = mysqli_fetch_assoc($res);
$currentUsername = $user['username'];
$message = "";

// Only allow logged-in user to update their own username
if ($_SERVER['REQUEST_METHOD'] === 'POST' && $loggedInUser === $profileUser) {
    $newUsername = $_POST['new_username'] ?? '';

    // ⚠️ Vulnerable to SQLi
    $updateSQL = "UPDATE users SET username='$newUsername' WHERE username='$profileUser'";
    $result = mysqli_query($conn, $updateSQL);

    if ($result) {
        $message = "Username updated successfully.";
        $_SESSION['username'] = $newUsername;
        $profileUser = $newUsername;
        $currentUsername = $newUsername;
    } else {
        $message = "Update failed: " . mysqli_error($conn);
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title><?=htmlspecialchars($currentUsername)?>'s Profile</title>
    <link rel="stylesheet" href="style.css" />
</head>
<body>
<div class="profile-container">
    <div class="profile-card">
        <img src="https://i.pravatar.cc/150?u=<?=urlencode($currentUsername)?>" alt="Profile Picture" class="profile-pic" />
        <h2><?=htmlspecialchars($currentUsername)?></h2>
        <p class="profile-email"><?=htmlspecialchars($currentUsername)?>@vulnlab.local</p>
        <div class="actions">
            <a href="home.php" class="btn">Home</a>
            <a href="logout.php" class="btn">Logout</a>
        </div>

        <?php if ($loggedInUser === $profileUser): ?>
        <form method="post" class="update-form">
            <label for="new_username">Update Username</label><br />
            <input type="text" name="new_username" id="new_username" value="<?=htmlspecialchars($currentUsername)?>" required />
            <button type="submit">Update</button>
        </form>
        <?php endif; ?>

        <?php if ($message): ?>
            <p class="message"><?=htmlspecialchars($message)?></p>
        <?php endif; ?>
    </div>
</div>
</body>
</html>
