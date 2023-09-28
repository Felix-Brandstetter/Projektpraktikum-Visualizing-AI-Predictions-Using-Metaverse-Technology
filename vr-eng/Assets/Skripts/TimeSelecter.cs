using System.Collections.Generic;
using TMPro;
using UnityEngine;

/// <summary>
/// Allows selection of game time on specific weekdays and displays a clock for the selection.
/// </summary>
public class TimeSelecter : MonoBehaviour
{
    public GameObject weekdayPrefab; // Reference to a weekdayPrefab used for weekday selection.
    public GameObject clockPrefab;  // Reference to a clock prefab for time selection.
    public float spawnRadius = 2f; // Radius for spawning the weekday circles.
    public float yOffset = 0.5f; // Adjustable offset in the Y-coordinate.
    public KeyCode keyToWatch = KeyCode.Space; // Key code to trigger an action. (DEBUGGING)
    public GameObject nearMenu; // Reference to a menu object. Used for confirmation of time.
    private List<GameObject> spawnedWeekdays = new List<GameObject>(); // List to keep track of spawned weekday circles.
    private GameObject spawnedClock; // Reference to the spawned clock object.
    private Vector3 directionTo12; // Direction vector to 12 o'clock.
    private string weekdayText; // Text representing the selected weekday. Used on weekday prefab.
    private string _selectedTime; // Selected time in string format.
    private string selecteDay; // Selected day of the week.


    /// <summary>
    /// Called when the script starts.
    /// </summary>
    public void Start()
    {
        // Listen for the timeChangeEvent from the TimeManager instance.
        TimeManager.instance.timeChangeEvent.AddListener(OnTimeChange); // Hör auf das TimeChangeEvent

        // Deactivate the nearMenu GameObject
        nearMenu.SetActive(false);
    }

    /// <summary>
    /// Spawns the weekday prefabs in a circle around the player.
    /// </summary>
    public void SpawnWeekdayCircles()
    {
        RemovespawnedWeekdays(); // Remove any existing weekdays.

        // Loop through weekdays (5 times).
        for (int i = 0; i < 5; i++)
        {
            float angle = i * 360f / 5;
            Vector3 spawnPosition = transform.position + Quaternion.Euler(0f, angle, 0f) * Vector3.forward * spawnRadius;
            spawnPosition -= new Vector3(0f, yOffset, 0f);
            Vector3 lookDirection = Camera.main.transform.position - spawnPosition;
            Quaternion rotation = Quaternion.LookRotation(lookDirection, Vector3.up);
            rotation.x = 0f;
            rotation.z = 0f;

            // Instantiate a new circle prefab at the calculated position and rotation.
            GameObject newWeekday = Instantiate(weekdayPrefab, spawnPosition, rotation);
            spawnedWeekdays.Add(newWeekday);

            // Set the weekday text based on the current iteration.
            switch (i)
            {
                case 0:
                    weekdayText = "MO";
                    break;
                case 1:
                    weekdayText = "DI";
                    break;
                case 2:
                    weekdayText = "MI";
                    break;
                case 3:
                    weekdayText = "DO";
                    break;
                case 4:
                    weekdayText = "FR";
                    break;
                default:
                    weekdayText = "SA";
                    break;
            }
            newWeekday.name = weekdayText;

            // Set the text of the TMP_Text component within the circle prefab.
            TMP_Text textMesh = newWeekday.GetComponentInChildren<TMP_Text>();
            if (textMesh != null)
            {
                textMesh.text = weekdayText;
            }
        }
    }

    /// <summary>
    /// Called when a GameObject enters the collider of this object. -> When Player walks into weekday Box-Collider
    /// </summary>
    /// <param name="other">The Collider of the entering GameObject.</param>
    private void OnTriggerEnter(Collider other)
    {
        // Check if the colliding object is not the same as this prefab.
        if (other.gameObject != gameObject)
        {
            selecteDay = other.gameObject.name; // Get the selected weekday.
            RemovespawnedWeekdays(); // Remove existing weekdays.
            SpawnClock(); // Spawn the clock for time selection.
        }
    }

    /// <summary>
    /// Removes all spawned wekkdays from scene
    /// </summary>
    private void RemovespawnedWeekdays()
    {
        // Iterate through the list of spawned weekdays and destroy them.
        foreach (GameObject weekday in spawnedWeekdays)
        {
            Destroy(weekday);
        }

        // Clear the list to prepare for new weekdays.
        spawnedWeekdays.Clear();
    }

