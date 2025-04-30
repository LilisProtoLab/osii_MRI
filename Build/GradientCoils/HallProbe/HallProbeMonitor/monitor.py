import serial
import csv
import matplotlib.pyplot as plt
from collections import deque

def read_serial_data():
    ser = serial.Serial('COM3', 9600, timeout=1)

    with open('output.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['BFieldX', 'BFieldY', 'BFieldZ'])  #
    
        max_points = 100
        bfield_x = deque(maxlen=max_points)
        bfield_y = deque(maxlen=max_points)
        bfield_z = deque(maxlen=max_points)
        time = deque(maxlen=max_points)
        current_time = 0

        plt.ion()
        fig, ax = plt.subplots()
        line1, = ax.plot(time, bfield_x, label='BFieldX')
        line2, = ax.plot(time, bfield_y, label='BFieldY')
        line3, = ax.plot(time, bfield_z, label='BFieldZ')
        ax.set_xlabel('Time')
        ax.set_ylabel('Magnetic Field')
        ax.legend()
        plt.show()
    
        try:
            while True:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    print(f"Received: {line}")
                    data = line.split(',')
                    if len(data) == 3:
                        writer.writerow(data)
                        bfield_x.append(float(data[0]))
                        bfield_y.append(float(data[1]))
                        bfield_z.append(float(data[2]))
                        time.append(current_time)
                        current_time += 1
                        line1.set_xdata(time)
                        line1.set_ydata(bfield_x)
                        line2.set_xdata(time)
                        line2.set_ydata(bfield_y)
                        line3.set_xdata(time)
                        line3.set_ydata(bfield_z)
                        ax.relim()
                        ax.autoscale_view()
                        plt.pause(0.01)
        except KeyboardInterrupt:
            print("Exiting...")
        finally:
            ser.close()
    

if __name__ == "__main__":
    read_serial_data()