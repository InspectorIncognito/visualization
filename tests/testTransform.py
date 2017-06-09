from django.test import TestCase
from django.utils import timezone
from datetime import datetime, date

from AndroidRequests.models import EventForBusStop, EventForBusv2, Busv2, ReportInfo

import transform as t

from testHelper import TestHelper

# Create your tests here.

class AddTimePeriodsTestCase(TestCase):
    """ evalute transform functions """

    def setUp(self):
        ''' '''
        self.test = TestHelper(self)

        self.gtfs = self.test.createGTFS('v1.0');

        self.phoneId = '067e6162-3b6f-4ae2-a171-2470b63dff00'

        event1 = self.test.createEvent(
            'evn00201', 'test name1', 'test desc1', 30)
        event2 = self.test.createEvent(
            'evn00202', 'test name2', 'test desc2', 30)
        event3 = self.test.createEvent(
            'evn00203', 'test name3', 'test desc3', 30)
        self.events = [event1, event2, event3]

        # days
        saturday = datetime(2017, 04, 29, 0, 0, 0)
        saturday = timezone.make_aware(saturday)
        sunday = datetime(2017, 04, 30, 0, 0, 0)
        sunday = timezone.make_aware(sunday)
        workingDay = datetime(2017, 04, 28, 0, 0, 0)
        workingDay = timezone.make_aware(workingDay)

        self.days = [saturday, sunday, workingDay]

        self.minutesWindow = 60 * 24 * 7 # a week to past
        self.transformTime = datetime(2017, 05, 1, 15, 0, 0, 0)
        self.transformTime = timezone.make_aware(self.transformTime)

    def test_addTimePeriodsForBusEvent(self):
        '''  '''
        service = '507'
        licencePlate = 'AAAA11'
        bus = self.test.createBus(self.phoneId, licencePlate)
        assignment = self.test.createAssignment(bus, service)

        for day, event in zip(self.days, self.events):
            self.test.createReportBusEvent(assignment, event, 
                self.phoneId, day, 1, 0, day)

        t.add_time_periods(self.transformTime, self.minutesWindow)

        for report in EventForBusv2.objects.all():
            self.assertIsNotNone(report.timePeriod)

    def test_addTimePeriodsForStopEvent(self):
        '''  '''
        code = 'PA459'
        self.test.createStop(code, 'name test', self.gtfs)

        for day, event in zip(self.days, self.events):
            self.test.createReportStopEvent(code, event, 
                self.phoneId, day, 1, 0, day)

        t.add_time_periods(self.transformTime, self.minutesWindow)

        for report in EventForBusStop.objects.all():
            self.assertIsNotNone(report.timePeriod)

class ValidatePlateTestCase(TestCase):
    """ evalute transform functions """

    def setUp(self):
        ''' '''
        self.test = TestHelper(self)

        self.phoneId = '067e6162-3b6f-4ae2-a171-2470b63dff00'

    def test_checkPlateWithGoodFormat(self):
        '''  '''
        licencePlate = 'AAAA11'
        bus = self.test.createBus(self.phoneId, licencePlate)

        t.validate_plates()

        formattedLicencePlate = 'AA AA 11'
        newLicencePlate = Busv2.objects.first().registrationPlate
        self.assertEqual(newLicencePlate, formattedLicencePlate)

    def test_checkPlateWithDummyPlate(self):
        '''  '''
        licencePlate = 'dummylPt'
        bus = self.test.createBus(self.phoneId, licencePlate)

        t.validate_plates()

        formattedLicencePlate = u'No Info.'
        newLicencePlate = Busv2.objects.first().registrationPlate
        self.assertEqual(newLicencePlate, formattedLicencePlate)


