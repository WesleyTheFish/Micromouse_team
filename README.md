Micromouse_team
===

This repository contains a Micromouse project with two main parts:

- A desktop Python maze simulator and solver (under `src/maze_solver/`).
- Prototype CircuitPython code to communicate with different sensors on a Pico-based robot (under `src/pico/`).

Summary
-------

This README briefly describes what each folder does, how to run the simulator, known issues in the hardware code, and suggested next steps.

1) src/maze_solver/
	 - Purpose: A text-mode maze simulator and Micromouse-style solver. It models the maze as Cells and Walls and uses a flood-fill (weight propagation) algorithm to compute shortest paths to the finish.
	 - Key modules:
		 - `cell.py` — cell data (address, weight, surrounding walls) and text-print helper.
		 - `wall.py` — wall representation and colorized printing.
		 - `maze.py` — builds maze grid, creates a hard-coded "key" maze layout (size 5 and 16 supported), and contains weight propagation and printing routines.
		 - `mouse.py` — simulated mouse that explores the maze by copying wall information from the maze key into its discovered map, recomputes weights, and chooses next moves.
		 - `main.py` — example runner that creates a maze (16×16 by default), runs the simulation, and prints the result.
	 - How it works: The solver repeatedly updates discovered walls, recomputes cell weights from the finish (flood-fill), and moves to the neighboring cell with the smallest weight (ties prefer the current facing direction). After reaching the finish the simulator runs back to the start to compute a shortest route.
	 - Run (desktop): Install Python 3 and the `colorama` package, then run:

		 ```
		 python src/maze_solver/main.py
		 ```

2) src/pico/
	 - Purpose: CircuitPython code that implements a small `Assembly` class that composes motors, encoders, ToF distance sensors, and an IMU for a Pico robot.
	 - Key modules:
		 - `assembly.py` — high-level assembly combining `Motor`, `Encoder`, and `IMU` objects and providing simple motion methods (forward/back/turn).
		 - `motor.py` — simple motor wrapper using `digitalio` for direction and `pwmio.PWMOut` for speed control.
		 - `encoder.py` — intended quadrature encoder reader.
		 - `imu.py` — wrapper around an Adafruit BNO055 driver.
		 - `distance_sensor.py`, `oled.py` — Not implemented yet.
		 - `code.py` — a short demo script that instantiates `Assembly` and runs a brief forward/back motion.
	 - Notes: This code targets CircuitPython on a Pico and depends on Adafruit libraries (e.g., `adafruit_bno055`, `adafruit_vl53l1x`, `adafruit_displayio_ssd1306`). It is prototype-level and requires small fixes to run on hardware.

Component Usage
----
- IMU Fields
	- **temperature** - The sensor temperature in degrees Celsius.
	- **acceleration** - This is a 3-tuple of X, Y, Z axis accelerometer values in meters per second squared.
	- **magnetic** - This is a 3-tuple of X, Y, Z axis magnetometer values in microteslas.
	- **gyro** - This is a 3-tuple of X, Y, Z axis gyroscope values in degrees per second.
	- **euler** - This is a 3-tuple of orientation Euler angle values.
	- **quaternion** - This is a 4-tuple of orientation quaternion values.
	- **linear_acceleration** - This is a 3-tuple of X, Y, Z linear acceleration values (i.e. without effect of gravity) in meters per second squared.
	- **gravity** - This is a 3-tuple of X, Y, Z gravity acceleration values (i.e. without the effect of linear acceleration) in meters per second squared.

Known issues (pico code)
------------------------
- Live async encoder reading needs to be implemented

Languages
-----------
- Python
- Circuit Python
- Markdown

Required Packages
-------
| Desktop / Standard    | CircuitPython / Hardware  |
|           ---         |           ---             |
|        Colorama       |         digitalio         |
|                       |          pwmio            |
|                       |          board            |
|                       |          asyncio          |
|                       |          time             |
|                       | adafruit_vl53l1x (ToF sensor) |
|                       |    adafruit_bno055 (IMU)  |


Authors
---------------
- Wesley Bass (`src/maze_solver`, `src/pico`)
- Miriam Sinton-Remes (`src/pico`)
- Kate Burton (`src/pico`)
- Elizabeth Williams (`src/pico`)