import fastf1 as ff1
import fastf1.core
from fastf1.plotting import get_team_name

def get_lap_top_speed(lap: fastf1.core.Lap) -> int:
    """
    Get the top speed of a lap
    @param lap: the lap object
    @return: the top speed of the lap
    """
    telemetry = lap.get_car_data()
    return telemetry['Speed'].max()

def get_laps_top_speeds(driver_laps: fastf1.core.Laps, top_n: int = 15) -> list:
    """
    Get the top speeds from a set of laps
    @param driver_laps: Laps object
    @param top_n: Number of top speeds to return
    @return: List of tuples with top speed and DRS status
    """
    top_speeds = []
    for lap in driver_laps.iterlaps():
        top_speed = get_lap_top_speed(lap[1])
        drs_status = lap_has_drs(lap[1])
        if top_speed > 200:
            top_speeds.append((top_speed, drs_status))
    if top_n > len(top_speeds) > 2:
        for i in range(top_n - len(top_speeds)):
            top_speeds.append((-1, False))
    return sorted(top_speeds, reverse=True)[:top_n]

def get_session_driver_top_speeds(session: fastf1.core.Session, top_n: int = 15) -> dict:
    """
    Get the top speeds of the drivers in a session
    E.g. dict:
    {
        44: [(300, True), (299, False), ...],
        77: [(298, False), (297, True), ...],
        ...
    }
    @param session: F1 session object
    @param top_n: Number of top speeds to return
    @return: Dictionary with driver number as key and list of top speeds as value
    """
    top_speeds = {}
    for driver in session.drivers:
        driver_laps = session.laps.pick_driver(driver)
        driver_top_speeds = get_laps_top_speeds(driver_laps, top_n)
        if len(driver_top_speeds) > 0:
            top_speeds[driver] = driver_top_speeds
    return top_speeds

def get_session_team_top_1_speeds(session: fastf1.core.Session) -> list:
    """
    Get the top speed of the fastest lap of each team in a session
    @param session: F1 session object
    @return: Decreasingly sorted list of tuples with team name and top speed
    """
    team_top_speeds = {}
    for driver in session.drivers:
        team = session.get_driver(driver)['TeamName']
        try:
            team = get_team_name(team, session, short=True)
        except KeyError:
            team = team
        driver_laps = session.laps.pick_driver(driver)
        driver_top_speeds = get_laps_top_speeds(driver_laps, 1)
        if len(driver_top_speeds) > 0:
            if team not in team_top_speeds or driver_top_speeds[0][0] > team_top_speeds[team][0]:
                team_top_speeds[team] = driver_top_speeds[0]
    sorted_top_speeds = sorted(team_top_speeds.items(), key=lambda x: x[1][0], reverse=True)
    return sorted_top_speeds

def lap_has_drs(lap: fastf1.core.Lap) -> bool:
    """
    Check if in a lap the DRS was used
    @param lap: The lap object
    @return: True if DRS was used, False otherwise
    """
    drs_data = list(lap.get_car_data()['DRS'])
    return 10 in drs_data or 12 in drs_data or 14 in drs_data