class AddHalfHourPeriodsTestCase(TestCase):
    """ evaluate transform functions """

    def setUp(self):
        ''' '''
        self.test = TestHelper(self)

        self.gtfs = self.test.createGTFS('v1.0');

        self.phoneId = '067e6162-3b6f-4ae2-a171-2470b63dff00'

        event1 = self.test.createEvent(
            'evn00201', 'test name1', 'test desc1', 30)
        event2 = self.test.createEvent(
            'evn00202', 'test name2', 'test desc2', 30)
        event3 = self.test.createEvent(
            'evn00203', 'test name3', 'test desc3', 30)
        self.events = [event1, event2, event3]

        # days
        saturday = datetime(2017, 04, 29, 0, 0, 0)
        saturday = timezone.make_aware(saturday)
        sunday = datetime(2017, 04, 30, 0, 0, 0)
        sunday = timezone.make_aware(sunday)
        workingDay = datetime(2017, 04, 28, 0, 0, 0)
        workingDay = timezone.make_aware(workingDay)

        self.days = [saturday, sunday, workingDay]

        self.minutesWindow = 60 * 24 * 7 # a week to past
        self.transformTime = datetime(2017, 05, 1, 15, 0, 0, 0)
        self.transformTime = timezone.make_aware(self.transformTime)

    def test_addHalfHourPeriodsForBusEvent(self):
        '''  '''
        service = '507'
        licencePlate = 'AAAA11'
        bus = self.test.createBus(self.phoneId, licencePlate)
        assignment = self.test.createAssignment(bus, service)

        for day, event in zip(self.days, self.events):
            self.test.createReportBusEvent(assignment, event, 
                self.phoneId, day, 1, 0, day)

        t.add_half_hour_periods(self.transformTime, self.minutesWindow)

        for report in EventForBusv2.objects.all():
            self.assertIsNotNone(report.halfHourPeriod)

    def test_addHalfHourPeriodsForStopEvent(self):
        '''  '''
        code = 'PA459'
        self.test.createStop(code, 'name test', self.gtfs)

        for day, event in zip(self.days, self.events):
            self.test.createReportStopEvent(code, event, 
                self.phoneId, day, 1, 0, day)

        t.add_half_hour_periods(self.transformTime, self.minutesWindow)

        for report in EventForBusStop.objects.all():
            self.assertIsNotNone(report.halfHourPeriod)

class AddReportInfoTestCase(TestCase):
    """ evaluate transform functions """

    def setUp(self):
        ''' '''
        self.test = TestHelper(self)

        self.gtfs = self.test.createGTFS('v1.0');

        self.phoneId = '067e6162-3b6f-4ae2-a171-2470b63dff00'

        self.report = self.test.createReport(self.phoneId, '', '{}', 
            timezone.now(), '', False)

        self.minutesWindow = 10

    def test_addBadReportInfo(self):
        '''  '''
        reportInfo = '{]'
        self.report.reportInfo = reportInfo
        self.report.save()

        t.add_report_info(timezone.now(), self.minutesWindow)

        self.report.refresh_from_db()
        self.assertFalse(self.report.transformed)
        self.assertEqual(ReportInfo.objects.count(), 0)

    def test_evaluateWrongLatLon(self):
        '''  '''
        reportInfoWithBadLatitude = """
        {
          "locationUser": {
            "latitude": "problem",
            "longitude": -70.32
          }
        }
        """
        reportInfoWithBadLongitude = """
        {
          "locationUser": {
            "latitude": -30.01,
            "longitude": "problem"
          }
        }
        """
        reports = [reportInfoWithBadLatitude, reportInfoWithBadLongitude]

        for report in reports:
            self.report.reportInfo = report
            self.report.save()

            t.add_report_info(timezone.now(), self.minutesWindow)

            self.report.refresh_from_db()
            self.assertTrue(self.report.transformed)
            self.assertEqual(ReportInfo.objects.count(), 0)

            self.report.transformed=False
            self.report.save()

    def test_processBusEvent(self):
        '''  '''
        reportInfoOk = """
        {
          "locationUser": {
            "latitude": "problem",
            "longitude": -70.32
          },
          "bus": {
            "licensePlate": "AAAA11",
            "machineId": "123456",
            "service": "506I",
            "latitude": -30.23,
            "longitude": -70.32
          } 
        }
        """
        self.report.reportInfo = reportInfo
        self.report.save()

        t.add_report_info(timezone.now(), self.minutesWindow)

        #self.assertTrue(self.report.transformed)
        #self.assertEqual(ReportInfo.objects.count(), 0)


