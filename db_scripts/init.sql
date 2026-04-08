CREATE TABLE IF NOT EXISTS gp (
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
    file                BIGINT
);

-- Fixture
INSERT INTO gp (
    object_name, object_id, norad_cat_id, gp_id,
    center_name, ref_frame, time_system, mean_element_theory,
    classification_type, ephemeris_type, element_set_no,
    epoch, mean_motion, eccentricity, inclination,
    ra_of_asc_node, arg_of_pericenter, mean_anomaly,
    rev_at_epoch, bstar, mean_motion_dot, mean_motion_ddot,
    semimajor_axis, period, apoapsis, periapsis,
    object_type, rcs_size, country_code, launch_date,
    site, decay_date, file
) VALUES (
    'FREGAT R/B', '2026-071B', 68572, 318237661,
    'EARTH', 'TEME', 'UTC', 'SGP4',
    'U', 0, 999,
    '2026-04-03T07:42:42.175872', 2.01041412, 0.73138199, 63.0589,
    237.9448, 284.9724, 10.3188,
    1, 0.00035051942000, -0.00001541, 0.0,
    26518.248, 716.270, 39535.082, 745.144,
    'ROCKET BODY', NULL, NULL, NULL,
    NULL, NULL, 5115996
);