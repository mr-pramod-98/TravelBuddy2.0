from django.shortcuts import render, HttpResponse
import mysql.connector
from .models import Packages, DestinationDetails, PackagesGuide, PackagesHotel, VehicleAndGeneralDetails, HotelImages
from datetime import datetime
from email.message import EmailMessage
import smtplib


# THIS CLASS IS USED TO SEND CONFIRMATION MAIL
class SendConfirmationMail:

    def confirmation_mail(self, username, email, booking_id, number_of_seats, amount):

        msg = EmailMessage()

        # SUBJECT OF THE MAIL
        msg['Subject'] = "TravelBuddy Booking Confirmation mail"

        # FROM ADDRESS
        msg['From'] = 'cookingguide.dsatm@gmail.com'

        # TO ADDRESS
        msg['To'] = email

        # BODY OF THE MAIL
        mail_body = "USERNAME: " + username + "\n" \
                    "BOOKING-ID: " + booking_id + "\n" \
                    "SEATS BOOKED: " + number_of_seats + "\n" \
                    "AMOUNT: " + amount
        msg.set_content(mail_body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('cookingguide.dsatm@gmail.com', 'CookingGuideProject')
            smtp.send_message(msg)


# THIS CLASS IS USED TO FIND VACANCIES IN PACKAGES
class FindVacancies:

    def __init__(self):
        self.my_db = mysql.connector.Connect(host='localhost', user='root', passwd='password', database='TravelBuddy')
        self.my_cur = self.my_db.cursor()

    # "calculate" METHOD CALCULATES THE VACANCY A PARTICULAR PACKAGE
    def calculate(self, destination_id):

        # QUERY TO FIND THE TOTAL NUMBER OF SEATS BOOKED FOR A PACKAGE --> STARTS
        query = "select sum(number_of_seats) " \
                "from travello_packagesbookings " \
                "where location_id_id = %s"

        values = (destination_id,)

        self.my_cur.execute(query, values)

        seats_booked = self.my_cur.fetchall()[0][0]
        # QUERY TO FIND THE TOTAL NUMBER OF SEATS BOOKED FOR A PACKAGE --> ENDS

        # QUERY TO FIND THE TOTAL NUMBER OF SEATS IN A PACKAGE --> STARTS
        query = "select total_number_seats " \
                "from travello_packages " \
                "where location_id = %s"

        self.my_cur.execute(query, (destination_id,))

        total_number_seats = self.my_cur.fetchall()[0][0]
        # QUERY TO FIND THE TOTAL NUMBER OF SEATS IN A PACKAGE --> ENDS

        # IF NO SEATS ARE BOOKED THEN ADD "total_number_seats" AS THE VACANCY TO "vacancies" LIST
        # ELSE CALCULATE VACANCY AND THE ADD IT TO "vacancies" LIST
        if seats_booked is None:

            # SETTING "vacancies" AS "total_number_seats"
            vacancies = total_number_seats
        else:

            # CALCULATING VACANCIES
            vacancies = total_number_seats - seats_booked

        # RETURNING VACANCIES
        return vacancies

    # "calculate_all" METHOD CALCULATES THE VACANCIES OF ALL AVAILABLE PACKAGES
    def calculate_for_all(self, destinations):

        vacancies = []

        for dest in destinations:

            # QUERY TO FIND THE TOTAL NUMBER OF SEATS IN A PACKAGE --> STARTS
            query = "select total_number_seats " \
                    "from travello_packages " \
                    "where location_id = %s"

            self.my_cur.execute(query, (dest.location_id,))

            total_number_seats = self.my_cur.fetchall()[0][0]
            # QUERY TO FIND THE TOTAL NUMBER OF SEATS IN A PACKAGE --> ENDS

            # QUERY TO FIND THE TOTAL NUMBER OF SEATS BOOKED FOR A PACKAGE --> STARTS
            query = "select sum(number_of_seats) " \
                    "from travello_packagesbookings " \
                    "where location_id_id = %s"

            values = (dest.location_id,)

            self.my_cur.execute(query, values)

            seats_booked = self.my_cur.fetchall()[0][0]
            # QUERY TO FIND THE TOTAL NUMBER OF SEATS BOOKED FOR A PACKAGE --> ENDS

            # IF NO SEATS ARE BOOKED THEN ADD "total_number_seats" AS THE VACANCY TO "vacancies" LIST
            # ELSE CALCULATE VACANCY AND THE ADD IT TO "vacancies" LIST
            if seats_booked is None:

                # SETTING "vacancies" AS "total_number_seats"
                total_seats = {
                    'total_number_seats': total_number_seats
                }

                vacancies.append(total_seats)

            else:

                # CALCULATING VACANCIES
                vacancy = total_number_seats - seats_booked

                available_seats = {
                    'total_number_seats': vacancy
                }

                vacancies.append(available_seats)

        # RETURNING VACANCIES
        # HERE "vacancies" IS LIST OF DICTIONARIES
        return vacancies


# Create your views here.
# "travello" METHOD IS CALLED WHET THE USER LOGIN'S SUCCESSFULLY AND EVERY-TIME USER REQUESTS FOR "travello" PAGE
def travello(request, username):

    # FETCHING ALL RECORDS( i.e, DESTINATIONS) FOR "Packages" TABLE
    dests = Packages.objects.all()

    # CALCULATING THE VACANCIES IN EVERY PACKAGE
    finder = FindVacancies()
    vacancies = finder.calculate_for_all(dests)

    # CONNECTING TO DATABASE TO FETCH THE COUNT OF AVAILABLE OFFERS ON PACKAGES
    my_db = mysql.connector.connect(host='localhost', user='root', passwd='password', database='TravelBuddy')
    my_cur = my_db.cursor()

    # QUERY TO FETCH COUNT OF AVAILABLE OFFERS ON PACKAGES
    query = "select count(offer) " \
            "from travello_packages " \
            "where offer = %s"

    my_cur.execute(query, (1,))

    # FETCHING THE VALUE FROM LIST OF TUPLES
    count_of_offers = my_cur.fetchall()[0][0]

    # RETURNING THE REQUESTED PAGE( i.e, travello.html)
    # "dests" AND "vacancies" ARE ZIPPED SO THAT THEY CAN BE ITERATED OVER FOR LOOP SIMULTANEOUSLY
    return render(request, 'travello.html', {'dests_vacancies': zip(dests, vacancies), 'offers': count_of_offers})


# "destination_details" METHOD IS CALLED WHET THE USER REQUESTS FOR "destinations" PAGE
def destination_details(request, username, destination_id):

    dest = Packages.objects.get(location_id=destination_id)

    # FETCHING ALL RELATED RECORDS OF A PARTICULAR LOCATION FROM "DestinationDetails" TABLE AND
    # ORDERING THEM BASED ON "visiting_on" FIELD
    dests_local = DestinationDetails.objects.all().filter(location_id=destination_id).order_by('visiting_on')

    # FETCHING ALL RELATED RECORDS OF A PARTICULAR LOCATION FROM "PackagesGuide" TABLE
    guides = PackagesGuide.objects.all().filter(location_id=destination_id)

    # FETCHING ALL RELATED RECORDS OF A PARTICULAR LOCATION FROM "PackagesHotel" TABLE
    hotels = PackagesHotel.objects.get(location_id=destination_id)

    # FETCHING ALL RELATED RECORDS OF A PARTICULAR HOTEL FROM "PackagesHotel" TABLE
    hotel_images = HotelImages.objects.all().filter(hotel_id=hotels.hotel_id)

    # FETCHING ALL RELATED RECORDS OF A PARTICULAR LOCATION FROM "PackagesHotel" TABLE
    general_details = VehicleAndGeneralDetails.objects.get(location_id=destination_id)

    # CALCULATING THE VACANCY FOR A PARTICULAR LOCATION
    finder = FindVacancies()
    vacancy = finder.calculate(destination_id)

    # CONNECTING TO DATABASE TO FETCH THE LAST DATE TO BOOK THE SELECTED PACKAGE
    my_db = mysql.connector.connect(host='localhost', user='root', passwd='password', database='TravelBuddy')
    my_cur = my_db.cursor()

    # QUERY TO FETCH THE LAST DATE TO BOOK A PARTICULAR PACKAGE --> STARTS
    query = "select date " \
            "from travello_packages " \
            "where location_id = %s"

    my_cur.execute(query, (destination_id,))

    last_date = str(my_cur.fetchall()[0][0])
    # QUERY TO FETCH THE LAST DATE TO BOOK A PARTICULAR PACKAGE --> ENDS

    # FETCHING TODAY'S DATE
    today = str(datetime.now()).split(" ")[0]

    # IF TODAY'S DATE IS LESS THEN LAST BOOKING DATE THEN SET "can_be_booked" TO True ELSE False
    if today <= last_date:
        can_be_booked = 1
    else:
        can_be_booked = 0

    # RETURNING THE REQUESTED PAGE( i.e, destinations.html)
    return render(request, 'destinations.html', {'dest': dest, 'dests_local': dests_local, 'guides': guides,
                                                 'hotels': hotels, 'destination_id': destination_id, 'vacancy': vacancy,
                                                 'can_be_booked': can_be_booked, 'general_details': general_details,
                                                 'hotel_images': hotel_images})


# "bookings" METHOD IS CALLED WHET THE USER CLICK'S ON "Book Now :)" BUTTON
def bookings(request, username, destination_id):

    # IF THE REQUEST METHOD IS "POST" THEN EXECUTE if BLOCK
    if request.method == "POST":

        # READING NUMBER OF SEATS REQUESTED TO BE BOOKED
        seat_count = request.POST["seat_count"]

        # CONNECTING TO DATABASE TO FETCH THE BASIC PRICE OF THE SELECTED PACKAGE
        my_db = mysql.connector.connect(host='localhost', user='root', passwd='password', database='TravelBuddy')
        my_cur = my_db.cursor()

        # QUERY TO FETCH PRICE OF THE SELECTED PACKAGE(i.e, price per person)
        query = "select price " \
                "from travello_packages " \
                "where location_id = %s"

        my_cur.execute(query, (destination_id,))

        # FETCHING THE VALUE FROM LIST OF TUPLES
        price_per_person = my_cur.fetchall()[0][0]

        # CALCULATING THE TOTAL COST BY MULTIPLYING "NUMBER OF SEATS" AND "PRICE PER PERSON"
        total_cost = int(seat_count) * int(price_per_person)

        # RETURNING THE REQUESTED PAGE( i.e, bookings.html)
        return render(request, 'bookings.html', {'seat_count': seat_count, 'total_cost': total_cost,
                                                 'destination_id': destination_id})


def bookings_confirmed(request, username, destination_id):

    # IF THE REQUEST METHOD IS "POST" THEN EXECUTE if BLOCK
    if request.method == "POST":

        # EXTRACTING "14" FROM "Number of seats: 14"
        seat_count = request.POST["seat_count"].split(" ")[-1]

        # EXTRACTING "700" FROM "Amount: $700"
        amount = request.POST["amount"].split(" ")[-1][1:]

        email = request.POST["email"]

        # GENERATING "booking_id" BY CONCATENATING "username" AND THE "DATE AND TIME" OF BOOKING
        booking_id = username + str(datetime.now())

        # CONNECTING TO DATABASE TO STORE THE BOOKING DETAILS
        my_db = mysql.connector.connect(host='localhost', user='root', passwd='password', database='TravelBuddy')
        my_cur = my_db.cursor()

        # QUERY TO INSERT THE RECORD INTO "travello_packagesbookings" TABLE
        query = "INSERT INTO travello_packagesbookings" \
                "(booking_id, number_of_seats, total_amount, location_id_id, username_id) " \
                "VALUES(%s, %s, %s, %s, %s)"

        values = (booking_id, seat_count, amount, destination_id, username)

        my_cur.execute(query, values)
        my_db.commit()

        # SEND CONFIRMATION MAIL
        send_mail = SendConfirmationMail()
        send_mail.confirmation_mail(username, email, booking_id, seat_count, amount)

        # RETURNING THE CONFORMATION MESSAGE TO THE USER
        return HttpResponse("Booking confirmed check your mail id (" + email + ")for more details")
