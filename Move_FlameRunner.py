'''
Move_FlameRunner.py
Tufts Create®3 Educational Robot
by Maddie Pero
Edited by Vibha, Cardi, and Ethan

In this example we will publish random colors to the LED ring on the Create®3.
'''

'''
These statements allow the Node class to be used.
'''
import sys
import rclpy
from rclpy.node import Node
import random
import time
import FlameRunner # Import FlameRunner.py file so we can read from AirTable

'''
These statements import Twist messages to send to /cmd_vel
And Vector3 to create the Twist messages
'''
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3

class MovePublisher(Node):
    '''
    The MovePublisher class is created which is a subclass of Node.
    This defines the class' constructor.
    '''
    def __init__(self):    
        '''
        The following line calls the Node class's constructor and gives it the Node name,
        which is 'mv_publisher.'
        '''
        super().__init__('mv_publisher')
        
        '''
        We are declaring how we want the Node to publish message. We've imported Twist
        from geometry_msgs.msg over the topic '/cmd_vel' with a queue size of 10.
        Queue size is a quality of service setting that limiits amount of queued messages.
        Basically, we are determining what type of data we want to publish. 
        '''
        print('Creating publisher')
        self.move_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
        '''
        The timer allows the callback to execute every 2 seconds, with a counter iniitialized.
        The timer_callback function is called every two seconds
        '''
        print('Creating a callback timer') 
        timer_period = 2
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        # Create the Twist message that we will use to publish the new movement values
        self.twist = Twist()

    def timer_callback(self):
        '''
        In this function we read the data from the AirTable and publish it to the robot
        '''
        
        # Create Vector3s that we can use to create the Twist message
        linear = Vector3()
        angular = Vector3()
        
        # Read data from AirTable and store those values in the Vector3s
        # Only read the data from the table for the XYZ values that matter (X for linear, Z for angular)
        # The other XYZ values that aren't read from the table are always set to zero
        # If data is not read correctly, don't move (hence the try, except block)
        try:
            data = FlameRunner.get_data()
            linear.x = float(data[0]) #Set linear value to value from AirTable
            linear.y = float(0)
            linear.z = float(0)
            
            angular.x = float(0)
            angular.y = float(0)
            angular.z = float(data[1]) #Set angular value to value from AirTable
        except:
            linear.x = float(0)
            linear.y = float(0)
            linear.z = float(0)
            
            angular.x = float(0)
            angular.y = float(0)
            angular.z = float(0)
        
        current_time = self.get_clock().now()
        print('Changing the speed/angle of the robot')
        
        # Update the linear and angular values for the twist message and publish them to the robot
        self.twist.linear = linear
        self.twist.angular = angular
        self.move_publisher.publish(self.twist)

def main(args=None):
    '''
    The rclpy library is initialized.
    '''
    rclpy.init(args=args)
    
    '''
    The node is created and can be used in other parts of the script.
    '''
    mv_publisher = MovePublisher()

    '''
    The node is "spun" so the callbacks can be called.
    '''
    print('Callbacks are called')
    try:
        rclpy.spin(mv_publisher)
    except KeyboardInterrupt:
        print('\nCaught Keyboard Interrupt')
    finally:
        print("Done")  
        #mv_publisher.reset() - errors if we call this function and not necessary because the robot stops anyway
        print('shutting down')
        mv_publisher.destroy_node() # Destroy the node explicitly
        #rclpy.shutdown() - errors if we call this function: "rcl_shutdown already called on the given context"


if __name__ == '__main__':
    main()
