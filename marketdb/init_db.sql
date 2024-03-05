CREATE TABLE IF NOT EXISTS item (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR
);

CREATE TABLE IF NOT EXISTS store (
    id INTEGER NOT NULL,
    item_id INTEGER NOT NULL REFERENCES item (id),
    price INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY(id, item_id)
);

CREATE TABLE IF NOT EXISTS address (
    id INTEGER NOT NULL PRIMARY KEY,
    flat_number INTEGER NOT NULL,
    post_code INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS customer (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR NOT NULL,
    address_id INTEGER NOT NULL REFERENCES address (id)
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER NOT NULL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customer (id),
    item_id INTEGER NOT NULL REFERENCES item (id),
    quantity INTEGER NOT NULL
);

-- Insert sample data

INSERT INTO item VALUES (1, 'Milk', '1L bottle of milk');
INSERT INTO item VALUES (2, 'Kit Kat', 'a chocolate');
INSERT INTO item VALUES (3, 'Bread', 'a loaf of bread');
INSERT INTO item VALUES (4, 'Onion', 'an onions');

INSERT INTO store VALUES (1, 1, 6, 10);
INSERT INTO store VALUES (1, 2, 2, 25);
INSERT INTO store VALUES (1, 3, 4, 15);
INSERT INTO store VALUES (2, 1, 5, 5);
INSERT INTO store VALUES (2, 4, 1, 10);
INSERT INTO store VALUES (2, 2, 2, 30);

INSERT INTO address VALUES (1, 101, 10001);
INSERT INTO address VALUES (2, 201, 10002);
INSERT INTO address VALUES (3, 301, 10003);

INSERT INTO customer VALUES (1, 'Alex', 1);
INSERT INTO customer VALUES (2, 'Blake', 2);
INSERT INTO customer VALUES (3, 'Cam', 3);

INSERT INTO orders VALUES (1, 1, 3, 2);