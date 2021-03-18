# HW5 requirements
#   At least one function
#   At least one if statement (can be if/else or if/elif/else)
#   At least one list OR one dictionary
#   Some level of communication or interaction with a user (printed status updates on code as it runs,
#     requests for inputs, or reading in data from the user’s (your) computer)
#   At least one library

# Note: You will need a Garmin Connect account in order to use this API:
#   https://connect.garmin.com/signin
#
#   Once you have an account, configure your credentials using environment variables:
#   GARMIN_EMAIL
#   GARMIN_PASSWORD

import datetime
import logging
import os
import json
from pprint import pprint
from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError
)

# The intent is to implement a full data pump from Garmin's API to my own data store. In conjunction
# with a separate work-in-progress frontend, this data would then be displayed in graphical format
# e.g. showing cumulative cycling distance for the year.
#
# For now, we just implement a simple method to demonstrate functionality and to meet the homework requirements :)
class GarimDataPump:

    def __init__(self):
        # TODO: hardcode for now
        self.DATE_SINCE = '2021-02-01'

        log_level = os.getenv('LOG_LEVEL')
        if log_level not in ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'):
            print("Invalid log level provided")
            log_level = 'INFO'

        logging.basicConfig(level=getattr(logging, log_level))
        self.logger = logging.getLogger(__name__)

        email = os.getenv('GARMIN_EMAIL')
        password = os.getenv('GARMIN_PASSWORD')

        try:
            self.client = Garmin(email, password)
            self.client.login()
        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError
        ) as err:
            self.logger.error("Error occured during Garmin Connect Client init/login: %s" % err)
            quit()
        except Exception:
            self.logger.error("Unknown error occurred during Garmin Connect Client init")
            quit()

    def get_activities_by_type(self, activity_type, num_weeks):
        valid_activities = ('cycling', 'indoor_cycling', 'running', 'swimming')

        # We can't get activities for all-time so we're just going to get the last N weeks
        end = datetime.date.today()
        start = end - datetime.timedelta(weeks=num_weeks)
        self.logger.info(f'Getting {activity_type} data for the last {num_weeks} weeks...')

        if activity_type not in valid_activities:
            self.logger.warn(f'Invalid activity type specified: {activity_type}')
            return

        try:
            return self.client.get_activities_by_date(start, end, activity_type)
        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError
        ) as err:
            self.logger.error(f"Error occurred during Garmin Connect Client get stats: {err}")
        except Exception as err:  # pylint: disable=broad-except
            self.logger.error(f"Unknown error occurred during Garmin Connect Client get stats: {err}")

    def upload_data(self):
        # Stub for now
        return

if __name__ == "__main__":

    garmin = GarimDataPump()
    activities = garmin.get_activities_by_type('cycling', 12)

    cumulative_meters = 0
    cumulative_meters_indoor = 0
    cumulative_meters_outdoor = 0
    cumulative_vertical = 0
    for activity in activities:
        cumulative_meters += activity['distance']
        if activity['elevationGain'] is not None:
            cumulative_vertical += activity['elevationGain']

        if activity['activityType']['typeKey'] == 'indoor_cycling':
            cumulative_meters_indoor += activity['distance']

        if activity['activityType']['typeKey'] == 'cycling':
            cumulative_meters_outdoor += activity['distance']

    total_miles = cumulative_meters * 0.00062137
    total_outdoor_miles = cumulative_meters_outdoor * 0.00062137
    total_indoor_miles = cumulative_meters_indoor * 0.00062137
    total_vertical_feet = cumulative_vertical * 3.280839895
    print(f'Total mileage YTD: {round(total_miles)}mi')
    print(f'Total outdoor mileage YTD: {round(total_outdoor_miles)}mi')
    print(f'Total indoor mileage YTD: {round(total_indoor_miles)}mi')
    print(f'Total vertical feet YTD: {round(total_vertical_feet)}ft')
