using TMPro;
using UnityEngine;

/// <summary>
/// This script displays the selected time from the TimeManager on a TextMeshPro component.
/// Time Manger returns a float number. Time starts Mondays at 8:00 am and runs until 6:00 pm. A TimeIndex of 601 corresponds to Tuesday at 8:01 am.
/// </summary>
public class ShowSelectedTime : MonoBehaviour
{
    public TextMeshPro textMesh; // The TextMeshPro component to display the selected time.

    /// <summary>
    /// Called once per frame to update the displayed time.
    /// </summary>
    private void Update()
    {
        // Convert the selected time (as an index) to a formatted time string.
        string time = TimeConverter.MinuteIndexToTime(TimeManager.instance.SelectedTime);

        // Update the TextMeshPro text with the formatted time string.
        textMesh.text = time;

    }
}
