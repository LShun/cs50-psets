// Helper functions for music

#include <cs50.h>

#include "helpers.h"

#include <string.h>
#include <math.h>
#include <stdio.h>

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    double X = fraction[0] - 48;
    double Y = fraction[2] - 48;
    //sprintf(fraction, "%i/%i", X, Y);
    double fract = (X * 8) / Y;
    return fract;//fraction;
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    double a = 0; // accidental flag
    int char_point = 1; // character pointer flag
    if (strlen(note) == 3)
    {
        a = (note[1] == 35) ? 1 : -1; // ternary to check if its a sharp
        char_point++;
    }
    if (note[0] == 'B') // if its B, since B is the only one which is above 'A'
    {
        a += 2;
    }
    else if (note[0] > 'E') // if its more than E, since anything more than E will have the correct semitone.
    {
        a += (note[0] - 72) * 2;
    }
    else if (note[0] > 'B')
        // if its more than B, sinc eeverything more than B will have one less semitone due to the gap between F4 and E4, so one less negative.
    {
        a += (note[0] - 72) * 2 + 1;
    }
    double n = (note[char_point] - '4') * 12 + a;
    double f = round(pow(2, n / 12) * 440);
    //sprintf(note, "%f\n", f);
    return f;
}

// Determines whether a string represents a rest
bool is_rest(string s)
{

    if (strcmp(s, "\0") == 0)
    {
        return true;
    }
    else
    {
        return false;
    }

}
