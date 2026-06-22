"""Pre-defined content sources for common electronics circuits."""
# flake8: noqa: E501

from typing import TypedDict


class SourceDict(TypedDict, total=False):
    name: str
    url: str


class CircuitContent(TypedDict):
    title: str
    type: str
    description: str
    components: list[str]
    wiring_steps: list[str]
    explanation: str
    circuit_diagram_description: str
    sources: list[SourceDict]


CIRCUIT_LIBRARY: list[CircuitContent] = [
    {
        "title": "LED Blink Circuit",
        "type": "circuit_generation",
        "description": "A simple astable multivibrator circuit using a 555 timer IC "
        "that blinks an LED at a adjustable frequency, perfect for beginners learning "
        "about timing circuits and LED indicators.",
        "components": ["555 Timer IC", "Resistor 1k\u2126 (2x)", "Resistor 220\u2126",
                       "Capacitor 10\u00b5F", "Capacitor 100nF", "LED (any colour)",
                       "9V Battery", "Battery clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Place 555 timer across the centre channel of the breadboard",
                         "Connect pin 1 (GND) to the negative rail",
                         "Connect pin 8 (VCC) to the positive rail via 220\u2126 resistor",
                         "Connect pin 4 (RESET) to the positive rail",
                         "Wire 1k\u2126 resistor between pin 7 (DISCH) and pin 8 (VCC)",
                         "Wire 1k\u2126 resistor between pin 7 (DISCH) and pin 6 (THRESH)",
                         "Connect 10\u00b5F capacitor from pin 6 to GND",
                         "Wire 100nF capacitor from pin 5 (CONT) to GND",
                         "Connect LED anode through 220\u2126 resistor to pin 3 (OUT)",
                         "Connect LED cathode to GND",
                         "Connect 9V battery: positive to rail, GND to negative rail"],
        "explanation": "The 555 timer operates in astable mode, oscillating between "
        "charging and discharging the capacitor through the resistors. The output (pin 3) "
        "toggles high and low, causing the LED to blink. Frequency is determined by "
        "R1, R2, and C1: f = 1.44 / ((R1 + 2*R2) * C1).",
        "circuit_diagram_description": "Standard 555 astable multivibrator with LED output. "
        "Pin 7 connects to VCC via R1 and to pin 6 via R2. Pin 6 connects to GND via C1. "
        "Output pin 3 drives LED through current-limiting resistor to GND.",
        "sources": [
            {"name": "Wikipedia - 555 Timer IC",
             "url": "https://en.wikipedia.org/wiki/555_timer_IC"},
            {"name": "Electronics Tutorials - 555 Astable",
             "url": "https://www.electronics-tutorials.ws/waveforms/555_oscillator.html"},
        ],
    },
    {
        "title": "Buzzer Circuit",
        "type": "circuit_generation",
        "description": "A simple buzzer circuit using a piezoelectric buzzer element "
        "driven by a 555 timer oscillator, producing an audible tone.",
        "components": ["555 Timer IC", "Piezoelectric buzzer", "Resistor 10k\u2126",
                       "Resistor 100k\u2126", "Capacitor 100nF", "Capacitor 10\u00b5F",
                       "9V Battery", "Battery clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Place 555 timer on breadboard",
                         "Connect pin 1 to GND, pin 8 to VCC",
                         "Wire 10k\u2126 between pin 7 and pin 8",
                         "Wire 100k\u2126 between pin 7 and pin 6",
                         "Connect 10\u00b5F from pin 6 to GND",
                         "Connect 100nF from pin 5 to GND",
                         "Connect buzzer positive to pin 3, negative to GND",
                         "Power with 9V battery"],
        "explanation": "The 555 generates a square wave in the audio frequency range. "
        "The piezoelectric buzzer converts electrical oscillations into sound waves. "
        "Frequency is set by the resistor-capacitor network.",
        "circuit_diagram_description": "555 astable configuration with piezo buzzer on output pin 3.",
        "sources": [
            {"name": "Wikipedia - Buzzer",
             "url": "https://en.wikipedia.org/wiki/Buzzer"},
            {"name": "Wikipedia - 555 Timer IC",
             "url": "https://en.wikipedia.org/wiki/555_timer_IC"},
        ],
    },
    {
        "title": "Battery Tester Circuit",
        "type": "circuit_generation",
        "description": "A simple battery tester that uses an LED bar graph or "
        "individual LEDs to indicate the voltage level of a battery under test.",
        "components": ["LM3914 Dot/Bar Display Driver", "LED (10x, any colour)",
                       "Resistor 1k\u2126", "Resistor 10k\u2126 (adjustable)",
                       "Capacitor 10\u00b5F", "9V Battery", "Battery clip",
                       "Breadboard", "Jumper wires"],
        "wiring_steps": ["Place LM3914 on breadboard",
                         "Connect pin 2 (GND) and pin 4 to GND",
                         "Connect pin 3 (VCC) to positive rail via 1k\u2126 resistor",
                         "Wire 10k\u2126 potentiometer between pin 7 and pin 8",
                         "Connect capacitor from pin 2 to pin 3",
                         "Connect LED anodes to pins 1, 18, 17, 16, 15, 14, 13, 12, 11, 10",
                         "Connect LED cathodes to GND via 220\u2126 each",
                         "Connect battery under test to input pin 5",
                         "Power the LM3914 from 9V supply"],
        "explanation": "The LM3914 senses the input voltage on pin 5 and illuminates "
        "one or more LEDs in proportion. Each LED represents approximately 1.25V steps, "
        "giving a visual voltage readout.",
        "circuit_diagram_description": "LM3914 in dot mode with 10 LEDs forming a bar graph, "
        "input on pin 5 through voltage divider.",
        "sources": [
            {"name": "Wikipedia - LM3914",
             "url": "https://en.wikipedia.org/wiki/LM3914"},
            {"name": "Electronics Tutorials - Voltage Indicator",
             "url": "https://www.electronics-tutorials.ws/blog/voltage-level-indicator.html"},
        ],
    },
    {
        "title": "Push Button LED Circuit",
        "type": "circuit_generation",
        "description": "A basic push-button controlled LED circuit. Pressing the "
        "button turns the LED on; releasing turns it off.",
        "components": ["LED (any colour)", "Resistor 220\u2126", "Push button (momentary)",
                       "9V Battery", "Battery clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Place LED on breadboard with anode towards positive rail",
                         "Connect 220\u2126 resistor from LED anode to positive rail",
                         "Connect LED cathode to one terminal of push button",
                         "Connect other push button terminal to GND",
                         "Power with 9V battery"],
        "explanation": "When the button is pressed, the circuit completes, allowing "
        "current to flow through the resistor and LED to GND. The resistor limits "
        "current to protect the LED.",
        "circuit_diagram_description": "Simple series circuit: battery positive to resistor, "
        "resistor to LED anode, LED cathode to push button, push button to GND.",
        "sources": [
            {"name": "Wikipedia - Switch",
             "url": "https://en.wikipedia.org/wiki/Switch"},
            {"name": "Wikipedia - LED Circuit",
             "url": "https://en.wikipedia.org/wiki/LED_circuit"},
        ],
    },
    {
        "title": "Darkness Detector Circuit",
        "type": "circuit_generation",
        "description": "An LDR-based circuit that turns on an LED when ambient "
        "light levels drop below a threshold — a simple night-light.",
        "components": ["LDR (Light Dependent Resistor)", "Resistor 10k\u2126",
                       "Resistor 220\u2126", "Transistor BC547 (NPN)",
                       "LED", "Potentiometer 100k\u2126", "9V Battery",
                       "Battery clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Place BC547 on breadboard",
                         "Connect LDR from positive rail to transistor base",
                         "Connect 10k\u2126 from base to GND (pull-down)",
                         "Connect potentiometer wiper to base via 1k\u2126",
                         "Connect emitter to GND",
                         "Connect 220\u2126 resistor and LED from collector to positive rail",
                         "Adjust potentiometer to set sensitivity",
                         "Power with 9V battery"],
        "explanation": "In darkness, the LDR's resistance increases, raising the base "
        "voltage of BC547. When sufficient, the transistor saturates, allowing current "
        "through the LED. In light, LDR resistance drops, base voltage falls, transistor "
        "cuts off, LED turns off.",
        "circuit_diagram_description": "Voltage divider (LDR + 10k\u2126) drives transistor base. "
        "Collector has LED with current-limiting resistor to VCC. Emitter to GND.",
        "sources": [
            {"name": "Wikipedia - Light Dependent Resistor",
             "url": "https://en.wikipedia.org/wiki/Photoresistor"},
            {"name": "Wikipedia - Transistor",
             "url": "https://en.wikipedia.org/wiki/Transistor"},
        ],
    },
    {
        "title": "Light Sensor Circuit",
        "type": "circuit_generation",
        "description": "An LDR-based light sensor that activates a relay or LED when "
        "light exceeds a set threshold.",
        "components": ["LDR", "Resistor 10k\u2126", "Resistor 220\u2126",
                       "Transistor BC547", "LED", "Relay 5V (optional)",
                       "Potentiometer 100k\u2126", "9V Battery", "Battery clip",
                       "Breadboard", "Jumper wires"],
        "wiring_steps": ["Place BC547 on breadboard",
                         "Form voltage divider: LDR from VCC to base, 10k\u2126 base to GND",
                         "Connect potentiometer wiper to base through 1k\u2126 resistor",
                         "Connect emitter to GND",
                         "Connect LED with 220\u2126 resistor from collector to VCC",
                         "Adjust potentiometer for desired threshold",
                         "Power with 9V battery"],
        "explanation": "The LDR and fixed resistor form a voltage divider. When light "
        "intensity increases, LDR resistance decreases, raising base voltage and "
        "turning on the transistor.",
        "circuit_diagram_description": "Voltage divider (LDR + resistor) feeding transistor "
        "base. Collector load is LED with series resistor.",
        "sources": [
            {"name": "Wikipedia - Photoresistor",
             "url": "https://en.wikipedia.org/wiki/Photoresistor"},
        ],
    },
    {
        "title": "Transistor Switch Circuit",
        "type": "circuit_generation",
        "description": "A basic NPN transistor used as an electronic switch to "
        "control a high-current load from a low-current signal.",
        "components": ["Transistor BC547 (NPN)", "Resistor 1k\u2126 (base)",
                       "Resistor 220\u2126 (load)", "LED (load indicator)",
                       "Push button", "9V Battery", "Battery clip",
                       "Breadboard", "Jumper wires"],
        "wiring_steps": ["Place BC547 on breadboard (E B C facing left to right)",
                         "Connect 1k\u2126 resistor from push button to transistor base",
                         "Connect push button other terminal to VCC",
                         "Connect emitter to GND",
                         "Connect LED anode through 220\u2126 to VCC",
                         "Connect LED cathode to collector",
                         "Power with 9V battery"],
        "explanation": "When the button is pressed, base current flows through 1k\u2126. "
        "This forward-biases the base-emitter junction, saturating the transistor. "
        "Collector current then flows through the LED, lighting it.",
        "circuit_diagram_description": "Base driven via resistor and switch from VCC. "
        "Collector has LED load to VCC. Emitter to GND.",
        "sources": [
            {"name": "Wikipedia - Transistor",
             "url": "https://en.wikipedia.org/wiki/Transistor"},
            {"name": "Electronics Tutorials - Transistor as Switch",
             "url": "https://www.electronics-tutorials.ws/transistor/tran_4.html"},
        ],
    },
    {
        "title": "Water Level Indicator Circuit",
        "type": "circuit_generation",
        "description": "A circuit using conductive probes to sense water level and "
        "indicate it via multiple LEDs, useful for water tanks and reservoirs.",
        "components": ["Transistor BC547 (4x)", "LED (4x, different colours)",
                       "Resistor 220\u2126 (4x)", "Resistor 10k\u2126 (4x, base)",
                       "Waterproof probe wires (5x)", "9V Battery",
                       "Battery clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Place four BC547 transistors on breadboard",
                         "For each transistor: connect 10k\u2126 from base to probe wire",
                         "Connect all emitters to GND",
                         "Connect each collector through 220\u2126 to its corresponding LED",
                         "Connect all LED anodes to VCC",
                         "Place probes at increasing water depths",
                         "Connect common probe (ground) at bottom",
                         "Power with 9V battery"],
        "explanation": "Water conducts weakly between probes. When water reaches a probe, "
        "it provides a small base current to the transistor, turning it on. Each LED "
        "indicates a specific water level.",
        "circuit_diagram_description": "Four transistor stages, each base tied to a probe wire. "
        "Common ground probe. Collectors drive LEDs to VCC.",
        "sources": [
            {"name": "Wikipedia - Water Level Sensor",
             "url": "https://en.wikipedia.org/wiki/Water_level_sensor"},
        ],
    },
    {
        "title": "Rain Alarm Circuit",
        "type": "circuit_generation",
        "description": "A circuit that detects moisture (rain) using a sensor plate "
        "and triggers an audible alarm.",
        "components": ["Transistor BC547 (2x)", "Piezoelectric buzzer",
                       "Resistor 100k\u2126", "Resistor 1k\u2126",
                       "LED", "Rain sensor plate (DIY copper strip board)",
                       "9V Battery", "Battery clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Build rain sensor: two interleaved copper strips on PCB",
                         "Connect sensor to base of first BC547 via 100k\u2126 resistor",
                         "Connect first BC547 emitter to GND",
                         "Collector of first BC547 drives base of second via 1k\u2126",
                         "Second BC547 emitter to GND, collector to buzzer negative",
                         "Buzzer positive to VCC",
                         "LED with 220\u2126 from second collector to GND (visual)",
                         "Power with 9V battery"],
        "explanation": "Rain water bridges the sensor strips, allowing a small current "
        "to flow into the first transistor's base. This two-stage darlington-like "
        "amplification produces enough current to drive the buzzer.",
        "circuit_diagram_description": "Two-stage NPN amplifier. Sensor input to Q1 base. "
        "Q1 collector drives Q2 base. Q2 collector drives buzzer to VCC.",
        "sources": [
            {"name": "Wikipedia - Rain Sensor",
             "url": "https://en.wikipedia.org/wiki/Rain_sensor"},
        ],
    },
    {
        "title": "Touch Sensor Circuit",
        "type": "circuit_generation",
        "description": "A touch-sensitive circuit that activates an LED or relay when "
        "a touch plate is contacted, using the human body's capacitance.",
        "components": ["Transistor BC547 (2x)", "Resistor 1M\u2126 (2x)",
                       "Resistor 220\u2126", "LED", "Touch plate (metal piece)",
                       "9V Battery", "Battery clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Place two BC547 transistors in darlington configuration",
                         "Q1 base connects to touch plate via 1M\u2126 resistor",
                         "Q1 base also has 1M\u2126 pull-down to GND",
                         "Q1 emitter to Q2 base directly",
                         "Q2 emitter to GND",
                         "LED with 220\u2126 from Q2 collector to VCC",
                         "Touch plate is any exposed metal surface",
                         "Power with 9V battery"],
        "explanation": "Touching the plate introduces 50/60Hz hum from the body or "
        "a small DC bias. The darlington pair amplifies this tiny signal enough to "
        "saturate Q2 and light the LED.",
        "circuit_diagram_description": "Darlington pair (Q1+Q2). Touch plate to "
        "Q1 base with high-value resistor. Q2 collector drives LED to VCC.",
        "sources": [
            {"name": "Wikipedia - Touch Switch",
             "url": "https://en.wikipedia.org/wiki/Touch_switch"},
        ],
    },
    {
        "title": "Clap Switch Circuit",
        "type": "circuit_generation",
        "description": "A sound-activated switch using a condenser microphone to "
        "detect a clap and toggle a relay or LED on/off.",
        "components": ["Condenser microphone", "Transistor BC547 (3x)",
                       "Resistor 10k\u2126 (2x)", "Resistor 100k\u2126",
                       "Resistor 220\u2126", "Capacitor 10\u00b5F", "LED",
                       "Relay 5V (optional)", "9V Battery", "Battery clip",
                       "Breadboard", "Jumper wires"],
        "wiring_steps": ["Connect condenser mic to VCC via 10k\u2126 (bias)",
                         "Couple mic output through 10\u00b5F capacitor to Q1 base",
                         "Q1 emitter to GND, collector to VCC via 100k\u2126",
                         "Q1 output drives Q2 base via 10k\u2126",
                         "Q2 emitter to GND, collector drives Q3 base",
                         "Q3 emitter to GND, collector drives LED via 220\u2126",
                         "Toggle feedback from Q3 collector to Q2 base",
                         "Power with 9V battery"],
        "explanation": "The microphone converts sound (clap) to an electrical signal. "
        "The signal is amplified through three transistor stages. The feedback "
        "creates a latching toggle action.",
        "circuit_diagram_description": "Three-stage transistor amplifier with "
        "condenser mic input. Feedback creates toggle latch.",
        "sources": [
            {"name": "Wikipedia - Clap Switch",
             "url": "https://en.wikipedia.org/wiki/Clap_switch"},
        ],
    },
    {
        "title": "Burglar Alarm Circuit",
        "type": "circuit_generation",
        "description": "A simple magnetic reed switch based burglar alarm that "
        "triggers a buzzer when a door or window is opened.",
        "components": ["Magnetic reed switch (NC type)", "Transistor BC547 (2x)",
                       "Piezoelectric buzzer", "Resistor 10k\u2126",
                       "Resistor 1k\u2126", "LED", "9V Battery",
                       "Battery clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Connect reed switch in series with 10k\u2126 to Q1 base",
                         "Q1 base also has pull-up to VCC via 10k\u2126",
                         "Q1 emitter to GND",
                         "Q1 collector drives Q2 base via 1k\u2126 resistor",
                         "Q2 emitter to GND",
                         "Connect buzzer between Q2 collector and VCC",
                         "LED with 220\u2126 across buzzer for visual",
                         "Power with 9V battery"],
        "explanation": "With the magnet present (door closed), the reed switch is "
        "closed, keeping Q1 base high and Q1 on. This keeps Q2 base low, "
        "keeping the buzzer off. When the door opens, the switch opens, "
        "Q1 turns off, Q2 turns on, activating the alarm.",
        "circuit_diagram_description": "Reed switch voltage divider drives Q1. "
        "Q1 collector drives Q2 base. Q2 collector drives buzzer to VCC.",
        "sources": [
            {"name": "Wikipedia - Reed Switch",
             "url": "https://en.wikipedia.org/wiki/Reed_switch"},
            {"name": "Wikipedia - Burglar Alarm",
             "url": "https://en.wikipedia.org/wiki/Burglar_alarm"},
        ],
    },
    {
        "title": "Fire Alarm Circuit",
        "type": "circuit_generation",
        "description": "A heat/fire detection circuit using a thermistor that "
        "triggers a buzzer when temperature exceeds a threshold.",
        "components": ["Thermistor (NTC, 10k\u2126 @ 25\u00b0C)",
                       "Resistor 10k\u2126", "Potentiometer 100k\u2126",
                       "Transistor BC547 (2x)", "Piezoelectric buzzer",
                       "LED", "Resistor 220\u2126", "9V Battery",
                       "Battery clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Form voltage divider: thermistor from VCC to base node, "
                         "10k\u2126 from base node to GND",
                         "Connect potentiometer wiper to same node",
                         "Node connects to Q1 base",
                         "Q1 emitter to GND, collector to VCC via 10k\u2126",
                         "Q1 collector drives Q2 base",
                         "Q2 emitter to GND, collector drives buzzer to VCC",
                         "LED with 220\u2126 across buzzer",
                         "Adjust potentiometer for trigger temperature",
                         "Power with 9V battery"],
        "explanation": "The NTC thermistor's resistance decreases as temperature "
        "increases. At the threshold temperature, the voltage at the base node "
        "crosses the transistor's turn-on voltage, triggering the alarm.",
        "circuit_diagram_description": "Thermistor+resistor voltage divider drives "
        "two-stage transistor amplifier to buzzer.",
        "sources": [
            {"name": "Wikipedia - Thermistor",
             "url": "https://en.wikipedia.org/wiki/Thermistor"},
            {"name": "Wikipedia - Fire Alarm",
             "url": "https://en.wikipedia.org/wiki/Fire_alarm"},
        ],
    },
    {
        "title": "Smoke Detector Circuit",
        "type": "circuit_generation",
        "description": "An optical smoke detector circuit using an IR LED and "
        "phototransistor to detect smoke particles in the air.",
        "components": ["IR LED", "Phototransistor", "Transistor BC547 (2x)",
                       "Resistor 220\u2126", "Resistor 10k\u2126 (2x)",
                       "Piezoelectric buzzer", "LED (indicator)", "9V Battery",
                       "Battery clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Place IR LED and phototransistor facing each other (~2cm apart)",
                         "IR LED anode to VCC via 220\u2126, cathode to GND",
                         "Phototransistor collector to VCC via 10k\u2126",
                         "Phototransistor emitter to GND",
                         "Collector node drives Q1 base",
                         "Q1 emitter to GND, collector to VCC via 10k\u2126",
                         "Q1 collector drives Q2 base",
                         "Q2 emitter to GND, collector drives buzzer to VCC",
                         "Indicator LED with 220\u2126 across buzzer",
                         "Power with 9V battery"],
        "explanation": "Normally the phototransistor sees the IR beam and conducts. "
        "When smoke enters, it scatters the IR light, reducing the light reaching "
        "the phototransistor. This changes the voltage, triggering the alarm.",
        "circuit_diagram_description": "IR LED emits continuous beam. Phototransistor "
        "detects beam. Signal goes through two-stage amplifier to buzzer.",
        "sources": [
            {"name": "Wikipedia - Smoke Detector",
             "url": "https://en.wikipedia.org/wiki/Smoke_detector"},
        ],
    },
    {
        "title": "Doorbell Circuit",
        "type": "circuit_generation",
        "description": "A simple electronic doorbell using a 555 timer to produce "
        "a two-tone sound when a push button is pressed.",
        "components": ["555 Timer IC", "Push button", "Piezoelectric buzzer",
                       "Resistor 10k\u2126 (2x)", "Capacitor 10\u00b5F",
                       "Capacitor 100nF", "Diode 1N4148", "9V Battery",
                       "Battery clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Place 555 on breadboard",
                         "Connect push button between VCC and pin 4 (RESET)",
                         "Wire 10k\u2126 from pin 7 to VCC",
                         "Wire 10k\u2126 from pin 7 to pin 6",
                         "Connect 10\u00b5F from pin 6 to GND",
                         "Connect 100nF from pin 5 to GND",
                         "Connect buzzer positive to pin 3 via diode, negative to GND",
                         "Power with 9V battery"],
        "explanation": "When the doorbell button is pressed, the 555 is enabled "
        "(RESET goes high) and oscillates at an audio frequency. "
        "Releasing the button stops the sound.",
        "circuit_diagram_description": "555 astable with push-button on RESET pin. "
        "Output drives buzzer through protection diode.",
        "sources": [
            {"name": "Wikipedia - Doorbell",
             "url": "https://en.wikipedia.org/wiki/Doorbell"},
            {"name": "Wikipedia - 555 Timer IC",
             "url": "https://en.wikipedia.org/wiki/555_timer_IC"},
        ],
    },
    {
        "title": "Mini Fan Circuit",
        "type": "circuit_generation",
        "description": "A simple DC motor driver circuit for a small hobby fan, "
        "controlled by a transistor switch.",
        "components": ["DC motor (3-6V, small hobby fan)", "Transistor BC547 (or TIP31)",
                       "Resistor 1k\u2126 (base)", "Diode 1N4001 (flyback)",
                       "Push button or switch", "9V Battery (or 4xAA)",
                       "Battery clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Place transistor on breadboard",
                         "Connect 1k\u2126 from switch to transistor base",
                         "Switch other terminal to VCC",
                         "Transistor emitter to GND",
                         "Connect flyback diode across motor terminals "
                         "(cathode to VCC, anode to collector)",
                         "Connect motor between transistor collector and VCC",
                         "Power with battery",
                         "Press button to run fan"],
        "explanation": "The transistor acts as a switch. Base current from the push "
        "button saturates the transistor, allowing motor current through the collector. "
        "The flyback diode protects the transistor from voltage spikes when the motor "
        "turns off.",
        "circuit_diagram_description": "Transistor switching DC motor. "
        "Base driven via resistor and switch. Flyback diode across motor.",
        "sources": [
            {"name": "Wikipedia - DC Motor",
             "url": "https://en.wikipedia.org/wiki/DC_motor"},
        ],
    },
    {
        "title": "Temperature Alarm Circuit",
        "type": "circuit_generation",
        "description": "An over-temperature alarm using an NTC thermistor that "
        "activates a buzzer when the ambient temperature rises above a set point.",
        "components": ["NTC Thermistor (10k\u2126)", "Resistor 10k\u2126",
                       "Potentiometer 100k\u2126", "Transistor BC547 (2x)",
                       "Piezoelectric buzzer", "LED", "Resistor 220\u2126",
                       "9V Battery", "Battery clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Thermistor from VCC to junction node",
                         "10k\u2126 from junction node to GND",
                         "Potentiometer: one leg to VCC, wiper to junction",
                         "Junction to Q1 base",
                         "Q1 emitter to GND, collector via 10k\u2126 to VCC",
                         "Q1 collector to Q2 base",
                         "Q2 emitter to GND, collector to buzzer negative",
                         "Buzzer positive to VCC",
                         "Power with 9V battery"],
        "explanation": "The thermistor resistance drops with temperature. At the "
        "threshold set by the potentiometer, Q1 turns on, pulling its collector low, "
        "turning Q2 on and activating the buzzer.",
        "circuit_diagram_description": "Thermistor voltage divider driving "
        "two-stage transistor amplifier to buzzer.",
        "sources": [
            {"name": "Wikipedia - Thermistor",
             "url": "https://en.wikipedia.org/wiki/Thermistor"},
        ],
    },
    {
        "title": "Motion Detector Circuit (PIR)",
        "type": "circuit_generation",
        "description": "A passive infrared (PIR) motion detector circuit using a "
        "PIR sensor module to detect movement and trigger an alarm or light.",
        "components": ["PIR sensor module (HC-SR501)", "Transistor BC547",
                       "Relay 5V", "LED", "Resistor 220\u2126", "Resistor 1k\u2126",
                       "Diode 1N4001", "9V Battery", "Battery clip",
                       "Breadboard", "Jumper wires"],
        "wiring_steps": ["Connect PIR module VCC to VCC, GND to GND",
                         "PIR output (OUT) to Q1 base via 1k\u2126 resistor",
                         "Q1 base also has 10k\u2126 pull-down to GND",
                         "Q1 emitter to GND",
                         "Q1 collector drives relay coil negative",
                         "Relay coil positive to VCC with flyback diode across coil",
                         "LED with 220\u2126 from Q1 collector to VCC for indication",
                         "Power with 9V battery"],
        "explanation": "The PIR sensor detects infrared radiation changes from "
        "moving warm objects. Its output goes high, turning on Q1 which "
        "energizes the relay and lights the LED.",
        "circuit_diagram_description": "PIR sensor module output drives transistor. "
        "Transistor switches relay and indicator LED.",
        "sources": [
            {"name": "Wikipedia - Passive Infrared Sensor",
             "url": "https://en.wikipedia.org/wiki/Passive_infrared_sensor"},
        ],
    },
    {
        "title": "Gas Leakage Detector Circuit",
        "type": "circuit_generation",
        "description": "A gas sensor circuit using an MQ-2 or MQ-6 gas sensor "
        "that triggers an alarm when combustible gas is detected.",
        "components": ["Gas sensor module (MQ-2/MQ-6)", "Transistor BC547 (2x)",
                       "Piezoelectric buzzer", "LED", "Resistor 1k\u2126 (2x)",
                       "Resistor 220\u2126", "Potentiometer 10k\u2126",
                       "9V Battery", "Battery clip", "Breadcrumb", "Jumper wires"],
        "wiring_steps": ["Connect MQ sensor: VCC to 5V, GND to GND",
                         "Sensor analog out to potentiometer wiper",
                         "Potentiometer: one leg to VCC, other to GND",
                         "Wiper to Q1 base via 1k\u2126",
                         "Q1 emitter to GND, collector via 1k\u2126 to VCC",
                         "Q1 collector to Q2 base",
                         "Q2 emitter to GND, collector to buzzer negative",
                         "Buzzer positive to VCC",
                         "LED with 220\u2126 across buzzer",
                         "Power with 9V battery"],
        "explanation": "The MQ gas sensor's resistance changes with gas concentration. "
        "The potentiometer sets the threshold voltage. When gas exceeds the threshold, "
        "the comparator triggers the alarm buzzer.",
        "circuit_diagram_description": "Gas sensor with threshold potentiometer "
        "driving two-stage transistor amplifier to buzzer.",
        "sources": [
            {"name": "Wikipedia - Gas Detector",
             "url": "https://en.wikipedia.org/wiki/Gas_detector"},
        ],
    },
    {
        "title": "IR Sensor Circuit",
        "type": "circuit_generation",
        "description": "An infrared obstacle detection circuit using an IR LED and "
        "photodiode/phototransistor pair.",
        "components": ["IR LED", "Phototransistor (or IR receiver)",
                       "Transistor BC547", "Resistor 220\u2126", "Resistor 10k\u2126",
                       "LED (indicator)", "9V Battery", "Battery clip",
                       "Breadboard", "Jumper wires"],
        "wiring_steps": ["IR LED anode to VCC via 220\u2126, cathode to GND",
                         "Phototransistor collector to VCC via 10k\u2126",
                         "Phototransistor emitter to GND",
                         "Collector node to Q1 base",
                         "Q1 emitter to GND",
                         "Q1 collector to indicator LED anode via 220\u2126",
                         "Indicator LED cathode to VCC",
                         "Power with 9V battery"],
        "explanation": "The IR LED continuously emits infrared light. When an object "
        "reflects this IR back to the phototransistor, it conducts, pulling the "
        "collector node low and turning Q1 on. The indicator LED lights up.",
        "circuit_diagram_description": "IR LED emitter, phototransistor receiver, "
        "transistor amplifier, and indicator LED.",
        "sources": [
            {"name": "Wikipedia - Infrared Sensor",
             "url": "https://en.wikipedia.org/wiki/Infrared_sensor"},
        ],
    },
    {
        "title": "Ultrasonic Sensor Circuit (HC-SR04)",
        "type": "circuit_generation",
        "description": "Interface circuit for HC-SR04 ultrasonic distance sensor "
        "with LED range indication.",
        "components": ["HC-SR04 Ultrasonic Sensor", "Arduino Uno (or any MCU)",
                       "LED (3x, green/yellow/red)", "Resistor 220\u2126 (3x)",
                       "Breadboard", "Jumper wires (male-female)"],
        "wiring_steps": ["Connect HC-SR04 VCC to 5V, GND to GND",
                         "Trig pin to Arduino digital pin 9",
                         "Echo pin to Arduino digital pin 10",
                         "Green LED anode via 220\u2126 to pin 5",
                         "Yellow LED anode via 220\u2126 to pin 6",
                         "Red LED anode via 220\u2126 to pin 7",
                         "All LED cathodes to GND",
                         "Power Arduino via USB"],
        "explanation": "The HC-SR04 sends an ultrasonic pulse (40kHz) and measures "
        "the echo return time. Distance = time x speed of sound / 2. "
        "LEDs indicate proximity ranges: green for far, yellow for mid, red for near.",
        "circuit_diagram_description": "HC-SR04 connected to Arduino. "
        "Trig/Echo on pins 9/10. LEDs on pins 5,6,7 for range indication.",
        "sources": [
            {"name": "Wikipedia - Ultrasonic Sensor",
             "url": "https://en.wikipedia.org/wiki/Ultrasonic_sensor"},
            {"name": "Arduino Docs - Ultrasonic Sensor",
             "url": "https://docs.arduino.cc/built-in-examples/sensors/Ping"},
        ],
    },
    {
        "title": "LDR Automatic Light Circuit",
        "type": "circuit_generation",
        "description": "An automatic dusk-to-dawn light that turns on an LED or bulb "
        "when ambient light falls below a threshold.",
        "components": ["LDR", "Resistor 10k\u2126", "Potentiometer 100k\u2126",
                       "Transistor BC547", "Relay 5V (for AC bulb) or LED",
                       "Diode 1N4001", "9V Battery", "Battery clip",
                       "Breadboard", "Jumper wires"],
        "wiring_steps": ["LDR from VCC to junction node",
                         "10k\u2126 from junction node to GND",
                         "Potentiometer wiper to junction node",
                         "Junction node to Q1 base",
                         "Q1 emitter to GND",
                         "Q1 collector to relay coil negative",
                         "Relay coil positive to VCC",
                         "Flyback diode across relay coil",
                         "Power with 9V battery"],
        "explanation": "At dusk, LDR resistance increases, raising base voltage "
        "of Q1. When sufficient, Q1 turns on, energizing the relay which "
        "switches the external light.",
        "circuit_diagram_description": "LDR voltage divider driving transistor "
        "that switches a relay for an external light.",
        "sources": [
            {"name": "Wikipedia - Photoresistor",
             "url": "https://en.wikipedia.org/wiki/Photoresistor"},
            {"name": "Wikipedia - Automatic Light",
             "url": "https://en.wikipedia.org/wiki/Automatic_light"},
        ],
    },
    {
        "title": "PIR Motion Sensor Light",
        "type": "circuit_generation",
        "description": "A PIR-based motion-activated light that turns on when "
        "movement is detected, with adjustable timer.",
        "components": ["PIR sensor (HC-SR501)", "Relay 5V", "LED or bulb (load)",
                       "Transistor BC547", "Resistor 1k\u2126", "Resistor 10k\u2126",
                       "Diode 1N4001", "Capacitor 100\u00b5F (timer)", "9V Battery",
                       "Battery clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Connect PIR sensor VCC to VCC, GND to GND",
                         "PIR OUT pin to Q1 base via 1k\u2126",
                         "10k\u2126 pull-down from Q1 base to GND",
                         "Q1 emitter to GND",
                         "Q1 collector to relay coil negative side",
                         "Relay coil positive to VCC",
                         "Flyback diode across relay coil",
                         "100\u00b5F from Q1 base to GND (holds output for timer)",
                         "Power with 9V battery"],
        "explanation": "When the PIR detects motion, its output goes high, "
        "turning Q1 on which energizes the relay. The capacitor keeps the "
        "relay engaged for a short period after motion stops.",
        "circuit_diagram_description": "PIR sensor drives transistor switch for relay. "
        "Capacitor provides delay-off timer.",
        "sources": [
            {"name": "Wikipedia - Passive Infrared Sensor",
             "url": "https://en.wikipedia.org/wiki/Passive_infrared_sensor"},
        ],
    },
    {
        "title": "Flame Sensor Circuit",
        "type": "circuit_generation",
        "description": "An IR flame detection circuit using a photodiode sensitive "
        "to the infrared wavelengths emitted by fire.",
        "components": ["IR photodiode (flame sensor)", "Transistor BC547",
                       "Resistor 10k\u2126 (2x)", "Resistor 220\u2126",
                       "LED (alarm indicator)", "Piezoelectric buzzer (optional)",
                       "Potentiometer 100k\u2126", "9V Battery",
                       "Battery clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Connect IR photodiode cathode to VCC, anode to junction",
                         "10k\u2126 from junction to GND (reverse bias)",
                         "Junction to positive input of comparator or Q1 base",
                         "Q1 emitter to GND",
                         "Q1 collector to LED via 220\u2126 to VCC",
                         "Potentiometer from VCC to GND, wiper to Q1 base",
                         "Adjust for sensitivity",
                         "Power with 9V battery"],
        "explanation": "The IR photodiode conducts when exposed to infrared "
        "radiation from a flame. The transistor amplifies this signal to "
        "illuminate the indicator LED and trigger the buzzer.",
        "circuit_diagram_description": "Reverse-biased IR photodiode feeds "
        "transistor amplifier. Potentiometer sets sensitivity threshold.",
        "sources": [
            {"name": "Wikipedia - Flame Detector",
             "url": "https://en.wikipedia.org/wiki/Flame_detector"},
        ],
    },
    {
        "title": "Humidity Sensor Circuit",
        "type": "circuit_generation",
        "description": "A humidity sensing circuit using a resistive humidity sensor "
        "with LED indication for dry, comfortable, and wet conditions.",
        "components": ["Resistive humidity sensor (HR202 or similar)",
                       "Transistor BC547 (3x)", "LED (3x: blue, green, red)",
                       "Resistor 10k\u2126 (3x)", "Resistor 220\u2126 (3x)",
                       "Potentiometer 100k\u2126 (2x)", "9V Battery",
                       "Battery clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Connect humidity sensor between VCC and junction node",
                         "10k\u2126 from junction node to GND",
                         "Junction to comparators or three transistor bases via thresholds",
                         "Each transistor stage has separate threshold potentiometer",
                         "Transistor emitters all to GND",
                         "Each collector drives its respective LED through 220\u2126 to VCC",
                         "Power with 9V battery"],
        "explanation": "The humidity sensor's resistance changes with relative humidity. "
        "Multiple transistor stages with different thresholds light LEDs indicating "
        "dry (blue), comfortable (green), or wet (red) conditions.",
        "circuit_diagram_description": "Humidity sensor voltage divider feeding "
        "three transistor threshold stages with indicator LEDs.",
        "sources": [
            {"name": "Wikipedia - Humidity Sensor",
             "url": "https://en.wikipedia.org/wiki/Humidity_sensor"},
        ],
    },
    {
        "title": "Soil Moisture Sensor Circuit",
        "type": "circuit_generation",
        "description": "A soil moisture detection circuit that indicates whether "
        "plants need watering using probe electrodes and an LED indicator.",
        "components": ["Copper probe electrodes (2x)", "Transistor BC547 (2x)",
                       "LED (red: dry, green: wet)", "Resistor 220\u2126 (2x)",
                       "Resistor 10k\u2126", "Resistor 1M\u2126",
                       "9V Battery", "Battery clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Insert two copper probes into soil",
                         "Probe 1 to VCC via 1M\u2126 resistor (current limit)",
                         "Probe 2 to Q1 base",
                         "10k\u2126 from Q1 base to GND (pull-down)",
                         "Q1 emitter to GND, collector to VCC via 10k\u2126",
                         "Q1 collector to Q2 base",
                         "Q2 emitter to GND",
                         "Green LED via 220\u2126 from Q2 collector to VCC",
                         "Red LED via 220\u2126 from Q1 collector to VCC (inverted)",
                         "Power with 9V battery"],
        "explanation": "Moist soil conducts weakly between the probes, providing "
        "base current to Q1. When wet, Q1 turns on, lighting green LED. Red LED "
        "lights when dry (Q1 off).",
        "circuit_diagram_description": "Probe electrodes in soil form a resistive "
        "divider. Two transistors drive complementary wet/dry LEDs.",
        "sources": [
            {"name": "Wikipedia - Soil Moisture Sensor",
             "url": "https://en.wikipedia.org/wiki/Soil_moisture_sensor"},
        ],
    },
    {
        "title": "Sound Sensor Circuit",
        "type": "circuit_generation",
        "description": "A sound detection circuit using an electret condenser "
        "microphone that lights an LED with sound intensity.",
        "components": ["Electret condenser microphone", "Transistor BC547 (2x)",
                       "Resistor 10k\u2126 (2x)", "Resistor 100k\u2126",
                       "Resistor 220\u2126", "Capacitor 10\u00b5F", "LED",
                       "9V Battery", "Battery clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Connect mic positive to VCC via 10k\u2126 (bias)",
                         "Mic negative to GND",
                         "Couple mic output through 10\u00b5F to Q1 base",
                         "Q1 base to GND via 100k\u2126",
                         "Q1 emitter to GND, collector via 10k\u2126 to VCC",
                         "Q1 output (collector) to Q2 base",
                         "Q2 emitter to GND",
                         "LED via 220\u2126 from Q2 collector to VCC",
                         "Power with 9V battery"],
        "explanation": "Sound waves vibrate the microphone diaphragm, generating "
        "a small AC signal. This is amplified by Q1 and further by Q2. "
        "Loud sounds saturate Q2, lighting the LED.",
        "circuit_diagram_description": "Electret microphone with bias resistor, "
        "AC-coupled into two-stage transistor amplifier driving LED.",
        "sources": [
            {"name": "Wikipedia - Microphone",
             "url": "https://en.wikipedia.org/wiki/Microphone"},
            {"name": "Wikipedia - Sound Sensor",
             "url": "https://en.wikipedia.org/wiki/Sound_sensor"},
        ],
    },
    {
        "title": "Voltage Regulator Circuit (7805)",
        "type": "circuit_generation",
        "description": "A fixed 5V voltage regulator circuit using a 7805 IC, "
        "essential for powering TTL logic and Arduino circuits.",
        "components": ["7805 Voltage Regulator IC", "Capacitor 100\u00b5F (input)",
                       "Capacitor 10\u00b5F (output)", "Capacitor 100nF (decoupling)",
                       "Diode 1N4001 (protection)", "Heat sink (for regulator)",
                       "9-12V DC input", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Place 7805 on breadboard (pin 1=IN, pin 2=GND, pin 3=OUT)",
                         "Connect 100\u00b5F electrolytic from pin 1 to GND (+ to IN)",
                         "Connect 10\u00b5F from pin 3 to GND (+ to OUT)",
                         "Connect 100nF ceramic from pin 3 to GND close to IC",
                         "Connect 1N4001 cathode to pin 1, anode to pin 2 "
                         "(reverse voltage protection)",
                         "Attach heat sink to 7805 tab",
                         "Apply 9-12V DC between pin 1 and GND",
                         "5V output available on pin 3"],
        "explanation": "The 7805 is a linear voltage regulator that maintains a fixed "
        "5V output regardless of input voltage (7-25V range) and load current (up to 1A). "
        "Input and output capacitors ensure stability and filter noise.",
        "circuit_diagram_description": "7805 with input/output filter capacitors. "
        "Protection diode on input. Heat sink recommended for >500mA loads.",
        "sources": [
            {"name": "Wikipedia - 7805",
             "url": "https://en.wikipedia.org/wiki/78xx"},
            {"name": "Wikipedia - Voltage Regulator",
             "url": "https://en.wikipedia.org/wiki/Voltage_regulator"},
        ],
    },
    {
        "title": "Relay Switching Circuit",
        "type": "circuit_generation",
        "description": "A transistor-driven relay circuit that allows a low-current "
        "signal to switch high-power AC or DC loads.",
        "components": ["Relay 5V (SPDT)", "Transistor BC547 (or TIP31 for more current)",
                       "Diode 1N4001 (flyback)", "Resistor 1k\u2126",
                       "LED (indicator)", "Resistor 220\u2126",
                       "Push button or logic input", "9V Battery",
                       "Battery clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Place relay on breadboard",
                         "Connect 1k\u2126 from input signal to Q1 base",
                         "Q1 emitter to GND",
                         "Connect relay coil between Q1 collector and VCC",
                         "Place flyback diode across relay coil "
                         "(cathode to VCC, anode to collector)",
                         "LED with 220\u2126 from Q1 collector to VCC (optional)",
                         "Connect NC/COM/NO terminals to load",
                         "Power relay coil with 5V and signal with 3.3-5V"],
        "explanation": "A small base current (a few mA) saturates Q1, allowing "
        "coil current (50-100mA for 5V relay) to flow. The relay's electromagnetic "
        "switch then controls high-power loads up to 250VAC/10A.",
        "circuit_diagram_description": "Transistor switch driving relay coil. "
        "Flyback diode across coil. Indicator LED on collector.",
        "sources": [
            {"name": "Wikipedia - Relay",
             "url": "https://en.wikipedia.org/wiki/Relay"},
        ],
    },
    {
        "title": "Traffic Light Circuit",
        "type": "circuit_generation",
        "description": "A traffic light simulation circuit using a 555 timer and "
        "4017 decade counter to sequence red, yellow, and green LEDs.",
        "components": ["555 Timer IC", "4017 Decade Counter IC",
                       "LED (red, yellow, green)", "Resistor 220\u2126 (3x)",
                       "Resistor 100k\u2126", "Capacitor 10\u00b5F",
                       "Capacitor 100nF", "9V Battery", "Battery clip",
                       "Breadboard", "Jumper wires"],
        "wiring_steps": ["Build 555 astable clock (as in LED blink circuit)",
                         "555 pin 3 (OUT) to 4017 pin 14 (CLOCK)",
                         "4017 pin 13 (CLOCK ENABLE) to GND",
                         "4017 pin 15 (RESET) to GND",
                         "4017 pin 3 (Q0) to red LED via 220\u2126 to GND",
                         "4017 pin 2 (Q1) to yellow LED via 220\u2126 to GND",
                         "4017 pin 4 (Q2) to green LED via 220\u2126 to GND",
                         "4017 pin 1 (Q5) to RESET via diode (back to pin 15)",
                         "Power both ICs from VCC and GND",
                         "Adjust 555 frequency for timing"],
        "explanation": "The 555 provides a clock signal to the 4017 decade counter, "
        "which sequentially activates its outputs. The red LED on Q0, yellow on Q1, "
        "green on Q2. When the counter reaches Q5, it resets, cycling the sequence.",
        "circuit_diagram_description": "555 astable clocks 4017 decade counter. "
        "First three outputs drive red, yellow, green LEDs. Reset on Q5.",
        "sources": [
            {"name": "Wikipedia - 4017 Counter",
             "url": "https://en.wikipedia.org/wiki/4017"},
            {"name": "Wikipedia - Traffic Light",
             "url": "https://en.wikipedia.org/wiki/Traffic_light"},
        ],
    },
    {
        "title": "Digital Counter Circuit",
        "type": "circuit_generation",
        "description": "A 0-9 digital counter using a 555 timer and 4017 decade counter "
        "with LED display output.",
        "components": ["555 Timer IC", "4017 Decade Counter",
                       "LED (10x)", "Resistor 220\u2126 (10x)",
                       "Resistor 100k\u2126", "Capacitor 10\u00b5F",
                       "Push button (manual clock)", "9V Battery",
                       "Battery clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Wire 555 as astable or use push button for manual clock",
                         "555 pin 3 or button output to 4017 pin 14",
                         "4017 pins 3,2,4,7,10,1,5,6,9,11 (Q0-Q9) to LEDs via 220\u2126",
                         "All LED cathodes to GND",
                         "4017 pin 13 to GND (enable)",
                         "4017 pin 15 to GND (reset)",
                         "Power both ICs",
                         "Press button or let 555 auto-advance"],
        "explanation": "Each clock pulse advances the 4017 counter by one. "
        "The ten outputs (Q0-Q9) light sequentially, providing a visual count "
        "from 0 to 9.",
        "circuit_diagram_description": "Clock source (555 or button) drives 4017 "
        "counter. Ten output LEDs show current count.",
        "sources": [
            {"name": "Wikipedia - 4017",
             "url": "https://en.wikipedia.org/wiki/4017"},
            {"name": "Wikipedia - Counter",
             "url": "https://en.wikipedia.org/wiki/Counter_(digital)"},
        ],
    },
    {
        "title": "Frequency Generator Circuit (555)",
        "type": "circuit_generation",
        "description": "A variable frequency square wave generator using a 555 timer "
        "with adjustable duty cycle and frequency.",
        "components": ["555 Timer IC", "Resistor 10k\u2126 (2x)",
                       "Potentiometer 100k\u2126 (frequency adj)",
                       "Capacitor 10\u00b5F", "Capacitor 100nF",
                       "LED (output indicator)", "Resistor 220\u2126",
                       "9V Battery", "Battery clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Place 555 on breadboard",
                         "Pin 8 and pin 4 to VCC",
                         "Pin 1 to GND",
                         "10k\u2126 from pin 7 to VCC",
                         "Potentiometer between pin 7 and pin 6",
                         "10\u00b5F from pin 6 to GND",
                         "100nF from pin 5 to GND",
                         "Output on pin 3 drives LED via 220\u2126",
                         "Vary pot to change frequency"],
        "explanation": "This is an astable multivibrator where the charging resistor "
        "is varied by the potentiometer. The frequency range depends on the RC "
        "time constant. f = 1.44 / (R1 + 2*R2) * C.",
        "circuit_diagram_description": "555 astable with potentiometer replacing "
        "standard resistors for variable frequency output.",
        "sources": [
            {"name": "Wikipedia - 555 Timer IC",
             "url": "https://en.wikipedia.org/wiki/555_timer_IC"},
            {"name": "Electronics Tutorials - 555",
             "url": "https://www.electronics-tutorials.ws/waveforms/555_oscillator.html"},
        ],
    },
    {
        "title": "555 Timer Basics",
        "type": "circuit_generation",
        "description": "Fundamental 555 timer circuits in three configurations: "
        "monostable (one-shot), astable (oscillator), and bistable (flip-flop).",
        "components": ["555 Timer IC", "Resistor 100k\u2126", "Resistor 10k\u2126",
                       "Resistor 220\u2126", "Capacitor 10\u00b5F",
                       "Capacitor 100nF", "Push button (2x)", "LED",
                       "9V Battery", "Battery clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Monostable: pin 2 triggers low, output high for R*C seconds",
                         "Astable: pin 2+6 connected, cap charges through R1+R2",
                         "Bistable: pin 2 SET, pin 4 RESET (no timing components)",
                         "Common: pin 8 to VCC, pin 1 to GND",
                         "Output pin 3 drives LED through 220\u2126",
                         "Pin 5 decoupled with 100nF to GND"],
        "explanation": "The 555 timer contains two comparators, a voltage divider, "
        "and an RS flip-flop. In monostable mode, a trigger pulse produces a single "
        "output pulse. Astable mode produces a continuous square wave. Bistable mode "
        "acts as a set/reset latch.\n\n"
        "Monostable pulse width: T = 1.1 * R * C\n"
        "Astable frequency: f = 1.44 / ((R1 + 2*R2) * C1)",
        "circuit_diagram_description": "Three classic 555 configurations "
        "(monostable, astable, bistable) with common power and output stages.",
        "sources": [
            {"name": "Wikipedia - 555 Timer IC",
             "url": "https://en.wikipedia.org/wiki/555_timer_IC"},
            {"name": "Electronics Tutorials - 555",
             "url": "https://www.electronics-tutorials.ws/waveforms/555_oscillator.html"},
        ],
    },
    {
        "title": "LED Chaser Circuit",
        "type": "circuit_generation",
        "description": "A classic LED chaser (Knight Rider style) using a 555 timer "
        "and 4017 decade counter to sequentially light LEDs in a running pattern.",
        "components": ["555 Timer IC", "4017 Decade Counter IC",
                       "LED (10x, same colour)", "Resistor 220\u2126 (10x)",
                       "Resistor 100k\u2126", "Capacitor 10\u00b5F",
                       "Capacitor 100nF", "9V Battery", "Battery clip",
                       "Breadboard", "Jumper wires"],
        "wiring_steps": ["Build 555 astable on breadboard",
                         "555 pin 3 to 4017 pin 14 (clock input)",
                         "4017 pin 13 to GND (enable low)",
                         "4017 pin 15 to GND (reset)",
                         "Connect each 4017 output pin through 220\u2126 to its LED",
                         "All LED cathodes to GND",
                         "Connect VCC to pin 8 of 555 and pin 16 of 4017",
                         "Connect GND to pin 1 of 555 and pin 8 of 4017",
                         "Power with 9V battery"],
        "explanation": "The 555 generates a clock signal. The 4017 decade counter "
        "advances one step per clock pulse, lighting LEDs in sequence Q0 through Q9. "
        "Speed is controlled by the 555's RC timing network.",
        "circuit_diagram_description": "555 astable clocks 4017 decade counter. "
        "Each of the 10 outputs drives an LED through a current-limiting resistor.",
        "sources": [
            {"name": "Wikipedia - 4017",
             "url": "https://en.wikipedia.org/wiki/4017"},
            {"name": "Wikipedia - LED Chaser",
             "url": "https://en.wikipedia.org/wiki/LED_chaser"},
        ],
    },
    {
        "title": "Police Light Circuit",
        "type": "circuit_generation",
        "description": "An alternating flasher circuit that simulates police "
        "emergency lights using a 555 timer and flip-flop.",
        "components": ["555 Timer IC", "4017 Decade Counter (or 7473 JK FF)",
                       "LED (red, blue, 2x each)", "Resistor 220\u2126 (4x)",
                       "Resistor 100k\u2126", "Capacitor 10\u00b5F",
                       "Capacitor 100nF", "9V Battery", "Battery clip",
                       "Breadboard", "Jumper wires"],
        "wiring_steps": ["Build 555 astable for base timing (approx 1-2Hz)",
                         "555 output drives a J-K flip-flop in toggle mode",
                         "Flip-flop Q output drives red LED pair (alternating)",
                         "Flip-flop not-Q output drives blue LED pair",
                         "Each LED has its own 220\u2126 current limit resistor",
                         "Power all ICs from VCC and GND",
                         "Power with 9V battery"],
        "explanation": "The 555 produces a fast clock that drives a flip-flop "
        "which divides the frequency by 2. The Q and not-Q outputs alternately "
        "light the red and blue LED pairs, creating the police-light effect.",
        "circuit_diagram_description": "555 clock divided by flip-flop. "
        "Red LEDs on Q, blue LEDs on not-Q, alternating at half clock rate.",
        "sources": [
            {"name": "Wikipedia - Flip-flop",
             "url": "https://en.wikipedia.org/wiki/Flip-flop_(electronics)"},
        ],
    },
    {
        "title": "Emergency Light Circuit",
        "type": "circuit_generation",
        "description": "An automatic emergency light that turns on a high-brightness "
        "LED when mains power fails, using a relay and battery backup.",
        "components": ["Relay 5V (SPDT)", "Transistor BC547",
                       "High-brightness white LED (3x)", "Resistor 10\u2126 (3x)",
                       "Diode 1N4001 (2x)", "Capacitor 1000\u00b5F (filter)",
                       "9V rechargeable battery", "9V DC adapter (input)",
                       "Breadboard", "Jumper wires"],
        "wiring_steps": ["Connect 9V DC adapter to relay coil via protection diode",
                         "Relay COM terminal to battery positive",
                         "Relay NC terminal to LED anodes through 10\u2126 resistors",
                         "All LED cathodes to GND",
                         "Capacitor across battery terminals for filtering",
                         "Battery negative to GND",
                         "When mains is present, relay is energized (NC open)",
                         "On power failure, relay closes, connecting battery to LEDs"],
        "explanation": "During normal operation, the relay is energized by the mains "
        "adapter, keeping the battery disconnected. On power failure, the relay "
        "de-energizes, connecting the battery to the LEDs automatically.",
        "circuit_diagram_description": "Relay controlled by mains adapter. "
        "NC contacts connect battery to LEDs on power failure.",
        "sources": [
            {"name": "Wikipedia - Emergency Light",
             "url": "https://en.wikipedia.org/wiki/Emergency_light"},
        ],
    },
    {
        "title": "Mobile Charger Indicator Circuit",
        "type": "circuit_generation",
        "description": "An LED indicator circuit that shows when a mobile phone "
        "charger is actively charging a battery.",
        "components": ["Transistor BC547", "LED (red for charging, green for full)",
                       "Resistor 220\u2126 (2x)", "Resistor 10k\u2126 (2x)",
                       "Zener diode 4.7V", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Connect charger positive to circuit input",
                         "Zener diode cathode to input, anode to GND (regulation)",
                         "Red LED via 220\u2126 from input to collector of Q1",
                         "Q1 base to charging current sense resistor",
                         "Green LED via 220\u2126 from charger output to Q2 collector",
                         "Q2 base detects full voltage via voltage divider",
                         "Q1 and Q2 emitters to GND",
                         "Circuit input from USB charger (5V)"],
        "explanation": "During charging, current flow is detected, biasing Q1 to "
        "light the red LED. When the battery reaches full voltage (4.2V), Q2 "
        "turns on, lighting the green LED. The zener diode provides over-voltage protection.",
        "circuit_diagram_description": "Dual-transistor charge status indicator. "
        "Red LED for charging, green LED for full. Zener regulation.",
        "sources": [
            {"name": "Wikipedia - Battery Charger",
             "url": "https://en.wikipedia.org/wiki/Battery_charger"},
        ],
    },
    {
        "title": "Battery Charging Indicator Circuit",
        "type": "circuit_generation",
        "description": "A multi-stage battery charging indicator using an LM3914 "
        "or discrete LEDs to show charging progress.",
        "components": ["LM3914 Dot/Bar Display Driver", "LED (10x)",
                       "Resistor 1k\u2126", "Resistor 10k\u2126",
                       "Potentiometer 10k\u2126", "Capacitor 10\u00b5F",
                       "Diode 1N4001", "Battery under charge",
                       "Charging source", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Connect LM3914: pin 2,4 to GND; pin 3 to VCC via 1k\u2126",
                         "Battery voltage through voltage divider to pin 5",
                         "Potentiometer from pin 6 to pin 7, wiper to pin 8",
                         "10 \u00b5F from pin 2 to pin 3",
                         "LEDs from pins 1,10-18 through 220\u2126 each to GND",
                         "Connect battery under charge to input",
                         "Power LM3914 from charging source"],
        "explanation": "The LM3914 senses battery voltage and lights LEDs "
        "proportionally, giving a real-time charge level display. "
        "Each LED represents approximately 1/10 of the full charge range.",
        "circuit_diagram_description": "LM3914 bar graph driver with battery "
        "voltage input and 10-LED charge level display.",
        "sources": [
            {"name": "Wikipedia - LM3914",
             "url": "https://en.wikipedia.org/wiki/LM3914"},
        ],
    },
    {
        "title": "Power Supply Circuit (5V/12V)",
        "type": "circuit_generation",
        "description": "A regulated dual-output power supply providing stable "
        "5V and 12V DC from a transformer input.",
        "components": ["Step-down transformer (230V to 15V AC)",
                       "Bridge rectifier (4x 1N4001 diodes)",
                       "Capacitor 2200\u00b5F (filter)",
                       "7805 Voltage Regulator (5V)",
                       "7812 Voltage Regulator (12V)",
                       "Capacitor 100\u00b5F (output, 2x)",
                       "Capacitor 100nF (decoupling, 2x)",
                       "Fuse 1A", "Power switch", "Breadboard/PCB",
                       "Screw terminals", "Jumper wires"],
        "wiring_steps": ["Connect transformer secondary to bridge rectifier AC inputs",
                         "Bridge rectifier (+) to 2200\u00b5F positive, (-) to GND",
                         "Filtered DC to input of 7805 (pin 1) and 7812 (pin 1)",
                         "7805 pin 2 (GND) to common GND",
                         "7812 pin 2 (GND) to common GND",
                         "100\u00b5F from each regulator output to GND",
                         "100nF ceramic close to each regulator output",
                         "Fuse on transformer primary winding",
                         "Output terminals for 5V and 12V"],
        "explanation": "The transformer steps down AC mains voltage. The bridge "
        "rectifier converts AC to pulsating DC. The filter capacitor smooths the "
        "ripple. The 7805 and 7812 linear regulators provide stable 5V and 12V "
        "outputs, each capable of 1A with proper heat sinking.",
        "circuit_diagram_description": "Transformer -> bridge rectifier -> "
        "filter capacitor -> dual voltage regulators (7805, 7812) -> output terminals.",
        "sources": [
            {"name": "Wikipedia - Power Supply",
             "url": "https://en.wikipedia.org/wiki/Power_supply"},
            {"name": "Wikipedia - 78xx",
             "url": "https://en.wikipedia.org/wiki/78xx"},
        ],
    },
    {
        "title": "Arduino LED Blink",
        "type": "circuit_generation",
        "description": "The classic Arduino starter project: blinking an LED on and "
        "off using a digital output pin.",
        "components": ["Arduino Uno (or any board)", "LED", "Resistor 220\u2126",
                       "Breadboard", "Jumper wires (male-male, male-female)"],
        "wiring_steps": ["Connect Arduino GND to breadboard negative rail",
                         "Connect Arduino 5V to breadboard positive rail",
                         "Place LED on breadboard (anode to positive side)",
                         "Connect 220\u2126 from Arduino digital pin 13 to LED anode",
                         "Connect LED cathode to GND",
                         "Upload Blink sketch from Arduino IDE"],
        "explanation": "The Arduino digital pin 13 has a built-in resistor for LED, "
        "but an external resistor is good practice. The Blink sketch sets pin 13 HIGH, "
        "waits 1 second, sets LOW, waits 1 second.",
        "circuit_diagram_description": "Arduino pin 13 -> 220\u2126 -> LED anode -> "
        "LED cathode -> GND.",
        "sources": [
            {"name": "Arduino Docs - Blink",
             "url": "https://docs.arduino.cc/built-in-examples/basics/Blink"},
            {"name": "Wikipedia - Arduino",
             "url": "https://en.wikipedia.org/wiki/Arduino"},
        ],
    },
    {
        "title": "Arduino Traffic Light",
        "type": "circuit_generation",
        "description": "An Arduino-based traffic light controller with red, yellow, "
        "and green LEDs simulating a road traffic signal.",
        "components": ["Arduino Uno", "LED (red, yellow, green)", "Resistor 220\u2126 (3x)",
                       "Breadboard", "Jumper wires"],
        "wiring_steps": ["Connect red LED anode via 220\u2126 to pin 13, cathode to GND",
                         "Connect yellow LED anode via 220\u2126 to pin 12, cathode to GND",
                         "Connect green LED anode via 220\u2126 to pin 11, cathode to GND",
                         "Upload traffic light code from Arduino IDE or write custom",
                         "Power Arduino via USB"],
        "explanation": "The Arduino sequentially activates each LED: green (5s), "
        "yellow (2s), red (5s), simulating a traffic light cycle. "
        "Timing is controlled via delay() or millis() functions.",
        "circuit_diagram_description": "Three LEDs on pins 13, 12, 11 with "
        "current-limiting resistors. Common GND.",
        "sources": [
            {"name": "Arduino Docs - Traffic Light",
             "url": "https://docs.arduino.cc/built-in-examples/digital/BlinkWithoutDelay"},
            {"name": "Wikipedia - Traffic Light",
             "url": "https://en.wikipedia.org/wiki/Traffic_light"},
        ],
    },
    {
        "title": "Arduino Temperature Monitor",
        "type": "circuit_generation",
        "description": "An Arduino temperature monitoring system using an LM35 "
        "or DHT11 sensor with serial output and LED alerts.",
        "components": ["Arduino Uno", "LM35 Temperature Sensor (or DHT11)",
                       "LED (red, blue)", "Resistor 220\u2126 (2x)",
                       "Breadboard", "Jumper wires"],
        "wiring_steps": ["Connect LM35 VCC to 5V, GND to GND",
                         "LM35 VOUT to Arduino analog pin A0",
                         "Blue LED via 220\u2126 to pin 9 (cold indicator)",
                         "Red LED via 220\u2126 to pin 10 (hot indicator)",
                         "Upload temperature monitoring sketch",
                         "Open serial monitor to view temperature"],
        "explanation": "The LM35 outputs 10mV per degree Celsius. Arduino reads "
        "the analog voltage and converts to temperature. Blue LED lights below "
        "20\u00b0C, red LED above 30\u00b0C.",
        "circuit_diagram_description": "LM35 analog output to A0. "
        "Alert LEDs on pins 9 and 10. Serial output for temperature display.",
        "sources": [
            {"name": "Arduino Docs - Temperature Sensor",
             "url": "https://docs.arduino.cc/built-in-examples/sensors/Temperature"},
            {"name": "Wikipedia - LM35",
             "url": "https://en.wikipedia.org/wiki/LM35"},
        ],
    },
    {
        "title": "Arduino Ultrasonic Distance Meter",
        "type": "circuit_generation",
        "description": "An Arduino HC-SR04 ultrasonic distance meter that measures "
        "distance and displays on the serial monitor with LED range indicators.",
        "components": ["Arduino Uno", "HC-SR04 Ultrasonic Sensor",
                       "LED (3x)", "Resistor 220\u2126 (3x)",
                       "16x2 LCD display (optional)", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Connect HC-SR04 VCC to 5V, GND to GND",
                         "Trig to digital pin 9, Echo to digital pin 10",
                         "Green LED via 220\u2126 to pin 5 (>50cm)",
                         "Yellow LED via 220\u2126 to pin 6 (20-50cm)",
                         "Red LED via 220\u2126 to pin 7 (<20cm)",
                         "Upload ultrasonic distance sketch",
                         "View measurements on serial monitor"],
        "explanation": "The HC-SR04 emits a 40kHz ultrasonic pulse and measures "
        "the echo return time. Distance (cm) = (pulse duration in \u00b5s) / 58. "
        "LEDs indicate proximity zones.",
        "circuit_diagram_description": "HC-SR04 connected to Arduino pins 9/10. "
        "Three LEDs on pins 5/6/7 for range indication.",
        "sources": [
            {"name": "Arduino Docs - Ultrasonic Sensor",
             "url": "https://docs.arduino.cc/built-in-examples/sensors/Ping"},
            {"name": "Wikipedia - Ultrasonic Sensor",
             "url": "https://en.wikipedia.org/wiki/Ultrasonic_sensor"},
        ],
    },
    {
        "title": "Arduino Smart Light",
        "type": "circuit_generation",
        "description": "An Arduino-based automatic lighting system using an LDR "
        "to control an LED or relay based on ambient light level.",
        "components": ["Arduino Uno", "LDR", "Resistor 10k\u2126",
                       "LED or Relay module", "Resistor 220\u2126 (if LED)",
                       "Breadboard", "Jumper wires"],
        "wiring_steps": ["Connect LDR from 5V to analog pin A0",
                         "Connect 10k\u2126 from A0 to GND (voltage divider)",
                         "Connect LED via 220\u2126 to pin 9",
                         "Or connect relay module signal to pin 9",
                         "Upload smart light sketch",
                         "Adjust threshold in code for desired light level"],
        "explanation": "The LDR and 10k\u2126 resistor form a voltage divider read "
        "by the Arduino ADC. When the light level drops below the threshold, "
        "the Arduino turns on the LED or relay.",
        "circuit_diagram_description": "LDR voltage divider on A0. "
        "Output control on pin 9 driving LED or relay module.",
        "sources": [
            {"name": "Arduino Docs - Light Sensor",
             "url": "https://docs.arduino.cc/built-in-examples/sensors/Photoresistor"},
            {"name": "Wikipedia - LDR",
             "url": "https://en.wikipedia.org/wiki/Photoresistor"},
        ],
    },
    {
        "title": "Bluetooth Controlled LED (HC-05)",
        "type": "circuit_generation",
        "description": "An Arduino project using an HC-05 Bluetooth module to "
        "control an LED wirelessly from a smartphone.",
        "components": ["Arduino Uno", "HC-05 Bluetooth Module",
                       "LED", "Resistor 220\u2126",
                       "Resistor 1k\u2126 (2x, voltage divider for RX)",
                       "Breadboard", "Jumper wires", "Smartphone with BT terminal app"],
        "wiring_steps": ["Connect HC-05 VCC to 5V, GND to GND",
                         "HC-05 TX to Arduino RX (pin 0)",
                         "HC-05 RX to Arduino TX (pin 1) via voltage divider "
                         "(1k\u2126 from TX to HC-05 RX, 1k\u2126 from HC-05 RX to GND)",
                         "LED via 220\u2126 on pin 13",
                         "Upload Bluetooth control sketch",
                         "Pair with HC-05 (default pass: 1234)",
                         "Send '1' to turn LED on, '0' to off"],
        "explanation": "The HC-05 communicates over serial UART. The Arduino reads "
        "characters from the Bluetooth serial connection and controls the LED "
        "accordingly. The voltage divider on RX is needed to drop Arduino 5V TX "
        "to HC-05's 3.3V logic level.",
        "circuit_diagram_description": "HC-05 connected to Arduino serial pins "
        "with voltage divider on RX. LED on pin 13.",
        "sources": [
            {"name": "Wikipedia - Bluetooth",
             "url": "https://en.wikipedia.org/wiki/Bluetooth"},
            {"name": "Arduino Docs - HC-05",
             "url": "https://docs.arduino.cc/retired/hc-05-bluetooth"},
        ],
    },
    {
        "title": "Smart Irrigation System",
        "type": "circuit_generation",
        "description": "An Arduino-based automatic plant watering system using a "
        "soil moisture sensor and relay-controlled water pump.",
        "components": ["Arduino Uno", "Soil moisture sensor (YL-69)",
                       "Relay module 5V", "Water pump (DC, 5V)",
                       "LED (green, red)", "Resistor 220\u2126 (2x)",
                       "Power supply for pump", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Connect YL-69 VCC to 5V, GND to GND, A0 to Arduino A0",
                         "Relay module signal to Arduino pin 7",
                         "Relay VCC to 5V, GND to GND",
                         "Water pump via relay COM/NO terminals",
                         "Green LED via 220\u2126 to pin 8 (watering active)",
                         "Red LED via 220\u2126 to pin 9 (soil dry alert)",
                         "Upload irrigation sketch",
                         "Power Arduino and pump separately"],
        "explanation": "The soil moisture sensor reads soil conductivity. When dry "
        "(below threshold), Arduino activates the relay to run the pump. "
        "The green LED indicates watering, red LED indicates dry soil needing attention.",
        "circuit_diagram_description": "Moisture sensor on A0. Relay + pump on pin 7. "
        "Status LEDs on pins 8 and 9.",
        "sources": [
            {"name": "Wikipedia - Irrigation",
             "url": "https://en.wikipedia.org/wiki/Irrigation"},
            {"name": "Wikipedia - Soil Moisture Sensor",
             "url": "https://en.wikipedia.org/wiki/Soil_moisture_sensor"},
        ],
    },
    {
        "title": "Home Automation (Relay Control)",
        "type": "circuit_generation",
        "description": "An Arduino-based home automation system using relays to "
        "control home appliances through serial commands.",
        "components": ["Arduino Uno", "Relay module 4-channel 5V",
                       "Push button (4x, manual override)",
                       "LED (4x, status indicators)", "Resistor 220\u2126 (4x)",
                       "9V power supply for relay module", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Connect relay module: IN1-IN4 to pins 6,7,8,9",
                         "Relay VCC to 5V, GND to GND",
                         "Push buttons to pins 2,3,4,5 with pull-down resistors",
                         "Status LEDs via 220\u2126 to pins 10,11,12,13",
                         "Connect appliances to relay COM/NO terminals",
                         "Upload home automation sketch",
                         "Control via serial commands or buttons"],
        "explanation": "The Arduino reads serial commands (e.g., '1 ON', '2 OFF') "
        "and button presses to toggle relays. Each relay controls a home appliance. "
        "Status LEDs show which relays are active.",
        "circuit_diagram_description": "Four relay channels driven from pins 6-9. "
        "Manual override buttons on pins 2-5. Status LEDs on pins 10-13.",
        "sources": [
            {"name": "Wikipedia - Home Automation",
             "url": "https://en.wikipedia.org/wiki/Home_automation"},
            {"name": "Arduino Docs - Relay Control",
             "url": "https://docs.arduino.cc/learn/electronics/relay"},
        ],
    },
    {
        "title": "Smart Parking Sensor",
        "type": "circuit_generation",
        "description": "An ultrasonic parking sensor with distance display "
        "and audible/visual alerts, simulating car reverse parking assist.",
        "components": ["Arduino Uno", "HC-SR04 Ultrasonic Sensor",
                       "Piezoelectric buzzer", "LED (green, yellow, red)",
                       "Resistor 220\u2126 (3x)", "16x2 LCD with I2C (optional)",
                       "Breadboard", "Jumper wires"],
        "wiring_steps": ["Connect HC-SR04: VCC to 5V, GND to GND, Trig to pin 9, "
                         "Echo to pin 10",
                         "Buzzer positive to pin 5, negative to GND",
                         "Green LED via 220\u2126 to pin 6 (>100cm)",
                         "Yellow LED via 220\u2126 to pin 7 (50-100cm)",
                         "Red LED via 220\u2126 to pin 8 (<50cm)",
                         "Upload parking sensor sketch",
                         "Serial monitor shows distance"],
        "explanation": "The ultrasonic sensor measures distance continuously. "
        "Green LED for safe (>100cm), yellow for caution (50-100cm), "
        "red for stop (<50cm). The buzzer beeps faster as distance decreases, "
        "simulating a reversing parking sensor.",
        "circuit_diagram_description": "HC-SR04 on pins 9/10. Three range LEDs on "
        "pins 6/7/8. Buzzer on pin 5 for variable beep rate.",
        "sources": [
            {"name": "Wikipedia - Parking Sensor",
             "url": "https://en.wikipedia.org/wiki/Parking_sensor"},
            {"name": "Arduino Docs - Ultrasonic",
             "url": "https://docs.arduino.cc/built-in-examples/sensors/Ping"},
        ],
    },
    {
        "title": "Complete Beginner Electronics Project: LED Dice",
        "type": "circuit_generation",
        "description": "A complete beginner project: electronic dice using a 555 "
        "timer and 4017 counter that randomly selects an LED when a button is pressed.",
        "components": ["555 Timer IC", "4017 Decade Counter",
                       "LED (6x, or use 7 LEDs with proper mapping)",
                       "Resistor 100k\u2126", "Resistor 10k\u2126",
                       "Capacitor 10\u00b5F", "Capacitor 100nF",
                       "Push button", "Resistor 220\u2126 (6x)",
                       "9V Battery and clip", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Build 555 oscillator section (pins 1-8)",
                         "555 pin 3 to 4017 pin 14 (clock)",
                         "4017 pin 13 to GND, pin 15 to GND",
                         "Use diodes to map 4017 outputs to 6 dice face LEDs",
                         "Outputs: Q0,Q1 -> LED1, Q2,Q3 -> LED2, Q4,Q5 -> LED3, "
                         "Q6,Q7 -> LED4, Q8 -> LED5, Q9 -> LED6",
                         "Each LED through 220\u2126 to GND",
                         "Push button between VCC and 555 RESET (pin 4)",
                         "When button is released, 555 starts fast clock",
                         "Press button again to stop and show random value",
                         "Power with 9V battery"],
        "explanation": "When the push button is released, the 555 rapidly clocks "
        "the 4017 counter (thousands of times per second). Pressing the button "
        "resets the 555, stopping the count at a random position. "
        "The active LED shows a pseudo-random dice value (1-6).\n\n"
        "This project teaches: 555 operation, counter ICs, diode logic, "
        "breadboarding, and LED current limiting.",
        "circuit_diagram_description": "555 astable clocks 4017 decade counter. "
        "Six outputs drive dice face LEDs. Push button controls start/stop.",
        "sources": [
            {"name": "Wikipedia - 555 Timer IC",
             "url": "https://en.wikipedia.org/wiki/555_timer_IC"},
            {"name": "Wikipedia - Electronic Dice",
             "url": "https://en.wikipedia.org/wiki/Dice"},
            {"name": "SparkFun - Beginner Projects",
             "url": "https://learn.sparkfun.com/tutorials"},
        ],
    },
    {
        "title": "Simple Audio Amplifier using LM386",
        "type": "circuit_generation",
        "description": "Build a low-power audio amplifier using LM386 IC for small speakers and headphones.",
        "components": ["LM386 Audio Amplifier IC", "Resistor 10kΩ", "Capacitor 10µF (2x)", "Capacitor 100µF", "Capacitor 0.1µF", "Speaker 8Ω", "Potentiometer 10kΩ", "3.5mm Audio Jack", "9V Battery", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Connect LM386 pin 1 to pin 8 via 10µF capacitor for gain of 200", "Pin 2 and pin 4 to GND", "Pin 3 to audio input via 10µF capacitor and 10kΩ potentiometer", "Pin 5 to 100µF capacitor positive leg, negative to speaker", "Pin 6 to 9V positive", "Pin 7 to GND via 0.1µF capacitor", "Add 10kΩ resistor from pin 3 to GND"],
        "explanation": "The LM386 is a low-voltage audio amplifier with fixed gain of 20 (or 200 with pin 1-8 capacitor). The input signal is AC-coupled through the capacitor while the potentiometer controls volume. The output drives an 8Ω speaker through a coupling capacitor that blocks DC.",
        "circuit_diagram_description": "simple audio amplifier using lm386 wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Passive Tone Control Circuit",
        "type": "circuit_generation",
        "description": "A simple bass and treble control circuit using RC filters for audio applications.",
        "components": ["Resistor 100kΩ (2x)", "Resistor 10kΩ (2x)", "Capacitor 0.1µF (2x)", "Capacitor 0.01µF", "Potentiometer 100kΩ (2x)", "Audio input jack", "Audio output jack", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Connect input signal to first 100kΩ resistor", "For bass control: 100kΩ pot with 0.1µF capacitor to GND", "For treble control: 10kΩ pot with 0.01µF capacitor in series", "Connect mid-point of bass pot to treble section through 100kΩ resistor", "Output from treble section through 10kΩ resistor", "Use shielded audio cables for input and output"],
        "explanation": "RC filter networks selectively attenuate or boost frequency ranges. The bass section uses a low-pass filter (100kΩ + 0.1µF, cutoff ~16Hz) while treble uses a high-pass filter (10kΩ + 0.01µF, cutoff ~1.6kHz).",
        "circuit_diagram_description": "passive tone control circuit wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Microphone Preamplifier Circuit",
        "type": "circuit_generation",
        "description": "Electret microphone preamplifier using transistor for clear voice pickup.",
        "components": ["Electret Microphone", "NPN Transistor BC547", "Resistor 10kΩ", "Resistor 100kΩ", "Resistor 2.2kΩ", "Capacitor 10µF (2x)", "Capacitor 100µF", "5V Power Supply", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Connect microphone positive to 5V through 10kΩ resistor", "Microphone output to BC547 base through 10µF capacitor", "BC547 collector to 5V through 2.2kΩ resistor", "BC547 emitter to GND", "100kΩ resistor from base to 5V (bias)", "Output from collector through 10µF capacitor", "100µF capacitor across power supply"],
        "explanation": "The electret microphone requires a bias voltage (provided by 10kΩ resistor). The BC547 transistor amplifies the small audio signal. The 100kΩ resistor sets the operating point. Output is AC-coupled for connection to audio amplifiers.",
        "circuit_diagram_description": "microphone preamplifier circuit wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Variable Voltage Power Supply using LM317",
        "type": "circuit_generation",
        "description": "Adjustable voltage regulator circuit from 1.25V to 37V using LM317.",
        "components": ["LM317 Voltage Regulator", "Resistor 240Ω", "Potentiometer 10kΩ", "Capacitor 0.1µF", "Capacitor 1µF", "Capacitor 10µF", "Heat Sink", "Transformer 12-0-12V", "Diode 1N4007 (4x)", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Build bridge rectifier using 4x 1N4007 diodes", "Connect transformer secondary to bridge AC inputs", "Bridge output (+) to LM317 input (pin 3)", "LM317 adjust (pin 1) to 240Ω resistor to GND", "10kΩ potentiometer between adjust pin and GND", "0.1µF capacitor from input pin to GND", "1µF capacitor from output pin (pin 2) to GND", "10µF capacitor from adjust to GND", "Mount LM317 on heat sink"],
        "explanation": "The LM317 maintains 1.25V between output and adjust pins. The output voltage is Vout = 1.25 × (1 + R2/240). With 10kΩ pot, output ranges from 1.25V to about 28V depending on input voltage.",
        "circuit_diagram_description": "variable voltage power supply using lm317 wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "5V Power Supply using 7805",
        "type": "circuit_generation",
        "description": "Regulated 5V DC power supply from AC mains using 7805 voltage regulator.",
        "components": ["Transformer 9-0-9V, 500mA", "Diode 1N4007 (4x)", "Capacitor 1000µF 25V", "Capacitor 0.33µF", "Capacitor 0.1µF", "7805 Voltage Regulator", "Heat Sink", "Fuse 500mA", "Power cord", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Connect fuse to AC mains live wire", "Transformer primary to mains through fuse", "Build bridge rectifier with 4x 1N4007 diodes", "Capacitor 1000µF across rectifier output (polarity correct)", "7805 input to rectifier positive, GND to negative", "0.33µF capacitor from 7805 input to GND", "0.1µF capacitor from 7805 output to GND", "Mount 7805 on heat sink"],
        "explanation": "The transformer steps down 230V AC to 9V AC. The bridge rectifier converts to pulsating DC, and 1000µF capacitor filters it. The 7805 regulator provides clean 5V output rated up to 1A. Output capacitors improve transient response.",
        "circuit_diagram_description": "5v power supply using 7805 wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Dual Polarity Power Supply (±12V)",
        "type": "circuit_generation",
        "description": "Split power supply providing +12V and -12V from single transformer.",
        "components": ["Transformer 12-0-12V, 1A", "Diode 1N4007 (4x)", "Capacitor 1000µF (2x)", "Capacitor 0.33µF (2x)", "Capacitor 0.1µF (2x)", "7812 Voltage Regulator", "7912 Voltage Regulator", "Heat Sinks (2x)", "Fuse 1A", "Breadboard"],
        "wiring_steps": ["Connect transformer center tap to GND", "Bridge rectifier from outer secondary wires", "1000µF capacitor from +DC to GND", "1000µF capacitor from GND to -DC", "7812 input to +DC, GND pin to system GND", "7912 GND pin to system GND, input to -DC", "Capacitors 0.33µF on both regulator inputs", "Capacitors 0.1µF on both regulator outputs", "Mount both regulators on heat sinks"],
        "explanation": "The center-tapped transformer with bridge rectifier creates both positive and negative DC rails. 7812 regulates +12V and 7912 regulates -12V. This supply is essential for op-amp circuits requiring dual supply voltages.",
        "circuit_diagram_description": "dual polarity power supply (±12v) wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Battery Charger Circuit for Li-Ion",
        "type": "circuit_generation",
        "description": "Constant current/constant voltage charger for single Li-Ion cells using TP4056.",
        "components": ["TP4056 Charging Module", "Li-Ion Battery 3.7V", "Resistor 1.2kΩ (programs 1A charge)", "LED Red (charging indicator)", "LED Blue (full indicator)", "Capacitor 10µF", "Capacitor 0.1µF", "5V Power Supply (USB)", "Battery holder", "PCB"],
        "wiring_steps": ["Connect 5V input to TP4056 IN+ and IN-", "Add 10µF and 0.1µF capacitors across input", "Set charge current with 1.2kΩ resistor on PROG pin", "Connect battery to BAT+ and BAT- terminals", "Red LED to CHRG pin via 1kΩ resistor", "Blue LED to STDBY pin via 1kΩ resistor", "Ensure proper polarity on battery connections"],
        "explanation": "TP4056 charges Li-Ion batteries with CC/CV profile: 1A constant current until 4.2V, then constant voltage with decreasing current. The PROG resistor sets charge current (1.2kΩ = 1A). Red LED glows during charging, blue indicates full charge.",
        "circuit_diagram_description": "battery charger circuit for li-ion wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Digital Thermometer using LM35",
        "type": "circuit_generation",
        "description": "Precise temperature measurement circuit using LM35 sensor and ADC.",
        "components": ["LM35 Temperature Sensor", "Arduino Uno", "16x2 LCD Display", "Resistor 10kΩ (for contrast)", "Potentiometer 10kΩ (LCD contrast)", "Breadboard", "Jumper wires", "5V Power Supply"],
        "wiring_steps": ["Connect LM35 VCC to 5V, GND to GND", "LM35 output to Arduino A0", "LCD RS to Arduino pin 12", "LCD E to pin 11", "LCD D4 to pin 5, D5 to pin 4, D6 to pin 3, D7 to pin 2", "10kΩ pot for contrast on LCD pin 3", "Read analog value: tempC = (analogRead(A0) * 5.0 / 1024.0) * 100", "Display temperature on LCD using LiquidCrystal library"],
        "explanation": "LM35 outputs 10mV per °C (250mV at 25°C). Arduino reads analog voltage and converts to temperature. LCD displays in Celsius. Accuracy is ±0.5°C at room temperature. The sensor can measure from -55°C to 150°C.",
        "circuit_diagram_description": "digital thermometer using lm35 wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Ultrasonic Distance Meter using HC-SR04",
        "type": "circuit_generation",
        "description": "Measure distance using ultrasonic sensor HC-SR04 with Arduino and display.",
        "components": ["HC-SR04 Ultrasonic Sensor", "Arduino Uno", "16x2 LCD Display", "Resistor 330Ω", "Resistor 470Ω (voltage divider for echo)", "Breadboard", "Jumper wires"],
        "wiring_steps": ["HC-SR04 VCC to 5V, GND to GND", "Trig pin to Arduino pin 9", "Echo pin to Arduino pin 10", "Voltage divider: 330Ω + 470Ω on echo line (optional)", "LCD connections as standard", "Send 10µs pulse to Trig", "Read pulse duration on Echo", "Distance = duration × 0.034 / 2 in cm"],
        "explanation": "HC-SR04 sends ultrasonic burst (40kHz) and measures echo return time. Sound speed is 343 m/s. Distance = (time × speed)/2. Range: 2cm to 400cm with ±3mm accuracy. The voltage divider protects Arduino pin from 5V echo signal.",
        "circuit_diagram_description": "ultrasonic distance meter using hc-sr04 wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Digital Voltmeter using ICL7107",
        "type": "circuit_generation",
        "description": "Precision 3.5 digit voltmeter using ICL7107 ADC with 7-segment display.",
        "components": ["ICL7107 ADC IC", "7-Segment LED Display (3.5 digit)", "Resistor 47kΩ", "Resistor 1MΩ", "Resistor 100kΩ", "Capacitor 0.22µF", "Capacitor 0.1µF", "Capacitor 0.47µF", "Potentiometer 10kΩ (calibration)", "5V Power Supply"],
        "wiring_steps": ["ICL7107 pin 1 to 5V, pin 21 to GND", "Reference: pin 36 through 47kΩ to 5V", "47kΩ + 1MΩ voltage divider on input (pin 30-31)", "0.22µF on pin 27-28 (integrator)", "0.47µF on pin 29 to GND (auto-zero)", "100kΩ + 0.1µF on pin 33-34 (clock)", "Connect segment display to pins 2-19", "Calibrate with 10kΩ pot on reference"],
        "explanation": "ICL7107 is a 3.5-digit ADC with direct 7-segment drivers. It uses dual-slope conversion for high noise rejection. Resolution is 0.05% (2000 counts). Input range is ±200mV without divider, or higher with external voltage divider. Common for DIY multimeters.",
        "circuit_diagram_description": "digital voltmeter using icl7107 wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "FM Transmitter Circuit",
        "type": "circuit_generation",
        "description": "Simple FM transmitter broadcasting on 88-108MHz band using transistor.",
        "components": ["NPN Transistor 2N3904", "Electret Microphone", "Resistor 10kΩ (2x)", "Resistor 100Ω", "Capacitor 10pF", "Capacitor 100pF", "Capacitor 4.7pF", "Capacitor 0.1µF", "Inductor 5 turns of 22AWG on 5mm former", "Trimmer Capacitor 5-20pF", "Antenna (30cm wire)", "3V Battery", "Breadboard"],
        "wiring_steps": ["Wind 5-turn inductor on 5mm former (0.5µH)", "Connect transistor base to 100pF capacitor to inductor", "100Ω from collector to 3V positive", "10kΩ from collector to base (feedback)", "Microphone to base through 0.1µF and 10kΩ", "10pF capacitor from inductor to antenna", "Trimmer capacitor parallel to inductor", "4.7pF from collector to inductor tap"],
        "explanation": "The transistor oscillates at FM band frequency (88-108MHz) determined by LC tank (inductor + trimmer). Audio from microphone frequency-modulates the oscillator by varying base capacitance (varactor effect). Range is about 50-100 meters. Use trimmer to adjust frequency to clear channel.",
        "circuit_diagram_description": "fm transmitter circuit wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Simple Radio Receiver (Crystal Set)",
        "type": "circuit_generation",
        "description": "Basic AM radio receiver using a germanium diode and tuned LC circuit.",
        "components": ["Germanium Diode 1N34A", "Inductor 100µH (ferrite rod antenna)", "Variable Capacitor 365pF", "Resistor 100kΩ", "Capacitor 0.01µF", "Piezoelectric Earphone (high impedance)", "Antenna wire (10-20m long)", "Ground rod"],
        "wiring_steps": ["Connect ferrite rod antenna coil to variable capacitor (parallel LC)", "1N34A diode anode to LC tank top", "Diode cathode to 100kΩ resistor", "0.01µF capacitor from resistor to GND", "Piezo earphone across the 0.01µF capacitor", "Antenna wire to LC tank top (via 100pF if needed)", "Ground rod to circuit GND", "Tune variable capacitor for different stations"],
        "explanation": "The LC tank resonates at the desired AM frequency (530-1600kHz). The germanium diode rectifies the modulated RF signal, extracting the audio. The capacitor + resistor filter removes RF carrier. Requires good antenna and ground for strong reception. No batteries needed - runs on radio wave energy.",
        "circuit_diagram_description": "simple radio receiver (crystal set) wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "RF Remote Control using 433MHz",
        "type": "circuit_generation",
        "description": "Wireless on/off control using 433MHz RF modules and HT12D/E encoder-decoder.",
        "components": ["433MHz RF Transmitter Module", "433MHz RF Receiver Module", "HT12E Encoder IC", "HT12D Decoder IC", "Resistor 1MΩ (oscillator)", "Resistor 51kΩ (oscillator)", "Push buttons (4x)", "LEDs (4x)", "Resistor 220Ω (4x)", "9V Battery (2x)", "Breadboards (2x)"],
        "wiring_steps": ["Transmitter side: HT12E pins 1-8 as address/data", "HT12E pin 15 to 1MΩ resistor to GND", "HT12E pin 14 to RF transmitter DATA", "Push buttons from pins 10-13 to GND", "Receiver side: RF receiver DATA to HT12D pin 14", "HT12D pin 15 to 51kΩ resistor to GND", "HT12D pins 10-13 to 220Ω resistors to LEDs", "LEDs to GND", "Match address pins (1-8) on both ICs"],
        "explanation": "HT12E converts parallel data (button presses) to serial, which the RF module transmits at 433MHz. HT12D decodes serial back to parallel outputs. Each button controls one output LED. Range is about 50-100 meters in open air. The 1MΩ and 51kΩ resistors set internal oscillator frequencies for encoder and decoder respectively.",
        "circuit_diagram_description": "rf remote control using 433mhz wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "DC Motor Speed Controller using PWM",
        "type": "circuit_generation",
        "description": "Motor speed control using 555 timer PWM generator and MOSFET driver.",
        "components": ["555 Timer IC", "IRFZ44N N-Channel MOSFET", "Diode 1N4007 (flyback)", "Potentiometer 100kΩ (speed control)", "Resistor 1kΩ", "Resistor 10kΩ", "Capacitor 0.1µF", "Capacitor 10µF", "DC Motor (6-12V)", "12V Power Supply", "Breadboard"],
        "wiring_steps": ["Wire 555 as astable: pin 8 and 4 to VCC, pin 1 to GND", "Pin 7 to 10kΩ to VCC, pin 7 to 1kΩ to pin 6", "100kΩ pot between pin 6 and pin 2", "0.1µF from pin 2 to GND", "555 output (pin 3) to MOSFET gate via 1kΩ", "MOSFET drain to motor, source to GND", "Flyback diode across motor (cathode to motor +)", "Capacitor 10µF across power supply"],
        "explanation": "555 timer generates PWM signal at ~7kHz. The potentiometer varies duty cycle from 0% to 100% by changing the charge/discharge time ratio. The MOSFET switches the motor at high frequency, and average motor voltage = duty cycle × supply voltage. The flyback diode protects the MOSFET from inductive spikes.",
        "circuit_diagram_description": "dc motor speed controller using pwm wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Stepper Motor Driver using ULN2003",
        "type": "circuit_generation",
        "description": "Drive unipolar stepper motor using ULN2003 Darlington array.",
        "components": ["28BYJ-48 Stepper Motor (5V)", "ULN2003 Driver Board", "Arduino Uno", "Potentiometer 10kΩ (speed control)", "Push button (direction)", "10kΩ pull-up resistor", "5V Power Supply", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Connect stepper motor to ULN2003 board", "ULN2003 IN1 to Arduino pin 8", "IN2 to pin 9, IN3 to pin 10, IN4 to pin 11", "ULN2003 GND to Arduino GND, VCC to 5V", "Potentiometer wiper to Arduino A0", "Push button to Arduino pin 2 with 10kΩ pull-up", "Use Stepper.h library with 2048 steps/revolution", "Speed from pot: map(analogRead(A0), 0, 1023, 5, 20) RPM"],
        "explanation": "The 28BYJ-48 is a 5V unipolar stepper with 2048 steps per revolution (reduction gearbox). ULN2003 provides current amplification (500mA per channel). Sequence: IN1-IN2-IN3-IN4 in wave drive or half-step mode for smoother rotation. Speed controlled by step delay.",
        "circuit_diagram_description": "stepper motor driver using uln2003 wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Servo Motor Tester Circuit",
        "type": "circuit_generation",
        "description": "Simple servo motor tester using 555 timer to generate PWM control signal.",
        "components": ["555 Timer IC", "Servo Motor (SG90)", "Potentiometer 10kΩ (position control)", "Resistor 1kΩ", "Resistor 10kΩ (2x)", "Diode 1N4148 (2x)", "Capacitor 0.1µF", "Capacitor 10µF", "5V Power Supply", "Breadboard"],
        "wiring_steps": ["Wire 555 as astable with diodes for independent charge/discharge", "1kΩ + pot to pin 7 (charge path through D1)", "10kΩ to pin 7 discharge through D2", "0.1µF from pin 2 to GND", "Pin 3 output to servo control wire (white/orange)", "Servo red to 5V, brown/black to GND", "10µF capacitor across servo power", "Pot adjusts pulse width from 1ms to 2ms"],
        "explanation": "Servo position is controlled by pulse width: 1ms = 0°, 1.5ms = 90°, 2ms = 180°. The 555 generates a ~50Hz signal (20ms period). Diodes allow independent adjustment of charge and discharge times through the potentiometer, varying the duty cycle while maintaining frequency.",
        "circuit_diagram_description": "servo motor tester circuit wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Bidirectional Motor Control using H-Bridge",
        "type": "circuit_generation",
        "description": "Control DC motor forward/reverse using L293D H-Bridge IC.",
        "components": ["L293D Motor Driver IC", "DC Motor (6-12V)", "Arduino Uno", "Push buttons (3x: forward, reverse, stop)", "Resistor 10kΩ (3x, pull-down)", "Diode 1N4007 (4x, flyback)", "Capacitor 0.1µF", "12V Power Supply", "Breadboard"],
        "wiring_steps": ["L293D pin 1 (enable) to 5V", "Input pins: pin 2 to Arduino D8, pin 7 to D9", "Output pins: pin 3 to motor terminal 1, pin 6 to motor terminal 2", "L293D VCC (pin 16) to 5V, VS (pin 8) to 12V", "GND pins (4,5,12,13) to common GND", "Flyback diodes from each motor terminal to VS and GND", "Buttons to Arduino D2 (forward), D3 (reverse), D4 (stop)", "0.1µF capacitor across power supply"],
        "explanation": "L293D is a dual H-bridge motor driver (1A per channel). For one motor: input 1 high + input 2 low = forward; reverse for opposite; both low = stop. The enable pin (connected to 5V) keeps the driver always active. Flyback diodes protect against motor inductive spikes.",
        "circuit_diagram_description": "bidirectional motor control using h-bridge wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Binary Counter using 74LS93",
        "type": "circuit_generation",
        "description": "4-bit binary counter circuit displaying count on LEDs using 7493 IC.",
        "components": ["74LS93 4-bit Binary Counter", "Resistor 330Ω (4x)", "LED (4x, different colors)", "Push button (clock)", "Resistor 10kΩ (pull-up)", "Capacitor 0.1µF (debounce)", "5V Power Supply", "Breadboard", "Jumper wires"],
        "wiring_steps": ["74LS93 pin 5 (VCC) to 5V, pin 10 (GND) to GND", "Clock input (pin 14) to push button through 10kΩ pull-up", "0.1µF capacitor from clock pin to GND (debounce)", "Output QA (pin 12) to first LED via 330Ω", "Output QB (pin 9) to second LED via 330Ω", "Output QC (pin 8) to third LED via 330Ω", "Output QD (pin 11) to fourth LED via 330Ω", "Connect pin 12 to pin 1 (internal divide-by-8 mode)", "All LED cathodes to GND"],
        "explanation": "The 74LS93 is a 4-bit binary counter that counts from 0 to 15 (0000 to 1111). Each press of the button increments the count. LEDs display the binary value: QD (MSB) to QA (LSB). The RC network debounces the push button to prevent multiple counts from mechanical bounce.",
        "circuit_diagram_description": "binary counter using 74ls93 wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "7-Segment Display Counter using 4026",
        "type": "circuit_generation",
        "description": "Count from 0-9 on 7-segment display using CD4026 decade counter.",
        "components": ["CD4026 Decade Counter IC", "7-Segment Common Cathode Display", "Resistor 220Ω (7x, segment resistors)", "Push button (clock)", "Resistor 10kΩ (pull-up)", "Capacitor 0.1µF (2x, debounce and bypass)", "5V Power Supply", "Breadboard"],
        "wiring_steps": ["CD4026 pin 16 (VDD) to 5V, pin 8 (VSS) to GND", "Clock input (pin 1) to push button with 10kΩ pull-up", "0.1µF debounce capacitor on clock input", "Display segments a-g to CD4026 pins: a-9, b-10, c-11, d-12, e-13, f-14, g-15", "Each segment pin through 220Ω to display", "Display common cathode to GND", "0.1µF bypass capacitor across power", "Pin 2 (enable) to GND, pin 3 (reset) to GND"],
        "explanation": "CD4026 is a decade counter with built-in 7-segment decoder/driver. It counts from 0 to 9 and resets. Each clock pulse advances the count by one. 220Ω resistors limit LED segment current. The display shows the current count value (0-9). Multiple 4026s can be cascaded for multi-digit counting.",
        "circuit_diagram_description": "7-segment display counter using 4026 wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Traffic Light Controller using 4017",
        "type": "circuit_generation",
        "description": "Sequential traffic light (Red-Yellow-Green) using 4017 decade counter and diodes.",
        "components": ["CD4017 Decade Counter IC", "555 Timer IC", "Resistor 100kΩ", "Resistor 10kΩ", "Capacitor 10µF", "Capacitor 0.1µF", "Diode 1N4148 (8x)", "Red LED", "Yellow LED", "Green LED", "Resistor 220Ω (3x, LED current)", "5V Power Supply", "Breadboard"],
        "wiring_steps": ["Wire 555 as astable: pin 8,4 to 5V; pin 1 to GND", "10kΩ between pin 7 and VCC", "100kΩ pot between pins 7 and 6", "10µF from pin 2 to GND", "555 pin 3 to 4017 pin 14 (clock)", "4017 pin 16 to 5V, pin 8 to GND", "Connect outputs via steering diodes to LEDs", "Q0 (pin 2) + Q1 (pin 4) to Red LED through diodes", "Q2 (pin 7) + Q3 (pin 10) to Yellow LED through diodes", "Q4 (pin 1) through Q9 to Green LED through diodes", "Each LED through 220Ω to GND"],
        "explanation": "The 4017 decade counter activates one output at a time. Diodes combine outputs: Q0-Q1 = Red (2 clock cycles), Q2-Q3 = Yellow (2 cycles), Q4-Q9 = Green (6 cycles). The 555 provides adjustable clock speed. This mimics a real traffic light sequence with proper timing ratios.",
        "circuit_diagram_description": "traffic light controller using 4017 wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Inverting Amplifier using LM358",
        "type": "circuit_generation",
        "description": "Basic inverting op-amp amplifier with adjustable gain for signal processing.",
        "components": ["LM358 Op-Amp IC", "Resistor 10kΩ (Rin)", "Resistor 100kΩ (Rf, sets gain = 10)", "Resistor 10kΩ (bias)", "Capacitor 10µF (2x, power supply filtering)", "Dual Power Supply ±5V", "Signal input source", "Breadboard", "Jumper wires"],
        "wiring_steps": ["LM358 pin 8 to +5V, pin 4 to -5V", "10µF capacitors from each supply pin to GND", "Non-inverting input (pin 3) to GND through 10kΩ", "Input signal to 10kΩ resistor (Rin) to inverting input (pin 2)", "100kΩ feedback resistor (Rf) from output (pin 1) to pin 2", "Apply input signal through input capacitor if AC coupling needed", "Measure output between pin 1 and GND"],
        "explanation": "Gain = -Rf/Rin = -100k/10k = -10. The output is 180° out of phase with input. For a 0.5V input, output = -5V. Circuit bandwidth depends on gain-bandwidth product (1MHz for LM358). Useful for sensor signal amplification and audio preamplification.",
        "circuit_diagram_description": "inverting amplifier using lm358 wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Non-Inverting Amplifier",
        "type": "circuit_generation",
        "description": "Simple non-inverting amplifier using LM358 with positive gain.",
        "components": ["LM358 Op-Amp IC", "Resistor 10kΩ (R1)", "Resistor 100kΩ (Rf)", "Capacitor 10µF (2x)", "Dual Power Supply ±5V", "Signal input", "Breadboard", "Jumper wires"],
        "wiring_steps": ["LM358 pin 8 to +5V, pin 4 to -5V", "10µF capacitors on supply pins", "Input signal to non-inverting input (pin 3)", "10kΩ (R1) from inverting input (pin 2) to GND", "100kΩ (Rf) from output (pin 1) to inverting input (pin 2)", "Measure output between pin 1 and GND"],
        "explanation": "Gain = 1 + Rf/R1 = 1 + 100k/10k = 11. The output is in phase with the input. Input impedance is very high (MΩ range). For 0.5V input, output = 5.5V. This circuit is commonly used for sensor buffering and signal conditioning.",
        "circuit_diagram_description": "non-inverting amplifier wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Active Low-Pass Filter",
        "type": "circuit_generation",
        "description": "Second-order Sallen-Key low-pass filter using LM358 for signal filtering.",
        "components": ["LM358 Op-Amp IC", "Resistor 10kΩ (2x)", "Capacitor 0.1µF (2x)", "Capacitor 10µF (2x)", "Dual Power Supply ±5V", "Signal input", "Breadboard", "Jumper wires"],
        "wiring_steps": ["Design for cutoff frequency: fc = 1/(2×π×R×C) = 1/(2×π×10k×0.1µF) ≈ 159Hz", "Connect input to first 10kΩ resistor", "First resistor to second 10kΩ resistor", "First capacitor (0.1µF) from junction of resistors to GND", "Second capacitor (0.1µF) from second resistor end to op-amp output", "Both capacitors meet at op-amp output", "Non-inverting input to junction of second resistor and second capacitor", "Inverting input to output (buffer configuration)", "Op-amp pin 8 to +5V, pin 4 to -5V"],
        "explanation": "The Sallen-Key topology provides a 2nd order (-40dB/decade) low-pass response. With equal resistors (10kΩ) and capacitors (0.1µF), cutoff is ~159Hz with Butterworth response (maximally flat). Above cutoff, signals attenuate sharply. Ideal for audio crossover and anti-aliasing filters.",
        "circuit_diagram_description": "active low-pass filter wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "PIR Motion Sensor Alarm",
        "type": "circuit_generation",
        "description": "Motion activated alarm using PIR sensor HC-SR501 and buzzer.",
        "components": ["PIR Sensor HC-SR501", "NPN Transistor BC547", "Buzzer 5V", "Resistor 10kΩ", "Resistor 1kΩ", "Capacitor 10µF", "LED (status indicator)", "Resistor 220Ω", "5V Power Supply", "Breadboard"],
        "wiring_steps": ["HC-SR501 VCC to 5V, GND to GND", "PIR output to BC547 base through 10kΩ resistor", "BC547 collector to 5V through 1kΩ + buzzer", "LED with 220Ω from collector to GND", "BC547 emitter to GND", "10µF capacitor across PIR power for stability", "Adjust PIR sensitivity and time via onboard pots", "Test: walk in front of sensor within 3-7m range"],
        "explanation": "PIR sensor detects infrared radiation changes from moving human body (warmth). When motion detected, output goes HIGH (3.3V) for adjustable duration. BC547 transistor drives the buzzer and LED. Detection range is 3-7 meters, 110° cone angle. Time delay adjustable from 5 seconds to 5 minutes.",
        "circuit_diagram_description": "pir motion sensor alarm wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Laser Security System",
        "type": "circuit_generation",
        "description": "Laser beam break detection alarm using LDR and laser module.",
        "components": ["Laser Diode Module (5V, <5mW)", "LDR (Light Dependent Resistor)", "LM358 Op-Amp", "Resistor 10kΩ (2x)", "Potentiometer 100kΩ (threshold adjust)", "Buzzer 5V", "NPN Transistor BC547", "Resistor 1kΩ", "LED (status)", "5V Power Supply", "Breadboard"],
        "wiring_steps": ["LM358 as comparator: non-inverting (pin 3) to voltage divider (LDR + 10kΩ)", "LDR to 5V, 10kΩ to GND, junction to pin 3", "Inverting (pin 2) to potentiometer wiper (threshold)", "Potentiometer between 5V and GND", "LM358 output (pin 1) to BC547 base through 1kΩ", "BC547 collector to buzzer and LED", "BC547 emitter to GND", "Laser aimed at LDR from across room", "When beam breaks, LDR resistance increases → triggers alarm"],
        "explanation": "LDR resistance is low (~1kΩ) when laser hits it, so voltage at pin 3 is low. When beam breaks, LDR resistance rises to ~1MΩ, voltage at pin 3 rises above threshold, LM358 output goes HIGH, triggering the buzzer. Threshold pot sets sensitivity.",
        "circuit_diagram_description": "laser security system wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Water Level Indicator",
        "type": "circuit_generation",
        "description": "Multi-level water tank indicator using transistor switches and LEDs.",
        "components": ["NPN Transistor BC547 (4x)", "Resistor 470Ω (4x, LED current)", "Resistor 10kΩ (4x, base resistors)", "LED Red (empty)", "LED Yellow (low)", "LED Blue (medium)", "LED Green (full)", "Buzzer 5V (overflow alarm)", "5V Power Supply", "Probe wires (copper, different lengths)", "Breadboard"],
        "wiring_steps": ["Place probes at different heights in tank: lowest = empty, highest = full", "Each probe to base of each BC547 via 10kΩ resistor", "Transistor emitters to GND", "Collector of each transistor to respective LED via 470Ω", "LEDs to 5V", "Add buzzer from highest probe transistor collector to 5V", "Common probe at bottom of tank to 5V through 1MΩ", "Water completes circuit between common probe and level probes"],
        "explanation": "When water touches a probe wire, it conducts (water has minerals making it slightly conductive). The BC547 transistor switches ON, lighting the corresponding LED. Multiple LEDs can be ON simultaneously showing exact water level. The highest probe triggers buzzer for overflow warning.",
        "circuit_diagram_description": "water level indicator wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Rain Alarm Circuit",
        "type": "circuit_generation",
        "description": "Simple rain detector using sensing pad and transistor switch.",
        "components": ["NPN Transistor BC547 (2x)", "Sensor grid (bare copper wires on PCB)", "Resistor 10kΩ", "Resistor 1kΩ", "Buzzer 5V", "LED (indicator)", "Resistor 220Ω", "Capacitor 10µF", "9V Battery", "Breadboard"],
        "wiring_steps": ["Create sensor grid: interleaved copper traces on small PCB", "Sensor grid one side to 9V through 10kΩ resistor", "Sensor grid other side to first BC547 base", "First BC547 collector to second BC547 base", "Second BC547 collector to buzzer and LED via resistor", "Both transistor emitters to GND", "Capacitor across sensor for debounce", "Test: drop water on sensor grid"],
        "explanation": "Rain water (containing minerals) bridges the sensor grid traces, completing the circuit. The first BC547 amplifies this small current and drives the second transistor (Darlington pair configuration) which activates the buzzer and LED. High gain allows detection even with minimal water. Useful for automatic window closing or garden monitoring.",
        "circuit_diagram_description": "rain alarm circuit wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Touch Switch Circuit",
        "type": "circuit_generation",
        "description": "Touch-activated switch using transistor pair without moving parts.",
        "components": ["NPN Transistor BC547 (2x)", "Resistor 100kΩ", "Resistor 1kΩ", "LED", "Resistor 220Ω", "Capacitor 0.1µF", "5V Power Supply", "Touch plate (copper or aluminum)", "Breadboard"],
        "wiring_steps": ["Connect touch plate to first BC547 base", "First BC547 collector to 100kΩ resistor to supply", "First BC547 emitter to GND", "Second BC547 base to first collector", "Second BC547 collector to LED via 220Ω to supply", "Second BC547 emitter to GND", "Capacitor from second base to GND (noise filtering)", "Touch the plate briefly to turn LED ON", "Touch again to turn OFF"],
        "explanation": "The circuit forms a bistable multivibrator (flip-flop) using two transistors. When you touch the plate, your body's capacitance triggers the first transistor, changing the state. The circuit latches in one state until touched again. Each touch toggles the output. Ideal for touch-sensitive lamps or switches.",
        "circuit_diagram_description": "touch switch circuit wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Bluetooth Controlled LED using HC-05",
        "type": "circuit_generation",
        "description": "Control LEDs wirelessly via smartphone Bluetooth using HC-05 module.",
        "components": ["HC-05 Bluetooth Module", "Arduino Uno", "LED (2x, different colors)", "Resistor 220Ω (2x)", "Resistor 1kΩ (HC-05 voltage divider)", "Resistor 2kΩ (HC-05 voltage divider)", "5V Power Supply", "Breadboard", "Jumper wires"],
        "wiring_steps": ["HC-05 VCC to 5V, GND to GND", "HC-05 TX to Arduino RX (pin 0)", "HC-05 RX to Arduino TX (pin 1) through voltage divider (1k+2kΩ)", "Arduino pin 9 to first LED via 220Ω", "Arduino pin 10 to second LED via 220Ω", "Upload Serial Bluetooth code with SoftwareSerial", "Pair with smartphone (PIN 1234)", "Send '1' for LED1 ON, '2' for OFF, '3' for LED2 ON, '4' for OFF"],
        "explanation": "HC-05 operates as serial-to-Bluetooth bridge. The voltage divider (1kΩ+2kΩ) drops Arduino 5V TX to 3.3V for HC-05 RX. Smartphone Serial Bluetooth Terminal app sends commands. The Arduino reads serial data and controls LEDs accordingly. Range is about 10 meters.",
        "circuit_diagram_description": "bluetooth controlled led using hc-05 wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "ESP8266 Wi-Fi Temperature Monitor",
        "type": "circuit_generation",
        "description": "IoT temperature monitoring using ESP8266 and LM35 with web dashboard.",
        "components": ["ESP8266 NodeMCU", "LM35 Temperature Sensor", "Resistor 10kΩ", "Breadboard", "5V Power Supply", "Jumper wires"],
        "wiring_steps": ["ESP8266 VIN to 5V, GND to GND", "LM35 VCC to 3.3V (ESP output), GND to GND", "LM35 output to ESP8266 A0", "Connect ESP to WiFi: WiFi.begin('SSID', 'password')", "Start web server on port 80", "Read analog: temp = analogRead(A0) * 3.3 / 1024 * 100", "Create HTML page with auto-refresh showing temperature", "Access ESP IP address from browser"],
        "explanation": "ESP8266 connects to WiFi network and runs a simple web server. LM35 provides analog voltage proportional to temperature. ESP reads ADC, converts to Celsius, and displays on a web page that auto-refreshes every few seconds. Can be expanded to control relays from the web interface.",
        "circuit_diagram_description": "esp8266 wi-fi temperature monitor wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Logic Probe Circuit",
        "type": "circuit_generation",
        "description": "Digital logic probe indicating HIGH, LOW, or PULSE states using LEDs.",
        "components": ["NPN Transistor BC547 (2x)", "PNP Transistor BC557", "LED Red (HIGH indicator)", "LED Green (LOW indicator)", "LED Yellow (PULSE indicator)", "Resistor 220Ω (3x)", "Resistor 10kΩ (2x)", "Resistor 100kΩ", "Diode 1N4148 (2x)", "Capacitor 0.1µF", "Probe tip (needle or stiff wire)", "5V Power Supply"],
        "wiring_steps": ["Probe tip to 100kΩ to both transistor bases", "BC547 (NPN) base to probe via 10kΩ, collector to Red LED via 220Ω to 5V", "BC557 (PNP) base to probe via 10kΩ, collector to Green LED via 220Ω to GND", "Pulse detector: both transistors drive Yellow LED through diodes", "Capacitor from probe to GND for noise filtering", "5V supply to probe reference ground", "Test: touch probe to 5V → Red ON, to GND → Green ON, toggling → Yellow", "Battery clip with 9V for portable use"],
        "explanation": "When probe touches a HIGH (logic 1) signal, BC547 turns ON lighting Red LED. When LOW (logic 0), BC557 turns ON lighting Green LED. Rapid toggling (pulse) activates both briefly, lighting Yellow LED. Essential tool for debugging digital circuits without an oscilloscope.",
        "circuit_diagram_description": "logic probe circuit wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Component Tester (ESR Meter)",
        "type": "circuit_generation",
        "description": "Simple ESR meter for testing electrolytic capacitors using 555 timer.",
        "components": ["555 Timer IC", "Resistor 1kΩ", "Resistor 10kΩ", "Potentiometer 10kΩ (calibration)", "Capacitor 0.1µF", "Capacitor 10µF", "Capacitor 100µF (known good for calibration)", "Diode 1N4148 (2x)", "Microammeter or multimeter (mV range)", "5V Power Supply", "Test probes"],
        "wiring_steps": ["Wire 555 as astable multivibrator at ~50kHz", "R1=1kΩ, R2=10kΩ, C=0.1µF", "555 output to capacitor under test through 1kΩ limiting resistor", "Rectify output using diodes and filter capacitor", "Connect microammeter across test capacitor", "Calibrate with known good 100µF capacitor", "Test unknown capacitors: higher reading = higher ESR", "Safe discharge all capacitors before testing"],
        "explanation": "ESR (Equivalent Series Resistance) is a measure of capacitor health. High ESR indicates aging/drying electrolyte. This circuit applies a 50kHz AC signal to the capacitor and measures the voltage drop across its ESR. Good capacitors show near-zero reading; bad capacitors show high readings. Typical good ESR for 100µF: <1Ω.",
        "circuit_diagram_description": "component tester (esr meter) wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Raspberry Pi GPIO LED Blink",
        "type": "circuit_generation",
        "description": "Control GPIO pins to blink LED from Raspberry Pi using Python.",
        "components": ["Raspberry Pi (any model)", "LED", "Resistor 330Ω", "Breadboard", "Male-female jumper wires"],
        "wiring_steps": ["Connect LED anode (long leg) to GPIO 17 (pin 11)", "Connect LED cathode through 330Ω resistor to GND (pin 6)", "Install RPi.GPIO library", "Write Python script: import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); GPIO.setup(17, GPIO.OUT)", "GPIO.output(17, GPIO.HIGH) for ON, LOW for OFF", "Run with sudo: sudo python3 blink.py", "Use time.sleep(1) for 1 second interval"],
        "explanation": "Raspberry Pi GPIO pins are 3.3V logic. The 330Ω resistor limits LED current to safe ~10mA. GPIO 17 is one of the general-purpose pins that can be set as output. Python's RPi.GPIO library provides simple control. Always use a resistor to protect both LED and GPIO pin.",
        "circuit_diagram_description": "raspberry pi gpio led blink wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Raspberry Pi Temperature and Humidity Sensor",
        "type": "circuit_generation",
        "description": "Read DHT11/DHT22 sensor data from Raspberry Pi and log to file.",
        "components": ["Raspberry Pi", "DHT11 Temperature/Humidity Sensor", "Resistor 10kΩ (pull-up)", "Breadboard", "Female-female jumper wires"],
        "wiring_steps": ["DHT11 pin 1 to 3.3V (pin 1 on Pi)", "DHT11 pin 2 to GPIO 4 (pin 7)", "10kΩ pull-up resistor from pin 2 to 3.3V", "DHT11 pin 4 to GND (pin 6 on Pi)", "Install Adafruit_DHT: pip install Adafruit_DHT", "Write Python script to read sensor every 2 seconds", "Log data with timestamp to CSV file", "Plot data using matplotlib for visualization"],
        "explanation": "DHT11 uses single-wire protocol to send temperature (°C) and humidity (%) data. Accuracy: ±2°C, ±5% RH. Range: 0-50°C, 20-80% RH. The 10kΩ pull-up keeps the data line HIGH. Read interval must be at least 1 second (DHT11 is slow). DHT22 provides better accuracy (±0.5°C, ±2% RH) and wider range.",
        "circuit_diagram_description": "raspberry pi temperature and humidity sensor wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Arduino OLED Display",
        "type": "circuit_generation",
        "description": "Display text and graphics on 0.96-inch SSD1306 OLED display with Arduino.",
        "components": ["Arduino Uno", "SSD1306 OLED Display (128x64, I2C)", "Breadboard", "Jumper wires"],
        "wiring_steps": ["OLED VCC to Arduino 5V", "OLED GND to Arduino GND", "OLED SCL to Arduino A5 (SCL)", "OLED SDA to Arduino A4 (SDA)", "Install libraries: Adafruit_SSD1306, Adafruit_GFX", "Initialize: display.begin(SSD1306_SWITCHCAPVCC, 0x3C)", "Use display.print() for text, display.drawPixel() for graphics", "display.display() to update screen"],
        "explanation": "SSD1306 OLED uses I2C protocol for communication. Resolution: 128×64 pixels. I2C address is typically 0x3C or 0x3D. The display doesn't require backlight (OLED is emissive). Adafruit libraries provide text, shapes, and bitmap drawing functions. Refresh rate: up to 30fps for simple graphics.",
        "circuit_diagram_description": "arduino oled display wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Arduino Keypad Lock",
        "type": "circuit_generation",
        "description": "4x4 matrix keypad electronic lock with relay output using Arduino.",
        "components": ["Arduino Uno", "4x4 Matrix Keypad", "Relay Module (5V)", "LED Green (unlock)", "LED Red (locked)", "Resistor 220Ω (2x)", "Buzzer (key press feedback)", "12V Solenoid Lock (optional)", "5V/12V Power Supply", "Breadboard"],
        "wiring_steps": ["Connect keypad rows to Arduino D8-D11", "Keypad columns to D4-D7", "Relay module IN to D12", "Green LED to D2 via 220Ω", "Red LED to D3 via 220Ω", "Buzzer to D13 via 1kΩ", "Set password: e.g. '1234' in code", "On correct password: activate relay for 3 seconds", "On wrong password: increment attempt counter, lock for 10s after 3 attempts", "Add EEPROM storage for persistent password"],
        "explanation": "Matrix keypad uses row-column scanning to detect key presses. The relay module can control high-voltage devices (solenoid lock, door strike). The Arduino compares entered code against stored password. Anti-tamper feature locks out after multiple wrong attempts. EEPROM stores password persistently.",
        "circuit_diagram_description": "arduino keypad lock wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "LED Audio Spectrum Analyzer",
        "type": "circuit_generation",
        "description": "Audio level display using LM3915 dot/bar display driver IC.",
        "components": ["LM3915 LED Bar Graph Driver", "Electret Microphone", "Resistor 1kΩ", "Resistor 10kΩ", "Capacitor 1µF (2x)", "Capacitor 0.1µF", "LED (10x, different colors recommended)", "Resistor 220Ω (10x)", "Potentiometer 10kΩ (gain adjust)", "5V Power Supply", "Breadboard"],
        "wiring_steps": ["LM3915 pin 3 to 5V, pin 2 to GND", "Audio input to pin 5 through 1µF capacitor", "10kΩ pot from pin 5 to GND (gain control)", "Pin 7 (REF ADJ) to GND through 1kΩ", "Pin 6 to pin 7 through 1kΩ", "Pin 8 (REF OUT) to +5V through 1kΩ", "LEDs from pins 1,18 through 10 to GND via 220Ω each", "Pin 9 set: to VCC for bar mode, float for dot mode", "0.1µF across power supply"],
        "explanation": "LM3915 is a logarithmic LED driver with 3dB/step suitable for audio. 10 LEDs cover a 30dB dynamic range. The internal voltage reference creates precision thresholds. Dot mode shows only one LED at a time (like VU meter); bar mode shows cumulative levels. Ideal for audio level monitoring and peak indicators.",
        "circuit_diagram_description": "led audio spectrum analyzer wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "12V to 5V USB Charger using LM2596",
        "type": "circuit_generation",
        "description": "Efficient buck converter for 5V 3A output from 12V input using LM2596.",
        "components": ["LM2596 Buck Converter Module", "Capacitor 220µF 25V (input)", "Capacitor 220µF 16V (output)", "USB Type-A Female Socket", "12V Power Supply", "LED (power indicator)", "Resistor 1kΩ (LED)", "Multimeter for calibration"],
        "wiring_steps": ["Connect 12V input to LM2596 IN+ and IN-", "220µF 25V capacitor across input terminals", "220µF 16V capacitor across output terminals", "Connect USB socket: D+ and D- can be left open for charging only", "USB VBUS to output positive, GND to negative", "LED with resistor across output (polarity correct)", "Adjust trimmer pot while measuring output for exactly 5.00V", "Do NOT exceed 3A continuous load"],
        "explanation": "LM2596 is a step-down (buck) switching regulator with up to 90% efficiency. Unlike linear regulators (like 7805), it doesn't waste excess voltage as heat. Output voltage is adjustable from 1.25V to 37V via the trimmer pot. At 3A output, a heat sink may be needed. Input should be at least 1.5V higher than output voltage.",
        "circuit_diagram_description": "12v to 5v usb charger using lm2596 wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "Electronic Dice using 4017",
        "type": "circuit_generation",
        "description": "Random number generator (1-6) using 4017 IC and 555 timer for dice game.",
        "components": ["555 Timer IC", "CD4017 Decade Counter", "LED (6x, arranged as dice face)", "Resistor 100kΩ", "Resistor 10kΩ", "Capacitor 10µF", "Capacitor 0.1µF", "Resistor 220Ω (6x)", "Push button (roll)", "9V Battery", "Breadboard"],
        "wiring_steps": ["555 astable: pin 8 to VCC, pin 1 to GND", "10kΩ between pins 7 and 8", "100kΩ pot between pins 6 and 7", "10µF from pin 2 to GND", "555 pin 3 to 4017 pin 14 (clock)", "4017 outputs Q0-Q5 (pins 2,4,7,10,1,5) to 6 LEDs via 220Ω", "Arrange LEDs in dice pattern: 2-3-1-4-6-5", "Push button from VCC to 555 pin 4 (RESET)", "Button released: fast counting; button pressed: stop and show value", "0.1µF across power"],
        "explanation": "When the button is pressed, RESET pin goes HIGH stopping the 555 oscillator. The count stops at that position showing a random dice value (1-6). The circuit cycles through thousands of counts per second, so the result is effectively random. LEDs arranged in standard dice pattern for authentic feel.",
        "circuit_diagram_description": "electronic dice using 4017 wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    },
    {
        "title": "LED Cube 3x3x3",
        "type": "circuit_generation",
        "description": "3D LED cube with 27 LEDs controlled by Arduino via multiplexing.",
        "components": ["Arduino Uno", "LED (27x, same color)", "Resistor 220Ω (9x, column resistors)", "NPN Transistor BC547 (3x, layer control)", "Resistor 10kΩ (3x, base resistors)", "Breadboard (for controller)", "Perfboard (for cube)", "5V Power Supply", "Jumper wires"],
        "wiring_steps": ["Build LED cube: 3 layers × 9 LEDs each on perfboard", "All LED anodes in same column connect together (9 columns)", "All LED cathodes in same layer connect together (3 layers)", "Column wires to Arduino D2-D10 via 220Ω resistors", "Layer wires to BC547 collectors", "BC547 bases to Arduino D11-D13 via 10kΩ", "BC547 emitters to GND", "Write multiplexing code: scan layers at >60Hz for flicker-free", "Create animation patterns (rain, snake, blink, rotate)"],
        "explanation": "Multiplexing turns on one layer at a time while enabling only the LEDs needed in that layer. By scanning all layers rapidly (>60Hz), persistence of vision makes all lit LEDs appear simultaneously. Power: at most 9 LEDs ON at once (3 per layer × 3 layers), keeping current within limits. Complex patterns can be stored in PROGMEM.",
        "circuit_diagram_description": "led cube 3x3x3 wiring diagram with all components connected as described.",
        "sources": [{"name": "Wikipedia - Electronics", "url": "https://en.wikipedia.org/wiki/Electronics"}, {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws"}],
    }

]


def search_circuits(query: str) -> list[CircuitContent]:
    """Search the circuit library by keyword matching on title, description,
    and components list. Uses word-level matching so any query keyword
    that appears in the title/description will match."""
    q = query.lower()
    words = [w for w in q.split() if len(w) > 2]

    def _matches(circuit: CircuitContent) -> bool:
        text = (
            circuit["title"].lower() + " "
            + circuit["description"].lower() + " "
            + " ".join(circuit["components"]).lower()
        )
        if len(words) > 1:
            return sum(1 for w in words if w in text) >= 2
        return any(w in text for w in words)

    results = [c for c in CIRCUIT_LIBRARY if _matches(c)]
    results.sort(
        key=lambda c: sum(1 for w in words if w in c["title"].lower()),
        reverse=True,
    )
    return results


def get_all_circuits() -> list[CircuitContent]:
    return CIRCUIT_LIBRARY.copy()


def format_circuit_response(circuit: CircuitContent) -> str:
    """Format a circuit entry into a readable text response."""
    lines = [
        f"# {circuit['title']}",
        "",
        circuit["description"],
        "",
        "## Components Needed",
    ]
    for comp in circuit["components"]:
        lines.append(f"- {comp}")
    lines.extend([
        "",
        "## Wiring Steps",
    ])
    for i, step in enumerate(circuit["wiring_steps"], 1):
        lines.append(f"{i}. {step}")
    lines.extend([
        "",
        "## Circuit Diagram",
        circuit["circuit_diagram_description"],
        "",
        "## How It Works",
        circuit["explanation"],
        "",
        "## Sources",
    ])
    for src in circuit["sources"]:
        lines.append(f"- {src['name']}: {src['url']}")
    return "\n".join(lines)


def format_circuit_response_compact(circuit: CircuitContent) -> str:
    comps = ", ".join(circuit["components"][:6])
    if len(circuit["components"]) > 6:
        comps += "..."
    srcs = ", ".join(f'{s["name"]} ({s["url"]})' for s in circuit["sources"])
    return (
        f"CIRCUIT: {circuit['title']}\n"
        f"Description: {circuit['description']}\n"
        f"Components: {comps}\n"
        f"Sources: {srcs}\n"
    )
