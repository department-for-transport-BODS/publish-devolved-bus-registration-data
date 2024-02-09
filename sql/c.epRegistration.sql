CREATE TABLE IF NOT EXISTS ep_registration (
    id SERIAL PRIMARY KEY,
    otc_licence_id INTEGER,
    route_number VARCHAR(255),
    route_description VARCHAR(255),
    variation_number INTEGER,
    start_point VARCHAR(255),
    finish_point VARCHAR(255),
    via VARCHAR(255),
    subsidised VARCHAR(5),
    subsidy_detail VARCHAR(255),
    is_short_notice BOOLEAN,
    received_date DATE,
    granted_date DATE,
    effective_date DATE,
    end_date DATE,
    otc_operator_id INTEGER,
    bus_service_type_id VARCHAR(255),
    bus_service_type_description VARCHAR(255),
    registration_number VARCHAR(255),
    traffic_area_id VARCHAR(255),
    application_type VARCHAR(255),
    publication_text VARCHAR(255),
    other_details VARCHAR(255)
);

ALTER TABLE ep_registration
ADD CONSTRAINT fk_otc_licence
FOREIGN KEY (otc_licence_id) 
REFERENCES otc_licence(id);

ALTER TABLE ep_registration
ADD CONSTRAINT fk_otc_operator
FOREIGN KEY (otc_operator_id) 
REFERENCES otc_operator(id);