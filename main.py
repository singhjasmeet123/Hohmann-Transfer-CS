import mysql.connector as sql
import math
import turtle
from tkinter import *

def option1():
    info_text.config(state=NORMAL)
    info_text.delete(1.0, END)
    info_text.insert(END, "A Hohmann Transfer is a very common orbital maneuver used by astrophysicists\n"
                          "to send a spacecraft from a small circular orbit to a larger one.\n")
    info_text.insert(END, "In this program, we will calculate the Hohmann transfer from one planet to another\n")
    info_text.config(state=DISABLED)

def option2():
    click_count = 0  # Counter to track the number of times "Calculate" is pressed
    output_text = ""
    P1_E = 0
    P2_M = 0
    R1_E = 0
    R2_M = 0
    def perform_calculation():
        nonlocal P2_M,P1_E,R1_E,R2_M
        nonlocal click_count, output_text
        input_planet = planet_entry.get().lower()

        planets = [planet[0].lower() for planet in output]

        if input_planet not in planets:
            output_text += "Invalid planet. Please enter a valid planet name from our solar system."

            info_text.config(state=NORMAL)
            info_text.delete(1.0, END)
            info_text.insert(END, output_text)
            info_text.config(state=DISABLED)
            return

        click_count += 1
        planet2 = input_planet.lower()

        if click_count == 1:
            planets = []
            for i in range(len(output)):
                planets.append(output[i][0])
            distances_from_sun = []
            for i in range(len(output)):
                distances_from_sun.append(output[i][1])
            d1 = int(distances_from_sun[0])
            # get user input for the two planets
            planet1 = 'Earth'
            if planet2 in planets:
                p2 = planets.index(planet2)
                d2 = int(distances_from_sun[p2])
            else:
                output_text = "Invalid planet. \nMake sure the planet name you entered is a valid planet in our solar system and has a greater distance from sun than Earth"

            # writing down the constants
            R1 = d1
            R2 = d2
            R1_E += R1
            R2_M += R2
            GM = 1.327 * (10 ** 11)  # standard gravitational parameter of sun in km³/s²

            # writing down orbital periods of planets in days
            orbital_periods = {
                'Earth': 365.25,
                'mars': 686.97,
                'jupiter': 4332.71,
                'saturn': 10759.721,
                'uranus': 30685.1868,
                'neptune': 60190.5955,
                'pluto': 90560
            }
            # calculating orbital periods of planet1 and planet2 in seconds
            P1 = (orbital_periods[planet1]) * 86400
            P2 = (orbital_periods[planet2]) * 86400
            P1_E += P1
            P2_M += P2
            a_transfer = (R1 + R2) / 2  # Semi major axis of transfer orbit

            def period(transfer):
                return math.sqrt(((4 * math.pi * 2) * (transfer * 3)) / GM)

            p_transfer = period(a_transfer)  # period of transfer orbit --

            V1 = (2 * math.pi * R1) / P1  # Velocity of Source Planet --
            V2 = (2 * math.pi * R2) / P2  # Velocity of Destination Planet --


            TOF = (p_transfer / 2) / 86400
            deg_move = 180 - ((360 / orbital_periods[planet2]) * TOF)
            unit = "days"
            tof_m = TOF / 30.417
            tof_y = tof_m / 12
            if tof_m >= 12:
                TOF = tof_y
                unit = "years"
            elif TOF >= 30:
                TOF = tof_m
                unit = "months"

            if output_text == "Invalid planet":
                pass
            else:
                output_text = f"Time of flight from {planet1} to {planet2}: {round(TOF, 1)} {unit}\n"
                output_text += f"Velocity of Earth V1 = {round(V1, 3)} km/s\n"
                output_text += f"Velocity of {planet2} V2 = {round(V2, 3)} km/s\n"
                output_text += f"A launch opportunity occurs when {planet2} is {round(deg_move, 0)} degrees ahead of Earth in its orbit.\n"
                output_text += "Press calculate again to get more information"


            info_text.config(state=NORMAL)
            info_text.delete(1.0, END)
            info_text.insert(END, output_text)
            info_text.config(state=DISABLED)
        else:
            P1 = P1_E
            P2 = P2_M
            GM = 1.327 * (10 ** 11)  # standard gravitational parameter of sun in km³/s²
            planet1 = 'Earth'
            a_transfer = (R1_E + R2_M) / 2  # Semi major axis of transfer orbit
            def period(transfer):
                return math.sqrt(((4 * math.pi * 2) * (transfer * 3)) / GM)
            p_transfer = period(a_transfer)  # period of transfer orbit --
            Vp = ((2 * math.pi * a_transfer) / p_transfer) * math.sqrt(((2 * a_transfer) / R1_E) - 1)  # --
            Va = ((2 * math.pi * a_transfer) / p_transfer) * math.sqrt(((2 * a_transfer) / R2_M) - 1)  # --
            V1 = (2 * math.pi * R1_E) / P1  # Velocity of Source Planet --
            V2 = (2 * math.pi * R2_M) / P2  # Velocity of Destination Planet --

            delta_V1 = Vp - V1  # Δv to enter Hohmann orbit from Earth's orbit --
            delta_V2 = V2 - Va
            output_text = (f"Distance of {planet1} from Sun : {R1_E} km\n")
            output_text += (f"Distance of {planet2} from Sun : {R2_M} km\n")
            output_text +=(f"Orbital Period of {planet1} : {P1} days\n")
            output_text +=(f"Orbital Period of {planet2} : {P2} days\n")
            output_text +=(f"Perihelion velocity = {round(Vp, 2)} km/s\n")
            output_text +=(f"Aphelion velocity  = {round(Va, 2)} km/s\n")
            output_text +=(f"ΔV1 = {round(delta_V1, 2)} km/s\nΔV1 is change of velocity from earth's orbit to transfer orbit\n"
                  f"This burst of velocity, ΔV1 is equal to the difference between the V perihelion and V1.\n")
            output_text +=(f"ΔV2  = {round(delta_V2, 2)} km/s\nΔV2 is the change in velocity necessary to send the spacecraft"
                  f" from the elliptical transfer orbit into {planet2}'s orbit")
            if (delta_V1 + delta_V2) < 11.2:
                output_text +=(
                    f"\nThe total ΔV required for a Hohmann transfer from Earth to {planet2} is about {round(delta_V1 + delta_V2, 1)} km/s.\n"
                    f"This is less than the ΔV required to escape Earth's gravity, which is about 11.2 km/s.\n"
                    f"This is because the spacecraft is able to use the gravity of the Sun to help it change its velocity.")
            else:
                output_text +=(
                    f"\nThe total ΔV required for a Hohmann transfer from Earth to {planet2} is about {round(delta_V1 + delta_V2, 1)} km/s.\n")
            output_text += (f"\nyou can confirm ΔV1 from https://en.wikipedia.org/wiki/Delta-v_budget")

            info_text.config(state=NORMAL)
            info_text.delete(1.0, END)
            info_text.insert(END, output_text)
            # info_text.config(state=DISABLED)


    info_text.config(state=NORMAL)
    info_text.delete(1.0, END)
    output_text = "Enter Destination planet in the new input box created below out of: \nMars, Jupiter, Saturn, Uranus, Neptune"
    info_text.insert(END, output_text)
    info_text.config(state=DISABLED)

    planet_label = Label(root, text="Enter destination planet:")
    planet_label.pack()

    planet_entry = Entry(root)
    planet_entry.pack()

    calculate_button = Button(root, text="Calculate", command=perform_calculation)
    calculate_button.pack()



