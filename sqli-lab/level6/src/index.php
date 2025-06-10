<?php
require 'db.php';

$ua = $_SERVER['HTTP_USER_AGENT'] ?? 'unknown';

// Vulnerable: no sanitization on $ua in SELECT query
$query = "SELECT id, ip, user_agent, note FROM logins WHERE user_agent = '$ua'";

$result = $mysqli->query($query);

if ($result) {
    while ($row = $result->fetch_assoc()) {
        echo implode(" | ", $row) . "<br>";
    }
} else {
    echo "SQL Error: " . $mysqli->error;
}
?>
