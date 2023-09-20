from django.db import models
from django.contrib.auth import get_user_model

BOOKING_STATUS = (
    ('BOOKED_NOT_PAID', 'BOOKED_NOT_PAID'),
    ('BOOKED_PAID', 'BOOKED_PAID')
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
    bus = models.OneToOneField('BusInfo', on_delete=models.CASCADE)
    total_seats = models.IntegerField() # hii sio lazima sana we just look on the row to have total seats 
    rows = models.CharField(max_length=500) # having rows can help us to position seats even if its 1 by 2, 2 by 3 and so on.
    seat_type = models.CharField(max_length=50)  # here i will have category of 1 * 2, 2 * 2 or 2 * 3 so as to know the seat layout, ni lazima umwambie boss kuwa hizo seat zinaidi ziwe na label kama za mabasi makubwa ili kujua ni siti ipi mtu amelipia
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bus_id
    
class BusAppearance(models.Model):
    bus = models.OneToOneField('BusInfo', on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bus_id
    
# one user can book as many seats as he want... one seat can be found in many bookings, that is why i have used manytomany field
# no need to create model of 'BookedSeats' because i have seat field here, kuhusu info za muda wa bus kuondoka na linapoelekea na 
# bei ya tiketi, zipo kwenye model ya BusInfo
class BusBooking(models.Model):
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
    booking_date = models.DateField() # naweza nika-book leo lakini safari iwe kesho, so hii field ni muhimu... ko mtu anaweza aka-book asafiri tarehe fulani, Ko kwenye ui inabidi uweke mtu a-pick tarehe ya safari, muda wa safari utakuwa kwenye model ya BusInfo ko ni constant but tarehe ina-depend na mtu anataka safari lini
    # booking_time = models.TimeField() # vilevile kwenye booking time, mtu anaweza aka-book asafiri saa fulani, cha muhimu ni kuwa na info za muda wa bus kuondoka na linapoelekea, but i don't think kama hii ni muhimu sana coz muda wa kuondoka na kuwasili upo kwenye model ya BusInfo, so mtu hawezi akajipangia muda wa kuondoka na kuwasili but ANAWEZA AKAPANGA TAREHE YA SAFARI KUTOKANA NA MUDA ULIOPO KWENYE MODEL YA BUSINFO
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.bus_id
    
class BookedSeat(models.Model):
    passenger_name = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)
    booked_by = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    seat_info = models.OneToOneField('BusSeat', on_delete=models.CASCADE)
    
# these are the seats of the bus, usisahau inabidi umwambie madam kuwa siti inabidi ziwe na label
class BusSeat(models.Model):
    bus = models.ForeignKey('BusInfo', on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    seat_label = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bus_id

class BusInfo(models.Model):
    bus_name = models.CharField(max_length=50)
    bus_type = models.CharField(max_length=50)
    # bus_date = models.DateField()
    plate_number = models.CharField(max_length=50)
    brand_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.bus_name
    

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
    bus = models.OneToOneField(BusInfo, on_delete=models.CASCADE)
    day = models.CharField(max_length=500) # monday, tuesday etc
    bus_source = models.CharField(max_length=50)
    departure_station = models.CharField(max_length=500)
    bus_destination = models.CharField(max_length=50)
    destination_station = models.CharField(max_length=500)
    bus_departure_time = models.TimeField()
    bus_arrival_time = models.TimeField()
    bus_fare = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    duration = models.CharField(max_length=500)



# this payment will be handled manually...
class LugaggePrice(models.Model):
    bus = models.OneToOneField(BusInfo, on_delete=models.CASCADE)
    weight = models.CharField(max_length=500)
    price = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

