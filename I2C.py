import smbus  # Import the SMBus library for I2C communication
import time   # Import the time module for timing and sleep functions

# Constants obtained from the sensor datasheet
DEVICE = 0x23  # Default I2C device address for the light sensor

POWER_DOWN = 0x00  # Device powered down
POWER_ON = 0x01    # Device powered on
RESET = 0x07        # Reset data register value

# Measurement modes constants
# Measurement at 1 lux resolution (typically 120ms)
ONE_TIME_HIGH_RES_MODE_1 = 0x20

# Initialize the I2C bus (change the bus number to 0 for Raspberry Pi Revision 1)
bus = smbus.SMBus(1)


def convertToNumber(data):
    """
    Convert a pair of data bytes into a decimal number.

    Args:
        data (list): A list containing two bytes representing sensor data.

    Returns:
        float: The decimal number converted from the data.
    """
    result = (data[1] + (256 * data[0])) / 1.2  # Conversion formula
    return result


def categorizeLightLevel(light_level):
    """
    Categorize light levels into descriptive categories.

    Args:
        light_level (float): The light level in lux.

    Returns:
        str: A descriptive category for the light level.
    """
    if light_level > 1000:
        return "Too Bright"
    elif light_level > 500:
        return "Bright"
    elif light_level > 100:
        return "Medium"
    elif light_level > 10:
        return "Dark"
    else:
        return "Too Dark"


def readLight(addr=DEVICE):
    """
    Read light data from the I2C interface.

    Args:
        addr (int): The I2C device address (default is 0x23).

    Returns:
        float: The light level in lux.
    """
    data = bus.read_i2c_block_data(
        addr, ONE_TIME_HIGH_RES_MODE_1)  # Read data from the sensor
    light_level = convertToNumber(data)  # Convert sensor data to lux
    return light_level


def main():
    """
    Main function for continuous reading and displaying light levels.
    """
    while True:
        light_level = readLight()  # Read light level from the sensor
        category = categorizeLightLevel(
            light_level)  # Categorize the light level
        print("Light Level : " + format(light_level, '.2f') +
              " lx (" + category + ")")  # Display the light level
        time.sleep(0.5)  # Pause for 0.5 seconds


if __name__ == "__main__":
    main()  # Execute the main function if this script is run directly
