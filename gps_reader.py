import gps
import time

session = gps.gps(mode=gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

try:
    while True:
        report = session.next()

        #print("Raw GPS Report:")
        #print(report)

        if report['class'] == 'TPV':

            latitude = report.lat if hasattr(report, 'lat') else 'No Data'
            longitude = report.lon if hasattr(report, 'lon') else 'No Data'
            elevation = report.altMSL if hasattr(report, 'altMSL') else 'No Data'

            print(f"Latitude: {latitude}")
            print(f"Longitude: {longitude}")
            print(f"Elevation: {elevation} meters")

        elif report['class'] == 'GSV':
            satellites = report.satellites if hasattr(report, 'satellites') else 'No Data'

            print(f"Satellites: {satellites}")
        
        print("===================================")
        time.sleep(1)

except KeyboardInterrupt:
    print("Program interrupted")
except Excption as e:
    print(f"Error: {e}")