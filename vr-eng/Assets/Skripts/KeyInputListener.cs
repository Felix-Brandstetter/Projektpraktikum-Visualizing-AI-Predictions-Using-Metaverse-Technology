using UnityEngine;

/// <summary>
/// Listens to key inputs and triggers actions based on the pressed keys.
/// </summary>
public class KeyInputListener : MonoBehaviour
{
    public KeyCode SetTime = KeyCode.Space; // Key code for setting a specific time.
    public KeyCode SpawnTimeSelecter = KeyCode.Space; // Key code for spawning the time selector.
    public TimeSelecter timeSelecter; // Reference to the TimeSelecter script.

    /// <summary>
    /// Called every frame to check for key inputs.
    /// </summary>
    void Update()
    {
        // Check if the "SetTime" key is pressed.
        if (Input.GetKeyDown(SetTime))
        {
            // Set the game time to a specific value (600f) using the TimeManager.
            TimeManager.instance.SelectedTime = 600f;

            // Set the current game time as the selected time..
            TimeManager.instance.SetCurrentTimeAsSelectedTime();

            // Activate or deactivate a speed ramp factor (set to 20).
            TimeManager.instance.activateDeactivateSpeedRampFactor(20);
        }

        // Check if the "SpawnTimeSelecter" key is pressed.
        if (Input.GetKeyDown(SpawnTimeSelecter))
        {
            // Call the SpawnWeekdayCircles method from the referenced TimeSelecter script.
            timeSelecter.SpawnWeekdayCircles();

            // Log the minute index obtained from the TimeConverter for a specific time string.
            Debug.Log(TimeConverter.TimeToMinuteIndexTimeToMinuteIndex("MO 19:30"));
        }
    }
}