def option3():
    t = turtle.Turtle()
    turtle.screensize(300, 300, "black")
    t.speed(10)
    t.pensize(1)
    import turtle as t
    t.Screen().bgcolor("black")

    def draw_circle(color, size, x, y):
        t.penup()
        t.color(color)
        t.fillcolor(color)
        t.goto(x, y)
        t.begin_fill()
        t.circle(size)
        t.end_fill()
        t.pendown()

    draw_circle("yellow", 10, 6, -7)
    t.color("white")
    t.up()
    t.goto(5, -48)
    t.down()
    t.color("blue")
    t.circle(50)
    t.color("red")

    def draw(rad):
        # rad --> radius of arc
        for i in range(2):
            # two arcs
            t.circle(rad, extent=90)
            t.circle(rad // 2, 90)

    # Main section
    # tilt the shape to 0 degrees
    t.seth(0)

    # calling draw method
    t.up()
    t.left(45)
    t.goto(40, -35)
    t.down()
    draw(100)
    t.color("white")
    t.up()
    t.goto(90, -83)
    t.down()
    t.circle(120)
    t.color("cyan")
    t.up()
    t.goto(5, -48)
    t.down()
    t.goto(5, -60)
    t.up()
    t.goto(5, -76)
    t.down()
    t.write("Earth's Orbit")
    t.color("white")
    t.up()
    t.goto(-20, 118)
    t.down()
    t.goto(5, 135)
    t.up()
    t.goto(7, 136)
    t.down()
    t.write("Mars' Orbit")
    t.color("red")
    t.up()
    t.goto(125, 55)
    t.down()
    t.right(180)
    t.forward(100)
    t.goto(125, 55)
    t.write("Transfer Orbit")
    t.hideturtle()
    t.exitonclick()

def option4():
    info_text.config(state=NORMAL)
    info_text.delete(1.0, END)
    info_text.insert(END, "The Hohmann transfer orbit has been used by many spacecraft, including the Apollo missions to the Moon, "
                          "the Voyager probes, and the Mars rovers.\n")
    info_text.insert(END, "The Hohmann transfer orbit is the most efficient way to transfer a spacecraft between two orbits "
                          "of different altitudes around a central body.\n")
    info_text.insert(END, "The Hohmann transfer orbit is not the only way to transfer a spacecraft between two orbits. Other methods, "
                          "such as a bi-elliptic transfer orbit, can be used to transfer a spacecraft more quickly, but they require more fuel.\n")
    info_text.insert(END, "The Hohmann transfer requires the spacecraft to perform two engine burns: one to raise its orbit and another "
                          "to lower it into the desired target orbit\n")
    info_text.config(state=DISABLED)

def exit_program():
    print("\nThanks for using our program!!!\n:)")
    root.destroy()

dbs = sql.connect(
    host="localhost",
    user="root",
    passwd="root")
dbcursor = dbs.cursor()

try:
    dbcursor.execute("create database hohmann_transfer")
except:
    print("Database exists")

try:
    dbcursor.execute("use hohmann_transfer")
except:
    print("Database already in use")

try:
    q1 = "create table dsun(Planets varchar(10) primary key,Distance_from_sun varchar(20) not null)"
    dbcursor.execute(q1)
except:
    print("table already exists")

try:
    dbcursor.execute("insert into dsun values('mercury','57910000')")
    dbs.commit()
    dbcursor.execute("insert into dsun values('venus','108210000')")
    dbs.commit()
    dbcursor.execute("insert into dsun values('earth','149597870')")
    dbs.commit()
    dbcursor.execute("insert into dsun values('mars','227920000')")
    dbs.commit()
    dbcursor.execute("insert into dsun values('jupiter','778570000')")
    dbs.commit()
    dbcursor.execute("insert into dsun values('saturn','1433530000')")
    dbs.commit()
    dbcursor.execute("insert into dsun values('uranus','2872460000')")
    dbs.commit()
    dbcursor.execute("insert into dsun values('neptune','4495060000')")
    dbs.commit()
except:
    print("Values already added in SQL")
dbcursor.execute("select *from dsun")
output = dbcursor.fetchall()

# Initialize the root window
root = Tk()
root.title("Hohmann Transfer Calculator")
bg = PhotoImage(file = "planets.ppm")
root.state('zoomed')
root.geometry("3840x2160")
label1 = Label( root, image = bg)
label1.place(x = 0, y = 0)
label2 = Label( root, text = "Welcome")
label2.pack(pady = 20)

frame1 = Frame(root)
frame1.pack(pady = 20 )

# Other code...
frame2 = Frame(root)
frame2.pack(pady=20)

root.title("Menu")
# Create widgets
info_text = Text(root, height=15, width=90, wrap=WORD)
info_text.pack(pady=10)
info_text.insert(END, "Welcome to Hohmann Transfer Calculator!\n\n")

frame1 = Frame(root)
frame1.pack(pady=20)


# Create buttons for each option
button1 = Button(root, text="Hohmann Transfer Intro", command=option1)
button1.pack(pady=5)

button2 = Button(root, text="Calculations", command=option2)
button2.pack(pady=5)

button3 = Button(root, text="Turtle Diagram", command=lambda : [button3.pack_forget(),option3()])
button3.pack(pady=5)

button4 = Button(root, text="Fun Facts", command=option4)
button4.pack(pady=5)

exit_button = Button(root, text="Exit", command=exit_program)
exit_button.pack(pady=5)

root.mainloop()