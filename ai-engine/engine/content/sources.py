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
