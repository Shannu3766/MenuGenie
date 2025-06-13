<?php
session_start();

function generateOTP() {
    return str_pad(rand(0, 999999), 6, '0', STR_PAD_LEFT);
}

function sendOTP($email, $otp) {
    require 'PHPMailer/src/Exception.php';
    require 'PHPMailer/src/PHPMailer.php';
    require 'PHPMailer/src/SMTP.php';

    $mail = new PHPMailer\PHPMailer\PHPMailer(true);
    
    try {
        $mail->isSMTP();
        $mail->Host = 'smtp.gmail.com';
        $mail->SMTPAuth = true;
        $mail->Username = ''; // Your email here
        $mail->Password = ''; // Your SMTP app password here
        $mail->SMTPSecure = 'tls';
        $mail->Port = 587;

        $mail->setFrom('your_email@gmail.com', 'MenuGenie');
        $mail->addAddress($email);
        $mail->isHTML(true);
        $mail->Subject = 'Your MenuGenie Verification Code';
        $mail->Body = "
            <h2>Email Verification</h2>
            <p>Your verification code is: <strong>{$otp}</strong></p>
            <p>This code will expire in 10 minutes.</p>
            <p>If you didn't request this code, please ignore this email.</p>
        ";

        $mail->send();
        return true;
    } catch (Exception $e) {
        return false;
    }
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = $_POST['action'] ?? '';
    
    if ($action === 'generate') {
        $email = filter_var($_POST['email'], FILTER_VALIDATE_EMAIL);
        if (!$email) {
            echo json_encode(['success' => false, 'message' => 'Invalid email address']);
            exit;
        }

        $otp = generateOTP();
        $_SESSION['otp'] = $otp;
        $_SESSION['otp_email'] = $email;
        $_SESSION['otp_time'] = time();

        if (sendOTP($email, $otp)) {
            echo json_encode(['success' => true, 'message' => 'OTP sent successfully']);
        } else {
            echo json_encode(['success' => false, 'message' => 'Failed to send OTP']);
        }
    }
    elseif ($action === 'verify') {
        $otp = $_POST['otp'] ?? '';
        $email = $_POST['email'] ?? '';

        if (empty($otp) || empty($email)) {
            echo json_encode(['success' => false, 'message' => 'Missing OTP or email']);
            exit;
        }

        if (!isset($_SESSION['otp']) || !isset($_SESSION['otp_email']) || !isset($_SESSION['otp_time'])) {
            echo json_encode(['success' => false, 'message' => 'OTP expired or not generated']);
            exit;
        }

        if (time() - $_SESSION['otp_time'] > 600) { // 10 minutes expiry
            echo json_encode(['success' => false, 'message' => 'OTP expired']);
            exit;
        }

        if ($_SESSION['otp'] === $otp && $_SESSION['otp_email'] === $email) {
            $_SESSION['email_verified'] = true;
            echo json_encode(['success' => true, 'message' => 'OTP verified successfully']);
        } else {
            echo json_encode(['success' => false, 'message' => 'Invalid OTP']);
        }
    }
}
?> 