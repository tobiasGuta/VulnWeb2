<?php
$host = 'mysql';           // Must match the docker-compose service name
$user = 'root';
$pass = 'root';
$db   = 'sqli_one';

$conn = new mysqli($host, $user, $pass, $db);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
