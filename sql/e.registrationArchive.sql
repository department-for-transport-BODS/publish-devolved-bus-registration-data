CREATE TABLE IF NOT EXISTS registration_archive (
    id SERIAL PRIMARY KEY,
    otc_licence_id INTEGER,
    route_number VARCHAR(255),
    route_description VARCHAR(255),
    variation_number INTEGER,
    start_point VARCHAR(255),
    finish_point VARCHAR(255),
    via VARCHAR(255),
    subsidised VARCHAR(10),
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
    other_details VARCHAR(255));
    
CREATE OR REPLACE FUNCTION handle_duplicate_records()
RETURNS TRIGGER AS
$func$
BEGIN
    INSERT INTO registration_archive (
        otc_licence_id,
        route_number,
        registration_number,
        route_description,
        variation_number,
        start_point,
        finish_point,
        via,
        subsidised,
        subsidy_detail,
        is_short_notice,
        received_date,
        granted_date,
        effective_date,
        end_date,
        otc_operator_id,
        bus_service_type_id,
        bus_service_type_description,
        traffic_area_id,
        application_type,
        publication_text,
        other_details
    )
    VALUES (
        OLD.otc_licence_id,
        OLD.route_number,
        OLD.registration_number,
        OLD.route_description,
        OLD.variation_number,
        OLD.start_point,
        OLD.finish_point,
        OLD.via,
        OLD.subsidised,
        OLD.subsidy_detail,
        OLD.is_short_notice,
        OLD.received_date,
        OLD.granted_date,
        OLD.effective_date,
        OLD.end_date,
        OLD.otc_operator_id,
        OLD.bus_service_type_id,
        OLD.bus_service_type_description,
        OLD.traffic_area_id,
        OLD.application_type,
        OLD.publication_text,
        OLD.other_details
    );
    RETURN NEW;
END;
$func$
LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER check_duplicate_records
AFTER UPDATE ON ep_registration
FOR EACH ROW
EXECUTE FUNCTION handle_duplicate_records();