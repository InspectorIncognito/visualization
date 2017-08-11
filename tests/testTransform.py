from django.test import TestCase
from django.utils import timezone
from datetime import datetime

from AndroidRequests.models import EventForBusStop, EventForBusv2, Busv2, ReportInfo

import transform as t

from testHelper import TestHelper

import json


# Create your tests here.


class AddTimePeriodsTestCase(TestCase):
    """ evalute transform functions """

    def setUp(self):
        """ """
        self.test = TestHelper(self)

        self.gtfs = self.test.createGTFS('v1.0')

        self.phoneId = '067e6162-3b6f-4ae2-a171-2470b63dff00'

        event1 = self.test.createEvent(
            'evn00201', 'test name1', 'test desc1', 30)
        event2 = self.test.createEvent(
            'evn00202', 'test name2', 'test desc2', 30)
        event3 = self.test.createEvent(
            'evn00203', 'test name3', 'test desc3', 30)
        self.events = [event1, event2, event3]

        # days
        saturday = datetime(2017, 4, 29, 0, 0, 0)
        saturday = timezone.make_aware(saturday)
        sunday = datetime(2017, 4, 30, 0, 0, 0)
        sunday = timezone.make_aware(sunday)
        workingDay = datetime(2017, 4, 28, 0, 0, 0)
        workingDay = timezone.make_aware(workingDay)

        self.days = [saturday, sunday, workingDay]

        self.minutesWindow = 60 * 24 * 7  # a week to past
        self.transformTime = datetime(2017, 5, 1, 15, 0, 0, 0)
        self.transformTime = timezone.make_aware(self.transformTime)

    def test_addTimePeriodsForBusEvent(self):
        """  """
        route = '507'
        license_plate = 'AAAA11'
        bus = self.test.createBus(self.phoneId, license_plate)
        assignment = self.test.createAssignment(bus, route)

        for day, event in zip(self.days, self.events):
            self.test.createReportBusEvent(assignment, event,
                                           self.phoneId, day, 1, 0, day)

        t.add_time_periods(self.transformTime, self.minutesWindow)

        for report in EventForBusv2.objects.all():
            self.assertIsNotNone(report.timePeriod)

    def test_addTimePeriodsForStopEvent(self):
        """  """
        code = 'PA459'
        self.test.createStop(code, 'name test', self.gtfs)

        for day, event in zip(self.days, self.events):
            self.test.createReportStopEvent(code, event,
                                            self.phoneId, day, 1, 0, day)

        t.add_time_periods(self.transformTime, self.minutesWindow)

        for report in EventForBusStop.objects.all():
            self.assertIsNotNone(report.timePeriod)


class ValidatePlateTestCase(TestCase):
    """ evaluate transform functions """

    def setUp(self):
        """ """
        self.test = TestHelper(self)

        self.gtfs = self.test.createGTFS('v1.0')

        self.phoneId = '067e6162-3b6f-4ae2-a171-2470b63dff00'

    def test_checkPlateWithGoodFormat(self):
        """  """
        licencePlate = 'AAAA11'
        self.test.createBus(self.phoneId, licencePlate)

        t.validate_plates()

        formattedLicencePlate = 'AA AA 11'
        newLicencePlate = Busv2.objects.first().registrationPlate
        self.assertEqual(newLicencePlate, formattedLicencePlate)

    def test_checkPlateWithDummyPlate(self):
        """  """
        licencePlate = 'dummylPt'
        self.test.createBus(self.phoneId, licencePlate)

        t.validate_plates()

        formattedLicencePlate = u'No Info.'
        newLicencePlate = Busv2.objects.first().registrationPlate
        self.assertEqual(newLicencePlate, formattedLicencePlate)


