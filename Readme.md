# Midilights


##### Channel Conventions

We send midi events to certain channels which are interpreted by the lights in various ways.  Conventions below:

| Midi Channel | Value Range | Expected Usage |
| ------------ | ----------- | -------------- |
| 0            | 127         | Kick |
| 1            | 127         | Snare |
| 2            | 127         | Clap |
| 3            | 127         | Closed Hat |
| 4            | 127         | Open Hat |
| 5            | 1-127       | Set patterns |
| 6            | 1-127       | Brightness |
| 7            | 1-127       | Set Color (from value) |
| 8            | 1-127       | Shift Color |
| 9            | 1-127       | Stack colors |