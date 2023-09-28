using CsvHelper.Configuration.Attributes;
using System;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

/// <summary>
/// Controls the behavior of a heating board and its associated data.
/// </summary>
public class HeizungsboardController : MonoBehaviour
{
    /// <summary>
    /// Represents the data structure for heating board information loaded from a CSV file. MinuteIndex stands for the time at which the data changes.
    /// </summary>
    // TODO Move to separated script
    public class HeizungsboardData
    {
        [Name("minute_idx")]
        public int MinuteIndex { get; set; } // The time index in minutes.(game time)

        [Name("PersonenAnzahl")]
        public int NumberOfPersonsInRoom { get; set; } // The number of persons in the room.

        [Name("temp")]
        public double Temperature { get; set; }  // The room temperature.

        [Name("rgb_value")]
        public string ColorString { get; set; } // The color of the room as an RGB string.

        [Name("in_usage")]
        public bool InUsage { get; set; } // Indicates if the room is in use.

        [Name("heating")]
        public bool Heating { get; set; }  // Indicates if the heating is active.

        [Name("next_person_enters")]
        public int MinutesNextPersonEnters { get; set; } // Minutes until the next person enters the room.
    }

    private List<HeizungsboardData> heizungsboardDataList = new List<HeizungsboardData>(); // List to store heating board data.
    private int currentTimeStepIndex = 0; // Index to track the current time step.
    public string csvFile; // Name of the CSV to be read(including extension). Must be located on Hololens in LocalState.In Windows under Documents/MVP Data
    public GameObject floorObject; // Reference to the floor object. Floor Object in smallModell which is colored in color corresponding to temperature of the room.
    private Renderer floorRenderer; // Renderer component of the floor.

    // TextMesh Objects for displaying information.
    public TMP_Text temperatureDisplay;
    public TMP_Text nextPersonDisplay;
    public TMP_Text clockDisplay;
    public TMP_Text speedRampFactorDisplay;
    public GameObject iconUsageTrue;
    public GameObject iconHeatingTrue;
    public GameObject iconUsageFalse;
    public GameObject iconHeatingFalse;

    public bool visible = true; // Indicates if the heating board is visible.



    /// <summary>
    ///  Initialization method.
    /// </summary>
    private void Start()
    {
        // Load CSV data from the specified file.
        LoadCSVData();

        // Check if data was loaded successfully.
        if (heizungsboardDataList == null || heizungsboardDataList.Count == 0)
        {
            Debug.LogError("HeizungsboardDataList konnte nicht aus CSV geladen werden " + gameObject.name);
        }
        else
        {
            Debug.Log("HeizungsboardDataList wurden aus CSV geladen. Länge: " + heizungsboardDataList.Count);
        }

        // Get the Renderer component of the floor object.
        floorRenderer = floorObject.GetComponent<Renderer>();
        if (floorRenderer == null)
        {
            Debug.LogError("FloorObject has no Renderer. Name of FloorObject:  " + gameObject.name);
        }
        else
        {
            Debug.Log("FloorObject has Renderer");
        }

        // Set initial state of icons to be inactive.
        iconUsageTrue.SetActive(false);
        iconHeatingTrue.SetActive(false);
        iconUsageFalse.SetActive(true);
        iconHeatingFalse.SetActive(true);

        // Deactivate the renderer if the 'visible' flag is set to false.
        if (!visible)
        {
            DeactivateRenderer();
        }

        // Listen for the TimeChangeEvent from the TimeManager.
        TimeManager.instance.timeChangeEvent.AddListener(OnTimeChange); // Hör auf das TimeChangeEvent

    }

    /// <summary>
    /// Update method called once per frame.
    /// </summary>
    void Update()
    {
        // Update the clock display and speed ramp factor display.
        clockDisplay.text = TimeConverter.MinuteIndexToTime(TimeManager.instance.CurrentTime);
        speedRampFactorDisplay.text = "Derzeitiger Zeitraffer: " + TimeManager.instance.SpeedRampFactor.ToString();
        
        // Check if there is data for the current time step.
        if (currentTimeStepIndex < heizungsboardDataList.Count)
        {
            // Check if the current time has reached or exceeded the minute index for the current data point.
            if (TimeManager.instance.CurrentTime >= heizungsboardDataList[currentTimeStepIndex].MinuteIndex)
            {
                // Update the displayed information.
                temperatureDisplay.text = heizungsboardDataList[currentTimeStepIndex].Temperature.ToString();
                nextPersonDisplay.text = TimeConverter.MinuteIndexToTime(heizungsboardDataList[currentTimeStepIndex].MinutesNextPersonEnters);

                // Update the floor color if a renderer is available.
                if (floorRenderer != null && floorRenderer.enabled)
                {
                    floorRenderer.material.color = ColorConversion.StringToColor(heizungsboardDataList[currentTimeStepIndex].ColorString);
                }

                // Update the heating and usage icons based on data.
                if (heizungsboardDataList[currentTimeStepIndex].Heating)
                {
                    iconHeatingTrue.SetActive(true);
                    iconHeatingFalse.SetActive(false);
                }
                else
                {
                    iconHeatingTrue.SetActive(false);
                    iconHeatingFalse.SetActive(true);
                }

                if (heizungsboardDataList[currentTimeStepIndex].InUsage)
                {
                    iconUsageTrue.SetActive(true);
                    iconUsageFalse.SetActive(false);
                }
                else
                {
                    iconUsageTrue.SetActive(false);
                    iconUsageFalse.SetActive(true);
                }

                // Move to the next time step.
                currentTimeStepIndex++;
            }
        }

    }