class AddHalfHourPeriodsTestCase(TestCase):
    """ evaluate add half hour to event """

    def setUp(self):
        """  """
        self.test = TestHelper(self)
        self.gtfs = self.test.createGTFS('v1.0')

        # events
        event1 = self.test.createEvent('evn00201', 'test name1', 'test desc1', 30)
        event2 = self.test.createEvent('evn00202', 'test name2', 'test desc2', 30)
        event3 = self.test.createEvent('evn00203', 'test name3', 'test desc3', 30)
        self.events = [event1, event2, event3]

        # days
        saturday = timezone.make_aware(datetime(2017, 4, 29, 1, 0, 0))
        sunday = timezone.make_aware(datetime(2017, 4, 30, 2, 0, 0))
        workingDay = timezone.make_aware(datetime(2017, 4, 28, 3, 0, 0))
        self.days = [saturday, sunday, workingDay]

        self.phoneId = '067e6162-3b6f-4ae2-a171-2470b63dff00'

        self.minutesWindow = 60 * 24 * 7  # a week to past
        self.transformTime = datetime(2017, 5, 1, 15, 0, 0, 0)
        self.transformTime = timezone.make_aware(self.transformTime)

    def test_halfHourForBusEvent(self):
        """ """
        route = '507'
        license_plate = 'AAAA11'
        bus = self.test.createBus(self.phoneId, license_plate)
        assignment = self.test.createAssignment(bus, route)

        for day, event in zip(self.days, self.events):
            self.test.createReportBusEvent(assignment, event, self.phoneId, day, 1, 0, day)

        t.add_half_hour_periods(self.transformTime, self.minutesWindow)

        events = EventForBusv2.objects.all()
        answers = ["01:00 - 01:29", "02:00 - 02:29", "03:00 - 03:29"]
        for event, answer in zip(events, answers):
            self.assertEqual(event.halfHourPeriod.name, answer)

    def test_halfHourForStopEvent(self):
        """ check if half hour is updated for stop events """
        code = 'PA459'
        self.test.createStop(code, 'name test', self.gtfs)

        for day, event in zip(self.days, self.events):
            self.test.createReportStopEvent(code, event, self.phoneId, day, 1, 0, day)

        t.add_half_hour_periods(self.transformTime, self.minutesWindow)

        events = EventForBusStop.objects.all()
        answers = ["01:00 - 01:29", "02:00 - 02:29", "03:00 - 03:29"]
        for event, answer in zip(events, answers):
            print(event.halfHourPeriod.name)
            self.assertEqual(event.halfHourPeriod.name, answer)


