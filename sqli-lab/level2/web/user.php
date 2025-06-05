<?php
$host = 'db';
$user = 'root';
$pass = 'root';
$db = 'blind_sqli';

$conn = new mysqli($host, $user, $pass, $db);
if ($conn->connect_error) {
    die("Connection failed");
}

$id = $_GET['id'] ?? '';

$sql = "SELECT * FROM users WHERE username = '$id'";
$result = $conn->query($sql);
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>User Lookup</title>
  <style>
    body {
      background-color: #0e1a25;
      color: #e2e8f0;
      font-family: "Segoe UI", sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
    .card {
      background: #1a2d3b;
      padding: 2rem;
      border-radius: 8px;
      box-shadow: 0 0 15px rgba(0,0,0,0.5);
      width: 350px;
      text-align: center;
    }
    h2 {
      margin-bottom: 1rem;
      color: #90cdf4;
    }
    .result {
      padding: 1rem;
      border: 1px solid #2c3e50;
      border-radius: 4px;
      background: #233445;
      color: #fff;
    }
  </style>
</head>
<body>
  <div class="card">
    <h2>User Verification Portal</h2>
    <div class="result">
      <?php
        if ($result && $result->num_rows > 0) {
            echo "✅ User Found";
        } else {
            echo "❌ No User Found";
        }
      ?>
    </div>
  </div>
</body>
</html>
