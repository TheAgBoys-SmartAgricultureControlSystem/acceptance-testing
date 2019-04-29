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
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

/* Driver Header files */
#include <ti/drivers/GPIO.h>
#include <ti/drivers/UART.h>

/* Example/Board Header files */
#include "Board.h"

#define PI 3.14156
#define theoreticalLatitude 40.0065079
#define theoreticalLongitude -105.262138

int parseUART(char *lineBuffer, char *latitude, char *longitude, char *latDirection, char *longDirection) {
    int latitudeIndex, longitudeIndex = 0; // Set indexes for strings to 0

    // Get latitude, lineBuffer[6] is a comma
    int i = 7;

    while (lineBuffer[i] != ',') {
        if (lineBuffer[i] != ' ') {
            latitude[latitudeIndex] = lineBuffer[i];
            latitudeIndex++;
        }
        i++;
    }

    if (latitudeIndex == 0) return 0; // Return 0 (fail) if no data to parse

    latitude[latitudeIndex] = '\0'; // Null terminate latitude
    i++; // Skip comma

    // Get N or S
    while (lineBuffer[i] != ',') {
        if (lineBuffer[i] == 'N' || lineBuffer[i] == 'S') {
            *latDirection = lineBuffer[i];
            latitudeIndex++;
        }
        i++;
    }

    i++; // Skip comma


    // Get longitude
    while (lineBuffer[i] != ',') {
       if (lineBuffer[i] != ' ') {
           longitude[longitudeIndex] = lineBuffer[i];
           longitudeIndex++;
       }
       i++;
    }

    longitude[longitudeIndex] = '\0'; // Null terminate longitude
    i++; // Skip comma


    // Get E or W
    while (lineBuffer[i] != ',') {
       if (lineBuffer[i] == 'E' || lineBuffer[i] == 'W') {
           *longDirection = lineBuffer[i];
           latitudeIndex++;
       }
       i++;
    }

    return 1; // No errors
}

// Convert GPS coordinate format to normal decimal degrees
float convertToDecimalDegrees(float gpsFormat, char direction) {
    // GPS format for longitude is ddmm.mmmm
    // To convert to decimal degrees we have to split it into two parts:
    // dd mm.mmmm
    // Then perform the following operation dd + (mm.mmmm/60)

    int dd = (int) (gpsFormat / 100); // Divide by 100 to get dd.mmmmmm, then cast to int to strip decimals
    float mm = gpsFormat - (dd * 100); // ddmm.mmmm - (dd * 100) = ddmm.mmmm - dd00 = mm.mmmm

    return  (direction == 'S' || direction == 'W') ? ((dd + (mm / 60)) * -1) : (dd + (mm / 60)); // Account for direction provided for GPS (N or W indicate negative coordinates)
}

// Converts degrees to radians
float degreestoRadians(float degrees) {
    return degrees * PI / 180;
}

// Calculated distance between two coordinates in m
float distanceBetweenCordinates(float lat1, float lon1, float lat2, float lon2) {
    int earthRadius = 6371000; // Radius of earth in meters
    lat1 = degreestoRadians(lat1);
    lon1 = degreestoRadians(lon1);
    lat2 = degreestoRadians(lat2);
    lon2 = degreestoRadians(lon2);
    float deltaLat = lat1 - lat2;
    float deltaLon = lon1- lon2;

    // Calculate distance between coordinates using law of haversines
    float a = sin(deltaLat / 2) * sin(deltaLat / 2) + cos(lat1) * cos(lat2) * sin(deltaLon / 2) * sin(deltaLon / 2);
    float c = 2 * atan2(sqrt(a), sqrt(1 - a));

    return earthRadius * c;
}

/*
 *  ======== mainThread ========
 */
void *mainThread(void *arg0)
{
    char        input;
    char        inputDebug;
    const char waitingForFix[] = "Waiting for GPS fix...\r\n";
    const char CEPText[] = ", CEP: ";
    const char CEPString[20]; // String to use with ToString for printing CEP
    UART_Handle uart;
    UART_Handle uartDebug;
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

    UART_write(uart, waitingForFix, sizeof(waitingForFix));

    char    lineBuffer[100];
    int     bufferIndex = 0;
    char    latitude[20]; // Stores values for latitude
    char    latDirection; // Stores 'N' or 'S'
    char    longitude[20]; // Stores values for longitude
    char    longDirection; // Stores 'E' or 'W'
    int     print = 0; // Will only print values if print == 1
    int     alreadyWaiting = 1;
    float   latitudeFloat;
    float   longitudeFloat;
    float   CEP = 0.0;
    int CEPStringLength = 0;

    /* Loop forever echoing */
    while (1) {
        UART_read(uart, &input, 1);

        print = 0;

        if (input == '\r' || input == '\n') {
            bufferIndex = 0;

            if (lineBuffer[5] == 'L') { // Add longitude and latitude to write buffer
                /*lineBuffer[6] = ',';
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
                lineBuffer[39] = '\n';*/

                if (parseUART(lineBuffer, latitude, longitude, &latDirection, &longDirection)) { // Only continue if no errors from parse
                    // Error calculations
                    latitudeFloat = convertToDecimalDegrees(atof(latitude), latDirection);
                    longitudeFloat = convertToDecimalDegrees(atof(longitude), longDirection);

                    CEP = distanceBetweenCordinates(latitudeFloat, longitudeFloat, theoreticalLatitude, theoreticalLongitude);

                    print = 1; // Set print flag
                    alreadyWaiting = 0;
                }

                else if (!alreadyWaiting){
                    UART_write(uart, waitingForFix, sizeof(waitingForFix));
                    alreadyWaiting = 1;
                }
            }
        }

        else {
            lineBuffer[bufferIndex] = input;
            bufferIndex++;
        }

        if (print) {
            int j = 0;

            // Print latitude
            for (j = 0; j < strlen(latitude); j++) {
               input = latitude[j];
               UART_write(uart, &input, 1);
            }

            input = ' ';
            UART_write(uart, &input, 1);

            // Print latitude direction
            UART_write(uart, &latDirection, 1);

            input = ',';
            UART_write(uart, &input, 1);
            input = ' ';
            UART_write(uart, &input, 1);

            // Print longitude
            for (j = 0; j < strlen(longitude); j++) {
              input = longitude[j];
              UART_write(uart, &input, 1);
            }

            input = ' ';
            UART_write(uart, &input, 1);

            // Print longitude direction
            UART_write(uart, &longDirection, 1);

            // Write set up for CEP
            UART_write(uart, CEPText, sizeof(CEPText));

            // Print CEP
            CEPStringLength = snprintf(NULL, 0, "%f", CEP); // Convert CEP to string with a total of 4 digits (should give three decimal points if GPS is accurate enough)
            char *CEPString = (char *) malloc(CEPStringLength + 1);
            snprintf(CEPString, CEPStringLength + 1, "%f", CEP);
            UART_write(uart, CEPString, CEPStringLength);
            free(CEPString);

            // Print carriage return and newline
            input = '\r';
            UART_write(uart, &input, 1);
            input = '\n';
            UART_write(uart, &input, 1);
        }
    }
}
