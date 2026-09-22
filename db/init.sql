CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer TEXT NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    status TEXT NOT NULL
);

INSERT INTO orders (customer, amount, status) VALUES
    ('Acme Retail', 1499.99, 'confirmed'),
    ('Globex Labs', 250.00, 'processing');