class AddReportInfoTestCase(TestCase):
    """ evaluate process free reports """

    def setUp(self):
        """  """
        self.test = TestHelper(self)

        # days
        saturday = timezone.make_aware(datetime(2017, 4, 29, 1, 0, 0))
        sunday = timezone.make_aware(datetime(2017, 4, 30, 2, 0, 0))
        workingDay = timezone.make_aware(datetime(2017, 4, 28, 3, 0, 0))
        self.days = [saturday, sunday, workingDay]

        self.phoneId = '067e6162-3b6f-4ae2-a171-2470b63dff00'

        self.minutesWindow = 60 * 24 * 7  # a week to past
        self.transformTime = datetime(2017, 5, 1, 15, 0, 0, 0)
        self.transformTime = timezone.make_aware(self.transformTime)

        # for stop event
        self.message = "no hay paradero"
        self.imageName = "no image"

    def test_reportWithBadReportInfo(self):
        """ user send report with bad report info """

        reportInfo = "{this is a bad json format ]"

        report = self.test.createReport(message=self.message, timestamp=self.days[0], phoneId=self.phoneId,
                                        imageName=self.imageName, reportInfo=reportInfo)

        t.add_report_info(self.transformTime, self.minutesWindow)

        report.refresh_from_db()
        self.assertTrue(report.transformed)
        self.assertEqual(ReportInfo.objects.count(), 0)

    def test_reportWithLocationUser(self):
        """ user send report with location user field on reportInfo """

        additionalInfoTemplate = {
            "locationUser": {
                "longitude": "\/-70.6264852",
                "latitude": "\/-33.4929384"
            },
            "bus_stop": {
                "id": "PH217",
                "longitude": -70.61356902,
                "latitude": -33.50856476
            }
        }
        reportInfo1 = json.dumps(additionalInfoTemplate)

        additionalInfoTemplate["locationUser"]["latitude"] = "test"
        additionalInfoTemplate["locationUser"]["longitude"] = "test"

        reportInfo2 = json.dumps(additionalInfoTemplate)

        reportList = [reportInfo1, reportInfo2]
        longitudeList = [-70.6264852, None]
        latitudeList = [-33.4929384, None]

        for additionalInfo, latitude, longitude in zip(reportList, latitudeList, longitudeList):
            reportObj = self.test.createReport(message=self.message, timestamp=self.days[0], phoneId=self.phoneId,
                                               imageName=self.imageName, reportInfo=additionalInfo)

            t.add_report_info(self.transformTime, self.minutesWindow)

            reportObj.refresh_from_db()
            self.assertTrue(reportObj.transformed)

            reportInfo = ReportInfo.objects.first()
            self.assertEqual(reportInfo.userLatitude, latitude)
            self.assertEqual(reportInfo.userLongitude, longitude)

            reportObj.delete()
            ReportInfo.objects.all().delete()

    def test_reportOfBus(self):
        """ user send report of  field on reportInfo """

        additionalInfoTemplate = {
            "bus": {
                "service": "301",
                "licensePlate": "BJFT69",
                "machineId": "90939da7-034b-404c-80e5-959457b79bc9",
                "latitude": -33.4588248,
                "longitude": -70.6492881
            }
        }
        additionalInfo = json.dumps(additionalInfoTemplate)

        self.test.createReport(message=self.message, timestamp=self.days[0], phoneId=self.phoneId,
                               imageName=self.imageName, reportInfo=additionalInfo)

        t.add_report_info(self.transformTime, self.minutesWindow)

        reportInfo = ReportInfo.objects.first()
        self.assertEqual(reportInfo.registrationPlate, "BJ FT 69")
        self.assertEqual(str(reportInfo.busUUID), additionalInfoTemplate["bus"]["machineId"])
        self.assertEqual(reportInfo.latitude, additionalInfoTemplate["bus"]["latitude"])
        self.assertEqual(reportInfo.longitude, additionalInfoTemplate["bus"]["longitude"])
        self.assertEqual(reportInfo.service, additionalInfoTemplate["bus"]["service"])
        self.assertIsNotNone(reportInfo.report)

    def test_reportOfBusWithoutMachineId(self):
        """ report without machineId """
        licensePlate = "BJFT69"
        formattedLicensePlate = "BJ FT 69"
        self.test.createBus(self.phoneId, formattedLicensePlate)
        additionalInfoTemplate = {
            "bus": {
                "service": "301",
                "licensePlate": licensePlate,
                "latitude": -33.4588248,
                "longitude": -70.6492881
            }
        }
        additionalInfo = json.dumps(additionalInfoTemplate)

        self.test.createReport(message=self.message, timestamp=self.days[0], phoneId=self.phoneId,
                               imageName=self.imageName, reportInfo=additionalInfo)

        t.add_report_info(self.transformTime, self.minutesWindow)

        reportInfo = ReportInfo.objects.first()
        self.assertEqual(reportInfo.registrationPlate, formattedLicensePlate)
        self.assertEqual(str(reportInfo.busUUID), self.phoneId)
        self.assertEqual(reportInfo.latitude, additionalInfoTemplate["bus"]["latitude"])
        self.assertEqual(reportInfo.longitude, additionalInfoTemplate["bus"]["longitude"])
        self.assertEqual(reportInfo.service, additionalInfoTemplate["bus"]["service"])
        self.assertIsNotNone(reportInfo.report)

    def test_reportOfBusWithDummyLicensePlate(self):
        """ report without dummy license plate """
        licensePlate = "DUMMYLPT"
        formattedLicensePlate = "No Info."
        self.test.createBus(self.phoneId, formattedLicensePlate)
        additionalInfoTemplate = {
            "bus": {
                "service": "this is a wrong service name",
                "licensePlate": licensePlate,
                "latitude": -33.4588248,
                "longitude": -70.6492881
            }
        }
        additionalInfo = json.dumps(additionalInfoTemplate)

        self.test.createReport(message=self.message, timestamp=self.days[0], phoneId=self.phoneId,
                               imageName=self.imageName, reportInfo=additionalInfo)

        t.add_report_info(self.transformTime, self.minutesWindow)

        reportInfo = ReportInfo.objects.first()
        self.assertEqual(reportInfo.registrationPlate, formattedLicensePlate)
        self.assertEqual(reportInfo.busUUID, None)
        self.assertEqual(reportInfo.latitude, additionalInfoTemplate["bus"]["latitude"])
        self.assertEqual(reportInfo.longitude, additionalInfoTemplate["bus"]["longitude"])
        self.assertEqual(reportInfo.service, "JAVA")
        self.assertIsNotNone(reportInfo.report)

    def test_reportOfStopWithNewStopId(self):
        """ report with new stop id in json """
        stopCode = "PH217"
        additionalInfoTemplate = {
            "busStop": {
                "id": stopCode,
                "longitude": -70.61356902,
                "latitude": -33.50856476
            }
        }
        additionalInfo = json.dumps(additionalInfoTemplate)

        self.test.createReport(message=self.message, timestamp=self.days[0], phoneId=self.phoneId,
                               imageName=self.imageName, reportInfo=additionalInfo)

        t.add_report_info(self.transformTime, self.minutesWindow)

        reportInfo = ReportInfo.objects.first()
        self.assertEqual(reportInfo.stopCode, stopCode)
        self.assertEqual(reportInfo.latitude, additionalInfoTemplate["busStop"]["latitude"])
        self.assertEqual(reportInfo.longitude, additionalInfoTemplate["busStop"]["longitude"])
        self.assertIsNotNone(reportInfo.report)


