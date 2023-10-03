from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

BOOKING_STATUS = (
    ('BOOKED_NOT_PAID', 'BOOKED_NOT_PAID'),
    ('BOOKED_PAID', 'BOOKED_PAID')
)

SEAT_LAYOUT = (
    ('1 by 2', '1 by 2'),
    ('2 by 2', '2 by 2'),
    ('2 by 3', '2 by 3'),
    ('3 by 3', '3 by 3'),
)

LUGGAGE_WEIGHT = (
    ('-15KG', '-15KG'),
    ('+15KG', '+15KG'),
    ('+30KG', '+30KG'),
    ('+50KG', '+50KG'),
)

DAYS = (
    ('MONDAY', 'MONDAY'),
    ('TUESDAY', 'TUESDAY'),
    ('WEDNESDAY', 'WEDNESDAY'),
    ('THURSDAY', 'THURSDAY'),
    ('FRIDAY', 'FRIDAY'),
    ('SATURDAY', 'SATURDAY'),
    ('SUNDAY', 'SUNDAY'),
)



# Create your models here.

class BusImages(models.Model):
    bus = models.ForeignKey('BusInfo', on_delete=models.CASCADE)
    bus_image = models.ImageField(upload_to='images/',default='images/None/Noimg.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bus_id

# what's the logic behind the bus total_seats and seat_type ... ok the idea behind if we're have total seats
# lets say "30" and we have seat layout like 2 * 2 we're knowing ok in our drawing in mobile app we're taking 30 * 2
# so we'll have 15 rows, and i think it will be okay to not includes zile seat za mbele sana ambazo zinaharibu
# utaratibu wa 2 * 2 and whatsover. so inabidi umwambie "Adelina" kuwa inabidi asizi-include seat zinazoharibu 
# utaratibu wa 2 by 2 or 1 by 2 kama vipi asizihesabie kabisa, inabid ufanye hivyo... i think itakuwa rahisi sasa hapa 
# kwenye ui inabidi for kila ki-box u-track its id or label... label muhimu i don't know how we handle this logic my god..
# but naweza nikamwambia hizi seat tuzipe number na sio lazima yeye anitumie mimi label but inabidi tukubaliane if we use
# number as our label in our system we should make sure they also use number to label their seats in their buses.
class BusSeatLayout(models.Model):
    bus = models.OneToOneField('BusInfo', on_delete=models.CASCADE, related_name="seatmetadata")
    total_seats = models.IntegerField() # VERY USEFUL, hii ina umuhimu kwenye kujua siti ngapi zimebakia, don't forget to tell "Adelina" to avoid including the seats which are not in 2 by 2 or 1 by 2... just understand the logic here...
    rows = models.CharField(max_length=500) # having rows can help us to position seats even if its 1 by 2, 2 by 3 and so on.
    seat_type = models.CharField(choices=SEAT_LAYOUT, max_length=50)  # here i will have category of 1 * 2, 2 * 2 or 2 * 3 so as to know the seat layout, ni lazima umwambie boss kuwa hizo seat zinaidi ziwe na label kama za mabasi makubwa ili kujua ni siti ipi mtu amelipia
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bus.bus_name
    
class BusAppearance(models.Model):
    bus = models.OneToOneField('BusInfo', on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bus.bus_name
    
# one user can book as many seats as he want... one seat can be found in many bookings, that is why i have used manytomany field
# no need to create model of 'BookedSeats' because i have seat field here, kuhusu info za muda wa bus kuondoka na linapoelekea na 
# bei ya tiketi, zipo kwenye model ya BusInfo
class BusBooking(models.Model):
    bookingId = models.CharField(max_length=255)
    bus = models.ForeignKey('BusInfo', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    seats = models.ManyToManyField('BookedSeat')
    status = models.CharField(max_length=500, choices=BOOKING_STATUS, default='BOOKED_NOT_PAID')
    startdatetime_counting_deadline_for_it_to_be_marked_deleted = models.DateTimeField(null=True, blank=True)  # after user filled all the names and phone number of passenger booked when he clicked next
    # we fill this field but the logic is what if its BOOKED_NOT_PAID and the user is in fill details of 
    # tickets but not clicked "next" button, how you gonna solve this issue ok i think we'll use "updated_at"
    # field and we should set it to "40 minutes" since this fields will not be "populated" with value and 
    # for that purpose we'll "updated_at" field in case this field here is not yet supplied and what if 
    # its deleted but still user in adding ticket details page ok when he place click the submit page we'll 
    # tell him/her that booking has been released due to "too long inactivity" that's how we'll do our stuffs
    # so all the booked seats will be deleted by having this one field of "mark_it_deleted" here
    mark_it_deleted = models.BooleanField(default=False)
    booking_date = models.DateField() # HII NI TAREHE YA SAFARI, naweza nika-book leo lakini safari iwe kesho, so hii field ni muhimu... ko mtu anaweza aka-book asafiri tarehe fulani, Ko kwenye ui inabidi uweke mtu a-pick tarehe ya safari, muda wa safari utakuwa kwenye model ya BusInfo ko ni constant but tarehe ina-depend na mtu anataka safari lini
    # booking_time = models.TimeField() # vilevile kwenye booking time, mtu anaweza aka-book asafiri saa fulani, cha muhimu ni kuwa na info za muda wa bus kuondoka na linapoelekea, but i don't think kama hii ni muhimu sana coz muda wa kuondoka na kuwasili upo kwenye model ya BusInfo, so mtu hawezi akajipangia muda wa kuondoka na kuwasili but ANAWEZA AKAPANGA TAREHE YA SAFARI KUTOKANA NA MUDA ULIOPO KWENYE MODEL YA BUSINFO
    # kuna scenario hapa what if kweli nimebook bus la tarehe 18 but  the logic behind is that tar hiyo 18 kuna 
    # mabasi mengi yanayoenda hiyo route kwa muda tofauti tofauti, inakuwa ngumu ku-detect hii booking ni ya muda gani
    # wa basi kuondoka coz hata nikijaribu kuquery muda wa safari by using bus info trips available kwa siku hiyo
    # trip zipo nyingi za same route.. Ko hapa ni lazima tu-link hii booking na busTrip coz ndo ina-actual data ya safari ya
    # booking muda wa kuondoka na whatsover we can't link with busInfo coz busInfo inatugea information ya bus na bus info to 
    # bustrip ni many trips so we can get many trips if we depend on the "businfo" so we should have the trip linked here in order
    # to point exactly trip which is required for this booking, otherwise itakuwa ni ngumu, so our relation now is 
    # booking should contain one trip and one trip can have many bookings, so we should have foreign key of trip here
    bustrip = models.ForeignKey('BusTrip', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.bus.bus_name
    
class BookedSeat(models.Model):
    passenger_name = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)
    booked_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE) # one passenger can have many booking ok.
    seat_info = models.OneToOneField('BusSeat', on_delete=models.CASCADE)
    
# these are the seats of the bus, usisahau inabidi umwambie madam kuwa siti inabidi ziwe na label
class BusSeat(models.Model):
    bus = models.ForeignKey('BusInfo', on_delete=models.CASCADE)
    seat_number = models.IntegerField() # i think i don't care about seat number
    seat_label = models.CharField(max_length=50) # we care about seat label
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bus.bus_name

class BusInfo(models.Model):
    bus_name = models.CharField(max_length=50)
    bus_type = models.CharField(max_length=50)
    # bus_date = models.DateField()
    plate_number = models.CharField(max_length=50)
    brand_name = models.CharField(max_length=50)   # here i mean manufacturer of that bus
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.bus_name

    # cheat code here is to return all trips of that bus and then take total seats minus booked seats
    @property
    def bookings_metadata(self):
        # print("IM AT YOUR ASS ", datetime.today().date())
        # lets have booking which booking date is at least today
        # and then we'll have booked seats of that bus
        # and then we'll have total seats of that bus
        # print("OUT TARGET BUS ", self.bus_name)
        # __gte means greater than or equal to, __lte means less than or equal to
        bks = BusBooking.objects.all()
        # print("BKS ", bks.first().booking_date)
        # print("FILTERED ", bks.filter(booking_date__gte=datetime.today().date()))
        # print("FILTERED WITH BUS", bks.filter(booking_date__gte=datetime.today().date(), bus=self))
        bookings = BusBooking.objects.filter(booking_date__gte=datetime.today().date(), bus=self)
        # print("BOOKINGS ", bookings)
        # print("SOMETIMES WE'RE GETTING ZERO BOOKING BECAUSE THE CURRENT BOOKING IS OLD ONE JUST LOOK AT ABOVE CONDITION ONLY BOOKING WHICH HAVE BEEN PLACED TODAY OR ON NEXT DAY SO IF WE'RE HAVING THE ONE WHICH IS BEFORE TODAY IT WILL NOT BE RETURNED, IT CAN BE MONDAY BUT DIFFERENT DATE REMEMBER THIS")
        # ok now we have those bookings, i think for each booking i should return metadata or dictionary
        # of it with "total_seats" and "booked_seats" and then i should return the difference of those two
        # make sure u store all booking inside the list
        booking_metadata = []
        for booking in bookings:
            # print('STILL INSIDE')
            # lets have total seats of that bus
            total_seats = BusSeatLayout.objects.get(bus=self).total_seats
            # print("Total seats of this bus is ", total_seats)
            # lets have booked seats of that bus
            # how to get booked seats my guy....
            # lets see the relation between bus and booked seats, count the booked seats from the bus booking, but its not okay
            # since booked seat belong to given booking we should all booking and check the booked_seats then count..
            # bus available seat should not be calculated here coz bus_booking have total number of booking only for 
            # given booking, and remember one bus can have many booking right...
            # lets get all booking of this bus which have same trip source and destination and the same date and departure time
            # then it will be easy to get available seats of that bus, its okay with booking date to use here since the 
            # booking date ndo tarehe ya safari.... the same date, bus and trip booking is resolved in bustrip field
            all_bks = BusBooking.objects.filter(bus=self, booking_date=booking.booking_date, bustrip=booking.bustrip)
            print("ALL BKS ", all_bks)
            # print("The same date, bus and trip booking ", all_bks)        
            # lets now calculate the available seats by substructing total seats with booked seats
            # lets first calculate total seat for each booking in all_bks
            booked = 0
            for bk in all_bks:
                booked += bk.seats.count()
            print("Booked seats of this bus is ", booked)
            # lets have available seats of that bus
            remained = total_seats - booked
            booked_seats = booking.seats.count()
            # print("Booked seats of this bus is ", booked_seats)
            # lets have booking metadata
            # we can have many trip time for one bus for the same day and same route
            # for example "Abood" dar to moro linaenda mara 3 kwa siku...
            print({
                "booking_id": booking.id,
                "total_seats": total_seats,
                "booked_seats": booked_seats,
                "available_seats": remained,
                "trip_date": booking.booking_date,
                "trip_time": booking.bustrip.bus_departure_time,
                "created_at": booking.created_at,
                "updated_at": booking.updated_at
            })
            booking_metadata.append({
                "booking_id": booking.id,
                "total_seats": total_seats,
                "booked_seats": booked_seats,
                "available_seats": remained,
                "trip_date": booking.booking_date,
                "trip_time": booking.bustrip.bus_departure_time,
                "created_at": booking.created_at,
                "updated_at": booking.updated_at
            })
      
        print("BOOKING METADATA ", booking_metadata)
        return booking_metadata


# nashauri kujua if bus lipo siku hiyo tuwe na siku na route linapoenda for example 
# hiace yangu ya "230" linafanya safari jumatatu(dar - iringa), jumanne(iringa - dar) alhamisi(mwanza - musoma)
# kupitia hii logic itakuwa rahisi ku-fetch au ku-detect mabasi yote yanayo-move siku hiyo ya tarehe husika
# so if  user aki-select tarrehe fulani then system ita-detect the "day" of that date na then ita-fetch route, afu itakuwa vizuri tuweke ni muda gani unatumika mpaka basi lifike, i call it "duration"
# aliyo-chagua .... so lets have the model contain of bus tripwhich have day .. also we should have the 
# station (kituo cha watu kukutana) as starting point together with the "station" for end point (sehemu) 
# ambapo basi linaishia safari kwa mfano Magufuli terminal... but kwenye issue ya utalii i don't think if 
# this terminals have point, kwa ishu ya kusafiri kimkoa its okay coz you can say hey im travel to dar and
# i will drop at "Magufuli bus terminal", i think we should leave them here no need to use terminals
# but i think it make sense to have these lets call it kituo cha kuondokea na kituo cha kufikia inamake sense
# ko hapa lets have them i call them "departure_station" and "destination_station"
class BusTrip(models.Model):
    bus = models.ForeignKey(BusInfo, on_delete=models.CASCADE, related_name="bustrip")
    day = models.CharField(choices= DAYS, max_length=500) # monday, tuesday etc
    bus_source = models.CharField(max_length=50)
    departure_station = models.CharField(max_length=500)
    bus_destination = models.CharField(max_length=50)
    destination_station = models.CharField(max_length=500)
    source_arrival_time = models.CharField(max_length=500, help_text='eg. 17:30, put format in 24 hours, muda wa basi kufika kituo cha kuanza safari')
    bus_departure_time = models.CharField(max_length=500, help_text='eg. 18:00, put format in 24 hours, muda wa basi kuondoka kuanza safari')
    bus_fare = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    destination_arrival_time = models.CharField(max_length=500, help_text='eg. 17:30, put format in 24 hours, muda wa basi kufika kituo cha mwisho cha safari')


    def __str__(self):
        return self.bus.bus_name + ', ' + self.bus_source + ' to ' + self.bus_destination


    @property
    def bus_info(self):
        return {
            "id": self.bus.id,
            "bus_name": self.bus.bus_name,
            "bus_type": self.bus.bus_type,
            "plate_number": self.bus.plate_number,
            "brand_name": self.bus.brand_name,
            "created_at": self.bus.created_at,
            "updated_at": self.bus.updated_at,
            'bookings_metadata': self.bus.bookings_metadata
        }
    

# this payment will be handled manually...
class LugaggePrice(models.Model):
    bus = models.ForeignKey(BusInfo, on_delete=models.CASCADE)
    weight = models.CharField(choices=LUGGAGE_WEIGHT, max_length=500)
    price = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bus.bus_name + ' weight: ' + self.weight