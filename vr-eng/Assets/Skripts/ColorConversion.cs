using UnityEngine;

/// <summary>
/// A utility class for converting RGB color strings to Color objects.
/// </summary>
public class ColorConversion
{    /// <summary>
     /// Converts an RGB color string to a Unity Color object.
     /// </summary>
     /// <param name="rgbString">A string in the format "R;G;B" representing RGB color values.</param>
     /// <returns>A Color object representing the RGB color.</returns>
    public static Color StringToColor(string rgbString)
    {
        // Remove parentheses and split the string into individual RGB values.
        string[] rgbValues = rgbString.Trim('(', ')').Split(';');

        // Extract the RGB values as integers.
        int r = int.Parse(rgbValues[0]);
        int g = int.Parse(rgbValues[1]);
        int b = int.Parse(rgbValues[2]);

        // Create a new Color object using the extracted values. Divide by 255 to normalize to the [0, 1] range.
        Color color = new Color(r / 255f, g / 255f, b / 255f);

        return color;

    }

}
