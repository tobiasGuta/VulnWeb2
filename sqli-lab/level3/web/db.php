<?php
// Connect to DB using env vars - procedural style
$host = getenv('DB_HOST') ?: 'localhost';
$user = getenv('DB_USER') ?: 'root';
$pass = getenv('DB_PASS') ?: '';
$dbname = getenv('DB_NAME') ?: 'vulnapp';

$conn = mysqli_connect($host, $user, $pass, $dbname);
if (!$conn) {
    die("DB connection failed: " . mysqli_connect_error());
}
?>
