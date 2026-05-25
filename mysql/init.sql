CREATE TABLE IF NOT EXISTS functions (

    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(255) UNIQUE NOT NULL,

    runtime VARCHAR(50) NOT NULL,

    image VARCHAR(255) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS function_entrypoints (

    id INT AUTO_INCREMENT PRIMARY KEY,

    function_id INT NOT NULL,

    function_name VARCHAR(255) NOT NULL,

    entrypoint VARCHAR(255) NOT NULL,

    FOREIGN KEY (function_id)
    REFERENCES functions(id)
    ON DELETE CASCADE
);