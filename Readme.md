# Midilights


##### Channel Conventions

We send midi events to certain channels which are interpreted by the lights in various ways.  Conventions below:

| Midi Channel | Value Range | Expected Usage |
| ------------ | ----------- | -------------- |
| 0-3          | 127         | Principally drums.  Gate signals are used to trigger lights |
| 5            | 1-127       | Brightness |
| 6            | 1-127       | Set Color |
| 7            | 1-127       | Set patterns |