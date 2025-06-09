<?php
$mysqli = new mysqli("db", "root", "root", "vulnapp");

if ($mysqli->connect_errno) {
    die("Failed to connect to MySQL: " . $mysqli->connect_error);
}

if (isset($_GET['username'])) {
    $username = $_GET['username'];

    // Dumb filter removing spaces and some SQL keywords (case-sensitive)
    $filters = [' ', 'AND', 'and', 'OR', 'or', 'UNION', 'SELECT'];
    foreach ($filters as $filter) {
        $username = str_replace($filter, '', $username);
    }

    // Dangerous: directly inject filtered input
    $sql = "SELECT username, password FROM users WHERE username = '$username'";

    echo "<p>Injected SQL: <code>" . htmlspecialchars($sql) . "</code></p>";

    $result = $mysqli->query($sql);

    if (!$result) {
        die("<pre>SQL Error: " . htmlspecialchars($mysqli->error) . "</pre>");
    }

    if ($result->num_rows > 0) {
        echo "<h3>User Data Dump:</h3><table border='1' cellpadding='5'><tr><th>Username</th><th>Password</th></tr>";
        while ($row = $result->fetch_assoc()) {
            echo "<tr><td>" . htmlspecialchars($row['username']) . "</td><td>" . htmlspecialchars($row['password']) . "</td></tr>";
        }
        echo "</table>";
    } else {
        echo "<h3>No user found.</h3>";
    }
} else {
    echo "<p>Try changing the username via: ?username=your_input</p>";
}
?>
