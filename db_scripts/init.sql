CREATE TABLE IF NOT EXISTS gp (
    -- Header
    ccsds_omm_vers      TEXT,
    comment             TEXT,
    creation_date       TIMESTAMP,
    originator          TEXT,

    -- Identity
    object_name         TEXT,
    object_id           TEXT,
    norad_cat_id        INTEGER PRIMARY KEY,
    gp_id               BIGINT,

    -- Metadata
    center_name         TEXT,
    ref_frame           TEXT,
    time_system         TEXT,
    mean_element_theory TEXT,
    classification_type TEXT,
    ephemeris_type      INTEGER,
    element_set_no      INTEGER,

    -- Mean Elements
    epoch               TIMESTAMP,
    mean_motion         DOUBLE PRECISION,
    eccentricity        DOUBLE PRECISION,
    inclination         DOUBLE PRECISION,
    ra_of_asc_node      DOUBLE PRECISION,
    arg_of_pericenter   DOUBLE PRECISION,
    mean_anomaly        DOUBLE PRECISION,

    -- TLE Parameters
    rev_at_epoch        INTEGER,
    bstar               DOUBLE PRECISION,
    mean_motion_dot     DOUBLE PRECISION,
    mean_motion_ddot    DOUBLE PRECISION,

    -- User Defined
    semimajor_axis      DOUBLE PRECISION,
    period              DOUBLE PRECISION,
    apoapsis            DOUBLE PRECISION,
    periapsis           DOUBLE PRECISION,
    object_type         TEXT,
    rcs_size            TEXT,
    country_code        TEXT,
    launch_date         DATE,
    site                TEXT,
    decay_date          DATE,
    file                BIGINT,

    -- TLE Lines
    tle_line0           VARCHAR(69),
    tle_line1           VARCHAR(69),
    tle_line2           VARCHAR(69)
);

-- Copy the CSV
COPY gp (
    ccsds_omm_vers, comment, creation_date, originator,
    object_name, object_id, center_name, ref_frame,
    time_system, mean_element_theory, epoch,
    mean_motion, eccentricity, inclination,
    ra_of_asc_node, arg_of_pericenter, mean_anomaly,
    ephemeris_type, classification_type, norad_cat_id,
    element_set_no, rev_at_epoch, bstar,
    mean_motion_dot, mean_motion_ddot,
    semimajor_axis, period, apoapsis, periapsis,
    object_type, rcs_size, country_code, launch_date,
    site, decay_date, file, gp_id,
    tle_line0, tle_line1, tle_line2
)
FROM '/tmp/omm_data.csv'
WITH (FORMAT csv, HEADER true, FORCE_NULL(decay_date, launch_date));
