CREATE TABLE IF NOT EXISTS item (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR NOT NULL,
    price DECIMAL NOT NULL,
    description VARCHAR
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
    id INTEGER NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    customer_id INTEGER NOT NULL REFERENCES customer (id),
    order_time TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS order_items (
    order_id INTEGER NOT NULL REFERENCES orders (id),
    item_id INTEGER NOT NULL REFERENCES item (id),
    quantity INTEGER NOT NULL,
    PRIMARY KEY (order_id, item_id)
);

-- Insert sample data

INSERT INTO item VALUES (1, 'Milk', 5, '1L bottle of milk');
INSERT INTO item VALUES (2, 'Kit Kat', 1, 'a chocolate');
INSERT INTO item VALUES (3, 'Bread', 10.5, 'a loaf of bread');
INSERT INTO item VALUES (4, 'Onion', 2, 'an onion');

INSERT INTO address VALUES (1, 101, 10001);
INSERT INTO address VALUES (2, 201, 10002);
INSERT INTO address VALUES (3, 301, 10003);

INSERT INTO customer VALUES (1, 'Alex', 1);
INSERT INTO customer VALUES (2, 'Blake', 2);
INSERT INTO customer VALUES (3, 'Cam', 3);

INSERT INTO orders (customer_id, order_time) VALUES (1, '2024-03-18 10:30:00');
INSERT INTO orders (customer_id, order_time) VALUES (3, '2024-03-20 11:00:00');
INSERT INTO orders (customer_id, order_time) VALUES (2, '2024-03-25 15:00:00');

INSERT INTO order_items VALUES (1, 2, 4);
INSERT INTO order_items VALUES (1, 3, 2);
INSERT INTO order_items VALUES (1, 1, 1);
INSERT INTO order_items VALUES (2, 2, 2);
INSERT INTO order_items VALUES (2, 4, 5);