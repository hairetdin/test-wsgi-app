BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS area
    (
    name VARCHAR(255)
    );
    CREATE TABLE IF NOT EXISTS city
        (
        name VARCHAR(255),
        area INTEGER,
        FOREIGN KEY (area) REFERENCES area(rowid)
        ON UPDATE SET NULL
        ON DELETE SET NULL
        );
CREATE TABLE IF NOT EXISTS people_info
    (
    last_name VARCHAR(100),
    first_name VARCHAR(100),
    patronymic_name VARCHAR(100),
    area integer,
    city integer,
    phone VARCHAR(255),
    email VARCHAR(255),
    additional text,
    FOREIGN KEY (area) REFERENCES area(rowid),
    FOREIGN KEY (city) REFERENCES city(rowid)
    ON UPDATE SET NULL
    ON DELETE SET NULL
    );
COMMIT;
