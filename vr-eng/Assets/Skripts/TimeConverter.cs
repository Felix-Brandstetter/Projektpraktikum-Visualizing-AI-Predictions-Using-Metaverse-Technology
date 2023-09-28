using UnityEngine;

/// <summary>
/// Utility class for converting between minute indexes (game time) and time strings (real time).
/// Game Time starts Mondays at 8:00 am and runs until 6:00 pm. A TimeIndex (time) of 601 corresponds to Tuesday at 8:01 am.
/// </summary>
// TODO Revise so that game time reflects real time (24h). For this, the data in the CSV files must also be adjusted (Data Science Team).A revision would make this class simpler, more logical and easier to understand.
public class TimeConverter : MonoBehaviour
{
    /// <summary>
    /// Converts a minute index (game time) to a formatted time string (real time) including the weekday.
    /// </summary>
    /// <param name="minuteIndex">The minute index representing a specific time (game time).</param>
    /// <returns>A formatted time string (e.g., "MO 08:30").</returns>
    public static string MinuteIndexToTime(float minuteIndex)
    {
        string weekdayString = "";
        int weekday = (int) (minuteIndex / 600); // Calculate the weekday index based on the minuteIndex.

        switch (weekday)
        {
            case 0:
                weekdayString =  "MO "; // Montag
                break;
            case 1:
                weekdayString = "DI "; // Dienstag
                break;
            case 2:
                weekdayString = "MI "; // Mittwoch
                break;
            case 3:
                weekdayString = "DO "; // Donnerstag
                break;
            case 4:
                weekdayString = "FR "; // Freitag
                break;
            case 5:
                weekdayString = "SA "; // Samstag
                break;
            case 6:
                weekdayString = "SO "; // Sonntag
                break;
            default:
                weekdayString = ""; // Fehlerfall oder ungültiger Wert
                break;
        }

        // Calculate the time portion in minutes and format it as HH:MM. One weekday has 600 min 8am to 6 pm.
        int timeInMinutes = (int) (minuteIndex - (weekday * 600) + (8*60));
        int hours = Mathf.FloorToInt(timeInMinutes / 60);
        int minutes = Mathf.FloorToInt(timeInMinutes % 60);
        string timeString = string.Format("{0:00}:{1:00}", hours, minutes);

        return weekdayString + timeString; // Combine weekday and time and return the formatted string.
    }

    /// <summary>
    /// Converts a time string (real time) including the weekday to a minute index (game time).
    /// </summary>
    /// <param name="timeString">A formatted time string (e.g., "MO 08:30").</param>
    /// <returns>The minute index representing the specified time.</returns>
    public static int TimeToMinuteIndexTimeToMinuteIndex(string timeString)
    {
        int minuteIndex = 0;

        // Split the input time string into weekday and time parts.
        string[] timeParts = timeString.Split(' ');
        if (timeParts.Length != 2)
        {
            Debug.LogError("Ungültiges Format für Zeitangabe. Verwenden Sie 'WOCHENTAG STUNDE:MINUTE'");
            return 0;
        }

        // Convert the weekday string to an index.
        int weekdayIndex = 0;
        switch (timeParts[0])
        {
            case "MO":
                weekdayIndex = 0;
                break;
            case "DI":
                weekdayIndex = 1;
                break;
            case "MI":
                weekdayIndex = 2;
                break;
            case "DO":
                weekdayIndex = 3;
                break;
            case "FR":
                weekdayIndex = 4;
                break;
            case "SA":
                weekdayIndex = 5;
                break;
            case "SO":
                weekdayIndex = 6;
                break;
            default:
                Debug.LogError("Ungültiger Wochentag.");
                return 0;
        }

        // Split the time part into hours and minutes, and validate the format.
        string[] timeParts2 = timeParts[1].Split(':');
        if (timeParts2.Length != 2 || !int.TryParse(timeParts2[0], out int hours) || !int.TryParse(timeParts2[1], out int minutes))
        {
            Debug.LogError("Ungültiges Format für Uhrzeit. Verwenden Sie 'STUNDE:MINUTE'");
            return 0;
        }

        // Calculate the total minutes from the input time.
        // Note: In the TimeSelecter, the times 19 and 20 o'clock can be selected on the clock. However, the game time is modeled only until 18:00 (600 min per day). Therefore the restriction is made here
        if (hours * 60 + minutes - 8 * 60 > 600)
        {
            minuteIndex = weekdayIndex * 600 + 600; // Jump to next weekday (+600)
        }
        else
        {
            minuteIndex = weekdayIndex * 600 + hours * 60 + minutes - 8 * 60; // -8 * 60 is used because game time starts at 8 am. //TODO
        }
        return minuteIndex;
    }

}