    /// <summary>
    /// Spawns the clock for time selection.
    /// </summary>
    public void SpawnClock()
    {
        RemovespawnedWeekdays(); // Remove existing weekdays
        nearMenu.SetActive(true); // Activate the nearMenu GameObject. Used for confirmation of time.

        // Destroy the previous clock if it exists.
        if (spawnedClock != null)
        {
            Destroy(spawnedClock); // Zerstöre die vorherige Uhr, falls vorhanden
        }

        // Calculate the spawn position and rotation for the clock.
        Vector3 spawnPosition = transform.position;
        spawnPosition -= new Vector3(0f, yOffset, 0f);
        Quaternion cameraRotation = Camera.main.transform.rotation;
        Quaternion rotation = Quaternion.Euler(-90f, cameraRotation.eulerAngles.y, 180f);
        directionTo12 = -Camera.main.transform.forward; //watch is spawned facing the twelfth dial.

        // Instantiate the clock prefab with the calculated position and rotation.
        spawnedClock = Instantiate(clockPrefab, spawnPosition, rotation);
        Vector3 scale = spawnedClock.transform.localScale;
        scale.x *= -1f; //TODO Change clock Prefab to right orintation and scale.
        spawnedClock.transform.localScale = scale;


    }

    /// <summary>
    /// Called in every frame update.
    /// </summary>
    void Update()
    {
        if (spawnedClock != null)
        {
            CalculateTime();
        }
    }

    /// <summary>
    /// Calculates the selected time based on the player`s position on the spawned clock.
    /// </summary>
    private void CalculateTime()
    {
        // Calculate the angle between the clock's direction and 12 o'clock.
        Vector3 directionToClock = spawnedClock.transform.position - Camera.main.transform.position;
        directionToClock.y = 0f; // y coordinate is not relevant for horizontal angle
        directionTo12.y = 0f; // y coordinate is not relevant for horizontal angle
        float angle = CalculateAngleBetween(directionToClock, directionTo12);


        // Calculate the time in string format based on the angle.
        string selectedTime = CalculateTimeFromAngle(angle);

        // Update the text displayed on the clock.
        TMP_Text textMesh = spawnedClock.GetComponentInChildren<TMP_Text>();
        if (textMesh != null)
        {
            textMesh.text = selectedTime;
        }
    }

    /// <summary>
    /// Calculates the angle between two direction vectors.
    /// </summary>
    /// <param name="direction1">The first direction vector.</param>
    /// <param name="direction2">The second direction vector.</param>
    /// <returns>The angle between the two vectors.</returns>
    private float CalculateAngleBetween(Vector3 direction1, Vector3 direction2)
    {
        float angle = Vector3.Angle(direction2, direction1);
        // Use cross product to determine the sign of the angle (clockwise or counterclockwise). Relevant. Since angle should always be positive starting from 12:00 on the clock
        Vector3 cross = Vector3.Cross(direction2, direction1);
        if (cross.y < 0f)
        {
            angle = 360f - angle;
        }
        return angle;
    }

    /// <summary>
    /// Calculates the time in string format based on the given angle.
    /// </summary>
    /// <param name="angle"> >The angle to calculate the time from.</param>
    /// <returns>The time in string format (e.g., "MO 08:30")</returns>
    private string CalculateTimeFromAngle(float angle)
    {
        // Calculate the total angle covered in 12 hours (360 degrees).
        float totalAngleInHours = 12f;

        // Calculate the time for the given angle in hours.
        float hours = angle * (totalAngleInHours / 360f);
        hours %= 12f;
        if (hours > 0f && hours < 8f)
        {
            hours += 12f;
        }


        // Calculate the remaining minutes in the hour
        float minutesInHour = 60f;
        float minutes = (hours - Mathf.Floor(hours)) * minutesInHour;

        // Format the time as a string
        _selectedTime = string.Format(selecteDay + " {0:00}:{1:00}", (int)hours, (int)minutes);
        float minutes_index_simulation = TimeConverter.TimeToMinuteIndexTimeToMinuteIndex(_selectedTime);
        TimeManager.instance.SelectedTime = minutes_index_simulation;
        return _selectedTime;
    }

    /// <summary>
    /// Called when the game time changes.
    /// </summary>
    /// <param name="currentTime">The current game time</param>
    public void OnTimeChange(float currentTime)
    {
        RemovespawnedWeekdays(); // Remove existing weekdays.
        if (spawnedClock != null)
        {
            Destroy(spawnedClock);  // Destroy the previous clock if it exists.
        }
        nearMenu.SetActive(false); // Deactivate the nearMenu GameObject.
    }



}
