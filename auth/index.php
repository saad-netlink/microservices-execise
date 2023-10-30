<?php
require 'vendor/autoload.php';

use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;
use Slim\Factory\AppFactory;

$app = AppFactory::create();

// Read MySQL credentials from environment variables
$dbHost = getenv('DB_HOST');
$dbName = getenv('DB_NAME');
$dbUser = getenv('DB_USER');
$dbPassword = getenv('DB_PASSWORD');

$pdo = new \PDO("mysql:host=$dbHost;dbname=$dbName", $dbUser, $dbPassword);

$app->post('/validatetoken', function (Request $request, Response $response, $args) use ($pdo) {
    $data = json_decode($request->getBody(), true);

    if (!$data || !isset($data['token']) || !isset($data['version'])) {
        return $response->withJson(['error' => 'Invalid JSON request'], 400);
    }

    $token = $data['token'];
    $version = $data['version'];

    $stmt = $pdo->prepare("SELECT * FROM `auth` WHERE `key` = ? AND version = ?");
    $stmt->execute([$token, $version]);
    $result = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($result) {
        return $response->withJson(['valid' => true]);
    } else {
        return $response->withJson(['valid' => false]);
    }
});

$app->run();
