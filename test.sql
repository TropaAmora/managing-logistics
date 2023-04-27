SELECT user.id, client.name
FROM client
INNER JOIN user
ON user.id = client.user_id;