ChangeLog
---------

+------------+------------------------------------------------------------------------+------------+
| Version    | Description                                                            | Date       |
+============+========================================================================+============+
| **0.8.0**  | * Change MAX7219's block_orientation to support ±90° angle correction  | 2017/03/19 |
|            | * Deprecate "vertical" and "horizontal" block_orientation              |            |
+------------+------------------------------------------------------------------------+------------+
| **0.7.0**  | * **BREAKING CHANGE:** Move sevensegment class to                      | 2017/03/04 |
|            |   ``luma.led_matrix.virtual`` package                                  |            |
|            | * Documentation updates & corrections                                  |            |
+------------+------------------------------------------------------------------------+------------+
| **0.6.2**  | * Allow MAX7219 and NeoPixel driver constructors to accept any args    | 2017/03/02 |
+------------+------------------------------------------------------------------------+------------+
| **0.6.1**  | * Restrict exported Python symbols from ``luma.led_matrix.device``     | 2017/03/02 |
+------------+------------------------------------------------------------------------+------------+
| **0.6.0**  | * Add support for arbitrary MxN matrices rathern than a single chain   | 2017/02/22 |
+------------+------------------------------------------------------------------------+------------+
| **0.5.3**  | * Huge performance improvements for cascaded MAX7219 devices           | 2017/02/21 |
|            | * Documentation updates                                                |            |
+------------+------------------------------------------------------------------------+------------+
| **0.5.2**  | * Add apostrophe representation to seven-segment display               | 2017/02/19 |
|            | * Deprecate ``luma.led_matrix.legacy`` (moved to ``luma.core.legacy``) |            |
+------------+------------------------------------------------------------------------+------------+
| **0.4.4**  | * Support both common-row anode and common-row cathode LED matrices    | 2017/02/02 |
+------------+------------------------------------------------------------------------+------------+
| **0.4.3**  | * Add translation mapping to accomodate Pimoroni's 8x8 Unicorn HAT     | 2017/01/29 |
|            | * MAX7219 optimizations                                                |            |
+------------+------------------------------------------------------------------------+------------+
| **0.4.2**  | * Fix bug in neopixel initialization                                   | 2017/01/27 |
|            | * Improved demo scripts                                                |            |
|            | * Additional tests                                                     |            |
+------------+------------------------------------------------------------------------+------------+
| **0.4.0**  | * Add support for WS2812 NeoPixel strips/arrays                        | 2017/01/23 |
+------------+------------------------------------------------------------------------+------------+
| **0.3.3**  | * Fix for dot muncher: not handling full-stop at line end              | 2017/01/21 |
|            | * Documentation updates                                                |            |
+------------+------------------------------------------------------------------------+------------+
| **0.3.2**  | * Replace bytearray with mutable_string implementation                 | 2017/01/20 |
|            | * More tests                                                           |            |
+------------+------------------------------------------------------------------------+------------+
| **0.3.1**  | * Python 3 compatibility (fix exception in bytearray creation)         | 2017/01/20 |
|            | * Begin to add tests & test infrastructure                             |            |
+------------+------------------------------------------------------------------------+------------+
| **0.3.0**  | * **BREKING CHANGE:** Package rename to ``luma.led_matrix``            | 2017/01/19 |
+------------+------------------------------------------------------------------------+------------+
| **0.2.3**  | * Bit-bang version using wiringPi                                      | 2013/01/28 |
+------------+------------------------------------------------------------------------+------------+
