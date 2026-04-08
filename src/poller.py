import os
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import text

SPACETRACK_LOGIN = "https://www.space-track.org/ajaxauth/login"
SPACETRACK_GP = "https://www.space-track.org/basicspacedata/query/class/gp/orderby/EPOCH desc/limit/1000/format/json"

session = requests.Session()

def login():
    session.post(SPACETRACK_LOGIN, data={
        "identity": os.environ["SPACETRACK_USER"],
        "password": os.environ["SPACETRACK_PASS"]
    })

def poll_and_upsert(engine):
    resp = session.get(SPACETRACK_GP)
    records = resp.json()

    with engine.connect() as conn:
        for r in records:
            conn.execute(text("""
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
                    :object_name, :object_id, :norad_cat_id, :gp_id,
                    :center_name, :ref_frame, :time_system, :mean_element_theory,
                    :classification_type, :ephemeris_type, :element_set_no,
                    :epoch, :mean_motion, :eccentricity, :inclination,
                    :ra_of_asc_node, :arg_of_pericenter, :mean_anomaly,
                    :rev_at_epoch, :bstar, :mean_motion_dot, :mean_motion_ddot,
                    :semimajor_axis, :period, :apoapsis, :periapsis,
                    :object_type, :rcs_size, :country_code, :launch_date,
                    :site, :decay_date, :file
                )
                ON CONFLICT (norad_cat_id) DO UPDATE SET
                    epoch = EXCLUDED.epoch,
                    mean_motion = EXCLUDED.mean_motion,
                    eccentricity = EXCLUDED.eccentricity,
                    inclination = EXCLUDED.inclination,
                    ra_of_asc_node = EXCLUDED.ra_of_asc_node,
                    arg_of_pericenter = EXCLUDED.arg_of_pericenter,
                    mean_anomaly = EXCLUDED.mean_anomaly,
                    bstar = EXCLUDED.bstar,
                    mean_motion_dot = EXCLUDED.mean_motion_dot,
                    gp_id = EXCLUDED.gp_id,
                    file = EXCLUDED.file
            """), {
                "object_name": r.get("OBJECT_NAME"),
                "object_id": r.get("OBJECT_ID"),
                "norad_cat_id": r.get("NORAD_CAT_ID"),
                "gp_id": r.get("GP_ID"),
                "center_name": r.get("CENTER_NAME"),
                "ref_frame": r.get("REF_FRAME"),
                "time_system": r.get("TIME_SYSTEM"),
                "mean_element_theory": r.get("MEAN_ELEMENT_THEORY"),
                "classification_type": r.get("CLASSIFICATION_TYPE"),
                "ephemeris_type": r.get("EPHEMERIS_TYPE"),
                "element_set_no": r.get("ELEMENT_SET_NO"),
                "epoch": r.get("EPOCH"),
                "mean_motion": r.get("MEAN_MOTION"),
                "eccentricity": r.get("ECCENTRICITY"),
                "inclination": r.get("INCLINATION"),
                "ra_of_asc_node": r.get("RA_OF_ASC_NODE"),
                "arg_of_pericenter": r.get("ARG_OF_PERICENTER"),
                "mean_anomaly": r.get("MEAN_ANOMALY"),
                "rev_at_epoch": r.get("REV_AT_EPOCH"),
                "bstar": r.get("BSTAR"),
                "mean_motion_dot": r.get("MEAN_MOTION_DOT"),
                "mean_motion_ddot": r.get("MEAN_MOTION_DDOT"),
                "semimajor_axis": r.get("SEMIMAJOR_AXIS"),
                "period": r.get("PERIOD"),
                "apoapsis": r.get("APOAPSIS"),
                "periapsis": r.get("PERIAPSIS"),
                "object_type": r.get("OBJECT_TYPE"),
                "rcs_size": r.get("RCS_SIZE"),
                "country_code": r.get("COUNTRY_CODE"),
                "launch_date": r.get("LAUNCH_DATE") or None,
                "site": r.get("SITE"),
                "decay_date": r.get("DECAY_DATE") or None,
                "file": r.get("FILE"),
            })
        conn.commit()
