/*
 * Copyright (c) 2015-2017, Texas Instruments Incorporated
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * *  Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 * *  Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * *  Neither the name of Texas Instruments Incorporated nor the names of
 *    its contributors may be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
 * OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
 * OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
 * EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

/*
 *  ======== uartecho.c ========
 */
#include <stdint.h>
#include <stddef.h>

/* Driver Header files */
#include <ti/drivers/GPIO.h>
#include <ti/drivers/UART.h>

/* Example/Board Header files */
#include "Board.h"

/*
 *  ======== mainThread ========
 */
void *mainThread(void *arg0)
{
    char        input;
    const char  echoPrompt[] = "Echoing characters:\r\n";
    UART_Handle uart;
    UART_Params uartParams;

    /* Call driver init functions */
    GPIO_init();
    UART_init();

    /* Configure the LED pin */
    GPIO_setConfig(Board_GPIO_LED0, GPIO_CFG_OUT_STD | GPIO_CFG_OUT_LOW);

    /* Turn on user LED */
    GPIO_write(Board_GPIO_LED0, Board_GPIO_LED_ON);

    /* Create a UART with data processing off. */
    UART_Params_init(&uartParams);
    uartParams.writeDataMode = UART_DATA_BINARY;
    uartParams.readDataMode = UART_DATA_BINARY;
    uartParams.readReturnMode = UART_RETURN_FULL;
    uartParams.readEcho = UART_ECHO_OFF;
    uartParams.baudRate = 9600;

    uart = UART_open(Board_UART0, &uartParams);

    if (uart == NULL) {
        /* UART_open() failed */
        while (1);
    }

    UART_write(uart, echoPrompt, sizeof(echoPrompt));

    char lineBuffer[100];
    int bufferIndex = 0;

    int i = 0;

    /* Loop forever echoing */
    while (1) {
        UART_read(uart, &input, 1);

        if (input == 13 || input == '\n') {
            bufferIndex = 0; // 13 is ascii for carriage return

            if (lineBuffer[5] == 'L') { // Add longitude and latitude to write buffer
                lineBuffer[6] = ',';
                lineBuffer[7] = ' ';
                lineBuffer[8] = '3';
                lineBuffer[9] = '7';
                lineBuffer[10] = '2';
                lineBuffer[11] = '3';
                lineBuffer[12] = '.';
                lineBuffer[13] = '2';
                lineBuffer[14] = '4';
                lineBuffer[15] = '7';
                lineBuffer[16] = '5';
                lineBuffer[17] = '6';
                lineBuffer[18] = ',';
                lineBuffer[19] = ' ';
                lineBuffer[20] = 'N';
                lineBuffer[21] = ',';
                lineBuffer[22] = ' ';
                lineBuffer[23] = '1';
                lineBuffer[24] = '2';
                lineBuffer[25] = '1';
                lineBuffer[26] = '5';
                lineBuffer[27] = '8';
                lineBuffer[28] = '.';
                lineBuffer[29] = '3';
                lineBuffer[30] = '4';
                lineBuffer[31] = '1';
                lineBuffer[32] = '6';
                lineBuffer[33] = '2';
                lineBuffer[34] = ',';
                lineBuffer[35] = ' ';
                lineBuffer[36] = 'W';
                lineBuffer[37] = ',';
                lineBuffer[38] = ' ';
                lineBuffer[39] = '\n';

                // Get latitude, lineBuffer[6] is a comma
                i = 7;

                while (lineBuffer[i] != ',') {
                    input = lineBuffer[i];
                    UART_write(uart, &input, 1);
                    i++;
                }

                i++; // Don't print comma


                // Get N or S
                while (lineBuffer[i] != ',') {
                    input = lineBuffer[i];
                    UART_write(uart, &input, 1);
                    i++;
                }

                i++; // Don't print comma


               // Print comma for clarity
               input = ',';
               UART_write(uart, &input, 1);


               // Get longitude
               while (lineBuffer[i] != ',') {
                   input = lineBuffer[i];
                   UART_write(uart, &input, 1);
                   i++;
               }

               i++; // Don't print comma


               // Get E or W
               while (lineBuffer[i] != ',') {
                   input = lineBuffer[i];
                   UART_write(uart, &input, 1);
                   i++;
               }


               // Print newline for clarity
               input = '\n';
               UART_write(uart, &input, 1);
            }

        }

        else {
            lineBuffer[bufferIndex] = input;
            bufferIndex++;
        }

        //UART_write(uart, &input, 1);
    }
}
