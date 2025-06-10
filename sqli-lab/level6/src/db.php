<?php
$mysqli = new mysqli("db", "root", "rootpass", "vulnapp");

if ($mysqli->connect_error) {
    die("Connection failed: " . $mysqli->connect_error);
}
?>
