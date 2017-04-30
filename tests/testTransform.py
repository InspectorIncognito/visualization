from django.test import TestCase
from django.utils import timezone
from datetime import datetime, date

from AndroidRequests.models import EventForBusStop, EventForBusv2

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


