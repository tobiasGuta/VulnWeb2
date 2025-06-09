<?php
session_start();

// Hardcoded logged-in user (for demo: change to 'admin' or 'randomuser')
if (!isset($_SESSION['username'])) {
    $_SESSION['username'] = 'randomuser'; 
}
$currentUser = $_SESSION['username'];

// SQLite DB path (persist in /tmp for container life)
$db = new PDO('sqlite:/tmp/users.db');
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

// Initialize DB if needed
$db->exec("CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    name TEXT NOT NULL
)");

// Insert default users if not exist
$stmt = $db->prepare("SELECT COUNT(*) FROM users");
$count = $stmt->execute() ? $stmt->fetchColumn() : 0;
if ($count == 0) {
    $db->exec("INSERT INTO users (username, name) VALUES
        ('admin', 'Administrator'),
        ('randomuser', 'Random User')
    ");
}

// Blacklist filter (case-sensitive naive)
$special_chars = array(
    "OR", "or", "AND", "and", "UNION", "SELECT", "WHERE", "'",
    " ",    // literal space
    "\t",   // tab
    "\n",   // newline
    "\r",   // carriage return
    "\0",   // null byte
);

function contains_blacklist($input, $blacklist) {
    foreach ($blacklist as $word) {
        if (strpos($input, $word) !== false) {
            return true;
        }
    }
    return false;
}

$message = "";
$message_type = "";
$executed_query = "";
$query_result = "";

function getRandomAvatar() {
    $avatars = [
        "https://randomuser.me/api/portraits/men/32.jpg",
        "https://randomuser.me/api/portraits/women/44.jpg",
        "https://randomuser.me/api/portraits/men/76.jpg",
        "https://randomuser.me/api/portraits/women/68.jpg",
        "https://randomuser.me/api/portraits/men/15.jpg",
        "https://randomuser.me/api/portraits/women/50.jpg"
    ];
    return $avatars[array_rand($avatars)];
}

$avatar = getRandomAvatar();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $newNameRaw = $_POST['name'] ?? '';
    $newName = urldecode($newNameRaw);

    if (contains_blacklist($newNameRaw, $GLOBALS['special_chars'])) {
        $message = "Input blocked by filter. Try URL encoding or case tricks.";
        $message_type = "error";
    } else {
        // Craft vulnerable query with user input concatenated directly
        $executed_query = "UPDATE users SET name = '$newName' WHERE username = '$currentUser'";

        try {
            $affected = $db->exec($executed_query);
            if ($affected !== false) {
                $message = "Name updated for user $currentUser.";
                $message_type = "success";
                $query_result = "Rows affected: $affected";
            } else {
                $message = "Update failed.";
                $message_type = "error";
                $query_result = "No rows affected.";
            }
        } catch (PDOException $e) {
            $message = "SQL error during update.";
            $message_type = "error";
            $query_result = "Error: " . $e->getMessage();
        }
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Profile Editor</title>
<link rel="stylesheet" href="style.css" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
</head>
<body>
<div class="profile-card">

    <div class="profile-pic" style="background-image: url('<?= htmlspecialchars($avatar) ?>');"></div>

    <div class="username"><?= htmlspecialchars($currentUser) ?></div>
    <div class="user-status">Logged in user</div>

    <h3>Users:</h3>
    <ul class="users-list">
    <?php
    $stmt = $db->query("SELECT username, name FROM users");
    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
        echo "<li><span class='user-username'>" . htmlspecialchars($row['username']) . "</span>: <span class='user-name'>" . htmlspecialchars($row['name']) . "</span></li>";
    }
    ?>
    </ul>

    <?php if (!empty($message)): ?>
        <div class="message <?= $message_type ?>"><?= htmlspecialchars($message) ?></div>
        <div class="sql-output">
            <strong>Executed Query:</strong><br />
            <code><?= htmlspecialchars($executed_query) ?></code><br /><br />
            <strong>Result:</strong><br />
            <code><?= htmlspecialchars($query_result) ?></code>
        </div>
    <?php endif; ?>

    <form method="POST" autocomplete="off" class="update-form">
        <label for="name">Change your name:</label>
        <input id="name" name="name" placeholder="New display name" />
        <button type="submit">Update</button>
    </form>

</div>
</body>
</html>