class AddCountyTestCase(TestCase):
    """ add county to event for bus and stop events """

    def setUp(self):
        """  """
        self.test = TestHelper(self)
        self.gtfs = self.test.createGTFS('v1.0')

        # events
        event1 = self.test.createEvent('evn00201', 'test name1', 'test desc1', 30)
        event2 = self.test.createEvent('evn00202', 'test name2', 'test desc2', 30)
        event3 = self.test.createEvent('evn00203', 'test name3', 'test desc3', 30)
        self.events = [event1, event2, event3]

        # days
        saturday = timezone.make_aware(datetime(2017, 4, 29, 1, 0, 0))
        sunday = timezone.make_aware(datetime(2017, 4, 30, 2, 0, 0))
        workingDay = timezone.make_aware(datetime(2017, 4, 28, 3, 0, 0))
        self.days = [saturday, sunday, workingDay]

        self.phoneId = '067e6162-3b6f-4ae2-a171-2470b63dff00'

        self.minutesWindow = 60 * 24 * 7  # a week to past
        self.transformTime = datetime(2017, 5, 1, 15, 0, 0, 0)
        self.transformTime = timezone.make_aware(self.transformTime)

        # for stop event
        self.message = "no hay paradero"
        self.imageName = "no image"

    def test_addCountyForBusEvent(self):
        """  """
        route = '507'
        license_plate = 'AAAA11'
        bus = self.test.createBus(self.phoneId, license_plate)
        assignment = self.test.createAssignment(bus, route)

        for day, event in zip(self.days, self.events):
            self.test.createReportBusEvent(assignment, event,
                                           self.phoneId, day, 1, 0, day)

        t.add_county(self.transformTime, self.minutesWindow)

        for report in EventForBusv2.objects.all():
            self.assertIsNotNone(report.zonification)


    def test_addCountyForStopEvent(self):
        """  """
        code = 'PA459'
        self.test.createStop(code, 'name test', self.gtfs)

        for day, event in zip(self.days, self.events):
            self.test.createReportStopEvent(code, event,
                                            self.phoneId, day, 1, 0, day)

        t.add_county(self.transformTime, self.minutesWindow)

        for report in EventForBusStop.objects.all():
            self.assertIsNotNone(report.zonification)

    def test_addCountyForReportRelatedWithStop(self):
        """  """
        stopCode = "PH217"
        # beauchef 851 location
        longitude = -70.664253
        latitude = -33.457372

        self.test.createReportInfoForStop(stopCode=stopCode, longitude=longitude, latitude=latitude, zoneObj=None,
                                         userLongitude=longitude, userLatitude=latitude)

        t.add_county(self.transformTime, self.minutesWindow)

        for report in ReportInfo.objects.all():
            self.assertIsNotNone(report.zonification)
            self.assertTrue(report.transformed)

    def test_addCountyForReportRelatedWithBus(self):
        """  """
        route = "506"
        licensePlate = "AAAAAA"
        # beauchef 851 location
        longitude = -70.664253
        latitude = -33.457372

        self.test.createReportInfoForBus(route=route, busUUID=self.phoneId, licensePlate=licensePlate, direction="I",
                                         longitude=longitude, latitude=latitude,
                                          userLongitude=longitude, userLatitude=latitude, zoneObj=None)

        t.add_county(self.transformTime, self.minutesWindow)

        for report in ReportInfo.objects.all():
            self.assertIsNotNone(report.zonification)
            self.assertTrue(report.transformed)
