from django.shortcuts import render
import mysql.connector


class QueryExecutor:

    def __init__(self):
        self.my_db = mysql.connector.Connect(host='localhost', user='root', passwd='password', database='TravelBuddy')
        self.my_cur = self.my_db.cursor()

    def get_count_of_available_packages(self):

        query = "select count(*)" \
                "from travello_packages"

        self.my_cur.execute(query)

        count_of_locations = self.my_cur.fetchall()[0][0]

        return count_of_locations

    def get_total_bookings(self):

        query = "select sum(number_of_seats)" \
                "from travello_packagesbookings"

        self.my_cur.execute(query)

        total_bookings = self.my_cur.fetchall()[0][0]

        return total_bookings

    def get_count_of_users(self):

        query = "select count(*)" \
                "from auth_user"

        self.my_cur.execute(query)

        number_of_users = self.my_cur.fetchall()[0][0]

        return number_of_users


# Create your views here.
def about(request, username):

    executor = QueryExecutor()

    count_of_locations = executor.get_count_of_available_packages()

    total_bookings = executor.get_total_bookings()

    number_of_users = executor.get_count_of_users()

    data = {
        'count_of_locations': count_of_locations,
        'total_bookings': total_bookings,
        'number_of_users': number_of_users,
        'number_of_tie_ups': 0
    }

    return render(request, 'about.html', {'data': data})
