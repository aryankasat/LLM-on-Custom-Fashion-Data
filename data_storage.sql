-- Create the database
CREATE DATABASE tshirts;
USE tshirts;

-- Create the t_shirts table
CREATE TABLE t_shirts(
    t_shirt_id INT AUTO_INCREMENT PRIMARY KEY,
    company ENUM('Max', 'Shoppers Stop', 'Wrogen', 'United Colors of Benetton') NOT NULL,
    color ENUM('Grey', 'Yellow', 'Green', 'Orange') NOT NULL,
    size ENUM('S', 'M', 'L') NOT NULL,
    price INT CHECK (price BETWEEN 10 AND 50),
    stock_quantity INT NOT NULL,
    UNIQUE KEY company_color_size (company, color, size)
);

-- Create the discounts table
CREATE TABLE discounts(
    discount_id INT AUTO_INCREMENT PRIMARY KEY,
    t_shirt_id INT NOT NULL,
    pct_discount DECIMAL(5,2) CHECK (pct_discount BETWEEN 0 AND 100),
    FOREIGN KEY (t_shirt_id) REFERENCES t_shirts(t_shirt_id)
);

-- Create a stored procedure to populate the t_shirts table
DELIMITER //
CREATE PROCEDURE PopulateTShirts()
BEGIN
    DECLARE counter INT DEFAULT 0;
    DECLARE max_records INT DEFAULT 100;
    DECLARE company ENUM('Max', 'Shoppers Stop', 'Wrogen', 'United Colors of Benetton');
    DECLARE color ENUM('Grey', 'Yellow', 'Green', 'Orange');
    DECLARE size ENUM('S', 'M', 'L');
    DECLARE price INT;
    DECLARE stock INT;

    -- Seed the random number generator
    SET SESSION rand_seed1 = UNIX_TIMESTAMP();

    WHILE counter < max_records DO
        -- Generate random values
        SET company = ELT(FLOOR(1 + RAND() * 4), 'Max', 'Shoppers Stop', 'Wrogen', 'United Colors of Benetton');
        SET color = ELT(FLOOR(1 + RAND() * 4), 'Grey', 'Yellow', 'Green', 'Orange');
        SET size = ELT(FLOOR(1 + RAND() * 3), 'S', 'M', 'L');
        SET price = FLOOR(10 + RAND() * 41);
        SET stock = FLOOR(10 + RAND() * 91);

        -- Attempt to insert a new record
        -- Duplicate brand, color, size combinations will be ignored due to the unique constraint
        BEGIN
            DECLARE CONTINUE HANDLER FOR 1062 BEGIN END;  -- Handle duplicate key error
            INSERT INTO t_shirts (company, color, size, price, stock_quantity)
            VALUES (company, color, size, price, stock);
            SET counter = counter + 1;
        END;
    END WHILE;
END//
DELIMITER ;

-- Call the stored procedure to populate the t_shirts table
CALL PopulateTShirts();

-- Insert at least 10 records into the discounts table
INSERT INTO discounts (t_shirt_id, pct_discount)
VALUES
(1, 10.00),
(2, 15.00),
(3, 20.00),
(4, 5.00),
(5, 25.00),
(6, 10.00),
(7, 30.00),
(8, 35.00),
(9, 40.00),
(10, 45.00);