    /// <summary>
    /// Asynchronous method to load CSV data from a file.
    /// File must be located on Hololens in LocalState. In Windows under Documents/MVP Data. See FileInteraction.cs for more Information
    /// </summary>
    private async void LoadCSVData()
    {
        try
        {
            string csvData = await FileInteraction.Load(csvFile); ;

            // Split the input string into lines
            string[] lines = csvData.Split('\n');

            // Process each line (skipping the header line)
            for (int i = 1; i < lines.Length - 1; i++)
            {
                string line = lines[i];
                string[] values = line.Split(',');
                HeizungsboardData heizungsboardData = new HeizungsboardData();
                heizungsboardData.MinuteIndex = (int)Math.Round(float.Parse(values[1].Trim())); ;
                heizungsboardData.NumberOfPersonsInRoom = (int)Math.Round(float.Parse(values[2].Trim()));
                heizungsboardData.Temperature = Math.Round(float.Parse(values[3].Trim()), 2);
                heizungsboardData.InUsage = Boolean.Parse(values[4].Trim());
                heizungsboardData.Heating = Boolean.Parse(values[5].Trim());
                heizungsboardData.ColorString = values[6].Trim();
                heizungsboardData.MinutesNextPersonEnters = int.Parse(values[7].Trim());
                heizungsboardDataList.Add(heizungsboardData);
            }
        }
        catch (Exception e)
        {

            Debug.LogError("Fehler beim Laden der CSV-Daten: " + csvFile + ": " + e.Message);
        }
    }

    /// <summary>
    /// Event handler for the TimeChangeEvent.
    /// </summary>
    /// <param name="currentTime">The current time in minutes. (game time)</param>
    public void OnTimeChange(float currentTime)
    {
        // Find the corresponding index for the given time.
        int newIndex = FindIndexForTime(currentTime);

        // Update the current time step index and display information based on the new index.
        if (newIndex >= 0)
        {
            currentTimeStepIndex = newIndex;
            temperatureDisplay.text = heizungsboardDataList[currentTimeStepIndex].Temperature.ToString();
            clockDisplay.text = TimeConverter.MinuteIndexToTime(TimeManager.instance.CurrentTime);
            nextPersonDisplay.text = TimeConverter.MinuteIndexToTime(heizungsboardDataList[currentTimeStepIndex].MinutesNextPersonEnters);

            // Update the floor color if a renderer is available.
            if (floorRenderer != null && floorRenderer.enabled)
            {
                floorRenderer.material.color = ColorConversion.StringToColor(heizungsboardDataList[currentTimeStepIndex].ColorString);
            }

            // Update the heating and usage icons based on data.
            if (heizungsboardDataList[currentTimeStepIndex].Heating)
            {
                iconHeatingTrue.SetActive(true);
                iconHeatingFalse.SetActive(false);
            }
            else
            {
                iconHeatingTrue.SetActive(false);
                iconHeatingFalse.SetActive(true);
            }

            if (heizungsboardDataList[currentTimeStepIndex].InUsage)
            {
                iconUsageTrue.SetActive(true);
                iconUsageFalse.SetActive(false);
            }
            else
            {
                iconUsageTrue.SetActive(false);
                iconUsageFalse.SetActive(true);
            }
        }
    }

    /// <summary>
    /// Deactivates the renderer components of icons and text mesh objects.
    /// </summary>
    private void DeactivateRenderer()
    {
        // Deactivate Mesh Renderer components of child objects.
        foreach (MeshRenderer renderer in gameObject.GetComponentsInChildren(typeof(MeshRenderer)))
        {
            renderer.enabled = false;
        }

        // Deactivate the SpriteRenderer (if present).
        SpriteRenderer spriteRenderer = gameObject.GetComponent<SpriteRenderer>();
        if (spriteRenderer != null)
        {
            spriteRenderer.enabled = false;
        }
    }

    /// <summary>
    /// Finds the index in the heating board data list for the given current time (game time).
    /// </summary>
    /// <param name="currentTime">The current time in minutes.</param>
    /// <returns>The index of the corresponding data point in the list. </returns>
    private int FindIndexForTime(float currentTime)
    {
        for (int i = 0; i < heizungsboardDataList.Count; i++)
        {
            if (heizungsboardDataList[i].MinuteIndex > currentTime)
            {
                return i - 1; // Return the previous index.
            }
        }

        return heizungsboardDataList.Count - 1; // If no matching time is found, return the last index.
    }
}
